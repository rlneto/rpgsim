"""
SPRINT 4: ECONOMIC INFRASTRUCTURE - WP-002
FOCUS: Economic foundation for RPG simulation
STRATEGY: Extend existing systems, respect project.md, single entry point
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def implement_economic_infrastructure():
    """Implement economic infrastructure for RPG simulation"""
    
    print("💰 SPRINT 4: ECONOMIC INFRASTRUCTURE")
    print("="*70)
    print("🎯 WORKING PACKAGE: WP-002 - Economic Foundation")
    print("✅ RESPECTING: project.md structure + BDD foundation")
    print()
    
    # 1. CITY MANAGEMENT SYSTEM
    print("🏰 IMPLEMENTING CITY MANAGEMENT SYSTEM...")
    implement_city_management()
    
    # 2. TRAVEL SYSTEM
    print("🗺️ IMPLEMENTING TRAVEL SYSTEM...")
    implement_travel_system()
    
    # 3. SHOP SYSTEM
    print("🏪 IMPLEMENTING SHOP SYSTEM...")
    implement_shop_system()
    
    # 4. INTEGRATION TESTING
    print("🧪 IMPLEMENTING INTEGRATION...")
    implement_economic_integration()
    
    print()
    print("✅ SPRINT 4 ECONOMIC INFRASTRUCTURE COMPLETE!")
    print("💰 City Management • 🗺️ Travel • 🏪 Shopping • 🧪 Integration")
    print("🚀 RUN: ./venv/bin/python main.py")

def implement_city_management():
    """Implement city management system"""
    
    city_management_code = '''"""
