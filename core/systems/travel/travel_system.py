"""
Travel System for Economic Infrastructure
FOCUS: Travel between cities with costs and routes
"""

from typing import Dict, List, Optional, Any
import random

# Global travel state
_travel_routes = {}
_travel_costs = {}
_travel_history = []

class TravelManager:
    """Manager for travel between cities"""
    
    def __init__(self):
        self.routes = _travel_routes
        self.costs = _travel_costs
        self.history = _travel_history
        self._initialize_travel_routes()
    
    def _initialize_travel_routes(self):
        """Initialize default travel routes"""
        default_routes = {
            "silverbrook_village": {
                "riverdale": {
                    "distance": 50,
                    "travel_time": 2,  # days
                    "cost": 20,
                    "difficulty": "easy",
                    "route_type": "road",
                    "dangers": ["bandits", "wild_animals"],
                    "landmarks": ["old_bridge", "riverside_inn"]
                },
                "mountain_fortress": {
                    "distance": 80,
                    "travel_time": 4,
                    "cost": 40,
                    "difficulty": "hard",
                    "route_type": "mountain_pass",
                    "dangers": ["avalanche", "mountain_lions", "frost"],
                    "landmarks": ["summit_view", "ice_cave"]
                }
            },
            "riverdale": {
                "port_city": {
                    "distance": 100,
                    "travel_time": 5,
                    "cost": 60,
                    "difficulty": "medium",
                    "route_type": "river",
                    "dangers": ["pirates", "storms", "river_monsters"],
                    "landmarks": ["trading_post", "lighthouse"]
                },
                "silverbrook_village": {
                    "distance": 50,
                    "travel_time": 2,
                    "cost": 20,
                    "difficulty": "easy",
                    "route_type": "road",
                    "dangers": ["bandits", "wild_animals"],
                    "landmarks": ["old_bridge", "riverside_inn"]
                }
            },
            "port_city": {
                "riverdale": {
                    "distance": 100,
                    "travel_time": 5,
                    "cost": 60,
                    "difficulty": "medium",
                    "route_type": "river",
                    "dangers": ["pirates", "storms", "river_monsters"],
                    "landmarks": ["trading_post", "lighthouse"]
                },
                "mountain_fortress": {
                    "distance": 150,
                    "travel_time": 8,
                    "cost": 100,
                    "difficulty": "hard",
                    "route_type": "coastal_road",
                    "dangers": ["coastal_raiders", "sea_storms", "cliff_paths"],
                    "landmarks": ["sea_cave", "coastal_village"]
                }
            }
        }
        
        self.routes.update(default_routes)
        
        # Calculate travel costs matrix
        for from_city, destinations in self.routes.items():
            self.costs[from_city] = {}
            for to_city, route_info in destinations.items():
                self.costs[from_city][to_city] = route_info["cost"]
    
    def get_available_destinations(self, from_city: str) -> Dict:
        """Get available travel destinations from city"""
        if from_city not in self.routes:
            return {"error": f"City '{from_city}' not found"}
        
        destinations = self.routes[from_city]
        
        return {
            "from_city": from_city,
            "destinations": [
                {
                    "to_city": to_city,
                    "distance": route["distance"],
                    "travel_time": route["travel_time"],
                    "cost": route["cost"],
                    "difficulty": route["difficulty"],
                    "route_type": route["route_type"]
                }
                for to_city, route in destinations.items()
            ]
        }
    
    def get_travel_route(self, from_city: str, to_city: str) -> Dict:
        """Get specific travel route information"""
        if from_city not in self.routes:
            return {"error": f"City '{from_city}' not found"}
        
        if to_city not in self.routes[from_city]:
            return {"error": f"No route from '{from_city}' to '{to_city}'"}
        
        route = self.routes[from_city][to_city]
        
        return {
            "from_city": from_city,
            "to_city": to_city,
            "route_info": route,
            "description": f"Travel from {from_city} to {to_city} via {route['route_type']}"
        }
    
    def calculate_travel_cost(self, from_city: str, to_city: str, character_level: int = 1) -> Dict:
        """Calculate travel cost with character discounts"""
        route_info = self.get_travel_route(from_city, to_city)
        
        if "error" in route_info:
            return route_info
        
        base_cost = route_info["route_info"]["cost"]
        
        # Character level discounts
        if character_level >= 10:
            discount = 0.20  # 20% discount for high level
        elif character_level >= 5:
            discount = 0.10  # 10% discount for mid level
        else:
            discount = 0.0
        
        final_cost = int(base_cost * (1 - discount))
        
        return {
            "from_city": from_city,
            "to_city": to_city,
            "base_cost": base_cost,
            "character_level": character_level,
            "discount": discount,
            "final_cost": final_cost,
            "savings": base_cost - final_cost
        }
    
    def initiate_travel(self, character_id: str, from_city: str, to_city: str, character_gold: int, character_level: int = 1) -> Dict:
        """Initiate travel between cities"""
        # Check route exists
        route_info = self.get_travel_route(from_city, to_city)
        
        if "error" in route_info:
            return route_info
        
        # Calculate cost
        cost_info = self.calculate_travel_cost(from_city, to_city, character_level)
        
        # Check if character has enough gold
        if character_gold < cost_info["final_cost"]:
            return {
                "error": "Insufficient gold for travel",
                "required": cost_info["final_cost"],
                "available": character_gold,
                "shortfall": cost_info["final_cost"] - character_gold
            }
        
        # Simulate travel events
        travel_event = self._simulate_travel_events(route_info["route_info"])
        
        # Record travel in history
        travel_record = {
            "character_id": character_id,
            "from_city": from_city,
            "to_city": to_city,
            "cost": cost_info["final_cost"],
            "travel_time": route_info["route_info"]["travel_time"],
            "travel_event": travel_event,
            "timestamp": len(self.history) + 1
        }
        
        self.history.append(travel_record)
        
        return {
            "status": "travel_initiated",
            "character_id": character_id,
            "from_city": from_city,
            "to_city": to_city,
            "travel_time": route_info["route_info"]["travel_time"],
            "cost": cost_info["final_cost"],
            "travel_event": travel_event,
            "arrival_time": len(self.history) + route_info["route_info"]["travel_time"]
        }
    
    def _simulate_travel_events(self, route_info: Dict) -> Optional[Dict]:
        """Simulate random travel events"""
        # Base event chance
        event_chance = 0.2  # 20% chance
        
        # Adjust based on route difficulty
        if route_info["difficulty"] == "hard":
            event_chance = 0.4  # 40% chance for hard routes
        elif route_info["difficulty"] == "easy":
            event_chance = 0.1  # 10% chance for easy routes
        
        if random.random() > event_chance:
            return None
        
        # Random events based on route dangers
        dangers = route_info.get("dangers", [])
        
        if not dangers:
            return None
        
        danger = random.choice(dangers)
        
        events = {
            "bandits": {"type": "combat", "description": "Bandits attack!", "outcome": "fight"},
            "wild_animals": {"type": "encounter", "description": "Wild animals cross your path!", "outcome": "avoid"},
            "avalanche": {"type": "obstacle", "description": "Avalanche blocks the path!", "outcome": "delay"},
            "mountain_lions": {"type": "combat", "description": "Mountain lions attack!", "outcome": "fight"},
            "pirates": {"type": "combat", "description": "Pirates raid your travel group!", "outcome": "fight"},
            "storms": {"type": "obstacle", "description": "Severe storms delay travel!", "outcome": "delay"},
            "river_monsters": {"type": "encounter", "description": "River monsters surface nearby!", "outcome": "avoid"}
        }
        
        event = events.get(danger, {"type": "unknown", "description": "Something happens...", "outcome": "unknown"})
        
        return {
            "danger": danger,
            "event": event,
            "description": event["description"],
            "outcome": event["outcome"]
        }
    
    def get_travel_history(self, character_id: Optional[str] = None) -> Dict:
        """Get travel history"""
        if character_id:
            character_travels = [t for t in self.history if t["character_id"] == character_id]
            return {
                "character_id": character_id,
                "travel_history": character_travels,
                "total_travels": len(character_travels)
            }
        
        return {
            "all_travel_history": self.history,
            "total_travels": len(self.history)
        }
    
    def get_all_routes(self) -> Dict:
        """Get all available travel routes"""
        all_routes = []
        
        for from_city, destinations in self.routes.items():
            for to_city, route_info in destinations.items():
                all_routes.append({
                    "from_city": from_city,
                    "to_city": to_city,
                    "route_info": route_info
                })
        
        return {
            "total_routes": len(all_routes),
            "routes": all_routes
        }

