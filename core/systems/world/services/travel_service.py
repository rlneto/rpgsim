"""
Travel logic and route calculation services
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from ..domain.world import World, Location, TravelConnection, TravelRequirement, TravelRequirementType


@dataclass
class TravelRoute:
    """Travel route with multiple steps"""
    from_location: str
    to_location: str
    steps: List[Dict]
    total_time: int
    total_difficulty: float
    requirements: List[TravelRequirement]
    is_valid: bool = True
    
    def get_summary(self) -> Dict:
        """Get route summary"""
        return {
            "from": self.from_location,
            "to": self.to_location,
            "steps": len(self.steps),
            "total_time": self.total_time,
            "total_difficulty": self.total_difficulty,
            "requirements": [req.get_total_requirements() for req in self.requirements],
            "valid": self.is_valid
        }


class TravelService:
    """Service for travel logic and route calculation"""
    
    def __init__(self, world: World):
        self.world = world
    
    def can_travel(self, from_location_id: str, to_location_id: str, character_data: Dict) -> bool:
        """Check if character can travel directly between locations"""
        if not self.world:
            return False
        
        return self.world.can_travel(from_location_id, to_location_id, character_data)
    
    def calculate_travel_time(self, from_location_id: str, to_location_id: str, character_data: Dict) -> int:
        """Calculate travel time for direct travel"""
        if not self.world:
            return 0
        
        connections = self.world.get_connections_from(from_location_id)
        
        for connection in connections:
            if connection.to_location_id == to_location_id:
                return self.world.calculate_travel_time(connection, character_data)
        
        return 0
    
    def get_travel_requirements(self, from_location_id: str, to_location_id: str) -> List[TravelRequirement]:
        """Get travel requirements for direct travel"""
        if not self.world:
            return []
        
        connections = self.world.get_connections_from(from_location_id)
        
        for connection in connections:
            if connection.to_location_id == to_location_id:
                return connection.requirements
        
        return []
    
    def find_route(self, from_location_id: str, to_location_id: str, character_data: Dict) -> Optional[TravelRoute]:
        """Find best route between two locations using pathfinding"""
        if not self.world:
            return None
        
        # Validate locations exist
        if from_location_id not in self.world.locations or to_location_id not in self.world.locations:
            return None
        
        # Use BFS to find shortest path
        route = self._bfs_pathfinding(from_location_id, to_location_id, character_data)
        return route
    
    def _bfs_pathfinding(self, start: str, end: str, character_data: Dict) -> Optional[TravelRoute]:
        """BFS pathfinding algorithm"""
        from collections import deque
        
        queue = deque([(start, [], 0, 0, [])])  # (current, path, time, difficulty, requirements)
        visited = set()
        
        while queue:
            current, path, total_time, total_difficulty, all_requirements = queue.popleft()
            
            if current in visited:
                continue
            
            visited.add(current)
            new_path = path + [current]
            
            if current == end:
                # Found destination
                steps = self._build_route_steps(new_path)
                return TravelRoute(
                    from_location=start,
                    to_location=end,
                    steps=steps,
                    total_time=total_time,
                    total_difficulty=total_difficulty,
                    requirements=all_requirements
                )
            
            # Explore connections
            connections = self.world.get_connections_from(current)
            for connection in connections:
                # Check if character can travel this connection
                if connection.can_travel(character_data):
                    next_loc = connection.to_location_id
                    if next_loc not in visited:
                        travel_time = self.world.calculate_travel_time(connection, character_data)
                        new_total_time = total_time + travel_time
                        new_total_difficulty = total_difficulty + connection.difficulty
                        new_requirements = all_requirements + connection.requirements
                        
                        queue.append((
                            next_loc,
                            new_path,
                            new_total_time,
                            new_total_difficulty,
                            new_requirements
                        ))
        
        # No route found
        return None
    
    def _build_route_steps(self, path: List[str]) -> List[Dict]:
        """Build route steps from path"""
        steps = []
        
        for i in range(len(path) - 1):
            from_loc = path[i]
            to_loc = path[i + 1]
            
            # Get connection details
            connections = self.world.get_connections_from(from_loc)
            connection = None
            for conn in connections:
                if conn.to_location_id == to_loc:
                    connection = conn
                    break
            
            if connection:
                steps.append({
                    "from": from_loc,
                    "to": to_loc,
                    "from_name": self.world.get_location(from_loc).name,
                    "to_name": self.world.get_location(to_loc).name,
                    "travel_time": connection.travel_time,
                    "difficulty": connection.difficulty,
                    "requirements": [req.get_total_requirements() for req in connection.requirements],
                    "description": connection.description
                })
        
        return steps
    
    def get_available_destinations(self, from_location_id: str, character_data: Dict) -> List[Dict]:
        """Get all available destinations from a location"""
        if not self.world:
            return []
        
        connections = self.world.get_connections_from(from_location_id)
        destinations = []
        
        for connection in connections:
            if connection.can_travel(character_data):
                to_location = self.world.get_location(connection.to_location_id)
                if to_location:
                    travel_time = self.world.calculate_travel_time(connection, character_data)
                    destinations.append({
                        "location_id": connection.to_location_id,
                        "name": to_location.name,
                        "type": to_location.location_type.value,
                        "travel_time": travel_time,
                        "difficulty": connection.difficulty,
                        "requirements": [req.get_total_requirements() for req in connection.requirements],
                        "description": connection.description
                    })
        
        return destinations
    
    def calculate_route_optimization(self, routes: List[TravelRoute], character_data: Dict) -> TravelRoute:
        """Optimize route selection based on character preferences"""
        if not routes:
            return None
        
        # Sort by priority: time first, then difficulty
        sorted_routes = sorted(routes, key=lambda r: (r.total_time, r.total_difficulty))
        
        return sorted_routes[0]
    
    def simulate_travel(self, route: TravelRoute, character_data: Dict) -> Dict:
        """Simulate travel along a route"""
        if not route or not route.is_valid:
            return {"success": False, "reason": "Invalid route"}
        
        simulation = {
            "success": True,
            "route": route.get_summary(),
            "events": [],
            "final_time": route.total_time,
            "resources_used": {}
        }
        
        # Simulate each step
        for i, step in enumerate(route.steps):
            step_events = []
            
            # Random events based on difficulty
            import random
            if random.random() < step["difficulty"] * 0.1:
                event_type = random.choice(["encounter", "delay", "discovery"])
                step_events.append({
                    "step": i + 1,
                    "type": event_type,
                    "description": f"Random {event_type} during travel"
                })
            
            # Resource consumption
            if "gold" in character_data:
                gold_cost = step["difficulty"] * 5
                simulation["resources_used"][f"step_{i+1}_gold"] = gold_cost
            
            simulation["events"].extend(step_events)
        
        return simulation
    
    def get_travel_statistics(self, character_data: Dict) -> Dict:
        """Get travel statistics for character"""
        if not self.world:
            return {}
        
        stats = {
            "total_locations": len(self.world.locations),
            "accessible_locations": len(self.world.get_accessible_locations(character_data)),
            "total_connections": sum(len(conns) for conns in self.world.connections.values()),
            "reachable_from_start": 0
        }
        
        # Count reachable locations from start
        start_location = self.world.get_start_location()
        if start_location:
            destinations = self.get_available_destinations(start_location.id, character_data)
            stats["reachable_from_start"] = len(destinations)
        
        return stats