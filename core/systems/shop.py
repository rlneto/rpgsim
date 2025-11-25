"""
Shop System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Tuple
import random

from core.models import Location, LocationType
from core.validation import ValidationError

# Global shop data storage (for TDD implementation)
SHOP_DATA: Dict[str, Dict[str, Any]] = {}


def create_shop(
    shop_id: str,
    name: str,
    shop_type: str,
    location_id: str,
    gold_reserve: int = 1000,
    inventory_size: int = 20,
    price_modifier: float = 1.0,
) -> Dict[str, Any]:
    """
    Create new shop with explicit contract.

    Args:
        shop_id: Unique shop identifier
        name: Shop name (3-50 chars)
        shop_type: Type of shop (weapon, armor, magic, general)
        location_id: ID of location where shop is located
        gold_reserve: Initial gold reserve (100-10000)
        inventory_size: Maximum inventory size (10-50)
        price_modifier: Price modifier (0.5-2.0)

    Returns:
        Dict[str, Any]: Created shop data

    Raises:
        ValidationError: If parameters are invalid
    """
    if not shop_id or len(shop_id.strip()) < 3:
        raise ValidationError("Shop ID must be at least 3 characters")

    if not name or len(name.strip()) < 3:
        raise ValidationError("Shop name must be at least 3 characters")

    if len(name) > 50:
        raise ValidationError("Shop name cannot exceed 50 characters")

    valid_shop_types = [
        "weapon_smith",
        "armor_merchant",
        "magic_shop",
        "general_store",
        "rare_dealer",
        "trading_post",
    ]
    if shop_type not in valid_shop_types:
        raise ValidationError(f"Invalid shop type: {shop_type}")

    if gold_reserve < 100 or gold_reserve > 10000:
        raise ValidationError("Gold reserve must be between 100 and 10000")

    if inventory_size < 10 or inventory_size > 50:
        raise ValidationError("Inventory size must be between 10 and 50")

    if price_modifier < 0.5 or price_modifier > 2.0:
        raise ValidationError("Price modifier must be between 0.5 and 2.0")

    shop = {
        "id": shop_id,
        "name": name,
        "type": shop_type,
        "location_id": location_id,
        "gold_reserve": gold_reserve,
        "max_inventory_size": inventory_size,
        "current_inventory_size": 0,
        "price_modifier": price_modifier,
        "inventory": [],
        "reputation_discounts": {},
        "restock_timer": 0,
        "customer_history": [],
    }

    SHOP_DATA[shop_id] = shop
    return shop


def get_shop_inventory(shop_id: str) -> List[Dict[str, Any]]:
    """
    Get shop inventory.

    Args:
        shop_id: Shop identifier

    Returns:
        List[Dict[str, Any]]: List of items in inventory

    Raises:
        ValidationError: If parameters are invalid
    """
    if not shop_id or shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    return SHOP_DATA[shop_id]["inventory"]


def buy_item_from_shop(
    shop_id: str, item_index: int, character_gold: int, character_reputation: int = 50
) -> Dict[str, Any]:
    """
    Buy item from shop.

    Args:
        shop_id: Shop identifier
        item_index: Index of item in inventory
        character_gold: Character's available gold
        character_reputation: Character's reputation (0-100)

    Returns:
        Dict[str, Any]: Transaction result

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    shop = SHOP_DATA[shop_id]

    if item_index < 0 or item_index >= len(shop["inventory"]):
        raise ValidationError("Invalid item index")

    item = shop["inventory"][item_index]
    base_price = item.get("price", 100)

    # Apply reputation discount
    reputation_discount = shop["reputation_discounts"].get("default", 0.0)
    if character_reputation >= 80:
        reputation_discount = 0.2  # 20% discount for high reputation
    elif character_reputation >= 60:
        reputation_discount = 0.1  # 10% discount for good reputation
    elif character_reputation >= 40:
        reputation_discount = 0.05  # 5% discount for neutral reputation

    # Calculate final price
    final_price = int(base_price * shop["price_modifier"] * (1.0 - reputation_discount))

    # Check if character can afford
    if character_gold < final_price:
        return {
            "success": False,
            "reason": "Insufficient gold",
            "required_gold": final_price,
            "available_gold": character_gold,
            "item": None,
        }

    # Check if shop has enough gold (for selling)
    if shop["gold_reserve"] < final_price:
        return {
            "success": False,
            "reason": "Shop cannot afford to buy this item",
            "item": None,
        }

    # Process transaction
    shop["gold_reserve"] -= final_price
    shop["inventory"].pop(item_index)
    shop["current_inventory_size"] = len(shop["inventory"])

    # Add to customer history
    shop["customer_history"].append(
        {
            "action": "buy",
            "item": item["name"],
            "price": final_price,
            "reputation": character_reputation,
        }
    )

    return {
        "success": True,
        "item": item,
        "price_paid": final_price,
        "gold_spent": final_price,
        "remaining_gold": character_gold - final_price,
        "shop_gold_remaining": shop["gold_reserve"],
    }


