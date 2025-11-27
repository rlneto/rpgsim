"""
Shop data repository interfaces
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from ..domain.shop import Shop, ShopItem, ShopTransaction


class ShopRepository(ABC):
    """Repository interface for shop data access"""
    
    @abstractmethod
    def save_shop(self, shop: Shop) -> bool:
        """Save shop to storage"""
        pass
    
    @abstractmethod
    def load_shop(self, shop_id: str) -> Optional[Shop]:
        """Load shop by ID"""
        pass
    
    @abstractmethod
    def delete_shop(self, shop_id: str) -> bool:
        """Delete shop by ID"""
        pass
    
    @abstractmethod
    def list_shops(self) -> List[Shop]:
        """List all shops"""
        pass
    
    @abstractmethod
    def find_shops_by_location(self, location: str) -> List[Shop]:
        """Find shops by location"""
        pass
    
    @abstractmethod
    def find_shops_by_type(self, shop_type: str) -> List[Shop]:
        """Find shops by type"""
        pass


class ShopItemRepository(ABC):
    """Repository interface for shop item data access"""
    
    @abstractmethod
    def save_item(self, shop_id: str, item: ShopItem) -> bool:
        """Save item to shop inventory"""
        pass
    
    @abstractmethod
    def load_item(self, shop_id: str, item_id: str) -> Optional[ShopItem]:
        """Load item by ID"""
        pass
    
    @abstractmethod
    def delete_item(self, shop_id: str, item_id: str) -> bool:
        """Delete item from shop inventory"""
        pass
    
    @abstractmethod
    def list_items(self, shop_id: str) -> List[ShopItem]:
        """List all items in shop inventory"""
        pass
    
    @abstractmethod
    def find_items_by_type(self, shop_id: str, item_type: str) -> List[ShopItem]:
        """Find items by type in shop inventory"""
        pass


class ShopTransactionRepository(ABC):
    """Repository interface for shop transaction data access"""
    
    @abstractmethod
    def save_transaction(self, shop_id: str, transaction: ShopTransaction) -> bool:
        """Save transaction to shop history"""
        pass
    
    @abstractmethod
    def load_transactions(self, shop_id: str, limit: int = 100) -> List[ShopTransaction]:
        """Load recent transactions from shop history"""
        pass
    
    @abstractmethod
    def load_transactions_by_type(self, shop_id: str, transaction_type: str, limit: int = 100) -> List[ShopTransaction]:
        """Load transactions by type from shop history"""
        pass
    
    @abstractmethod
    def get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, Any]:
        """Get transaction summary for recent period"""
        pass