City Management System for Economic Infrastructure
FOCUS: Living cities with economy, NPCs, and services
"""

from typing import Dict, List, Optional, Any
import random
import json

# Global city state
_cities = {}
_city_events = []
_city_populations = {}

class CityManager:
    """Manager for city systems and economy"""
    
    def __init__(self):
        self.cities = _cities
        self.events = _city_events
        self.populations = _city_populations
        self._initialize_default_cities()
    
    def _initialize_default_cities(self):
        """Initialize default cities for economic system"""
        default_cities = {
            "silverbrook_village": {
                "city_id": "silverbrook_village",
                "name": "Silverbrook Village",
                "type": "village",
                "size": "small",
                "population": 250,
                "economy": {
                    "gold_flow": 1000,  # Daily gold flow
                    "goods_produced": ["wheat", "livestock", "wood"],
                    "goods_needed": ["weapons", "armor", "tools"],
                    "trade_routes": ["river_valley", "mountain_pass"],
                    "tax_rate": 0.10,
                    "prosperity": 0.7  # 0.0 to 1.0
                },
                "services": {
                    "tavern": {"name": "Silver Tavern", "daily_income": 50, "customers": 20},
                    "blacksmith": {"name": "Silver Forge", "daily_income": 80, "customers": 15},
                    "market": {"name": "Village Market", "daily_income": 120, "customers": 50},
                    "inn": {"name": "Traveler's Rest", "daily_income": 60, "customers": 10}
                },
                "npcs": [
                    {"id": "mayor_thompson", "name": "Mayor Thompson", "role": "mayor", "wealth": 500},
                    {"id": "bartender", "name": "Sam", "role": "bartender", "wealth": 200},
                    {"id": "blacksmith", "name": "Thorin", "role": "blacksmith", "wealth": 800},
                    {"id": "merchant", "name": "Elara", "role": "merchant", "wealth": 1200}
                ],
                "locations": [
                    {"id": "town_square", "name": "Town Square", "type": "public", "activity": "high"},
                    {"id": "market_place", "name": "Market Place", "type": "commercial", "activity": "medium"},
                    {"id": "residential_area", "name": "Residential Area", "type": "residential", "activity": "low"},
                    {"id": "docks", "name": "Docks", "type": "transport", "activity": "medium"}
                ]
            },
            "riverdale": {
                "city_id": "riverdale",
                "name": "Riverdale",
                "type": "town",
                "size": "medium",
                "population": 800,
                "economy": {
                    "gold_flow": 3500,
                    "goods_produced": ["fish", "grain", "crafts"],
                    "goods_needed": ["iron", "wood", "luxury"],
                    "trade_routes": ["silverbrook", "mountain_fortress", "port_city"],
                    "tax_rate": 0.12,
                    "prosperity": 0.8
                },
                "services": {
                    "tavern": {"name": "Riverside Inn", "daily_income": 150, "customers": 60},
                    "blacksmith": {"name": "River Forge", "daily_income": 200, "customers": 40},
                    "market": {"name": "Riverdale Market", "daily_income": 400, "customers": 150},
                    "bank": {"name": "Riverdale Bank", "daily_income": 100, "customers": 80}
                },
                "npcs": [
                    {"id": "riverdale_mayor", "name": "Mayor Grant", "role": "mayor", "wealth": 2000},
                    {"id": "captain", "name": "Captain Morgan", "role": "guard_captain", "wealth": 600},
                    {"id": "banker", "name": "Mr. Sterling", "role": "banker", "wealth": 5000}
                ],
                "locations": [
                    {"id": "river_docks", "name": "River Docks", "type": "transport", "activity": "high"},
                    {"id": "merchant_district", "name": "Merchant District", "type": "commercial", "activity": "high"},
                    {"id": "temple_square", "name": "Temple Square", "type": "religious", "activity": "medium"}
                ]
            }
        }
        
        self.cities.update(default_cities)
        
        # Initialize populations
        for city_id, city_data in self.cities.items():
            self.populations[city_id] = city_data["population"]
    
    def get_city_info(self, city_id: str) -> Dict:
        """Get comprehensive city information"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        return {
            "city_id": city_id,
            "name": city["name"],
            "type": city["type"],
            "size": city["size"],
            "population": city["population"],
            "economy": city["economy"],
            "services": city["services"],
            "npcs": city["npcs"],
            "locations": city["locations"]
        }
    
    def get_city_economy(self, city_id: str) -> Dict:
        """Get city economic information"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        economy = city["economy"]
        
        # Calculate daily economic metrics
        total_services_income = sum(
            service["daily_income"] for service in city["services"].values()
        )
        
        daily_tax_revenue = economy["gold_flow"] * economy["tax_rate"]
        net_daily_income = total_services_income + daily_tax_revenue
        
        return {
            "city_id": city_id,
            "gold_flow": economy["gold_flow"],
            "tax_rate": economy["tax_rate"],
            "daily_services_income": total_services_income,
            "daily_tax_revenue": daily_tax_revenue,
            "net_daily_income": net_daily_income,
            "prosperity": economy["prosperity"],
            "goods_produced": economy["goods_produced"],
            "goods_needed": economy["goods_needed"],
            "trade_routes": economy["trade_routes"]
        }
    
    def simulate_city_day(self, city_id: str) -> Dict:
        """Simulate one day of city economic activity"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        # Random economic events
        event_roll = random.randint(1, 100)
        daily_event = None
        
        if event_roll <= 10:  # 10% chance of economic event
            events = [
                {"type": "merchant_arrival", "effect": "gold_boost", "amount": 200},
                {"type": "bad_weather", "effect": "trade_disruption", "amount": -100},
                {"type": "festival", "effect": "prosperity_boost", "amount": 0.1},
                {"type": "raider_attack", "effect": "damage", "amount": -150}
            ]
            daily_event = random.choice(events)
            
            # Apply event effect
            economy = city["economy"]
            if daily_event["effect"] == "gold_boost":
                economy["gold_flow"] += daily_event["amount"]
            elif daily_event["effect"] == "trade_disruption":
                economy["gold_flow"] += daily_event["amount"]
            elif daily_event["effect"] == "prosperity_boost":
                economy["prosperity"] = min(1.0, economy["prosperity"] + daily_event["amount"])
            elif daily_event["effect"] == "damage":
                economy["gold_flow"] += daily_event["amount"]
            
            self.events.append({
                "city_id": city_id,
                "day": len(self.events) + 1,
                "event": daily_event,
                "new_gold_flow": economy["gold_flow"]
            })
        
        # Calculate daily income
        economy_info = self.get_city_economy(city_id)
        
        return {
            "city_id": city_id,
            "day_simulated": True,
            "daily_event": daily_event,
            "daily_income": economy_info["net_daily_income"],
            "current_gold_flow": economy_info["gold_flow"],
            "prosperity": economy_info["prosperity"]
        }
    
    def get_city_services(self, city_id: str) -> Dict:
        """Get available services in city"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        return {
            "city_id": city_id,
            "services": city["services"],
            "total_services": len(city["services"]),
            "daily_income": sum(service["daily_income"] for service in city["services"].values())
        }
    
    def get_city_npcs(self, city_id: str) -> Dict:
        """Get NPCs in city"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        return {
            "city_id": city_id,
            "npcs": city["npcs"],
            "total_npcs": len(city["npcs"])
        }
    
    def get_all_cities(self) -> List[Dict]:
        """Get list of all cities"""
        return [
            {
                "city_id": city_id,
                "name": city_data["name"],
                "type": city_data["type"],
                "size": city_data["size"],
                "population": city_data["population"],
                "prosperity": city_data["economy"]["prosperity"]
            }
            for city_id, city_data in self.cities.items()
        ]
    
    def update_city_prosperity(self, city_id: str, change: float) -> Dict:
        """Update city prosperity"""
        city = self.cities.get(city_id)
        if not city:
            return {"error": f"City '{city_id}' not found"}
        
        old_prosperity = city["economy"]["prosperity"]
        new_prosperity = max(0.0, min(1.0, old_prosperity + change))
        city["economy"]["prosperity"] = new_prosperity
        
        return {
            "city_id": city_id,
            "old_prosperity": old_prosperity,
            "new_prosperity": new_prosperity,
            "change": change
        }

