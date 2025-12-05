from typing import List, Optional, Tuple, Dict
from ..domain.equipment import Item, ItemType
from ..interfaces.repositories import EquipmentRepository

class InventoryManagementService:
    def __init__(self, repository):
        self.inventory_repository = repository # Test expects this attribute name? Or just repository?
        # Test accesses manager.inventory_repository.get_all_items()

    def add_item(self, item: Item) -> bool:
        # Assuming repository has add_item (if it's inventory repo)
        # But if it's EquipmentRepository, it has add_item too.
        # But test passes InMemoryInventoryRepository.
        # Let's check test imports.
        # from core.systems.equipment.repositories import InMemoryInventoryRepository
        # I probably deleted it. I need to recreate it too?
        # Yes, I deleted in_memory_inventory_repository.py.
        # I need to restore/create it.

        # For now, let's implement service logic assuming repo has add_item
        if hasattr(self.inventory_repository, 'is_full') and self.inventory_repository.is_full():
            return False
        self.inventory_repository.add_item(item)
        return True

    def remove_item(self, item_id: str) -> bool:
        item = self.inventory_repository.get_item(item_id)
        if not item:
            return False
        self.inventory_repository.remove_item(item_id)
        return True

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.inventory_repository.get_item(item_id)

    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        all_items = self.inventory_repository.get_all_items()
        return [item for item in all_items if item.type == item_type]

    def sort_inventory(self, criteria: str) -> List[Item]:
        items = self.inventory_repository.get_all_items()
        if criteria == "name":
            items.sort(key=lambda x: x.name)
        elif criteria == "value":
            items.sort(key=lambda x: x.value, reverse=True)
        return items

    def get_inventory_value(self) -> int:
        items = self.inventory_repository.get_all_items()
        return sum(item.value for item in items)

    def get_inventory_space(self) -> Tuple[int, int]:
        # returns current, max
        current = len(self.inventory_repository.get_all_items())
        max_space = getattr(self.inventory_repository, 'max_size', 100)
        return current, max_space
