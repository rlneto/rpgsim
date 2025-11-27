"""
Shop domain models for RPGSim
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


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
