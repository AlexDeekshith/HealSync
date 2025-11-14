import numpy as np
from datetime import datetime
import random

class VirtualDoctorAI:
    def __init__(self):
        self.medical_protocols = self._load_medical_protocols()
        self.vital_ranges = self._load_vital_ranges()
        
    def _load_medical_protocols(self):
        return {
            'cardiac_arrest': {
                'steps': [
                    'Check responsiveness and breathing',
                    'Call for AED if available',
                    'Start CPR - 30 compressions, 2 breaths',
                    'Continue until AED arrives or patient responds',
                    'Monitor vitals continuously'
                ],
                'medications': ['Epinephrine', 'Amiodarone'],
                'priority': 'critical'
            },
            'stroke': {
                'steps': [
                    'Perform FAST assessment (Face, Arms, Speech, Time)',
                    'Check blood pressure',
                    'Maintain airway',
                    'Do not give food or water',
                    'Monitor neurological status'
                ],
                'medications': ['Aspirin (if confirmed ischemic)'],
                'priority': 'critical'
            },
            'trauma': {
                'steps': [
                    'Control bleeding with direct pressure',
                    'Check for spinal injury',
                    'Maintain airway',
                    'Monitor for shock',
                    'Immobilize suspected fractures'
                ],
                'medications': ['Morphine for pain', 'Saline for shock'],
                'priority': 'high'
            },
            'respiratory_distress': {
                'steps': [
                    'Position patient upright',
                    'Administer oxygen',
                    'Check for allergic reactions',
                    'Monitor oxygen saturation',
                    'Prepare for intubation if needed'
                ],
                'medications': ['Albuterol', 'Epinephrine (if anaphylaxis)'],
                'priority': 'high'
            }
        }
    
    def _load_vital_ranges(self):
        return {
            'heart_rate': {'normal': (60, 100), 'critical_low': 50, 'critical_high': 120},
            'blood_pressure_systolic': {'normal': (90, 140), 'critical_low': 80, 'critical_high': 180},
            'blood_pressure_diastolic': {'normal': (60, 90), 'critical_low': 50, 'critical_high': 110},
            'oxygen_saturation': {'normal': (95, 100), 'critical_low': 90, 'critical_high': 100},
            'respiratory_rate': {'normal': (12, 20), 'critical_low': 8, 'critical_high': 30},
            'temperature': {'normal': (36.1, 37.2), 'critical_low': 35.0, 'critical_high': 39.0}
        }
    
    def analyze_vitals(self, vitals):
        """
        AI analysis of patient vitals with medical guidance
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'vital_status': {},
            'risk_level': 'stable',
            'immediate_actions': [],
            'medication_suggestions': [],
            'condition_prediction': None,
            'doctor_alert': False
        }
        
        # Analyze each vital sign
        critical_count = 0
        
        for vital_name, value in vitals.items():
            if vital_name in self.vital_ranges:
                status = self._assess_vital_sign(vital_name, value)
                analysis['vital_status'][vital_name] = status
                
                if status['level'] == 'critical':
                    critical_count += 1
        
        # Determine overall risk level
        if critical_count >= 2:
            analysis['risk_level'] = 'critical'
            analysis['doctor_alert'] = True
        elif critical_count == 1:
            analysis['risk_level'] = 'high'
        
        # Predict possible condition based on vital patterns
        predicted_condition = self._predict_condition(vitals)
        analysis['condition_prediction'] = predicted_condition
        
        # Generate immediate actions based on condition
        if predicted_condition:
            protocol = self.medical_protocols.get(predicted_condition)
            if protocol:
                analysis['immediate_actions'] = protocol['steps'][:3]  # First 3 steps
                analysis['medication_suggestions'] = protocol['medications']
        
        # Add general emergency actions if critical
        if analysis['risk_level'] == 'critical':
            analysis['immediate_actions'].insert(0, 'ALERT: Critical vitals detected - prepare for emergency intervention')
        
        return analysis
    
    def _assess_vital_sign(self, vital_name, value):
        """Assess individual vital sign"""
        ranges = self.vital_ranges[vital_name]
        
        status = {
            'value': value,
            'level': 'normal',
            'message': 'Within normal range'
        }
        
        if value < ranges['critical_low']:
            status['level'] = 'critical'
            status['message'] = f'Critically low {vital_name}'
        elif value > ranges['critical_high']:
            status['level'] = 'critical'
            status['message'] = f'Critically high {vital_name}'
        elif value < ranges['normal'][0] or value > ranges['normal'][1]:
            status['level'] = 'abnormal'
            status['message'] = f'Abnormal {vital_name}'
        
        return status
    
    def _predict_condition(self, vitals):
        """AI-based condition prediction from vital patterns"""
        
        # Get vital values with defaults
        hr = vitals.get('heart_rate', 70)
        bp_sys = vitals.get('blood_pressure_systolic', 120)
        bp_dia = vitals.get('blood_pressure_diastolic', 80)
        o2_sat = vitals.get('oxygen_saturation', 98)
        resp_rate = vitals.get('respiratory_rate', 16)
        temp = vitals.get('temperature', 36.5)
        
        # Cardiac arrest pattern
        if hr < 50 or hr > 150 or bp_sys < 80:
            return 'cardiac_arrest'
        
        # Stroke pattern (high BP, normal/low HR)
        if bp_sys > 160 and hr < 80:
            return 'stroke'
        
        # Respiratory distress pattern
        if o2_sat < 92 or resp_rate > 25:
            return 'respiratory_distress'
        
        # Trauma/shock pattern (low BP, high HR)
        if bp_sys < 90 and hr > 100:
            return 'trauma'
        
        return None
    
    def get_cpr_guidance(self):
        """Provide step-by-step CPR guidance"""
        return {
            'steps': [
                {
                    'step': 1,
                    'instruction': 'Place heel of hand on center of chest, between nipples',
                    'duration': 'Setup'
                },
                {
                    'step': 2,
                    'instruction': 'Place other hand on top, interlace fingers',
                    'duration': 'Setup'
                },
                {
                    'step': 3,
                    'instruction': 'Push hard and fast at least 2 inches deep',
                    'duration': '30 compressions'
                },
                {
                    'step': 4,
                    'instruction': 'Tilt head back, lift chin, give 2 rescue breaths',
                    'duration': '2 breaths'
                },
                {
                    'step': 5,
                    'instruction': 'Continue cycles of 30 compressions and 2 breaths',
                    'duration': 'Until help arrives'
                }
            ],
            'rate': '100-120 compressions per minute',
            'depth': 'At least 2 inches (5 cm)',
            'allow_recoil': True
        }
    
    def get_bleeding_control_guidance(self):
        """Provide bleeding control instructions"""
        return {
            'steps': [
                'Apply direct pressure to wound with clean cloth',
                'If blood soaks through, add more cloth on top',
                'Elevate injured area above heart level if possible',
                'Apply pressure to pressure points if bleeding continues',
                'Do not remove embedded objects'
            ],
            'pressure_points': {
                'arm': 'Brachial artery - inside upper arm',
                'leg': 'Femoral artery - groin area',
                'head': 'Temporal artery - in front of ear'
            }
        }
    
    def generate_hospital_report(self, vitals_history, condition_prediction):
        """Generate report for receiving hospital"""
        
        latest_vitals = vitals_history[-1] if vitals_history else {}
        
        report = {
            'patient_summary': {
                'condition': condition_prediction or 'Unknown',
                'risk_level': self.analyze_vitals(latest_vitals)['risk_level'],
                'eta_minutes': random.randint(5, 15),  # Would come from routing
                'special_requirements': []
            },
            'vital_trends': self._analyze_vital_trends(vitals_history),
            'interventions_performed': [],
            'recommendations': []
        }
        
        # Add special requirements based on condition
        if condition_prediction == 'cardiac_arrest':
            report['patient_summary']['special_requirements'] = [
                'Cardiac team standby',
                'Defibrillator ready',
                'ICU bed preparation'
            ]
        elif condition_prediction == 'stroke':
            report['patient_summary']['special_requirements'] = [
                'Stroke team activation',
                'CT scan ready',
                'Neurologist on standby'
            ]
        elif condition_prediction == 'trauma':
            report['patient_summary']['special_requirements'] = [
                'Trauma team activation',
                'Blood bank notification',
                'OR preparation if needed'
            ]
        
        return report
    
    def _analyze_vital_trends(self, vitals_history):
        """Analyze trends in vital signs over time"""
        if len(vitals_history) < 2:
            return {'trend': 'insufficient_data'}
        
        trends = {}
        
        for vital in ['heart_rate', 'blood_pressure_systolic', 'oxygen_saturation']:
            values = [v.get(vital, 0) for v in vitals_history if vital in v]
            
            if len(values) >= 2:
                if values[-1] > values[0]:
                    trends[vital] = 'increasing'
                elif values[-1] < values[0]:
                    trends[vital] = 'decreasing'
                else:
                    trends[vital] = 'stable'
        
        return trends