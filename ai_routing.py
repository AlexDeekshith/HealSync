import numpy as np
import random
from geopy.distance import geodesic
from datetime import datetime, timedelta

class SmartRoutingEngine:
    def __init__(self):
        # Simulated traffic data and road conditions
        self.traffic_data = self._load_traffic_data()
        self.hospitals = self._load_hospital_data()
        
    def _load_traffic_data(self):
        # Simulated real-time traffic data
        return {
            'high_traffic_zones': [
                {'lat': 28.6139, 'lng': 77.2090, 'congestion_level': 0.8},  # Delhi
                {'lat': 19.0760, 'lng': 72.8777, 'congestion_level': 0.9},  # Mumbai
                {'lat': 12.9716, 'lng': 77.5946, 'congestion_level': 0.7},  # Bangalore
            ],
            'accident_hotspots': [
                {'lat': 28.6129, 'lng': 77.2295, 'severity': 'high'},
                {'lat': 19.0825, 'lng': 72.8417, 'severity': 'medium'},
            ]
        }
    
    def _load_hospital_data(self):
        return [
            {
                'id': 'H001',
                'name': 'City General Hospital',
                'location': {'lat': 28.6139, 'lng': 77.2090},
                'specialties': ['cardiac', 'trauma', 'general'],
                'current_load': 0.6,
                'icu_beds': 15,
                'emergency_beds': 8
            },
            {
                'id': 'H002', 
                'name': 'Metro Medical Center',
                'location': {'lat': 28.6289, 'lng': 77.2065},
                'specialties': ['neuro', 'cardiac', 'pediatric'],
                'current_load': 0.4,
                'icu_beds': 20,
                'emergency_beds': 12
            },
            {
                'id': 'H003',
                'name': 'Emergency Care Hospital',
                'location': {'lat': 28.6089, 'lng': 77.2190},
                'specialties': ['trauma', 'general', 'orthopedic'],
                'current_load': 0.3,
                'icu_beds': 10,
                'emergency_beds': 15
            }
        ]
    
    def get_optimal_route(self, pickup_location, patient_condition='general'):
        """
        AI-powered route optimization considering:
        - Real-time traffic
        - Road conditions
        - Hospital availability
        - Patient condition urgency
        """
        
        # Find best hospital based on condition and availability
        suitable_hospitals = self._filter_hospitals_by_condition(patient_condition)
        best_hospital = self._select_best_hospital(pickup_location, suitable_hospitals)
        
        # Calculate optimal route avoiding traffic
        route_points = self._calculate_route_with_traffic_avoidance(
            pickup_location, 
            best_hospital['location']
        )
        
        # Estimate arrival time
        estimated_time = self._estimate_arrival_time(route_points)
        
        return {
            'hospital': best_hospital,
            'route_points': route_points,
            'estimated_time_minutes': estimated_time,
            'traffic_alerts': self._get_traffic_alerts(route_points),
            'alternative_routes': self._get_alternative_routes(pickup_location, best_hospital['location'])
        }
    
    def _filter_hospitals_by_condition(self, condition):
        """Filter hospitals based on patient condition"""
        if condition in ['cardiac', 'heart_attack']:
            return [h for h in self.hospitals if 'cardiac' in h['specialties']]
        elif condition in ['trauma', 'accident']:
            return [h for h in self.hospitals if 'trauma' in h['specialties']]
        elif condition in ['stroke', 'neuro']:
            return [h for h in self.hospitals if 'neuro' in h['specialties']]
        else:
            return self.hospitals
    
    def _select_best_hospital(self, pickup_location, hospitals):
        """Select best hospital using AI scoring"""
        scores = []
        
        for hospital in hospitals:
            # Distance factor (closer is better)
            distance = geodesic(
                (pickup_location['lat'], pickup_location['lng']),
                (hospital['location']['lat'], hospital['location']['lng'])
            ).kilometers
            
            distance_score = max(0, 1 - (distance / 20))  # Normalize to 0-1
            
            # Load factor (less load is better)
            load_score = 1 - hospital['current_load']
            
            # Bed availability
            bed_score = min(1, (hospital['icu_beds'] + hospital['emergency_beds']) / 20)
            
            # Combined score
            total_score = (distance_score * 0.4) + (load_score * 0.4) + (bed_score * 0.2)
            scores.append((hospital, total_score))
        
        # Return hospital with highest score
        return max(scores, key=lambda x: x[1])[0]
    
    def _calculate_route_with_traffic_avoidance(self, start, end):
        """Calculate route avoiding high traffic areas"""
        # Simplified route calculation with traffic avoidance
        route_points = []
        
        # Add start point
        route_points.append(start)
        
        # Check for traffic hotspots and create waypoints to avoid them
        for traffic_zone in self.traffic_data['high_traffic_zones']:
            if self._is_route_affected_by_traffic(start, end, traffic_zone):
                # Add waypoint to avoid traffic
                waypoint = self._calculate_avoidance_waypoint(start, end, traffic_zone)
                route_points.append(waypoint)
        
        # Add end point
        route_points.append(end)
        
        return route_points
    
    def _is_route_affected_by_traffic(self, start, end, traffic_zone):
        """Check if direct route passes through high traffic zone"""
        # Simplified check - in real implementation, use proper geometric calculations
        zone_distance = geodesic(
            (start['lat'], start['lng']),
            (traffic_zone['lat'], traffic_zone['lng'])
        ).kilometers
        
        return zone_distance < 2 and traffic_zone['congestion_level'] > 0.7
    
    def _calculate_avoidance_waypoint(self, start, end, traffic_zone):
        """Calculate waypoint to avoid traffic zone"""
        # Simple avoidance - offset perpendicular to direct route
        offset_lat = traffic_zone['lat'] + 0.01 * random.choice([-1, 1])
        offset_lng = traffic_zone['lng'] + 0.01 * random.choice([-1, 1])
        
        return {'lat': offset_lat, 'lng': offset_lng}
    
    def _estimate_arrival_time(self, route_points):
        """Estimate arrival time considering traffic"""
        total_distance = 0
        
        for i in range(len(route_points) - 1):
            distance = geodesic(
                (route_points[i]['lat'], route_points[i]['lng']),
                (route_points[i+1]['lat'], route_points[i+1]['lng'])
            ).kilometers
            total_distance += distance
        
        # Average speed considering traffic (30 km/h in city with traffic)
        average_speed = 30
        estimated_minutes = (total_distance / average_speed) * 60
        
        return round(estimated_minutes, 1)
    
    def _get_traffic_alerts(self, route_points):
        """Get traffic alerts for the route"""
        alerts = []
        
        for point in route_points:
            for accident in self.traffic_data['accident_hotspots']:
                distance = geodesic(
                    (point['lat'], point['lng']),
                    (accident['lat'], accident['lng'])
                ).kilometers
                
                if distance < 1:  # Within 1km
                    alerts.append({
                        'type': 'accident',
                        'severity': accident['severity'],
                        'location': accident,
                        'message': f"Accident reported - {accident['severity']} severity"
                    })
        
        return alerts
    
    def _get_alternative_routes(self, start, end):
        """Generate alternative routes"""
        # Simplified - generate 2 alternative routes with different waypoints
        alternatives = []
        
        for i in range(2):
            waypoint = {
                'lat': start['lat'] + (0.005 * (i + 1) * random.choice([-1, 1])),
                'lng': start['lng'] + (0.005 * (i + 1) * random.choice([-1, 1]))
            }
            
            route = [start, waypoint, end]
            time_estimate = self._estimate_arrival_time(route)
            
            alternatives.append({
                'route_points': route,
                'estimated_time_minutes': time_estimate + random.randint(2, 8),
                'description': f'Alternative route {i + 1}'
            })
        
        return alternatives