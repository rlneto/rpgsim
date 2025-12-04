"""
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
