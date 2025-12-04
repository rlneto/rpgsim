"""
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
