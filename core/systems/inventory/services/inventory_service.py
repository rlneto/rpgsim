"""
Inventory service for RPGSim
Handles inventory business logic
"""

from typing import List, Dict, Any, Optional
from core.models import Item
from core.systems.inventory.domain.inventory import Inventory, InventorySlot


class InventoryService:
    """Service for managing inventory operations"""

    def __init__(self):
        self.inventories: Dict[str, Inventory] = {}

    def create_inventory(
        self, character_id: str, max_slots: int = 30, max_weight: float = 100.0
    ) -> Inventory:
        """Create new inventory for character"""
        inventory = Inventory(max_slots=max_slots, max_weight=max_weight)
        self.inventories[character_id] = inventory
        return inventory

    def get_inventory(self, character_id: str) -> Optional[Inventory]:
        """Get inventory by character ID"""
        return self.inventories.get(character_id)

    def add_item(self, character_id: str, item: Item, quantity: int = 1) -> bool:
        """Add item to character inventory"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return False
        return inventory.add_item(item, quantity)

    def remove_item(
        self, character_id: str, item_id: str, quantity: int = 1
    ) -> Optional[Item]:
        """Remove item from character inventory"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return None
        return inventory.remove_item(item_id, quantity)

    def get_item_count(self, character_id: str, item_id: str) -> int:
        """Get count of specific item in inventory"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return 0
        return inventory.get_item_count(item_id)

    def can_add_item(self, character_id: str, item: Item, quantity: int = 1) -> bool:
        """Check if item can be added to inventory"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return False
        return inventory.can_add_item(item, quantity)

    def equip_item(self, character_id: str, slot_index: int) -> bool:
        """Equip item from specific slot"""
        inventory = self.get_inventory(character_id)
        if not inventory or slot_index >= len(inventory.slots):
            return False
        return inventory.equip_item(inventory.slots[slot_index])

    def unequip_item(self, character_id: str, slot_type: str) -> Optional[Item]:
        """Unequip item from slot type"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return None

        from core.systems.inventory.domain.inventory import InventorySlotType

        try:
            slot_enum = InventorySlotType(slot_type)
            return inventory.unequip_item(slot_enum)
        except ValueError:
            return None

    def get_inventory_summary(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get inventory summary"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return None
        return inventory.get_summary()

    def get_equipped_items(self, character_id: str) -> Dict[str, Any]:
        """Get all equipped items"""
        inventory = self.get_inventory(character_id)
        if not inventory:
            return {}

        equipped = inventory.get_equipped_items()
        return {
            slot_type.value: item.model_dump() if item else None
            for slot_type, item in equipped.items()
        }

    def transfer_item(
        self,
        from_character_id: str,
        to_character_id: str,
        item_id: str,
        quantity: int = 1,
    ) -> bool:
        """Transfer item between characters"""
        from_inventory = self.get_inventory(from_character_id)
        to_inventory = self.get_inventory(to_character_id)

        if not from_inventory or not to_inventory:
            return False

        # Check if destination can receive item
        item = None
        for slot in from_inventory.slots:
            if slot.item and slot.item.id == item_id:
                item = slot.item
                break

        if not item or not to_inventory.can_add_item(item, quantity):
            return False

        # Remove from source and add to destination
        removed_item = from_inventory.remove_item(item_id, quantity)
        if removed_item:
            return to_inventory.add_item(removed_item, quantity)

        return False

    def delete_inventory(self, character_id: str) -> bool:
        """Delete character inventory"""
        if character_id in self.inventories:
            del self.inventories[character_id]
            return True
        return False
