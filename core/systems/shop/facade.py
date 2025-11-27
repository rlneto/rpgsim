"""
Facade for shop system operations
"""

from typing import List, Dict, Optional, Any
from .domain.shop import (
    Shop,
    ShopItem,
    ShopTransaction,
    ItemRarity,
    ItemCondition,
    ShopQuality,
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


class ShopSystem:
    """Facade for all shop system operations"""

    def __init__(
        self, shop_repository=None, item_repository=None, transaction_repository=None
    ):
        # Initialize repositories with dependency injection
        self.shop_repo = shop_repository or MemoryShopRepository()
        self.item_repo = item_repository or MemoryShopItemRepository(self.shop_repo)
        self.transaction_repo = (
            transaction_repository or MemoryShopTransactionRepository(self.shop_repo)
        )

        # Initialize services
        self.creation_service = ShopCreationService()
        self.transaction_service = ShopTransactionService()
        self.inventory_service = ShopInventoryService()
        self.economy_service = ShopEconomyService()
        self.management_service = ShopManagementService()
        self.item_service = ItemGenerationService()
        self.pricing_service = ItemPricingService()

    # Shop Management Methods
    def create_shop(
        self,
        shop_id: str,
        name: str,
        shop_type: str,
        owner: str,
        location: str,
        quality_level: str = ShopQuality.STANDARD.value,
        gold_reserve: Optional[int] = None,
        inventory_size: Optional[int] = None,
    ) -> Optional[Shop]:
        """Create a new shop"""
        shop = self.creation_service.create_shop(
            shop_id,
            name,
            shop_type,
            owner,
            location,
            quality_level,
            gold_reserve,
            inventory_size,
        )

        if shop:
            self.shop_repo.save_shop(shop)

        return shop

    def get_shop(self, shop_id: str) -> Optional[Shop]:
        """Get shop by ID"""
        return self.shop_repo.load_shop(shop_id)

    def list_shops(self) -> List[Shop]:
        """List all shops"""
        return self.shop_repo.list_shops()

    def find_shops_by_location(self, location: str) -> List[Shop]:
        """Find shops by location"""
        return self.shop_repo.find_shops_by_location(location)

    def find_shops_by_type(self, shop_type: str) -> List[Shop]:
        """Find shops by type"""
        return self.shop_repo.find_shops_by_type(shop_type)

    def delete_shop(self, shop_id: str) -> bool:
        """Delete shop by ID"""
        return self.shop_repo.delete_shop(shop_id)

    # Transaction Methods
    def process_transaction(
        self,
        shop_id: str,
        transaction_type: str,
        item_id: Optional[str] = None,
        item: Optional[ShopItem] = None,
        character_gold: int = 0,
        character_reputation: int = 50,
    ) -> Dict[str, Any]:
        """Process shop transaction (buy or sell)"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return {"success": False, "reason": "Shop not found"}

        if transaction_type == "buy":
            if not item_id:
                return {
                    "success": False,
                    "reason": "Item ID required for buy transaction",
                }
            result = self.transaction_service.process_buy_transaction(
                shop, item_id, character_gold, character_reputation
            )
        elif transaction_type == "sell":
            if not item:
                return {
                    "success": False,
                    "reason": "Item required for sell transaction",
                }
            result = self.transaction_service.process_sell_transaction(
                shop, item, character_reputation
            )
        else:
            return {"success": False, "reason": "Invalid transaction type"}

        # Save shop state after transaction
        self.shop_repo.save_shop(shop)
        return result

    def calculate_buy_price(
        self, shop_id: str, item_id: str, character_reputation: int = 50
    ) -> Optional[int]:
        """Calculate buy price for item"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        item = self.item_repo.load_item(shop_id, item_id)
        if not item:
            return None

        return self.pricing_service.calculate_buy_price(
            shop, item, character_reputation
        )

    def calculate_sell_price(
        self, shop_id: str, item: ShopItem, character_reputation: int = 50
    ) -> Optional[int]:
        """Calculate sell price for item"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        return self.pricing_service.calculate_sell_price(
            shop, item, character_reputation
        )

    # Inventory Methods
    def get_shop_inventory(self, shop_id: str) -> List[ShopItem]:
        """Get shop inventory"""
        return self.item_repo.list_items(shop_id)

    def refresh_inventory(self, shop_id: str, current_day: int) -> Dict[str, Any]:
        """Refresh shop inventory"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return {"success": False, "reason": "Shop not found"}

        result = self.inventory_service.refresh_inventory(shop, current_day)
        self.shop_repo.save_shop(shop)
        return result

    def restock_shop(
        self, shop_id: str, items: Optional[List[ShopItem]] = None
    ) -> Dict[str, Any]:
        """Restock shop inventory"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return {"success": False, "reason": "Shop not found"}

        result = self.inventory_service.restock_shop(shop, items)
        self.shop_repo.save_shop(shop)
        return result

    def add_item_to_inventory(self, shop_id: str, item: ShopItem) -> bool:
        """Add item to shop inventory"""
        success = self.item_repo.save_item(shop_id, item)
        if success:
            # Update shop in repository
            shop = self.shop_repo.load_shop(shop_id)
            if shop:
                self.shop_repo.save_shop(shop)
        return success

    def remove_item_from_inventory(self, shop_id: str, item_id: str) -> bool:
        """Remove item from shop inventory"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return False

        success = self.item_repo.delete_item(shop_id, item_id)
        if success:
            self.shop_repo.save_shop(shop)
        return success

    # Economic Methods
    def update_shop_economy(
        self, shop_id: str, economic_change: int, location_wealth_change: int = 0
    ) -> Dict[str, Any]:
        """Update shop economy"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return {"success": False, "reason": "Shop not found"}

        result = self.economy_service.update_shop_economy(
            shop, economic_change, location_wealth_change
        )
        self.shop_repo.save_shop(shop)
        return result

    def get_shop_economy(self, shop_id: str) -> Optional[Dict[str, Any]]:
        """Get shop economic information"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        return shop.economy.get_economic_status()

    def get_economic_analysis(self, shop_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed economic analysis"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        return self.economy_service.get_economic_analysis(shop)

    # Transaction History Methods
    def get_transaction_history(
        self, shop_id: str, limit: int = 100
    ) -> List[ShopTransaction]:
        """Get shop transaction history"""
        return self.transaction_repo.load_transactions(shop_id, limit)

    def get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, Any]:
        """Get transaction summary for recent period"""
        return self.transaction_repo.get_transaction_summary(shop_id, days)

    # Utility Methods
    def get_shop_overview(self, shop_id: str) -> Optional[Dict[str, Any]]:
        """Get complete shop overview"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        return self.management_service.get_shop_overview(shop)

    def get_shop_statistics(self, shop_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive shop statistics"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        return self.management_service.get_shop_statistics(shop)

    def generate_custom_item(
        self,
        name: str,
        item_type: str,
        base_value: int,
        rarity: str = ItemRarity.COMMON.value,
        condition: str = ItemCondition.GOOD.value,
        effect: str = "Standard effect",
    ) -> ShopItem:
        """Generate custom shop item"""
        return self.item_service.generate_custom_item(
            name, item_type, base_value, rarity, condition, effect
        )

    def calculate_dynamic_price(
        self,
        shop_id: str,
        item_id: str,
        supply_factor: float = 1.0,
        demand_factor: float = 1.0,
        location_wealth: float = 1.0,
    ) -> Optional[int]:
        """Calculate dynamic price based on market conditions"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        item = self.item_repo.load_item(shop_id, item_id)
        if not item:
            return None

        return self.pricing_service.calculate_dynamic_price(
            shop, item, supply_factor, demand_factor, location_wealth
        )

    def calculate_bulk_purchase_price(
        self, shop_id: str, item_ids: List[str], character_reputation: int = 50
    ) -> Optional[Dict[str, Any]]:
        """Calculate price for bulk purchase with discount"""
        shop = self.shop_repo.load_shop(shop_id)
        if not shop:
            return None

        items = []
        for item_id in item_ids:
            item = self.item_repo.load_item(shop_id, item_id)
            if item:
                items.append(item)

        if not items:
            return None

        return self.pricing_service.calculate_bulk_purchase_price(
            shop, items, character_reputation
        )

    # Backward Compatibility Methods (for existing tests)
    def refresh_shop_inventory(
        self, shop_id: str, current_day: int = 1
    ) -> Dict[str, Any]:
        """Refresh shop inventory (backward compatibility)"""
        return self.refresh_inventory(shop_id, current_day)


# Global facade instance for backward compatibility
_shop_system = ShopSystem()


# Backward compatibility functions
def create_shop(
    shop_id: str,
    name: str,
    shop_type: str,
    owner: str,
    location: str,
    quality_level: str = ShopQuality.STANDARD.value,
) -> Optional[Shop]:
    """Create shop (backward compatibility)"""
    return _shop_system.create_shop(
        shop_id, name, shop_type, owner, location, quality_level
    )


def buy_item_from_shop(
    shop_id: str, item_id: str, character_gold: int, character_reputation: int = 50
) -> Dict[str, Any]:
    """Buy item from shop (backward compatibility)"""
    return _shop_system.process_transaction(
        shop_id,
        "buy",
        item_id=item_id,
        character_gold=character_gold,
        character_reputation=character_reputation,
    )


def sell_item_to_shop(
    shop_id: str, item: ShopItem, character_reputation: int = 50
) -> Dict[str, Any]:
    """Sell item to shop (backward compatibility)"""
    return _shop_system.process_transaction(
        shop_id, "sell", item=item, character_reputation=character_reputation
    )


def get_shop_inventory(shop_id: str) -> List[ShopItem]:
    """Get shop inventory (backward compatibility)"""
    return _shop_system.get_shop_inventory(shop_id)


def restock_shop(
    shop_id: str, items: Optional[List[ShopItem]] = None
) -> Dict[str, Any]:
    """Restock shop (backward compatibility)"""
    return _shop_system.restock_shop(shop_id, items)


def calculate_shop_prices(
    shop_id: str, base_prices: List[int], character_reputation: int = 50
) -> List[int]:
    """Calculate shop prices (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    if not shop:
        return base_prices

    return [
        int(
            price
            * shop.economy.price_modifier
            * (1.0 - shop.get_reputation_discount(character_reputation))
        )
        for price in base_prices
    ]


def update_shop_economy(
    shop_id: str, economic_change: int, location_wealth_change: int = 0
) -> Dict[str, Any]:
    """Update shop economy (backward compatibility)"""
    return _shop_system.update_shop_economy(
        shop_id, economic_change, location_wealth_change
    )


def generate_shop_inventory(shop_type: str, inventory_size: int) -> List[ShopItem]:
    """Generate shop inventory (backward compatibility)"""
    return _shop_system.item_service.generate_inventory(shop_type, inventory_size)


def get_shop_data(shop_id: str) -> Optional[Dict[str, Any]]:
    """Get shop data (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    if not shop:
        return None

    return shop.get_summary()


# Export main class and compatibility functions
__all__ = [
    "ShopSystem",
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
