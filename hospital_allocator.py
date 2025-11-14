import numpy as np
from geopy.distance import geodesic
import random
from datetime import datetime, timedelta

class HospitalAllocator:
    def __init__(self):
        self.hospitals = self._load_hospital_database()
        self.real_time_data = self._initialize_real_time_data()
        
    def _load_hospital_database(self):
        return [
            {
                'id': 'H001',
                'name': 'All India Institute of Medical Sciences (AIIMS)',
                'location': {'lat': 28.5672, 'lng': 77.2100},
                'specialties': ['cardiac', 'neuro', 'trauma', 'pediatric', 'general'],
                'total_beds': 2500,
                'icu_beds': 200,
                'emergency_beds': 50,
                'cardiac_cath_lab': True,
                'trauma_center_level': 1,
                'stroke_center': True,
                'contact': '+91-11-26588500'
            },
            {
                'id': 'H002',
                'name': 'Fortis Escorts Heart Institute',
                'location': {'lat': 28.6139, 'lng': 77.2090},
                'specialties': ['cardiac', 'vascular', 'general'],
                'total_beds': 310,
                'icu_beds': 40,
                'emergency_beds': 15,
                'cardiac_cath_lab': True,
                'trauma_center_level': 2,
                'stroke_center': False,
                'contact': '+91-11-47135000'
            },
            {
                'id': 'H003',
                'name': 'Max Super Speciality Hospital',
                'location': {'lat': 28.6289, 'lng': 77.2065},
                'specialties': ['neuro', 'cardiac', 'trauma', 'orthopedic'],
                'total_beds': 500,
                'icu_beds': 60,
                'emergency_beds': 25,
                'cardiac_cath_lab': True,
                'trauma_center_level': 1,
                'stroke_center': True,
                'contact': '+91-11-26925858'
            },
            {
                'id': 'H004',
                'name': 'Apollo Hospital',
                'location': {'lat': 28.6089, 'lng': 77.2190},
                'specialties': ['cardiac', 'neuro', 'oncology', 'general'],
                'total_beds': 695,
                'icu_beds': 80,
                'emergency_beds': 30,
                'cardiac_cath_lab': True,
                'trauma_center_level': 2,
                'stroke_center': True,
                'contact': '+91-11-26925858'
            },
            {
                'id': 'H005',
                'name': 'Safdarjung Hospital',
                'location': {'lat': 28.5706, 'lng': 77.2081},
                'specialties': ['trauma', 'general', 'pediatric', 'orthopedic'],
                'total_beds': 1500,
                'icu_beds': 100,
                'emergency_beds': 40,
                'cardiac_cath_lab': False,
                'trauma_center_level': 1,
                'stroke_center': False,
                'contact': '+91-11-26165060'
            }
        ]
    
    def _initialize_real_time_data(self):
        """Initialize real-time hospital data (simulated)"""
        data = {}
        
        for hospital in self.hospitals:
            data[hospital['id']] = {
                'current_er_load': random.uniform(0.3, 0.9),
                'available_icu_beds': random.randint(2, hospital['icu_beds'] // 2),
                'available_emergency_beds': random.randint(1, hospital['emergency_beds'] // 2),
                'average_wait_time': random.randint(5, 45),
                'staff_availability': {
                    'emergency_doctors': random.randint(2, 8),
                    'nurses': random.randint(5, 20),
                    'specialists_on_call': random.randint(1, 5)
                },
                'equipment_status': {
                    'ct_scanner': random.choice(['available', 'busy', 'maintenance']),
                    'mri': random.choice(['available', 'busy']),
                    'cath_lab': random.choice(['available', 'busy']) if hospital.get('cardiac_cath_lab') else 'not_available',
                    'or_rooms': random.randint(1, 5)
                },
                'last_updated': datetime.now()
            }
        
        return data
    
    def allocate_hospital(self, pickup_location, patient_condition, patient_age=None):
        """
        AI-powered hospital allocation based on multiple factors
        """
        
        # Filter hospitals by specialty requirements
        suitable_hospitals = self._filter_by_specialty(patient_condition)
        
        # Score each hospital
        hospital_scores = []
        
        for hospital in suitable_hospitals:
            score = self._calculate_hospital_score(
                hospital, 
                pickup_location, 
                patient_condition,
                patient_age
            )
            hospital_scores.append((hospital, score))
        
        # Sort by score (highest first)
        hospital_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 3 recommendations
        recommendations = []
        for i, (hospital, score) in enumerate(hospital_scores[:3]):
            real_time = self.real_time_data[hospital['id']]
            
            recommendation = {
                'rank': i + 1,
                'hospital': hospital,
                'score': round(score, 2),
                'distance_km': self._calculate_distance(pickup_location, hospital['location']),
                'estimated_arrival': self._estimate_arrival_time(pickup_location, hospital['location']),
                'current_status': {
                    'er_load': real_time['current_er_load'],
                    'available_beds': real_time['available_emergency_beds'],
                    'wait_time_minutes': real_time['average_wait_time']
                },
                'why_recommended': self._generate_recommendation_reason(hospital, patient_condition, score)
            }
            recommendations.append(recommendation)
        
        # Return primary recommendation with alternatives
        return {
            'primary_hospital': recommendations[0] if recommendations else None,
            'alternatives': recommendations[1:] if len(recommendations) > 1 else [],
            'allocation_timestamp': datetime.now().isoformat(),
            'patient_condition': patient_condition
        }
    
    def _filter_by_specialty(self, patient_condition):
        """Filter hospitals based on required specialty"""
        
        specialty_mapping = {
            'cardiac': 'cardiac',
            'heart_attack': 'cardiac',
            'stroke': 'neuro',
            'trauma': 'trauma',
            'accident': 'trauma',
            'pediatric': 'pediatric',
            'general': 'general'
        }
        
        required_specialty = specialty_mapping.get(patient_condition, 'general')
        
        if required_specialty == 'general':
            return self.hospitals  # All hospitals can handle general cases
        
        return [h for h in self.hospitals if required_specialty in h['specialties']]
    
    def _calculate_hospital_score(self, hospital, pickup_location, patient_condition, patient_age):
        """Calculate comprehensive hospital score using AI scoring algorithm"""
        
        real_time = self.real_time_data[hospital['id']]
        
        # Distance factor (closer is better) - Weight: 25%
        distance = self._calculate_distance(pickup_location, hospital['location'])
        distance_score = max(0, 1 - (distance / 20))  # Normalize to 0-1, 20km max
        
        # Availability factor (more beds available is better) - Weight: 20%
        bed_availability = real_time['available_emergency_beds'] / hospital['emergency_beds']
        
        # Load factor (less ER load is better) - Weight: 20%
        load_score = 1 - real_time['current_er_load']
        
        # Specialty match factor - Weight: 15%
        specialty_score = self._calculate_specialty_score(hospital, patient_condition)
        
        # Equipment availability factor - Weight: 10%
        equipment_score = self._calculate_equipment_score(hospital, patient_condition, real_time)
        
        # Staff availability factor - Weight: 10%
        staff_score = min(1, real_time['staff_availability']['emergency_doctors'] / 5)
        
        # Calculate weighted score
        total_score = (
            distance_score * 0.25 +
            bed_availability * 0.20 +
            load_score * 0.20 +
            specialty_score * 0.15 +
            equipment_score * 0.10 +
            staff_score * 0.10
        )
        
        return total_score
    
    def _calculate_specialty_score(self, hospital, patient_condition):
        """Calculate specialty matching score"""
        
        if patient_condition in ['cardiac', 'heart_attack']:
            if 'cardiac' in hospital['specialties']:
                return 1.0 if hospital.get('cardiac_cath_lab') else 0.8
            return 0.3
        
        elif patient_condition == 'stroke':
            if 'neuro' in hospital['specialties']:
                return 1.0 if hospital.get('stroke_center') else 0.8
            return 0.2
        
        elif patient_condition in ['trauma', 'accident']:
            if 'trauma' in hospital['specialties']:
                level = hospital.get('trauma_center_level', 3)
                return 1.0 if level == 1 else 0.8 if level == 2 else 0.6
            return 0.4
        
        else:  # General condition
            return 0.7  # All hospitals can handle general cases
    
    def _calculate_equipment_score(self, hospital, patient_condition, real_time):
        """Calculate equipment availability score"""
        
        equipment = real_time['equipment_status']
        score = 0.5  # Base score
        
        if patient_condition in ['cardiac', 'heart_attack']:
            if equipment['cath_lab'] == 'available':
                score += 0.5
            elif equipment['cath_lab'] == 'busy':
                score += 0.2
        
        elif patient_condition == 'stroke':
            if equipment['ct_scanner'] == 'available':
                score += 0.3
            if equipment['mri'] == 'available':
                score += 0.2
        
        elif patient_condition in ['trauma', 'accident']:
            if equipment['ct_scanner'] == 'available':
                score += 0.3
            if equipment['or_rooms'] > 2:
                score += 0.2
        
        return min(1.0, score)
    
    def _calculate_distance(self, location1, location2):
        """Calculate distance between two locations"""
        return geodesic(
            (location1['lat'], location1['lng']),
            (location2['lat'], location2['lng'])
        ).kilometers
    
    def _estimate_arrival_time(self, pickup_location, hospital_location):
        """Estimate arrival time considering traffic"""
        distance = self._calculate_distance(pickup_location, hospital_location)
        
        # Average speed considering traffic and emergency vehicle priority
        average_speed = 35  # km/h in city with emergency vehicle
        
        time_minutes = (distance / average_speed) * 60
        return round(time_minutes, 1)
    
    def _generate_recommendation_reason(self, hospital, patient_condition, score):
        """Generate human-readable reason for recommendation"""
        
        reasons = []
        
        if score > 0.8:
            reasons.append("Excellent match for patient condition")
        elif score > 0.6:
            reasons.append("Good match for patient condition")
        
        if patient_condition in ['cardiac', 'heart_attack'] and hospital.get('cardiac_cath_lab'):
            reasons.append("Has cardiac catheterization lab")
        
        if patient_condition == 'stroke' and hospital.get('stroke_center'):
            reasons.append("Designated stroke center")
        
        if patient_condition in ['trauma', 'accident']:
            level = hospital.get('trauma_center_level', 3)
            if level == 1:
                reasons.append("Level 1 trauma center")
            elif level == 2:
                reasons.append("Level 2 trauma center")
        
        real_time = self.real_time_data[hospital['id']]
        if real_time['current_er_load'] < 0.5:
            reasons.append("Low emergency room load")
        
        if real_time['available_emergency_beds'] > 5:
            reasons.append("Good bed availability")
        
        return "; ".join(reasons) if reasons else "Available for emergency care"
    
    def update_hospital_status(self, hospital_id, status_update):
        """Update real-time hospital status"""
        if hospital_id in self.real_time_data:
            self.real_time_data[hospital_id].update(status_update)
            self.real_time_data[hospital_id]['last_updated'] = datetime.now()
            return True
        return False
    
    def get_hospital_details(self, hospital_id):
        """Get detailed hospital information"""
        hospital = next((h for h in self.hospitals if h['id'] == hospital_id), None)
        if hospital:
            real_time = self.real_time_data[hospital_id]
            return {
                'hospital': hospital,
                'real_time_status': real_time
            }
        return None