# Create global city manager
_city_manager = None

def get_city_manager():
    """Get global city manager"""
    global _city_manager
    if _city_manager is None:
        _city_manager = CityManager()
    return _city_manager

# Quick BDD functions
def get_city_info(city_id: str) -> Dict:
    """Get city information (BDD compliant)"""
    manager = get_city_manager()
    return manager.get_city_info(city_id)

def get_city_economy(city_id: str) -> Dict:
    """Get city economy (BDD compliant)"""
    manager = get_city_manager()
    return manager.get_city_economy(city_id)

def get_city_services(city_id: str) -> Dict:
    """Get city services (BDD compliant)"""
    manager = get_city_manager()
    return manager.get_city_services(city_id)

def simulate_city_day(city_id: str) -> Dict:
    """Simulate city day (BDD compliant)"""
    manager = get_city_manager()
    return manager.simulate_city_day(city_id)

def get_all_cities() -> List[Dict]:
    """Get all cities (BDD compliant)"""
    manager = get_city_manager()
    return manager.get_all_cities()
'''
    
    # Write city management system
    city_file = os.path.join(project_root, "core/systems/city/city_management.py")
    
    os.makedirs(os.path.dirname(city_file), exist_ok=True)
    
    with open(city_file, 'w') as f:
        f.write(city_management_code)
    
    print("  ✅ City management system implemented")

def implement_travel_system():
    """Implement travel system"""
    
    travel_system_code = '''"""
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
'''
    
    # Write travel system
    travel_file = os.path.join(project_root, "core/systems/travel/travel_system.py")
    
    os.makedirs(os.path.dirname(travel_file), exist_ok=True)
    
    with open(travel_file, 'w') as f:
        f.write(travel_system_code)
    
    print("  ✅ Travel system implemented")

def implement_shop_system():
    """Implement shop system"""
    
    shop_system_code = '''"""
