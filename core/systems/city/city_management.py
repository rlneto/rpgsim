"""
City Management System for Economic Infrastructure
FOCUS: Living cities with economy, NPCs, and services
"""

from typing import Dict, List, Optional, Any
import random
import json

# Global city state
_cities = {}
_city_events = {}
_city_populations = {}

class City:
    """City model for city management system"""
    
    def __init__(self, city_id: str, name: str, city_type: str = "town"):
        self.city_id = city_id
        self.name = name
        self.type = city_type
        self.population = 0
        self.economy = {}
        self.services = {}
        self.npcs = []
        self.locations = []

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
