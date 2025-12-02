"""
Shop system module - provides modular shop management
"""

from datetime import datetime

from .domain.shop import (
    Shop,
    ShopItem,
    ShopInventory,
    ShopEconomy,
    ShopTransaction,
    ShopType,
    ItemRarity,
    ItemCondition,
    ShopQuality,
    DEFAULT_SHOP_CONFIGS,
)
from .services.shop_service import (
    ShopCreationService,
    ShopTransactionService,
    ShopInventoryService,
    ShopEconomyService,
    ShopManagementService,
)
from .services.item_service import ItemGenerationService, ItemPricingService
from .repositories.memory_repository import (
    MemoryShopRepository,
    MemoryShopItemRepository,
    MemoryShopTransactionRepository,
)
from .interfaces.repositories import (
    ShopRepository,
    ShopItemRepository,
    ShopTransactionRepository,
)
from .facade import ShopSystem


class Pricing:
    """Legacy pricing class for backward compatibility"""

    @staticmethod
    def calculate_base_price(item_value: int, rarity: str, condition: str) -> int:
        """Calculate base price from item properties"""
        rarity_multiplier = 1.0 if rarity == "common" else 1.5
        condition_multiplier = 1.0 if condition == "good" else 0.8
        return int(item_value * rarity_multiplier * condition_multiplier)

    @staticmethod
    def calculate_profit_margin(base_price: int, quality: str) -> float:
        """Calculate profit margin based on shop quality"""
        quality_multipliers = {
            "basic": 0.2,
            "standard": 0.3,
            "premium": 0.4,
            "luxury": 0.5,
        }
        margin_multiplier = quality_multipliers.get(quality, 0.3)
        return base_price * margin_multiplier


class Transaction:
    """Legacy transaction class for backward compatibility"""

    def __init__(
        self, transaction_type: str, item_name: str, quantity: int, unit_price: int
    ):
        """Initialize transaction"""
        self.transaction_type = transaction_type
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.timestamp = datetime.now()

    @staticmethod
    def create_transaction(item: ShopItem, transaction_type: str, quantity: int = 1):
        """Create transaction from item"""
        unit_price = (
            item.value if transaction_type == "sell" else item.get_effective_price()
        )
        return Transaction(transaction_type, item.name, quantity, unit_price)

    def get_total_value(self) -> int:
        """Get total transaction value"""
        return self.quantity * self.unit_price


__all__ = [
    "ShopSystem",
    "Pricing",
    "Transaction",
]
