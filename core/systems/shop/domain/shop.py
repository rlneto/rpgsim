"""
Shop domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class ShopType(Enum):
    """Types of shops with different specializations"""
    WEAPONS = "weapons"
    ARMOR = "armor"
    POTIONS = "potions"
    MAGIC_ITEMS = "magic_items"
    GENERAL_GOODS = "general_goods"
    BLACKSMITHING = "blacksmithing"
    ARTIFACTS = "artifacts"
    SCROLLS = "scrolls"

    # Legacy types for compatibility
    WEAPON_SMITH = "weapon_smith"
    ARMOR_MERCHANT = "armor_merchant"
    MAGIC_SHOP = "magic_shop"
    GENERAL_STORE = "general_store"
    RARE_DEALER = "rare_dealer"
    TRADING_POST = "trading_post"

    @classmethod
    def all_types(cls) -> List[str]:
        """Get all shop types"""
        return [t.value for t in cls]

    @classmethod
    def is_valid_type(cls, shop_type: str) -> bool:
        """Check if shop type is valid"""
        return shop_type in cls.all_types()


class ItemRarity(Enum):
    """Rarity levels for items"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    @classmethod
    def all_rarities(cls) -> List[str]:
        """Get all rarity levels"""
        return [r.value for r in cls]

    @classmethod
    def is_valid_rarity(cls, rarity: str) -> bool:
        """Check if rarity is valid"""
        return rarity in cls.all_rarities()


class ItemCondition(Enum):
    """Condition levels for items"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

    @classmethod
    def all_conditions(cls) -> List[str]:
        """Get all condition levels"""
        return [c.value for c in cls]

    @classmethod
    def is_valid_condition(cls, condition: str) -> bool:
        """Check if condition is valid"""
        return condition in cls.all_conditions()


class ShopQuality(Enum):
    """Quality levels for shops"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    LUXURY = "luxury"

    @classmethod
    def all_qualities(cls) -> List[str]:
        """Get all quality levels"""
        return [q.value for q in cls]

    @classmethod
    def is_valid_quality(cls, quality: str) -> bool:
        """Check if quality is valid"""
        return quality in cls.all_qualities()


