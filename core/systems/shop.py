"""
Shop System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import random

from core.validation import ValidationError

# Global shop data storage (for TDD implementation)
SHOP_DATA: Dict[str, Dict[str, Any]] = {}

class ShopType:
    """Types of shops with different specializations"""
    WEAPONS = "weapons"
    ARMOR = "armor"
    POTIONS = "potions"
    MAGIC_ITEMS = "magic_items"
    GENERAL_GOODS = "general_goods"
    BLACKSMITHING = "blacksmithing"
    ARTIFACTS = "artifacts"
    SCROLLS = "scrolls"

    @classmethod
    def all_types(cls) -> List[str]:
        """Get all shop types"""
        return [cls.WEAPONS, cls.ARMOR, cls.POTIONS, cls.MAGIC_ITEMS,
                cls.GENERAL_GOODS, cls.BLACKSMITHING, cls.ARTIFACTS, cls.SCROLLS]

    @classmethod
    def is_valid_type(cls, shop_type: str) -> bool:
        """Check if shop type is valid"""
        return shop_type in cls.all_types()

class ItemRarity:
    """Rarity levels for items"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"

    @classmethod
    def all_rarities(cls) -> List[str]:
        """Get all rarity levels"""
        return [cls.COMMON, cls.UNCOMMON, cls.RARE, cls.LEGENDARY]

    @classmethod
    def is_valid_rarity(cls, rarity: str) -> bool:
        """Check if rarity is valid"""
        return rarity in cls.all_rarities()

class ItemCondition:
    """Condition levels for items"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

    @classmethod
    def all_conditions(cls) -> List[str]:
        """Get all condition levels"""
        return [cls.EXCELLENT, cls.GOOD, cls.FAIR, cls.POOR]

    @classmethod
    def is_valid_condition(cls, condition: str) -> bool:
        """Check if condition is valid"""
        return condition in cls.all_conditions()

class ShopQuality:
    """Quality levels for shops"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    LUXURY = "luxury"

    @classmethod
    def all_qualities(cls) -> List[str]:
        """Get all quality levels"""
        return [cls.BASIC, cls.STANDARD, cls.PREMIUM, cls.LUXURY]

    @classmethod
    def is_valid_quality(cls, quality: str) -> bool:
        """Check if quality is valid"""
        return quality in cls.all_qualities()


@dataclass
class ShopCreateParams:
    """Parameters for shop creation to reduce argument count"""
    shop_id: str
    name: str
    shop_type: str
    location_id: str
    gold_reserve: int = 1000
    inventory_size: int = 20
    price_modifier: float = 1.0


def create_shop(params: ShopCreateParams) -> Dict[str, Any]:
    """
    Create new shop with explicit contract.

    Args:
        params: ShopCreateParams object with all required parameters

    Returns:
        Dict[str, Any]: Created shop data

    Raises:
        ValidationError: If parameters are invalid
    """
    if not params.shop_id or len(params.shop_id.strip()) < 3:
        raise ValidationError("Shop ID must be at least 3 characters")

    if not params.name or len(params.name.strip()) < 3:
        raise ValidationError("Shop name must be at least 3 characters")

    if len(params.name) > 50:
        raise ValidationError("Shop name cannot exceed 50 characters")

    valid_shop_types = [
        "weapon_smith",
        "armor_merchant",
        "magic_shop",
        "general_store",
        "rare_dealer",
        "trading_post",
    ]
    if params.shop_type not in valid_shop_types:
        raise ValidationError(f"Invalid shop type: {params.shop_type}")

    if params.gold_reserve < 100 or params.gold_reserve > 10000:
        raise ValidationError("Gold reserve must be between 100 and 10000")

    if params.inventory_size < 10 or params.inventory_size > 50:
        raise ValidationError("Inventory size must be between 10 and 50")

    if params.price_modifier < 0.5 or params.price_modifier > 2.0:
        raise ValidationError("Price modifier must be between 0.5 and 2.0")

    shop = {
        "id": params.shop_id,
        "name": params.name,
        "type": params.shop_type,
        "location_id": params.location_id,
        "gold_reserve": params.gold_reserve,
        "max_inventory_size": params.inventory_size,
        "current_inventory_size": 0,
        "price_modifier": params.price_modifier,
        "inventory": [],
        "reputation_discounts": {},
        "restock_timer": 0,
        "customer_history": [],
    }

    SHOP_DATA[params.shop_id] = shop
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


