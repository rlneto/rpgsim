"""
Inventory Management Service
"""
from typing import List, Optional, Tuple
from core.models import Item, ItemType
from ..interfaces.iinventory_repository import IInventoryRepository


class InventoryManagementService:
    """Service for managing inventory"""

    def __init__(self, inventory_repository: IInventoryRepository):
        self.inventory_repository = inventory_repository

    def add_item(self, item: Item) -> bool:
        """Add item to inventory"""
        return self.inventory_repository.add_item(item)

    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory"""
        return self.inventory_repository.remove_item(item_id)

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get item by ID"""
        return self.inventory_repository.get_item_by_id(item_id)

    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        """Get items by type"""
        items = self.inventory_repository.get_all_items()
        return [item for item in items if item.type == item_type]

    def sort_inventory(self, key: str) -> None:
        """Sort inventory"""
        items = self.inventory_repository.get_all_items()
        if key == "name":
            items.sort(key=lambda x: x.name)
        elif key == "value":
            items.sort(key=lambda x: x.value, reverse=True)

    def get_inventory_value(self) -> int:
        """Get total value"""
        items = self.inventory_repository.get_all_items()
        return sum(item.value for item in items)

    def get_inventory_space(self) -> Tuple[int, int]:
        """Get space usage"""
        return self.inventory_repository.get_inventory_space()