def sell_item_to_shop(
    shop_id: str, item: Dict[str, Any], character_reputation: int = 50
) -> Dict[str, Any]:
    """
    Sell item to shop.

    Args:
        shop_id: Shop identifier
        item: Item to sell
        character_reputation: Character's reputation (0-100)

    Returns:
        Dict[str, Any]: Transaction result

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    if not isinstance(item, dict):
        raise ValidationError("Item must be a dictionary")

    shop = SHOP_DATA[shop_id]

    # Check if shop can buy this item type
    shop_type = shop["type"]
    item_type = item.get("type", "general")

    type_compatibility = {
        "weapon_smith": ["weapon"],
        "armor_merchant": ["armor", "shield"],
        "magic_shop": ["magic", "scroll", "potion"],
        "general_store": ["general"],
        "rare_dealer": ["rare", "epic", "legendary"],
        "trading_post": ["general", "trade_goods"],
    }

    if item_type not in type_compatibility.get(shop_type, ["general"]):
        return {
            "success": False,
            "reason": f"This shop doesn't buy {item_type} items",
            "gold_received": 0,
        }

    # Calculate offer price
    base_value = item.get("value", 50)
    rarity_multiplier = {
        "common": 1.0,
        "uncommon": 1.5,
        "rare": 2.5,
        "epic": 5.0,
        "legendary": 10.0,
    }

    item_rarity = item.get("rarity", "common")
    rarity_mult = rarity_multiplier.get(item_rarity, 1.0)

    # Apply reputation modifier
    reputation_modifier = 1.0
    if character_reputation >= 80:
        reputation_modifier = 1.2  # 20% bonus for high reputation
    elif character_reputation >= 60:
        reputation_modifier = 1.1  # 10% bonus for good reputation

    # Calculate final offer
    market_value = int(base_value * rarity_mult)
    final_offer = int(market_value * shop["price_modifier"] * reputation_modifier)

    # Check if shop can afford
    if shop["gold_reserve"] < final_offer:
        return {
            "success": False,
            "reason": "Shop doesn't have enough gold",
            "gold_received": 0,
        }

    # Process transaction
    shop["gold_reserve"] -= final_offer

    # Add to inventory if space available
    if shop["current_inventory_size"] < shop["max_inventory_size"]:
        shop["inventory"].append(item)
        shop["current_inventory_size"] += 1

    # Add to customer history
    shop["customer_history"].append(
        {
            "action": "sell",
            "item": item["name"],
            "price": final_offer,
            "reputation": character_reputation,
        }
    )

    return {
        "success": True,
        "item_sold": item,
        "gold_received": final_offer,
        "market_value": market_value,
        "shop_gold_remaining": shop["gold_reserve"],
    }


def restock_shop(
    shop_id: str, items: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Restock shop inventory.

    Args:
        shop_id: Shop identifier
        items: List of items to add (None for auto-restock)

    Returns:
        Dict[str, Any]: Restock result

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    shop = SHOP_DATA[shop_id]

    if items is None:
        # Auto-restock based on shop type
        items = generate_shop_inventory(shop["type"], shop["max_inventory_size"])

    # Add items to inventory
    added_count = 0
    for item in items:
        if shop["current_inventory_size"] < shop["max_inventory_size"]:
            shop["inventory"].append(item)
            shop["current_inventory_size"] += 1
            added_count += 1

    shop["restock_timer"] = 0  # Reset restock timer

    return {
        "success": True,
        "items_added": added_count,
        "current_inventory_size": shop["current_inventory_size"],
        "max_inventory_size": shop["max_inventory_size"],
    }


def calculate_shop_prices(
    shop_id: str, base_prices: List[int], character_reputation: int = 50
) -> List[int]:
    """
    Calculate shop prices with modifiers.

    Args:
        shop_id: Shop identifier
        base_prices: List of base item prices
        character_reputation: Character's reputation (0-100)

    Returns:
        List[int]: Modified prices

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    shop = SHOP_DATA[shop_id]

    # Calculate reputation discount
    reputation_discount = 0.0
    if character_reputation >= 80:
        reputation_discount = 0.2
    elif character_reputation >= 60:
        reputation_discount = 0.1
    elif character_reputation >= 40:
        reputation_discount = 0.05

    # Apply all modifiers
    modified_prices = []
    for base_price in base_prices:
        final_price = int(
            base_price * shop["price_modifier"] * (1.0 - reputation_discount)
        )
        modified_prices.append(final_price)

    return modified_prices


