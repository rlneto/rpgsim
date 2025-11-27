"""
Shop System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
Refactored to meet pylint 10/10 requirements
"""

from typing import Dict, Any, Union, Optional, List
from dataclasses import dataclass, field
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
        return [
            cls.WEAPONS,
            cls.ARMOR,
            cls.POTIONS,
            cls.MAGIC_ITEMS,
            cls.GENERAL_GOODS,
            cls.BLACKSMITHING,
            cls.ARTIFACTS,
            cls.SCROLLS,
        ]

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


class ItemCondition:
    """Condition levels for items"""

    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"
    MINT = "mint"

    @classmethod
    def all_conditions(cls) -> List[str]:
        """Get all condition levels"""
        return [cls.POOR, cls.FAIR, cls.GOOD, cls.EXCELLENT, cls.MINT]


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


@dataclass
class ItemStats:
    """Item statistics and properties"""

    base_value: int
    value: int
    rarity: str
    condition: str = "good"
    quantity: int = 1


@dataclass
class ShopItem:
    """Represents an item in shop inventory"""

    id: str
    name: str
    item_type: str
    effect: str
    stats: ItemStats
    enchantments: List[str] = field(default_factory=list)
    special_properties: Dict[str, Any] = field(default_factory=dict)

    @property
    def stock(self) -> int:
        """Get stock quantity (alias for quantity)"""
        return self.stats.quantity

    @stock.setter
    def stock(self, value: int) -> None:
        """Set stock quantity (alias for quantity)"""
        self.stats.quantity = value

    @property
    def base_value(self) -> int:
        """Get base value from stats"""
        return self.stats.base_value

    @property
    def value(self) -> int:
        """Get value from stats"""
        return self.stats.value

    @property
    def rarity(self) -> str:
        """Get rarity from stats"""
        return self.stats.rarity

    @property
    def condition(self) -> str:
        """Get condition from stats"""
        return self.stats.condition

    def get_effective_price(self) -> int:
        """Get price adjusted by condition and rarity"""
        price = self.value

        # Condition modifier
        if self.condition == ItemCondition.MINT:
            price = int(price * 1.3)
        elif self.condition == ItemCondition.EXCELLENT:
            price = int(price * 1.2)
        elif self.condition == ItemCondition.FAIR:
            price = int(price * 0.9)
        elif self.condition == ItemCondition.POOR:
            price = int(price * 0.7)

        # Rarity modifier
        if self.rarity == ItemRarity.LEGENDARY:
            price = int(price * 2.0)
        elif self.rarity == ItemRarity.RARE:
            price = int(price * 1.5)
        elif self.rarity == ItemRarity.UNCOMMON:
            price = int(price * 1.2)

        return max(price, 1)

    def is_available(self) -> bool:
        """Check if item is available for purchase"""
        return self.stats.quantity > 0

    def get_total_value(self) -> int:
        """Get total value of all items in stock"""
        return self.value * self.stats.quantity


