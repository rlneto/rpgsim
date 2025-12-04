"""
In-Memory Inventory Repository
"""
from typing import List, Optional, Tuple
from core.models import Item
from ..interfaces.iinventory_repository import IInventoryRepository


class InMemoryInventoryRepository(IInventoryRepository):
    """In-memory implementation of the inventory repository"""

    def __init__(self, max_size: int = 100):
        self._inventory: List[Item] = []
        self._max_size = max_size

    def get_all_items(self) -> List[Item]:
        return self._inventory

    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        for item in self._inventory:
            if item.id == item_id:
                return item
        return None

    def add_item(self, item: Item) -> bool:
        if len(self._inventory) >= self._max_size:
            return False
        self._inventory.append(item)
        return True

    def remove_item(self, item_id: str) -> bool:
        for i, item in enumerate(self._inventory):
            if item.id == item_id:
                self._inventory.pop(i)
                return True
        return False

    def get_inventory_space(self) -> Tuple[int, int]:
        return len(self._inventory), self._max_size
