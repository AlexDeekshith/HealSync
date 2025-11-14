from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import random
import time
from datetime import datetime
from ai_routing import SmartRoutingEngine
from virtual_doctor import VirtualDoctorAI
from hospital_allocator import HospitalAllocator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart_ambulance_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize AI modules
routing_engine = SmartRoutingEngine()
virtual_doctor = VirtualDoctorAI()
hospital_allocator = HospitalAllocator()

# Global state
active_emergencies = {}
ambulance_locations = {}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/ambulance')
def ambulance_interface():
    return render_template('ambulance.html')

@app.route('/doctor')
def doctor_interface():
    return render_template('doctor.html')

@app.route('/api/emergency', methods=['POST'])
def create_emergency():
    data = request.json
    emergency_id = f"EMG_{int(time.time())}"
    
    # Get optimal route and hospital
    route = routing_engine.get_optimal_route(
        data['pickup_location'], 
        data.get('patient_condition', 'general')
    )
    
    hospital = hospital_allocator.allocate_hospital(
        data['pickup_location'],
        data.get('patient_condition', 'general')
    )
    
    emergency = {
        'id': emergency_id,
        'pickup_location': data['pickup_location'],
        'patient_condition': data.get('patient_condition', 'general'),
        'route': route,
        'hospital': hospital,
        'status': 'dispatched',
        'created_at': datetime.now().isoformat()
    }
    
    active_emergencies[emergency_id] = emergency
    
    # Notify all connected clients
    socketio.emit('new_emergency', emergency)
    
    return jsonify({'emergency_id': emergency_id, 'emergency': emergency})

@app.route('/api/vitals', methods=['POST'])
def update_vitals():
    data = request.json
    emergency_id = data['emergency_id']
    vitals = data['vitals']
    
    # Get AI medical guidance
    guidance = virtual_doctor.analyze_vitals(vitals)
    
    # Update emergency record
    if emergency_id in active_emergencies:
        active_emergencies[emergency_id]['vitals'] = vitals
        active_emergencies[emergency_id]['ai_guidance'] = guidance
    
    # Send to connected doctors
    socketio.emit('vitals_update', {
        'emergency_id': emergency_id,
        'vitals': vitals,
        'ai_guidance': guidance
    })
    
    return jsonify({'guidance': guidance})

@socketio.on('ambulance_location')
def handle_ambulance_location(data):
    ambulance_id = data['ambulance_id']
    location = data['location']
    
    ambulance_locations[ambulance_id] = {
        'location': location,
        'timestamp': datetime.now().isoformat()
    }
    
    # Broadcast to all clients
    emit('location_update', {
        'ambulance_id': ambulance_id,
        'location': location
    }, broadcast=True)

@socketio.on('doctor_connect')
def handle_doctor_connect(data):
    emit('doctor_connected', {'status': 'connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)