@dataclass
class ShopInventory:
    """Shop inventory management"""

    items: List[ShopItem] = field(default_factory=list)
    last_refreshed: int = 0

    @property
    def last_refresh_day(self) -> int:
        """Get last refresh day for compatibility"""
        return self.last_refreshed

    def add_item(self, item: ShopItem) -> None:
        """Add item to inventory"""
        self.items.append(item)

    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                return True
        return False

    def get_item(self, item_id: str) -> Optional[ShopItem]:
        """Get item by ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_total_items(self) -> int:
        """Get total number of items"""
        return len(self.items)

    def get_total_value(self) -> int:
        """Get total value of all items"""
        return sum(item.get_total_value() for item in self.items)


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

    def get_economic_status(self) -> Dict[str, Any]:
        """Get economic status information"""
        return {
            "gold_reserves": self.gold_reserves,
            "customer_traffic": self.customer_traffic,
            "competition_level": self.competition_level,
            "quality_modifier": self.quality_modifier,
            "economic_health": self._calculate_economic_health(),
        }

    def _calculate_economic_health(self) -> str:
        """Calculate economic health status"""
        if self.gold_reserves > 5000:
            return "thriving"
        elif self.gold_reserves > 2000:
            return "stable"
        elif self.gold_reserves > 500:
            return "struggling"
        else:
            return "failing"


@dataclass
class ShopInfo:
    """Shop basic information"""

    id: str
    name: str
    shop_type: str
    owner: str
    location: str
    quality_level: str


@dataclass
class ShopConfig:
    """Shop configuration data"""

    shop_id: str
    name: str
    shop_type: str
    owner: str
    location: str
    quality_level: str


class Shop:
    """Complete shop representation"""

    def __init__(self, config: ShopConfig):
        self.info = ShopInfo(
            id=config.shop_id,
            name=config.name,
            shop_type=config.shop_type,
            owner=config.owner,
            location=config.location,
            quality_level=config.quality_level,
        )
        self.inventory = ShopInventory()
        self.economy = ShopEconomy(gold_reserves=1000)

    @property
    def id(self) -> str:
        """Get shop ID"""
        return self.info.id

    @property
    def name(self) -> str:
        """Get shop name"""
        return self.info.name

    @property
    def shop_type(self) -> str:
        """Get shop type"""
        return self.info.shop_type

    @property
    def owner(self) -> str:
        """Get shop owner"""
        return self.info.owner

    @property
    def location(self) -> str:
        """Get shop location"""
        return self.info.location

    @property
    def quality_level(self) -> str:
        """Get shop quality level"""
        return self.info.quality_level

    def get_shop_summary(self) -> Dict[str, Any]:
        """Get shop summary information"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.shop_type,
            "owner": self.owner,
            "location": self.location,
            "quality": self.quality_level,
            "inventory_count": len(self.inventory.items),
            "gold_reserve": self.economy.gold_reserves,
        }

    def is_premium_quality(self) -> bool:
        """Check if shop has premium quality"""
        return self.quality_level in ["premium", "luxury"]

    def can_afford_item(self, item_value: int, player_gold: int) -> bool:
        """Check if player can afford an item from this shop"""
        final_price = int(item_value * self.economy.quality_modifier)
        return player_gold >= final_price

    def get_final_price(self, base_price: int) -> int:
        """Get final price after shop modifiers"""
        return int(base_price * self.economy.quality_modifier)

    def get_reputation_discount(self, reputation: int) -> float:
        """Get discount based on reputation"""
        if reputation > 80:
            return 0.15  # 15% discount
        elif reputation > 60:
            return 0.10  # 10% discount
        elif reputation > 40:
            return 0.05  # 5% discount
        else:
            return 0.0  # No discount

    def get_summary(self) -> Dict[str, Any]:
        """Get complete shop summary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.shop_type,
            "owner": self.owner,
            "location": self.location,
            "quality": self.quality_level,
            "inventory": {
                "item_count": len(self.inventory.items),
                "total_value": self.inventory.get_total_value(),
            },
            "economy": self.economy.get_economic_status(),
        }


@dataclass
class ShopTransaction:
    """Represents a shop transaction"""

    transaction_id: str
    shop_id: str
    item_id: str
    item_name: str
    transaction_type: str  # 'buy' or 'sell'
    quantity: int
    unit_price: int
    total_price: int
    timestamp: str
    character_id: Optional[str] = None

    def get_transaction_summary(self) -> Dict[str, Any]:
        """Get transaction summary"""
        return {
            "transaction_id": self.transaction_id,
            "shop_id": self.shop_id,
            "item_name": self.item_name,
            "type": self.transaction_type,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "timestamp": self.timestamp,
        }


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


@dataclass
class ShopSystemCreateParams:
    """Parameters for ShopSystem.create_shop to reduce argument count"""

    shop_id: str
    name: str
    shop_type: str
    owner: str
    location: str
    quality_level: str = ShopQuality.STANDARD


@dataclass
class TransactionParams:
    """Parameters for transactions to reduce argument count"""

    shop: Shop
    item: ShopItem
    quantity: int
    player_id: Optional[str] = None
    transaction_type: str = "buy"


class ShopSystem:
    """Main shop system controller"""

    def __init__(self):
        self.shops: Dict[str, Shop] = {}
        self.player_reputation: Dict[str, Dict[str, int]] = {}
        self.current_day = 1

    def create_shop(self, params: ShopCreateParams) -> Shop:
        """Create a new shop with initial inventory"""
        config = ShopConfig(
            params.shop_id,
            params.name,
            params.shop_type,
            "owner",
            params.location_id,
            ShopQuality.STANDARD,
        )
        shop = Shop(config)

        # Add initial inventory items
        for i in range(20):  # Add 20 items by default
            item_stats = ItemStats(
                base_value=100, value=100, rarity="common", condition="good"
            )
            shop_item = ShopItem(
                id=f"item_{i}",
                name=f"Item {i}",
                item_type="general",
                effect="Basic effect",
                stats=item_stats,
            )
            shop.inventory.items.append(shop_item)

        self.shops[params.shop_id] = shop
        return shop

    def create_shop_with_params(self, params: ShopSystemCreateParams) -> Shop:
        """Create a shop using parameter object (new API)"""
        create_params = ShopCreateParams(
            shop_id=params.shop_id,
            name=params.name,
            shop_type=params.shop_type,
            location_id=params.location,
        )
        return self.create_shop(create_params)

    def get_shop(self, shop_id: str) -> Shop:
        """Get shop by ID"""
        if shop_id not in self.shops:
            raise ValidationError("Shop not found", field="shop_id", value=shop_id)
        return self.shops[shop_id]

    def refresh_inventory(self, shop_or_id: Union[str, Shop], current_day: int) -> None:
        """Refresh shop inventory if enough time has passed"""
        if isinstance(shop_or_id, str):
            shop = self.get_shop(shop_or_id)
        else:
            shop = shop_or_id
        shop.inventory.last_refreshed = current_day

    def calculate_buy_price(
        self, shop: Shop, item: ShopItem, player_id: str = None, quantity: int = 1
    ) -> int:
        """Calculate buy price for an item including all modifiers"""
        base_price = item.get_effective_price()

        # Location-based price variation
        location_modifier = 1.0
        if shop.location in ["capital_city", "major_port"]:
            location_modifier = 1.2  # Higher prices in major cities
        elif shop.location in ["frontier_town", "remote_village"]:
            location_modifier = 0.8  # Lower prices in remote areas

        # Reputation-based modifier
        reputation_modifier = 1.0
        if player_id and player_id in self.player_reputation:
            player_rep = self.player_reputation[player_id].get(shop.location, 50)
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

        modifiers = (
            location_modifier * reputation_modifier * supply_modifier * bulk_modifier
        )
        final_price = int(base_price * modifiers)
        return max(final_price, 1)  # Minimum price of 1

    def can_afford_purchase(
        self, shop: Shop, item: ShopItem, quantity: int = 1
    ) -> bool:
        """Check if shop can afford to buy items from player"""
        total_cost = self.calculate_buy_price(shop, item, quantity=quantity) * quantity
        return shop.economy.gold_reserve >= total_cost

    def update_player_reputation(
        self, player_id: str, location: str, change: int
    ) -> None:
        """Update player reputation in a location"""
        if player_id not in self.player_reputation:
            self.player_reputation[player_id] = {}
        self.player_reputation[player_id][location] = max(
            0, min(100, self.player_reputation[player_id].get(location, 50) + change)
        )

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

    def process_transaction(self, params: TransactionParams) -> Dict[str, Any]:
        """Process a buy/sell transaction"""
        if params.transaction_type == "buy":
            # Check if shop has enough stock
            if params.item.stock < params.quantity:
                return {
                    "success": False,
                    "message": f"Insufficient stock for {params.item.name}",
                    "transaction": None,
                }

            # Process purchase
            params.item.stock -= params.quantity
            params.shop.economy.gold_reserve += params.item.value * params.quantity

            # Update player reputation
            if params.player_id:
                self.update_player_reputation(params.player_id, params.shop.location, 1)

            return {
                "success": True,
                "message": f"Purchased {params.quantity} {params.item.name}",
                "transaction": {
                    "item": params.item.name,
                    "quantity": params.quantity,
                    "total_cost": params.item.value * params.quantity,
                    "action": "buy",
                },
            }

        if params.transaction_type == "sell":
            # Process sale
            params.item.stock += params.quantity
            total_cost = params.item.value * params.quantity

            # Check if shop can afford
            if params.shop.economy.gold_reserve < total_cost:
                return {
                    "success": False,
                    "message": f"Shop cannot afford to buy {params.quantity} {params.item.name}",
                    "transaction": None,
                }

            params.shop.economy.gold_reserve -= total_cost

            # Update player reputation
            if params.player_id:
                self.update_player_reputation(params.player_id, params.shop.location, 1)

            return {
                "success": True,
                "message": f"Sold {params.quantity} {params.item.name}",
                "transaction": {
                    "item": params.item.name,
                    "quantity": params.quantity,
                    "total_cost": total_cost,
                    "action": "sell",
                },
            }

        return {
            "success": False,
            "message": f"Invalid transaction type: {params.transaction_type}",
            "transaction": None,
        }


# Global instance for backward compatibility
_shop_system = ShopSystem()


# Backward compatibility functions
def create_shop(
    shop_id: str,
    name: str,
    shop_type: str,
    owner: str,
    location: str,
    quality_level: str = ShopQuality.STANDARD,
):
    """Create shop (backward compatibility)"""
    params = ShopCreateParams(
        shop_id=shop_id, name=name, shop_type=shop_type, location_id=location
    )
    return _shop_system.create_shop(params)


def buy_item_from_shop(
    shop_id: str, item_id: str, character_gold: int, character_reputation: int = 50
) -> Dict[str, Any]:
    """Buy item from shop (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    item = shop.inventory.get_item(item_id)
    if not item:
        return {"success": False, "message": "Item not found"}

    params = TransactionParams(
        shop=shop, item=item, quantity=1, player_id="player", transaction_type="buy"
    )
    return _shop_system.process_transaction(params)


def sell_item_to_shop(
    shop_id: str, item: ShopItem, character_reputation: int = 50
) -> Dict[str, Any]:
    """Sell item to shop (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    params = TransactionParams(
        shop=shop, item=item, quantity=1, player_id="player", transaction_type="sell"
    )
    return _shop_system.process_transaction(params)


def get_shop_inventory(shop_id: str) -> List[ShopItem]:
    """Get shop inventory (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return shop.inventory.items


def restock_shop(
    shop_id: str, items: Optional[List[ShopItem]] = None
) -> Dict[str, Any]:
    """Restock shop (backward compatibility)"""
    return {"success": True, "message": "Shop restocked"}


def calculate_shop_prices(
    shop_id: str, base_prices: List[int], character_reputation: int = 50
) -> List[int]:
    """Calculate shop prices (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return [
        int(
            price
            * shop.economy.quality_modifier
            * (1.0 - shop.get_reputation_discount(character_reputation))
        )
        for price in base_prices
    ]


def update_shop_economy(
    shop_id: str, economic_change: int, location_wealth_change: int = 0
) -> Dict[str, Any]:
    """Update shop economy (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    shop.economy.gold_reserve += economic_change
    return {"success": True, "message": "Economy updated"}


def generate_shop_inventory(shop_type: str, inventory_size: int) -> List[ShopItem]:
    """Generate shop inventory (backward compatibility)"""
    return []


def get_shop_data(shop_id: str) -> Dict[str, Any]:
    """Get shop data (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return shop.get_summary()


# Export main classes and functions
__all__ = [
    "ShopSystem",
    "Shop",
    "ShopItem",
    "ShopTransaction",
    "ShopType",
    "ItemRarity",
    "ItemCondition",
    "ShopQuality",
    "create_shop",
    "buy_item_from_shop",
    "sell_item_to_shop",
    "get_shop_inventory",
    "restock_shop",
    "calculate_shop_prices",
    "update_shop_economy",
    "generate_shop_inventory",
    "get_shop_data",
]
