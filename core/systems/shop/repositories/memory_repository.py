"""
Memory repository implementations for shop data
"""
from typing import List, Dict, Optional
from ..interfaces.repositories import (
    ShopRepository, ShopItemRepository, ShopTransactionRepository
)
from ..domain.shop import Shop, ShopItem, ShopTransaction


class MemoryShopRepository(ShopRepository):
    """In-memory shop repository"""

    def __init__(self):
        self._shops: Dict[str, Shop] = {}

    def save_shop(self, shop: Shop) -> bool:
        """Save shop to memory storage"""
        if not shop.id:
            return False

        self._shops[shop.id] = shop
        return True

    def load_shop(self, shop_id: str) -> Optional[Shop]:
        """Load shop by ID"""
        return self._shops.get(shop_id)

    def delete_shop(self, shop_id: str) -> bool:
        """Delete shop by ID"""
        if shop_id in self._shops:
            del self._shops[shop_id]
            return True
        return False

    def list_shops(self) -> List[Shop]:
        """List all shops"""
        return list(self._shops.values())

    def find_shops_by_location(self, location: str) -> List[Shop]:
        """Find shops by location"""
        return [shop for shop in self._shops.values() if shop.location == location]

    def find_shops_by_type(self, shop_type: str) -> List[Shop]:
        """Find shops by type"""
        return [shop for shop in self._shops.values() if shop.shop_type == shop_type]


class MemoryShopItemRepository(ShopItemRepository):
    """In-memory shop item repository"""

    def __init__(self, shop_repository: ShopRepository):
        self.shop_repository = shop_repository

    def save_item(self, shop_id: str, item: ShopItem) -> bool:
        """Save item to shop inventory"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return False

        return shop.inventory.add_item(item)

    def load_item(self, shop_id: str, item_id: str) -> Optional[ShopItem]:
        """Load item by ID"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return None

        return shop.inventory.find_item(item_id)

    def delete_item(self, shop_id: str, item_id: str) -> bool:
        """Delete item from shop inventory"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return False

        removed_item = shop.inventory.remove_item(item_id)
        return removed_item is not None

    def list_items(self, shop_id: str) -> List[ShopItem]:
        """List all items in shop inventory"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return []

        return shop.inventory.items.copy()

    def find_items_by_type(self, shop_id: str, item_type: str) -> List[ShopItem]:
        """Find items by type in shop inventory"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return []

        return shop.inventory.get_items_by_type(item_type)


class MemoryShopTransactionRepository(ShopTransactionRepository):
    """In-memory shop transaction repository"""

    def __init__(self, shop_repository: ShopRepository):
        self.shop_repository = shop_repository

    def save_transaction(self, shop_id: str, transaction: ShopTransaction) -> bool:
        """Save transaction to shop history"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return False

        shop.add_transaction(transaction)
        return True

    def load_transactions(self, shop_id: str, limit: int = 100) -> List[ShopTransaction]:
        """Load recent transactions from shop history"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return []

        return shop.customer_history[-limit:] if limit > 0 else shop.customer_history.copy()

    def load_transactions_by_type(self, shop_id: str, transaction_type: str,
                                   limit: int = 100) -> List[ShopTransaction]:
        """Load transactions by type from shop history"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return []

        filtered_transactions = [
            t for t in shop.customer_history if t.transaction_type == transaction_type
        ]

        return filtered_transactions[-limit:] if limit > 0 else filtered_transactions

    def get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, any]:
        """Get transaction summary for recent period"""
        shop = self.shop_repository.load_shop(shop_id)
        if not shop:
            return {}

        from datetime import datetime, timedelta

        # Get recent transactions
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_transactions = [
            t for t in shop.customer_history if t.timestamp >= cutoff_date
        ]

        # Calculate summary
        buy_count = sum(1 for t in recent_transactions if t.transaction_type == "buy")
        sell_count = sum(1 for t in recent_transactions if t.transaction_type == "sell")
        buy_total = sum(t.total_price for t in recent_transactions if t.transaction_type == "buy")
        sell_total = sum(t.total_price for t in recent_transactions if t.transaction_type == "sell")

        return {
            "period_days": days,
            "total_transactions": len(recent_transactions),
            "buy_transactions": buy_count,
            "sell_transactions": sell_count,
            "buy_total_value": buy_total,
            "sell_total_value": sell_total,
            "net_profit": buy_total - sell_total,
            "average_transaction_value": (
                (buy_total + sell_total) / max(1, len(recent_transactions))
            )
        }