Shop System for Economic Infrastructure
FOCUS: Dynamic shopping with inventory management and pricing
"""

from typing import Dict, List, Optional, Any
import random

# Global shop state
_shops = {}
_shop_inventories = {}
_price_history = {}

class ShopManager:
    """Manager for shops and economic transactions"""
    
    def __init__(self):
        self.shops = _shops
        self.inventories = _shop_inventories
        self.price_history = _price_history
        self._initialize_shops()
    
    def _initialize_shops(self):
        """Initialize default shops"""
        default_shops = {
            "silver_tavern": {
                "shop_id": "silver_tavern",
                "name": "Silver Tavern",
                "city_id": "silverbrook_village",
                "type": "tavern",
                "owner": "Sam the Bartender",
                "wealth": 500,
                "reputation": 0.8,
                "pricing": {
                    "markup": 0.20,  # 20% markup
                    "discount_threshold": 100,  # Discount after 100 gold spent
                    "discount_amount": 0.10  # 10% discount
                }
            },
            "silver_forge": {
                "shop_id": "silver_forge",
                "name": "Silver Forge",
                "city_id": "silverbrook_village",
                "type": "blacksmith",
                "owner": "Thorin Smith",
                "wealth": 2000,
                "reputation": 0.9,
                "pricing": {
                    "markup": 0.25,
                    "discount_threshold": 150,
                    "discount_amount": 0.15
                }
            },
            "riverdale_market": {
                "shop_id": "riverdale_market",
                "name": "Riverdale Market",
                "city_id": "riverdale",
                "type": "general_store",
                "owner": "Merchant Guild",
                "wealth": 5000,
                "reputation": 0.7,
                "pricing": {
                    "markup": 0.15,
                    "discount_threshold": 200,
                    "discount_amount": 0.12
                }
            },
            "riverside_inn": {
                "shop_id": "riverside_inn",
                "name": "Riverside Inn",
                "city_id": "riverdale",
                "type": "inn",
                "owner": "Innkeeper Martha",
                "wealth": 800,
                "reputation": 0.85,
                "pricing": {
                    "markup": 0.30,
                    "discount_threshold": 80,
                    "discount_amount": 0.10
                }
            }
        }
        
        self.shops.update(default_shops)
        
        # Initialize shop inventories
        self._initialize_shop_inventories()
    
    def _initialize_shop_inventories(self):
        """Initialize inventories for all shops"""
        default_inventories = {
            "silver_tavern": [
                {"item_id": "ale", "name": "Ale", "type": "drink", "base_price": 5, "quantity": 50, "quality": "good"},
                {"item_id": "mead", "name": "Mead", "type": "drink", "base_price": 8, "quantity": 30, "quality": "excellent"},
                {"item_id": "stew", "name": "Hot Stew", "type": "food", "base_price": 10, "quantity": 20, "quality": "good"},
                {"item_id": "bread", "name": "Fresh Bread", "type": "food", "base_price": 3, "quantity": 40, "quality": "good"}
            ],
            "silver_forge": [
                {"item_id": "iron_sword", "name": "Iron Sword", "type": "weapon", "base_price": 50, "quantity": 10, "quality": "good"},
                {"item_id": "iron_shield", "name": "Iron Shield", "type": "armor", "base_price": 30, "quantity": 15, "quality": "good"},
                {"item_id": "steel_axe", "name": "Steel Axe", "type": "weapon", "base_price": 80, "quantity": 5, "quality": "excellent"},
                {"item_id": "leather_armor", "name": "Leather Armor", "type": "armor", "base_price": 40, "quantity": 12, "quality": "good"}
            ],
            "riverdale_market": [
                {"item_id": "health_potion", "name": "Health Potion", "type": "consumable", "base_price": 15, "quantity": 25, "quality": "good"},
                {"item_id": "mana_potion", "name": "Mana Potion", "type": "consumable", "base_price": 20, "quantity": 20, "quality": "good"},
                {"item_id": "antidote", "name": "Antidote", "type": "consumable", "base_price": 12, "quantity": 30, "quality": "good"},
                {"item_id": "magic_scroll", "name": "Magic Scroll", "type": "scroll", "base_price": 35, "quantity": 10, "quality": "excellent"}
            ],
            "riverside_inn": [
                {"item_id": "room_rental", "name": "Room Rental", "type": "service", "base_price": 25, "quantity": 10, "quality": "good"},
                {"item_id": "breakfast", "name": "Breakfast", "type": "food", "base_price": 8, "quantity": 30, "quality": "excellent"},
                {"item_id": "bath", "name": "Hot Bath", "type": "service", "base_price": 5, "quantity": 20, "quality": "good"}
            ]
        }
        
        self.inventories.update(default_inventories)
    
    def get_shop_info(self, shop_id: str) -> Dict:
        """Get comprehensive shop information"""
        shop = self.shops.get(shop_id)
        if not shop:
            return {"error": f"Shop '{shop_id}' not found"}
        
        return {
            "shop_id": shop_id,
            "name": shop["name"],
            "city_id": shop["city_id"],
            "type": shop["type"],
            "owner": shop["owner"],
            "wealth": shop["wealth"],
            "reputation": shop["reputation"],
            "pricing": shop["pricing"]
        }
    
    def get_shop_inventory(self, shop_id: str) -> Dict:
        """Get shop inventory with pricing"""
        shop = self.shops.get(shop_id)
        if not shop:
            return {"error": f"Shop '{shop_id}' not found"}
        
        inventory = self.inventories.get(shop_id, [])
        pricing = shop["pricing"]
        
        # Calculate prices with markup and quality modifiers
        items_with_prices = []
        
        for item in inventory:
            base_price = item["base_price"]
            
            # Apply quality modifier
            quality_modifiers = {
                "poor": 0.8,
                "good": 1.0,
                "excellent": 1.3,
                "legendary": 2.0
            }
            
            quality_modifier = quality_modifiers.get(item["quality"], 1.0)
            price_with_quality = base_price * quality_modifier
            
            # Apply shop markup
            final_price = int(price_with_quality * (1 + pricing["markup"]))
            
            items_with_prices.append({
                "item_id": item["item_id"],
                "name": item["name"],
                "type": item["type"],
                "base_price": base_price,
                "final_price": final_price,
                "quantity": item["quantity"],
                "quality": item["quality"]
            })
        
        return {
            "shop_id": shop_id,
            "shop_name": shop["name"],
            "items": items_with_prices,
            "total_items": len(items_with_prices),
            "pricing_policy": pricing
        }
    
    def calculate_purchase_cost(self, shop_id: str, item_id: str, quantity: int, customer_spent_total: int = 0) -> Dict:
        """Calculate purchase cost with discounts"""
        shop = self.shops.get(shop_id)
        if not shop:
            return {"error": f"Shop '{shop_id}' not found"}
        
        inventory = self.inventories.get(shop_id, [])
        item = next((i for i in inventory if i["item_id"] == item_id), None)
        
        if not item:
            return {"error": f"Item '{item_id}' not found in shop"}
        
        if item["quantity"] < quantity:
            return {"error": f"Insufficient quantity. Available: {item['quantity']}, Requested: {quantity}"}
        
        # Calculate base cost
        base_price = item["base_price"]
        total_base_cost = base_price * quantity
        
        # Apply quality modifier
        quality_modifiers = {
            "poor": 0.8,
            "good": 1.0,
            "excellent": 1.3,
            "legendary": 2.0
        }
        
        quality_modifier = quality_modifiers.get(item["quality"], 1.0)
        cost_with_quality = total_base_cost * quality_modifier
        
        # Apply shop markup
        pricing = shop["pricing"]
        cost_with_markup = cost_with_quality * (1 + pricing["markup"])
        
        # Apply discount if threshold met
        discount = 0.0
        if customer_spent_total >= pricing["discount_threshold"]:
            discount = pricing["discount_amount"]
        
        final_cost = int(cost_with_markup * (1 - discount))
        
        return {
            "shop_id": shop_id,
            "item_id": item_id,
            "item_name": item["name"],
            "quantity": quantity,
            "base_price": base_price,
            "quality": item["quality"],
            "cost_with_quality": cost_with_quality,
            "cost_with_markup": cost_with_markup,
            "customer_spent_total": customer_spent_total,
            "discount_threshold": pricing["discount_threshold"],
            "discount_amount": discount,
            "final_cost": final_cost,
            "savings": int(cost_with_markup - final_cost)
        }
    
    def purchase_item(self, shop_id: str, item_id: str, quantity: int, character_gold: int, customer_spent_total: int = 0) -> Dict:
        """Purchase item from shop"""
        shop = self.shops.get(shop_id)
        if not shop:
            return {"error": f"Shop '{shop_id}' not found"}
        
        # Calculate cost
        cost_info = self.calculate_purchase_cost(shop_id, item_id, quantity, customer_spent_total)
        
        if "error" in cost_info:
            return cost_info
        
        # Check if character has enough gold
        if character_gold < cost_info["final_cost"]:
            return {
                "error": "Insufficient gold for purchase",
                "required": cost_info["final_cost"],
                "available": character_gold,
                "shortfall": cost_info["final_cost"] - character_gold
            }
        
        # Update shop inventory
        inventory = self.inventories.get(shop_id, [])
        item = next((i for i in inventory if i["item_id"] == item_id), None)
        
        if item:
            item["quantity"] -= quantity
            
            # Remove item if quantity reaches 0
            if item["quantity"] <= 0:
                inventory.remove(item)
        
        # Update shop wealth
        shop["wealth"] += cost_info["final_cost"]
        
        # Record transaction (simplified for BDD)
        transaction = {
            "shop_id": shop_id,
            "item_id": item_id,
            "quantity": quantity,
            "cost": cost_info["final_cost"],
            "timestamp": len(self.price_history) + 1
        }
        
        if shop_id not in self.price_history:
            self.price_history[shop_id] = []
        
        self.price_history[shop_id].append(transaction)
        
        return {
            "status": "purchase_complete",
            "shop_id": shop_id,
            "item_id": item_id,
            "item_name": cost_info["item_name"],
            "quantity": quantity,
            "final_cost": cost_info["final_cost"],
            "customer_spent_total": customer_spent_total + cost_info["final_cost"],
            "shop_wealth": shop["wealth"],
            "message": f"Purchased {quantity}x {cost_info['item_name']} for {cost_info['final_cost']} gold"
        }
    
    def get_shops_in_city(self, city_id: str) -> Dict:
        """Get all shops in a city"""
        city_shops = [
            shop for shop in self.shops.values() 
            if shop["city_id"] == city_id
        ]
        
        return {
            "city_id": city_id,
            "shops": city_shops,
            "total_shops": len(city_shops)
        }
    
    def get_all_shops(self) -> Dict:
        """Get all shops in all cities"""
        return {
            "total_shops": len(self.shops),
            "shops": [
                {
                    "shop_id": shop_id,
                    "name": shop["name"],
                    "city_id": shop["city_id"],
                    "type": shop["type"],
                    "reputation": shop["reputation"],
                    "wealth": shop["wealth"]
                }
                for shop_id, shop in self.shops.items()
            ]
        }
    
    def update_shop_prices(self, shop_id: str, price_change_factor: float) -> Dict:
        """Update shop prices (economic simulation)"""
        shop = self.shops.get(shop_id)
        if not shop:
            return {"error": f"Shop '{shop_id}' not found"}
        
        # Update markup
        old_markup = shop["pricing"]["markup"]
        new_markup = max(0.05, min(1.0, old_markup * price_change_factor))
        shop["pricing"]["markup"] = new_markup
        
        return {
            "shop_id": shop_id,
            "old_markup": old_markup,
            "new_markup": new_markup,
            "change_factor": price_change_factor
        }

# Create global shop manager
_shop_manager = None

def get_shop_manager():
    """Get global shop manager"""
    global _shop_manager
    if _shop_manager is None:
        _shop_manager = ShopManager()
    return _shop_manager

# Quick BDD functions
def get_shop_info(shop_id: str) -> Dict:
    """Get shop information (BDD compliant)"""
    manager = get_shop_manager()
    return manager.get_shop_info(shop_id)

def get_shop_inventory(shop_id: str) -> Dict:
    """Get shop inventory (BDD compliant)"""
    manager = get_shop_manager()
    return manager.get_shop_inventory(shop_id)

def purchase_item(shop_id: str, item_id: str, quantity: int, character_gold: int, customer_spent_total: int = 0) -> Dict:
    """Purchase item (BDD compliant)"""
    manager = get_shop_manager()
    return manager.purchase_item(shop_id, item_id, quantity, character_gold, customer_spent_total)

def get_shops_in_city(city_id: str) -> Dict:
    """Get shops in city (BDD compliant)"""
    manager = get_shop_manager()
    return manager.get_shops_in_city(city_id)

def get_all_shops() -> Dict:
    """Get all shops (BDD compliant)"""
    manager = get_shop_manager()
    return manager.get_all_shops()
'''
    
    # Write shop system
    shop_file = os.path.join(project_root, "core/systems/shop/shop_system.py")
    
    os.makedirs(os.path.dirname(shop_file), exist_ok=True)
    
    with open(shop_file, 'w') as f:
        f.write(shop_system_code)
    
    print("  ✅ Shop system implemented")

def implement_economic_integration():
    """Implement economic system integration"""
    
    integration_code = '''"""