@dataclass(frozen=True)
class ShopItem:
    """Item in shop inventory"""
    id: str
    name: str
    item_type: str
    effect: str
    base_value: int
    value: int
    rarity: str
    condition: str = ItemCondition.GOOD.value
    quantity: int = 1
    enchantments: List[str] = field(default_factory=list)
    special_properties: Dict[str, Any] = field(default_factory=dict)

    @property
    def stock(self) -> int:
        """Get stock quantity (alias for quantity)"""
        return self.quantity

    def is_rare(self) -> bool:
        """Check if item is rare or better"""
        return self.rarity in [
            ItemRarity.RARE.value,
            ItemRarity.EPIC.value,
            ItemRarity.LEGENDARY.value
        ]

    def get_effective_price(self) -> int:
        """Get price adjusted for condition and rarity"""
        condition_mult = (
            1.0 if self.condition == ItemCondition.GOOD.value else 0.8
        )
        rarity_mult = (
            1.0 if self.rarity == ItemRarity.COMMON.value else 1.5
        )
        return int(self.value * condition_mult * rarity_mult)

    def add_enchantment(self, enchantment: str) -> None:
        """Add enchantment to item"""
        if enchantment not in self.enchantments:
            self.enchantments.append(enchantment)

    def is_available(self) -> bool:
        """Check if item is available for purchase"""
        return self.quantity > 0

    def get_summary(self) -> Dict[str, Any]:
        """Get item summary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.item_type,
            "rarity": self.rarity,
            "condition": self.condition,
            "value": self.value,
            "effective_price": self.get_effective_price(),
            "stock": self.stock,
            "enchantments": self.enchantments.copy()
        }


@dataclass
class ShopInventory:
    """Shop inventory management"""
    items: List[ShopItem] = field(default_factory=list)
    last_refreshed: int = 0
    max_size: int = 30

    @property
    def last_refresh_day(self) -> int:
        """Get last refresh day for compatibility"""
        return self.last_refreshed

    @property
    def current_size(self) -> int:
        """Get current inventory size"""
        return len(self.items)

    def add_item(self, item: ShopItem) -> bool:
        """Add item to inventory"""
        if len(self.items) >= self.max_size:
            return False
        self.items.append(item)
        return True

    def remove_item(self, item_id: str) -> Optional[ShopItem]:
        """Remove item from inventory"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                return self.items.pop(i)
        return None

    def find_item(self, item_id: str) -> Optional[ShopItem]:
        """Find item in inventory"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_items_by_type(self, item_type: str) -> List[ShopItem]:
        """Get items by type"""
        return [item for item in self.items if item.item_type == item_type]

    def get_items_by_rarity(self, rarity: str) -> List[ShopItem]:
        """Get items by rarity"""
        return [item for item in self.items if item.rarity == rarity]

    def refresh(self, new_items: List[ShopItem]) -> int:
        """Refresh inventory with new items"""
        self.items = new_items[:self.max_size]
        self.last_refreshed = datetime.now().day
        return len(self.items)

    def get_summary(self) -> Dict[str, Any]:
        """Get inventory summary"""
        return {
            "total_items": len(self.items),
            "max_size": self.max_size,
            "last_refreshed": self.last_refreshed,
            "item_types": list(set(item.item_type for item in self.items)),
            "rarities": list(set(item.rarity for item in self.items))
        }


@dataclass
class ShopEconomy:
    """Shop economic data"""
    gold_reserves: int
    customer_traffic: int = 50
    competition_level: int = 3
    quality_modifier: float = 1.0
    price_modifier: float = 1.0

    @property
    def gold_reserve(self) -> int:
        """Get gold reserve (alias for gold_reserves)"""
        return self.gold_reserves

    def update_gold_reserves(self, amount: int) -> None:
        """Update gold reserves"""
        self.gold_reserves = max(0, self.gold_reserves + amount)

    def can_afford(self, amount: int) -> bool:
        """Check if shop can afford purchase"""
        return self.gold_reserves >= amount

    def get_economic_status(self) -> Dict[str, Any]:
        """Get economic status summary"""
        return {
            "gold_reserves": self.gold_reserves,
            "customer_traffic": self.customer_traffic,
            "competition_level": self.competition_level,
            "quality_modifier": self.quality_modifier,
            "price_modifier": self.price_modifier
        }


@dataclass
class ShopTransaction:
    """Shop transaction record"""
    transaction_type: str  # "buy" or "sell"
    item_name: str
    quantity: int
    unit_price: int
    total_price: int
    customer_reputation: int = 50
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def create_buy_transaction(
        cls,
        item: ShopItem,
        quantity: int,
        unit_price: int,
        reputation: int = 50
    ) -> 'ShopTransaction':
        """Create buy transaction"""
        return cls(
            transaction_type="buy",
            item_name=item.name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
            customer_reputation=reputation
        )

    @classmethod
    def create_sell_transaction(
        cls,
        item: ShopItem,
        quantity: int,
        unit_price: int,
        reputation: int = 50
    ) -> 'ShopTransaction':
        """Create sell transaction"""
        return cls(
            transaction_type="sell",
            item_name=item.name,
            quantity=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity,
            customer_reputation=reputation
        )


@dataclass
class Shop:
    """Shop aggregate root entity"""
    id: str
    name: str
    shop_type: str
    location: str
    owner: str
    quality_level: str
    inventory: ShopInventory = field(default_factory=ShopInventory)
    economy: ShopEconomy = field(
        default_factory=lambda: ShopEconomy(gold_reserves=1000)
    )
    reputation_discounts: Dict[str, float] = field(default_factory=dict)
    customer_history: List[ShopTransaction] = field(default_factory=list)
    restock_timer: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Post-initialization setup"""
        if not self.reputation_discounts:
            self.reputation_discounts = {
                "default": 0.0,
                "high": 0.2,  # 20% discount for high reputation
                "good": 0.1,  # 10% discount for good reputation
                "neutral": 0.05  # 5% discount for neutral reputation
            }

    def add_transaction(self, transaction: ShopTransaction) -> None:
        """Add transaction to history"""
        self.customer_history.append(transaction)

    def get_reputation_discount(self, reputation: int) -> float:
        """Get discount based on reputation"""
        if reputation >= 80:
            return self.reputation_discounts["high"]
        if reputation >= 60:
            return self.reputation_discounts["good"]
        if reputation >= 40:
            return self.reputation_discounts["neutral"]
        return self.reputation_discounts["default"]

    def can_buy_item_type(self, item_type: str) -> bool:
        """Check if shop can buy this item type"""
        type_compatibility = {
            ShopType.WEAPON_SMITH.value: ["weapon"],
            ShopType.ARMOR_MERCHANT.value: ["armor", "shield"],
            ShopType.MAGIC_SHOP.value: ["magic", "scroll", "potion"],
            ShopType.GENERAL_STORE.value: ["general"],
            ShopType.RARE_DEALER.value: ["rare", "epic", "legendary"],
            ShopType.TRADING_POST.value: ["general", "trade_goods"],
            ShopType.WEAPONS.value: ["weapon"],
            ShopType.ARMOR.value: ["armor", "shield"],
            ShopType.POTIONS.value: ["potion"],
            ShopType.MAGIC_ITEMS.value: ["magic", "scroll"],
            ShopType.GENERAL_GOODS.value: ["general"],
        }
        return item_type in type_compatibility.get(self.shop_type, ["general"])

    def get_summary(self) -> Dict[str, Any]:
        """Get shop summary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.shop_type,
            "location": self.location,
            "owner": self.owner,
            "quality_level": self.quality_level,
            "inventory": self.inventory.get_summary(),
            "economy": self.economy.get_economic_status(),
            "total_transactions": len(self.customer_history),
            "restock_timer": self.restock_timer
        }


# Sample shop configurations
DEFAULT_SHOP_CONFIGS = {
    "weapon_smith": {
        "quality_level": ShopQuality.STANDARD.value,
        "initial_gold": 1500,
        "inventory_size": 25
    },
    "armor_merchant": {
        "quality_level": ShopQuality.STANDARD.value,
        "initial_gold": 1200,
        "inventory_size": 20
    },
    "magic_shop": {
        "quality_level": ShopQuality.PREMIUM.value,
        "initial_gold": 2000,
        "inventory_size": 15
    },
    "general_store": {
        "quality_level": ShopQuality.BASIC.value,
        "initial_gold": 800,
        "inventory_size": 30
    },
    "rare_dealer": {
        "quality_level": ShopQuality.LUXURY.value,
        "initial_gold": 5000,
        "inventory_size": 10
    },
    "trading_post": {
        "quality_level": ShopQuality.STANDARD.value,
        "initial_gold": 1000,
        "inventory_size": 25
    }
}