# Create global travel manager
_travel_manager = None

def get_travel_manager():
    """Get global travel manager"""
    global _travel_manager
    if _travel_manager is None:
        _travel_manager = TravelManager()
    return _travel_manager

# Quick BDD functions
def get_available_destinations(from_city: str) -> Dict:
    """Get available travel destinations (BDD compliant)"""
    manager = get_travel_manager()
    return manager.get_available_destinations(from_city)

def get_travel_route(from_city: str, to_city: str) -> Dict:
    """Get travel route information (BDD compliant)"""
    manager = get_travel_manager()
    return manager.get_travel_route(from_city, to_city)

def calculate_travel_cost(from_city: str, to_city: str, character_level: int = 1) -> Dict:
    """Calculate travel cost (BDD compliant)"""
    manager = get_travel_manager()
    return manager.calculate_travel_cost(from_city, to_city, character_level)

def initiate_travel(character_id: str, from_city: str, to_city: str, character_gold: int, character_level: int = 1) -> Dict:
    """Initiate travel (BDD compliant)"""
    manager = get_travel_manager()
    return manager.initiate_travel(character_id, from_city, to_city, character_gold, character_level)

def get_all_travel_routes() -> Dict:
    """Get all travel routes (BDD compliant)"""
    manager = get_travel_manager()
    return manager.get_all_routes()