Economic System Integration for WP-002
FOCUS: Connect all economic systems (city, travel, shop)
"""

from typing import Dict, List, Optional, Any
import random

class EconomicIntegration:
    """Integration manager for all economic systems"""
    
    def __init__(self):
        self._import_managers()
    
    def _import_managers(self):
        """Import all economic managers"""
        try:
            from .city.city_management import get_city_manager
            from .travel.travel_system import get_travel_manager
            from .shop.shop_system import get_shop_manager
            
            self.city_manager = get_city_manager()
            self.travel_manager = get_travel_manager()
            self.shop_manager = get_shop_manager()
            
        except ImportError as e:
            print(f"Warning: Could not import economic managers: {e}")
            self.city_manager = None
            self.travel_manager = None
            self.shop_manager = None
    
    def get_economic_overview(self) -> Dict:
        """Get complete economic overview"""
        overview = {
            "cities": {},
            "travel_routes": {},
            "shops": {},
            "total_economy": {}
        }
        
        if self.city_manager:
            overview["cities"] = {
                city["city_id"]: city for city in self.city_manager.get_all_cities()
            }
        
        if self.travel_manager:
            overview["travel_routes"] = self.travel_manager.get_all_routes()
        
        if self.shop_manager:
            overview["shops"] = self.shop_manager.get_all_shops()
        
        # Calculate total economy metrics
        total_cities = len(overview["cities"])
        total_shops = len(overview["shops"].get("shops", []))
        
        overview["total_economy"] = {
            "total_cities": total_cities,
            "total_shops": total_shops,
            "average_shops_per_city": total_shops / max(1, total_cities),
            "economic_status": "active" if total_cities > 0 else "inactive"
        }
        
        return overview
    
    def get_city_economic_profile(self, city_id: str) -> Dict:
        """Get complete economic profile for a city"""
        profile = {
            "city_id": city_id,
            "city_info": {},
            "shops_in_city": {},
            "travel_destinations": {},
            "economic_metrics": {}
        }
        
        # Get city info
        if self.city_manager:
            profile["city_info"] = self.city_manager.get_city_info(city_id)
            profile["economic_metrics"] = self.city_manager.get_city_economy(city_id)
        
        # Get shops in city
        if self.shop_manager:
            profile["shops_in_city"] = self.shop_manager.get_shops_in_city(city_id)
        
        # Get travel destinations
        if self.travel_manager:
            profile["travel_destinations"] = self.travel_manager.get_available_destinations(city_id)
        
        return profile
    
    def simulate_economic_day(self) -> Dict:
        """Simulate one day of economic activity"""
        daily_results = {
            "city_simulations": {},
            "shop_transactions": {},
            "travel_events": {},
            "economic_summary": {}
        }
        
        # Simulate city economies
        if self.city_manager:
            cities = self.city_manager.cities.keys()
            for city_id in cities:
                city_sim = self.city_manager.simulate_city_day(city_id)
                daily_results["city_simulations"][city_id] = city_sim
        
        # Calculate economic summary
        total_cities = len(daily_results["city_simulations"])
        cities_with_events = len([
            sim for sim in daily_results["city_simulations"].values()
            if sim.get("daily_event")
        ])
        
        daily_results["economic_summary"] = {
            "simulated_cities": total_cities,
            "cities_with_events": cities_with_events,
            "event_rate": cities_with_events / max(1, total_cities),
            "economic_health": "growing" if cities_with_events > 0 else "stable"
        }
        
        return daily_results
    
    def get_character_economic_options(self, character_id: str, current_city: str, character_gold: int, character_level: int) -> Dict:
        """Get all economic options available to character"""
        options = {
            "character_id": character_id,
            "current_city": current_city,
            "available_options": {}
        }
        
        # City options
        if self.city_manager:
            city_info = self.city_manager.get_city_info(current_city)
            options["available_options"]["city"] = {
                "services": city_info.get("services", {}),
                "npcs": city_info.get("npcs", []),
                "locations": city_info.get("locations", [])
            }
        
        # Shop options
        if self.shop_manager:
            shops = self.shop_manager.get_shops_in_city(current_city)
            options["available_options"]["shops"] = shops
        
        # Travel options
        if self.travel_manager:
            destinations = self.travel_manager.get_available_destinations(current_city)
            
            # Filter by character budget
            affordable_destinations = []
            for dest in destinations.get("destinations", []):
                if dest["cost"] <= character_gold:
                    affordable_destinations.append(dest)
            
            options["available_options"]["travel"] = {
                "all_destinations": destinations,
                "affordable_destinations": affordable_destinations,
                "total_affordable": len(affordable_destinations)
            }
        
        # Character financial status
        options["financial_status"] = {
            "current_gold": character_gold,
            "character_level": character_level,
            "can_afford_travel": len(options["available_options"].get("travel", {}).get("affordable_destinations", [])) > 0,
            "shop_access": len(options["available_options"].get("shops", {}).get("shops", [])) > 0
        }
        
        return options
    
    def process_character_action(self, action_type: str, action_data: Dict) -> Dict:
        """Process character economic action"""
        if action_type == "purchase":
            return self._process_purchase(action_data)
        elif action_type == "travel":
            return self._process_travel(action_data)
        elif action_type == "city_service":
            return self._process_city_service(action_data)
        else:
            return {"error": f"Unknown action type: {action_type}"}
    
    def _process_purchase(self, action_data: Dict) -> Dict:
        """Process item purchase"""
        if not self.shop_manager:
            return {"error": "Shop system not available"}
        
        return self.shop_manager.purchase_item(
            action_data["shop_id"],
            action_data["item_id"],
            action_data["quantity"],
            action_data["character_gold"],
            action_data.get("customer_spent_total", 0)
        )
    
    def _process_travel(self, action_data: Dict) -> Dict:
        """Process travel"""
        if not self.travel_manager:
            return {"error": "Travel system not available"}
        
        return self.travel_manager.initiate_travel(
            action_data["character_id"],
            action_data["from_city"],
            action_data["to_city"],
            action_data["character_gold"],
            action_data.get("character_level", 1)
        )
    
    def _process_city_service(self, action_data: Dict) -> Dict:
        """Process city service usage"""
        # Simplified city service processing
        return {
            "status": "service_used",
            "service_type": action_data.get("service_type", "unknown"),
            "cost": action_data.get("cost", 0),
            "message": "City service used successfully"
        }

# Create global economic integration
_economic_integration = None

def get_economic_integration():
    """Get global economic integration"""
    global _economic_integration
    if _economic_integration is None:
        _economic_integration = EconomicIntegration()
    return _economic_integration

# Quick BDD functions
def get_economic_overview() -> Dict:
    """Get economic overview (BDD compliant)"""
    integration = get_economic_integration()
    return integration.get_economic_overview()

def get_city_economic_profile(city_id: str) -> Dict:
    """Get city economic profile (BDD compliant)"""
    integration = get_economic_integration()
    return integration.get_city_economic_profile(city_id)

def get_character_economic_options(character_id: str, current_city: str, character_gold: int, character_level: int) -> Dict:
    """Get character economic options (BDD compliant)"""
    integration = get_economic_integration()
    return integration.get_character_economic_options(character_id, current_city, character_gold, character_level)
'''
    
    # Write economic integration
    integration_file = os.path.join(project_root, "core/systems/economic/economic_integration.py")
    
    os.makedirs(os.path.dirname(integration_file), exist_ok=True)
    
    with open(integration_file, 'w') as f:
        f.write(integration_code)
    
    print("  ✅ Economic integration implemented")

if __name__ == "__main__":
    implement_economic_infrastructure()