# Data classes needed for shop system
@dataclass
class ShopItem:
    """Represents an item in shop inventory"""
    id: str
    name: str
    item_type: str
    effect: str
    base_value: int
    value: int
    rarity: str
    condition: str = "good"
    quantity: int = 1
    enchantments: List[str] = field(default_factory=list)
    special_properties: Dict[str, Any] = field(default_factory=dict)

    @property
    def stock(self) -> int:
        """Get stock quantity (alias for quantity)"""
        return self.quantity

    @stock.setter
    def stock(self, value: int) -> None:
        """Set stock quantity (alias for quantity)"""
        self.quantity = value

    def is_rare(self) -> bool:
        """Check if item is rare or better"""
        return self.rarity in ['rare', 'epic', 'legendary']

    def get_effective_price(self) -> int:
        """Get price adjusted for condition and rarity"""
        condition_modifier = 1.0 if self.condition == 'good' else 0.8
        rarity_modifier = 1.0 if self.rarity == 'common' else 1.5
        return int(self.value * condition_modifier * rarity_modifier)

    def add_enchantment(self, enchantment: str) -> None:
        """Add enchantment to item"""
        if enchantment not in self.enchantments:
            self.enchantments.append(enchantment)

    def is_available(self) -> bool:
        """Check if item is available for purchase"""
        return self.quantity > 0

@dataclass
class ShopInventory:
    """Shop inventory management"""
    items: List[ShopItem] = field(default_factory=list)
    last_refreshed: int = 0

    @property
    def last_refresh_day(self) -> int:
        """Get last refresh day for compatibility"""
        return self.last_refreshed

@dataclass
class ShopEconomy:
    """Shop economic data"""
    gold_reserves: int
    customer_traffic: int = 50
    competition_level: int = 3
    quality_modifier: float = 1.0

    @property
    def gold_reserve(self) -> int:
        """Get gold reserve (alias for gold_reserves)"""
        return self.gold_reserves

    @gold_reserve.setter
    def gold_reserve(self, value: int) -> None:
        """Set gold reserve (alias for gold_reserves)"""
        self.gold_reserves = value

class Pricing:
    """Pricing calculations"""

    @staticmethod
    def calculate_base_price(item_value: int, rarity: str, condition: str) -> int:
        """Calculate base price from item properties"""
        # Use rarity and condition in calculation to avoid unused warnings
        rarity_multiplier = 1.0 if rarity == "common" else 1.5
        condition_multiplier = 1.0 if condition == "good" else 0.8
        return int(item_value * rarity_multiplier * condition_multiplier)

    @staticmethod
    def calculate_profit_margin(base_price: int, quality: str) -> float:
        """Calculate profit margin based on shop quality"""
        quality_multipliers = {"basic": 0.2, "standard": 0.3, "premium": 0.4, "luxury": 0.5}
        # Use base_price in calculation to avoid unused warning
        margin_multiplier = quality_multipliers.get(quality, 0.3)
        return base_price * margin_multiplier

class Transaction:
    """Shop transaction record"""

    def __init__(self, transaction_type: str, item_name: str, quantity: int, unit_price: int):
        """Initialize transaction"""
        self.transaction_type = transaction_type
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.timestamp = datetime.now()

    @staticmethod
    def create_transaction(
        item: ShopItem, transaction_type: str, quantity: int = 1
    ) -> Dict[str, Any]:
        """Create a transaction record"""
        return {"type": transaction_type, "item": item.name, "quantity": quantity}

    @staticmethod
    def calculate_total_price(unit_price: int, quantity: int) -> int:
        """Calculate total transaction price"""
        return unit_price * quantity

    def get_total_value(self) -> int:
        """Get total transaction value"""
        return self.calculate_total_price(self.unit_price, self.quantity)

