"""
Memory repository for inventory
"""

from typing import Dict, Optional
from core.systems.inventory.interfaces.repositories import InventoryRepository
from core.systems.inventory.domain.inventory import Inventory


class MemoryInventoryRepository(InventoryRepository):
    """In-memory implementation of inventory repository"""

    def __init__(self):
        self._inventories: Dict[str, Inventory] = {}

    def save(self, character_id: str, inventory: Inventory) -> bool:
        """Save inventory to memory"""
        try:
            self._inventories[character_id] = inventory
            return True
        except Exception:
            return False

    def load(self, character_id: str) -> Optional[Inventory]:
        """Load inventory from memory"""
        return self._inventories.get(character_id)

    def delete(self, character_id: str) -> bool:
        """Delete inventory from memory"""
        if character_id in self._inventories:
            del self._inventories[character_id]
            return True
        return False

    def exists(self, character_id: str) -> bool:
        """Check if inventory exists"""
        return character_id in self._inventories
