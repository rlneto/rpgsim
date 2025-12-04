"""
Inventory Repository Interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from core.models import Item, ItemType


class IInventoryRepository(ABC):
    """Interface for inventory repository"""

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        """Get all items from inventory"""
        pass

    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        """Get a specific item by its ID"""
        pass

    @abstractmethod
    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory"""
        pass

    @abstractmethod
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the inventory"""
        pass

    @abstractmethod
    def get_inventory_space(self) -> Tuple[int, int]:
        """Get current and max inventory space"""
        pass