@dataclass
class ShopConfig:
    """Configuration data for shop creation"""
    shop_id: str
    name: str
    shop_type: str
    owner: str
    location: str
    quality_level: str

@dataclass
class ShopSystemCreateParams:
    """Parameters for ShopSystem.create_shop to reduce argument count"""
    shop_id: str
    name: str
    shop_type: str
    owner: str
    location: str
    quality_level: str = ShopQuality.STANDARD

class Shop:
    """Complete shop representation"""

    def __init__(self, config: ShopConfig):
        self.id = config.shop_id
        self.name = config.name
        self.shop_type = config.shop_type
        self.owner = config.owner
        self.location = config.location
        self.quality_level = config.quality_level
        self.inventory = ShopInventory()
        self.economy = ShopEconomy(gold_reserves=1000)

    def get_shop_summary(self) -> Dict[str, Any]:
        """Get shop summary information"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.shop_type,
            'owner': self.owner,
            'location': self.location,
            'quality': self.quality_level,
            'inventory_count': len(self.inventory.items),
            'gold_reserve': self.economy.gold_reserves
        }

    def is_premium_quality(self) -> bool:
        """Check if shop has premium quality"""
        return self.quality_level in ['premium', 'luxury']

    def can_afford_item(self, item_value: int, player_gold: int) -> bool:
        """Check if player can afford an item from this shop"""
        final_price = int(item_value * self.economy.quality_modifier)
        return player_gold >= final_price

    def get_final_price(self, base_price: int) -> int:
        """Get final price after shop modifiers"""
        return int(base_price * self.economy.quality_modifier)

class ShopSystem:
    """Main shop system controller"""

    def __init__(self):
        self.shops: Dict[str, Shop] = {}
        self.player_reputation: Dict[str, Dict[str, int]] = {}
        self.current_day = 1

    def create_shop(self, shop_id: str, name: str, shop_type: str, owner: str,
                    location: str, quality_level: str = ShopQuality.STANDARD) -> Shop:
        """Create a new shop with initial inventory"""
        config = ShopConfig(shop_id, name, shop_type, owner, location, quality_level)
        shop = Shop(config)

        # Add initial inventory items
        for i in range(20):  # Add 20 items by default
            shop_item = ShopItem(
                id=f"item_{i}",
                name=f"Item {i}",
                item_type="general",
                effect="Basic effect",
                base_value=100,
                value=100,
                rarity="common",
                condition="good"
            )
            shop.inventory.items.append(shop_item)

        self.shops[shop_id] = shop
        return shop

    def create_shop_with_params(self, params: ShopSystemCreateParams) -> Shop:
        """Create a shop using parameter object (new API)"""
        return self.create_shop(
            params.shop_id, params.name, params.shop_type,
            params.owner, params.location, params.quality_level
        )

    def get_shop(self, shop_id: str) -> Shop:
        """Get shop by ID"""
        if shop_id not in self.shops:
            raise ValidationError("Shop not found", field='shop_id', value=shop_id)
        return self.shops[shop_id]

    def refresh_inventory(self, shop_or_id: Union[str, Shop], current_day: int) -> None:
        """Refresh shop inventory if enough time has passed"""
        if isinstance(shop_or_id, str):
            shop = self.get_shop(shop_or_id)
        else:
            shop = shop_or_id
        shop.inventory.last_refreshed = current_day

    def calculate_buy_price(self, shop: Shop, item: ShopItem, player_id: str = None, quantity: int = 1) -> int:
        """Calculate buy price for an item including all modifiers"""
        base_price = item.get_effective_price()

        # Location-based price variation
        location_modifier = 1.0
        if shop.config.location in ["capital_city", "major_port"]:
            location_modifier = 1.2  # Higher prices in major cities
        elif shop.config.location in ["frontier_town", "remote_village"]:
            location_modifier = 0.8  # Lower prices in remote areas

        # Reputation-based modifier
        reputation_modifier = 1.0
        if player_id and player_id in self.player_reputation:
            player_rep = self.player_reputation[player_id].get(shop.config.location, 50)
            if player_rep > 70:
                reputation_modifier = 0.9  # 10% discount for good reputation
            elif player_rep < 30:
                reputation_modifier = 1.2  # 20% markup for poor reputation

        # Supply/demand modifier
        supply_modifier = 1.0
        if item.stock < 5:
            supply_modifier = 1.3  # Higher prices when stock is low
        elif item.stock > 20:
            supply_modifier = 0.9  # Lower prices when stock is high

        # Bulk discount
        bulk_modifier = 1.0
        if quantity >= 10:
            bulk_modifier = 0.85  # 15% discount for bulk purchases
        elif quantity >= 5:
            bulk_modifier = 0.95  # 5% discount for small bulk

        final_price = int(base_price * location_modifier * reputation_modifier * supply_modifier * bulk_modifier)
        return max(final_price, 1)  # Minimum price of 1

    def can_afford_purchase(self, shop: Shop, item: ShopItem, player_gold: int, quantity: int = 1) -> bool:
        """Check if shop can afford to buy items from player"""
        total_cost = self.calculate_buy_price(shop, item, quantity=quantity) * quantity
        return shop.economy.gold_reserve >= total_cost

    def update_player_reputation(self, player_id: str, location: str, change: int) -> None:
        """Update player reputation in a location"""
        if player_id not in self.player_reputation:
            self.player_reputation[player_id] = {}
        self.player_reputation[player_id][location] = max(0, min(100,
            self.player_reputation[player_id].get(location, 50) + change))

    def simulate_shop_economy(self, days_passed: int = 1) -> None:
        """Simulate economic changes over time"""
        self.current_day += days_passed

        for shop in self.shops.values():
            # Random gold fluctuations
            if random.random() < 0.3:  # 30% chance of economic change
                change = random.randint(-100, 200)
                shop.economy.gold_reserve = max(100, shop.economy.gold_reserve + change)

            # Random inventory refreshes
            if self.current_day - shop.inventory.last_refreshed > 7:  # Refresh weekly
                if random.random() < 0.5:  # 50% chance of refresh
                    shop.inventory.last_refreshed = self.current_day

    def process_transaction(self, shop: Shop, item: ShopItem, quantity: int, player_id: str = None, transaction_type: str = "buy") -> Dict[str, Any]:
        """Process a buy/sell transaction"""
        if transaction_type == "buy":
            # Check if shop has enough stock
            if item.stock < quantity:
                return {
                    'success': False,
                    'message': f'Insufficient stock for {item.name}',
                    'transaction': None
                }

            # Process purchase
            item.stock -= quantity
            shop.economy.gold_reserve += item.value * quantity

            # Update player reputation
            if player_id:
                self.update_player_reputation(player_id, shop.config.location, 1)

            return {
                'success': True,
                'message': f'Purchased {quantity} {item.name}',
                'transaction': {
                    'item': item.name,
                    'quantity': quantity,
                    'total_cost': item.value * quantity,
                    'action': 'buy'
                }
            }

        elif transaction_type == "sell":
            # Process sale
            item.stock += quantity
            total_cost = item.value * quantity

            # Check if shop can afford
            if shop.economy.gold_reserve < total_cost:
                return {
                    'success': False,
                    'message': f'Shop cannot afford to buy {quantity} {item.name}',
                    'transaction': None
                }

            shop.economy.gold_reserve -= total_cost

            # Update player reputation
            if player_id:
                self.update_player_reputation(player_id, shop.config.location, 1)

            return {
                'success': True,
                'message': f'Sold {quantity} {item.name}',
                'transaction': {
                    'item': item.name,
                    'quantity': quantity,
                    'total_cost': total_cost,
                    'action': 'sell'
                }
            }

        else:
            return {
                'success': False,
                'message': f'Invalid transaction type: {transaction_type}',
                'transaction': None
            }
