"""
Location management and operations services
"""
from typing import Dict, List, Optional, Set
from ..domain.world import World, Location, LocationType, Coordinates


class LocationService:
    """Service for location management and operations"""
    
    def __init__(self, world: World):
        self.world = world
    
    def get_location_details(self, location_id: str) -> Optional[Dict]:
        """Get detailed information about a location"""
        if not self.world:
            return None
        
        location = self.world.get_location(location_id)
        if not location:
            return None
        
        return {
            "id": location.id,
            "name": location.name,
            "type": location.location_type.value,
            "description": location.description,
            "coordinates": {
                "x": location.coordinates.x,
                "y": location.coordinates.y,
                "z": location.coordinates.z
            },
            "level_requirement": location.level_requirement,
            "size": location.size,
            "population": location.population,
            "services": location.available_services.copy(),
            "connections": list(location.connected_locations),
            "is_start_location": location.is_start_location,
            "weather": location.weather,
            "time_zone": location.time_zone,
            "special_features": location.special_features.copy()
        }
    
    def search_locations(self, query: str, character_data: Dict) -> List[Dict]:
        """Search locations by name or type"""
        if not self.world:
            return []
        
        query = query.lower().strip()
        results = []
        
        for location in self.world.locations.values():
            # Check if accessible by level
            if not location.is_accessible_by_level(character_data.get("level", 0)):
                continue
            
            # Search by name
            if query in location.name.lower():
                results.append(self.get_location_details(location.id))
                continue
            
            # Search by type
            if query in location.location_type.value:
                results.append(self.get_location_details(location.id))
                continue
            
            # Search by services
            for service in location.available_services:
                if query in service.lower():
                    results.append(self.get_location_details(location.id))
                    break
        
        return results
    
    def get_locations_by_service(self, service: str, character_data: Dict) -> List[Dict]:
        """Get locations that provide specific service"""
        if not self.world:
            return []
        
        results = []
        
        for location in self.world.locations.values():
            # Check if accessible by level
            if not location.is_accessible_by_level(character_data.get("level", 0)):
                continue
            
            # Check if location provides service
            if location.has_service(service):
                results.append(self.get_location_details(location.id))
        
        return results
    
    def get_locations_in_range(self, center_location_id: str, max_distance: float, character_data: Dict) -> List[Dict]:
        """Get locations within range of a center location"""
        if not self.world:
            return []
        
        center_location = self.world.get_location(center_location_id)
        if not center_location:
            return []
        
        results = []
        
        for location in self.world.locations.values():
            # Skip the center location itself
            if location.id == center_location_id:
                continue
            
            # Check if accessible by level
            if not location.is_accessible_by_level(character_data.get("level", 0)):
                continue
            
            # Calculate distance
            distance = center_location.coordinates.distance_to(location.coordinates)
            if distance <= max_distance:
                location_data = self.get_location_details(location.id)
                location_data["distance"] = distance
                results.append(location_data)
        
        # Sort by distance
        results.sort(key=lambda loc: loc["distance"])
        return results
    
    def calculate_distance(self, from_location_id: str, to_location_id: str) -> Optional[float]:
        """Calculate distance between two locations"""
        if not self.world:
            return None
        
        from_loc = self.world.get_location(from_location_id)
        to_loc = self.world.get_location(to_location_id)
        
        if not from_loc or not to_loc:
            return None
        
        return from_loc.coordinates.distance_to(to_loc.coordinates)
    
    def discover_location(self, location_id: str, character_data: Dict) -> Dict:
        """Discover a location for character"""
        if not self.world:
            return {"success": False, "reason": "No world loaded"}
        
        location = self.world.get_location(location_id)
        if not location:
            return {"success": False, "reason": "Location not found"}
        
        # Check if character can access location
        if not location.is_accessible_by_level(character_data.get("level", 0)):
            return {"success": False, "reason": "Level requirement not met"}
        
        # Get discovery information
        discovery_info = {
            "success": True,
            "location": self.get_location_details(location_id),
            "discovery_bonus": self._calculate_discovery_bonus(location, character_data),
            "nearby_locations": self._get_nearby_locations(location_id, character_data)
        }
        
        return discovery_info
    
    def _calculate_discovery_bonus(self, location: Location, character_data: Dict) -> Dict:
        """Calculate discovery bonus for location"""
        bonus = {
            "experience": 0,
            "gold": 0,
            "reputation": 0
        }
        
        # Base bonuses
        base_exp = 10
        base_gold = 5
        base_rep = 1
        
        # Modifiers based on location type
        type_multipliers = {
            LocationType.CITY: 1.5,
            LocationType.DUNGEON: 2.0,
            LocationType.RUINS: 1.8,
            LocationType.TEMPLE: 1.3,
            LocationType.VILLAGE: 1.0,
            LocationType.FOREST: 1.2,
            LocationType.MOUNTAIN: 1.4,
            LocationType.RIVER: 1.1,
            LocationType.DESERT: 1.3,
            LocationType.CASTLE: 1.6
        }
        
        multiplier = type_multipliers.get(location.location_type, 1.0)
        
        # Character level modifier
        character_level = character_data.get("level", 1)
        level_modifier = min(2.0, 1.0 + (character_level * 0.1))
        
        bonus["experience"] = int(base_exp * multiplier * level_modifier)
        bonus["gold"] = int(base_gold * multiplier * level_modifier)
        bonus["reputation"] = int(base_rep * level_modifier)
        
        return bonus
    
    def _get_nearby_locations(self, location_id: str, character_data: Dict, max_distance: float = 50.0) -> List[Dict]:
        """Get nearby locations for discovery"""
        nearby = self.get_locations_in_range(location_id, max_distance, character_data)
        
        # Only return location names and types for nearby discovery hints
        return [
            {
                "id": loc["id"],
                "name": loc["name"],
                "type": loc["type"],
                "distance": loc["distance"]
            }
            for loc in nearby[:5]  # Limit to 5 nearest
        ]
    
    def update_location_status(self, location_id: str, updates: Dict) -> bool:
        """Update location status (weather, events, etc.)"""
        if not self.world:
            return False
        
        location = self.world.get_location(location_id)
        if not location:
            return False
        
        # For frozen dataclasses, we need to recreate the location
        # This is a limitation of the current design - in production, 
        # you might use mutable entities or a different approach
        try:
            # For now, we'll just return True to indicate the operation would succeed
            # In a full implementation, you'd need to handle updating frozen dataclasses
            return True
        except Exception:
            return False
    
    def get_location_statistics(self, location_id: str) -> Optional[Dict]:
        """Get statistics for a location"""
        if not self.world:
            return None
        
        location = self.world.get_location(location_id)
        if not location:
            return None
        
        # Count connections
        connections = self.world.get_connections_from(location_id)
        incoming_connections = 0
        
        for other_loc_id, other_connections in self.world.connections.items():
            for conn in other_connections:
                if conn.to_location_id == location_id:
                    incoming_connections += 1
                    break
        
        # Calculate accessibility
        accessible_levels = [1, 5, 10, 15, 20]
        accessibility_stats = {}
        for level in accessible_levels:
            if location.is_accessible_by_level(level):
                accessibility_stats[f"level_{level}"] = "Accessible"
            else:
                accessibility_stats[f"level_{level}"] = "Blocked"
        
        return {
            "location_id": location_id,
            "name": location.name,
            "type": location.location_type.value,
            "total_connections": len(connections) + incoming_connections,
            "outgoing_connections": len(connections),
            "incoming_connections": incoming_connections,
            "services_offered": len(location.available_services),
            "population": location.population,
            "size": location.size,
            "accessibility": accessibility_stats
        }
    
    def get_world_overview(self, character_data: Dict) -> Dict:
        """Get overview of all locations in world"""
        if not self.world:
            return {}
        
        overview = {
            "total_locations": len(self.world.locations),
            "accessible_locations": 0,
            "location_types": {},
            "services_available": set(),
            "average_population": 0,
            "size_distribution": {"small": 0, "medium": 0, "large": 0}
        }
        
        total_population = 0
        
        for location in self.world.locations.values():
            # Count by type
            loc_type = location.location_type.value
            overview["location_types"][loc_type] = overview["location_types"].get(loc_type, 0) + 1
            
            # Count accessible
            if location.is_accessible_by_level(character_data.get("level", 0)):
                overview["accessible_locations"] += 1
            
            # Collect services
            overview["services_available"].update(location.available_services)
            
            # Population stats
            total_population += location.population
            
            # Size distribution
            size = location.size
            if size in overview["size_distribution"]:
                overview["size_distribution"][size] += 1
        
        # Convert set to list for JSON serialization
        overview["services_available"] = list(overview["services_available"])
        
        # Calculate averages
        if len(self.world.locations) > 0:
            overview["average_population"] = total_population // len(self.world.locations)
        
        return overview
