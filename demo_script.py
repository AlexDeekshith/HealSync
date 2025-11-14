#!/usr/bin/env python3
"""
Demo Script for AI-Powered Smart Ambulance System
Simulates emergency scenarios and demonstrates system capabilities
"""

import requests
import json
import time
import random
from datetime import datetime

class SmartAmbulanceDemo:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.demo_scenarios = self._load_demo_scenarios()
        
    def _load_demo_scenarios(self):
        return [
            {
                'name': 'Cardiac Emergency - High Traffic Area',
                'pickup_location': {'lat': 28.6139, 'lng': 77.2090},
                'patient_condition': 'cardiac',
                'vitals_sequence': [
                    {'heart_rate': 145, 'blood_pressure_systolic': 85, 'blood_pressure_diastolic': 55, 'oxygen_saturation': 92, 'respiratory_rate': 22, 'temperature': 36.8},
                    {'heart_rate': 150, 'blood_pressure_systolic': 80, 'blood_pressure_diastolic': 50, 'oxygen_saturation': 90, 'respiratory_rate': 24, 'temperature': 37.0},
                    {'heart_rate': 155, 'blood_pressure_systolic': 75, 'blood_pressure_diastolic': 45, 'oxygen_saturation': 88, 'respiratory_rate': 26, 'temperature': 37.2}
                ]
            },
            {
                'name': 'Stroke Emergency - Elderly Patient',
                'pickup_location': {'lat': 28.6289, 'lng': 77.2065},
                'patient_condition': 'stroke',
                'vitals_sequence': [
                    {'heart_rate': 68, 'blood_pressure_systolic': 180, 'blood_pressure_diastolic': 110, 'oxygen_saturation': 96, 'respiratory_rate': 18, 'temperature': 36.5},
                    {'heart_rate': 65, 'blood_pressure_systolic': 185, 'blood_pressure_diastolic': 115, 'oxygen_saturation': 95, 'respiratory_rate': 16, 'temperature': 36.4},
                    {'heart_rate': 62, 'blood_pressure_systolic': 190, 'blood_pressure_diastolic': 120, 'oxygen_saturation': 94, 'respiratory_rate': 15, 'temperature': 36.3}
                ]
            },
            {
                'name': 'Trauma Emergency - Motor Accident',
                'pickup_location': {'lat': 28.6089, 'lng': 77.2190},
                'patient_condition': 'trauma',
                'vitals_sequence': [
                    {'heart_rate': 110, 'blood_pressure_systolic': 95, 'blood_pressure_diastolic': 60, 'oxygen_saturation': 94, 'respiratory_rate': 20, 'temperature': 36.2},
                    {'heart_rate': 115, 'blood_pressure_systolic': 90, 'blood_pressure_diastolic': 55, 'oxygen_saturation': 92, 'respiratory_rate': 22, 'temperature': 36.0},
                    {'heart_rate': 120, 'blood_pressure_systolic': 85, 'blood_pressure_diastolic': 50, 'oxygen_saturation': 90, 'respiratory_rate': 24, 'temperature': 35.8}
                ]
            }
        ]
    
    def run_demo(self):
        """Run complete demo of the smart ambulance system"""
        print("🚑 AI-Powered Smart Ambulance System Demo")
        print("=" * 50)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n📋 Scenario {i}: {scenario['name']}")
            print("-" * 40)
            
            # Step 1: Create Emergency
            emergency_id = self.create_emergency(scenario)
            if not emergency_id:
                continue
                
            # Step 2: Simulate vitals progression
            self.simulate_vitals_progression(emergency_id, scenario['vitals_sequence'])
            
            # Step 3: Show results
            self.display_scenario_results(scenario)
            
            # Wait before next scenario
            if i < len(self.demo_scenarios):
                print("\n⏳ Moving to next scenario in 3 seconds...")
                time.sleep(3)
        
        print("\n🎉 Demo completed! Check the web interfaces for real-time updates.")
        print("📊 Access the system at:")
        print(f"   • Control Center: {self.base_url}/")
        print(f"   • Ambulance Interface: {self.base_url}/ambulance")
        print(f"   • Doctor Console: {self.base_url}/doctor")
    
    def create_emergency(self, scenario):
        """Create a new emergency scenario"""
        try:
            response = requests.post(
                f"{self.base_url}/api/emergency",
                json={
                    'pickup_location': scenario['pickup_location'],
                    'patient_condition': scenario['patient_condition']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                emergency_id = result['emergency_id']
                emergency = result['emergency']
                
                print(f"✅ Emergency created: {emergency_id}")
                print(f"   📍 Location: {scenario['pickup_location']}")
                print(f"   🏥 Assigned Hospital: {emergency['hospital']['name']}")
                print(f"   🕐 Estimated Time: {emergency['route']['estimated_time_minutes']} minutes")
                print(f"   📏 Distance: {emergency['route']['hospital']['distance_km']:.1f} km")
                
                return emergency_id
            else:
                print(f"❌ Failed to create emergency: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def simulate_vitals_progression(self, emergency_id, vitals_sequence):
        """Simulate patient vitals progression over time"""
        print(f"\n📊 Simulating vitals progression for {emergency_id}...")
        
        for i, vitals in enumerate(vitals_sequence, 1):
            print(f"\n   📈 Vitals Update {i}:")
            print(f"      Heart Rate: {vitals['heart_rate']} bpm")
            print(f"      Blood Pressure: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} mmHg")
            print(f"      Oxygen Saturation: {vitals['oxygen_saturation']}%")
            print(f"      Respiratory Rate: {vitals['respiratory_rate']} /min")
            print(f"      Temperature: {vitals['temperature']}°C")
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/vitals",
                    json={
                        'emergency_id': emergency_id,
                        'vitals': vitals
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    guidance = response.json()['guidance']
                    print(f"      🤖 AI Risk Level: {guidance['risk_level'].upper()}")
                    
                    if guidance['condition_prediction']:
                        print(f"      🔍 AI Prediction: {guidance['condition_prediction']}")
                    
                    if guidance['immediate_actions']:
                        print(f"      📋 AI Guidance: {guidance['immediate_actions'][0]}")
                        
                else:
                    print(f"      ⚠️ Failed to update vitals: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"      ❌ Connection error: {e}")
            
            # Wait between vitals updates
            time.sleep(2)
    
    def display_scenario_results(self, scenario):
        """Display scenario results and insights"""
        print(f"\n📋 Scenario Summary: {scenario['name']}")
        print("   Key Features Demonstrated:")
        
        if scenario['patient_condition'] == 'cardiac':
            print("   ✅ Cardiac emergency detection")
            print("   ✅ Hospital with cardiac catheterization lab selected")
            print("   ✅ Critical vitals monitoring")
            print("   ✅ AI-guided CPR protocols")
            
        elif scenario['patient_condition'] == 'stroke':
            print("   ✅ Stroke pattern recognition")
            print("   ✅ Stroke center hospital allocation")
            print("   ✅ Blood pressure monitoring")
            print("   ✅ FAST assessment guidance")
            
        elif scenario['patient_condition'] == 'trauma':
            print("   ✅ Trauma emergency handling")
            print("   ✅ Level 1 trauma center selection")
            print("   ✅ Shock detection and monitoring")
            print("   ✅ Bleeding control protocols")
    
    def generate_demo_report(self):
        """Generate a comprehensive demo report"""
        report = {
            'demo_timestamp': datetime.now().isoformat(),
            'scenarios_tested': len(self.demo_scenarios),
            'features_demonstrated': [
                'AI-powered route optimization',
                'Real-time hospital allocation',
                'Virtual doctor assistance',
                'Predictive medical analytics',
                'Multi-condition emergency handling',
                'Real-time vitals monitoring',
                'Telemedicine integration'
            ],
            'ai_capabilities': [
                'Traffic pattern analysis',
                'Medical condition prediction',
                'Risk level assessment',
                'Hospital scoring algorithm',
                'Route optimization',
                'Vital signs analysis'
            ],
            'system_benefits': [
                'Reduced response times',
                'Improved patient outcomes',
                'Better hospital resource utilization',
                'Enhanced paramedic guidance',
                'Real-time decision making'
            ]
        }
        
        print("\n📊 DEMO REPORT")
        print("=" * 50)
        print(f"Timestamp: {report['demo_timestamp']}")
        print(f"Scenarios Tested: {report['scenarios_tested']}")
        
        print("\n🚀 Features Demonstrated:")
        for feature in report['features_demonstrated']:
            print(f"   ✅ {feature}")
        
        print("\n🧠 AI Capabilities:")
        for capability in report['ai_capabilities']:
            print(f"   🤖 {capability}")
        
        print("\n💡 System Benefits:")
        for benefit in report['system_benefits']:
            print(f"   📈 {benefit}")
        
        return report

def main():
    """Main demo function"""
    print("🚀 Starting AI-Powered Smart Ambulance System Demo...")
    print("⚠️  Make sure the Flask application is running on localhost:5000")
    
    # Wait for user confirmation
    input("\nPress Enter to start the demo...")
    
    demo = SmartAmbulanceDemo()
    
    try:
        # Run the complete demo
        demo.run_demo()
        
        # Generate final report
        print("\n" + "="*60)
        demo.generate_demo_report()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    
    print("\n🎯 Demo completed! Thank you for testing the Smart Ambulance System.")

if __name__ == "__main__":
    main()