def update_shop_economy(
    shop_id: str, economic_change: int, location_wealth_change: int = 0
) -> Dict[str, Any]:
    """
    Update shop economy based on transactions.

    Args:
        shop_id: Shop identifier
        economic_change: Economic change (-1000 to +1000)
        location_wealth_change: Location wealth change (-10 to +10)

    Returns:
        Dict[str, Any]: Updated economic information

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    if economic_change < -1000 or economic_change > 1000:
        raise ValidationError("Economic change must be between -1000 and 1000")

    shop = SHOP_DATA[shop_id]

    # Update gold reserve
    shop["gold_reserve"] = max(100, shop["gold_reserve"] + economic_change)

    # Update price modifier based on location wealth
    if location_wealth_change != 0:
        wealth_factor = 1.0 + (location_wealth_change * 0.05)
        shop["price_modifier"] = max(
            0.5, min(2.0, shop["price_modifier"] * wealth_factor)
        )

    # Update restock timer
    shop["restock_timer"] = max(0, shop["restock_timer"] - 1)

    return {
        "old_gold_reserve": shop["gold_reserve"] - economic_change,
        "new_gold_reserve": shop["gold_reserve"],
        "economic_change": economic_change,
        "price_modifier": shop["price_modifier"],
        "restock_timer": shop["restock_timer"],
    }


def generate_shop_inventory(
    shop_type: str, inventory_size: int
) -> List[Dict[str, Any]]:
    """
    Generate inventory for shop based on type.

    Args:
        shop_type: Type of shop
        inventory_size: Maximum inventory size

    Returns:
        List[Dict[str, Any]]: Generated inventory
    """
    inventory = []

    # Define item pools for different shop types
    item_pools = {
        "weapon_smith": [
            {
                "name": "Iron Sword",
                "type": "weapon",
                "rarity": "common",
                "price": 100,
                "value": 80,
            },
            {
                "name": "Steel Axe",
                "type": "weapon",
                "rarity": "common",
                "price": 150,
                "value": 120,
            },
            {
                "name": "Silver Dagger",
                "type": "weapon",
                "rarity": "uncommon",
                "price": 300,
                "value": 250,
            },
        ],
        "armor_merchant": [
            {
                "name": "Leather Armor",
                "type": "armor",
                "rarity": "common",
                "price": 120,
                "value": 100,
            },
            {
                "name": "Chain Mail",
                "type": "armor",
                "rarity": "common",
                "price": 200,
                "value": 180,
            },
            {
                "name": "Iron Shield",
                "type": "shield",
                "rarity": "common",
                "price": 80,
                "value": 70,
            },
        ],
        "magic_shop": [
            {
                "name": "Health Potion",
                "type": "potion",
                "rarity": "common",
                "price": 50,
                "value": 40,
            },
            {
                "name": "Mana Potion",
                "type": "potion",
                "rarity": "common",
                "price": 60,
                "value": 50,
            },
            {
                "name": "Fire Scroll",
                "type": "scroll",
                "rarity": "uncommon",
                "price": 200,
                "value": 180,
            },
        ],
        "general_store": [
            {
                "name": "Torch",
                "type": "general",
                "rarity": "common",
                "price": 5,
                "value": 4,
            },
            {
                "name": "Rope",
                "type": "general",
                "rarity": "common",
                "price": 10,
                "value": 8,
            },
            {
                "name": "Rations",
                "type": "general",
                "rarity": "common",
                "price": 15,
                "value": 12,
            },
        ],
    }

    # Get appropriate item pool
    item_pool = item_pools.get(shop_type, item_pools["general_store"])

    # Generate inventory
    for i in range(min(inventory_size, len(item_pool))):
        item = item_pool[i % len(item_pool)].copy()
        item["id"] = f"{shop_type}_{i:03d}"
        inventory.append(item)

    return inventory


def get_shop_data(shop_id: str) -> Dict[str, Any]:
    """
    Get shop data.

    Args:
        shop_id: Shop identifier

    Returns:
        Dict[str, Any]: Shop data

    Raises:
        ValidationError: If parameters are invalid
    """
    if shop_id not in SHOP_DATA:
        raise ValidationError("Invalid shop ID")

    return SHOP_DATA[shop_id]
