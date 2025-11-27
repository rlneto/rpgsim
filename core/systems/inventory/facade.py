"""
Facade for inventory system
"""

from typing import Dict, Any, Optional
from ...models import Item
from .services.inventory_service import InventoryService
from .repositories.memory_repository import MemoryInventoryRepository


class InventorySystem:
    """Facade for inventory operations"""

    def __init__(self, repository=None):
        self.repository = repository or MemoryInventoryRepository()
        self.service = InventoryService()

    def create_inventory(self, character_id: str, max_slots: int = 30) -> bool:
        """Create inventory for character"""
        try:
            inventory = self.service.create_inventory(character_id, max_slots)
            return self.repository.save(character_id, inventory)
        except Exception:
            return False

    def add_item(self, character_id: str, item: Item, quantity: int = 1) -> bool:
        """Add item to character inventory"""
        return self.service.add_item(character_id, item, quantity)

    def remove_item(
        self, character_id: str, item_id: str, quantity: int = 1
    ) -> Optional[Item]:
        """Remove item from character inventory"""
        return self.service.remove_item(character_id, item_id, quantity)

    def get_inventory_summary(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get inventory summary"""
        return self.service.get_inventory_summary(character_id)

    def get_item_count(self, character_id: str, item_id: str) -> int:
        """Get count of specific item"""
        return self.service.get_item_count(character_id, item_id)
