"""
Inventory domain models for RPGSim
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

from core.models import Item


class InventorySlotType(str, Enum):
    """Types of inventory slots"""

    HEAD = "head"
    CHEST = "chest"
    LEGS = "legs"
    FEET = "feet"
    WEAPON = "weapon"
    SHIELD = "shield"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MISC = "misc"


@dataclass
class InventorySlot:
    """Represents a single inventory slot"""

    slot_type: InventorySlotType
    item: Optional[Item] = None
    quantity: int = 0
    max_quantity: int = 1
    equipped: bool = False

    def is_empty(self) -> bool:
        """Check if slot is empty"""
        return self.item is None or self.quantity <= 0

    def can_add_item(self, item: Item, quantity: int = 1) -> bool:
        """Check if item can be added to this slot"""
        if self.is_empty():
            return True

        if self.item.id != item.id:
            return False

        return self.quantity + quantity <= self.max_quantity

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """Add item to slot"""
        if not self.can_add_item(item, quantity):
            return False

        if self.is_empty():
            self.item = item

        self.quantity += quantity
        return True

    def remove_item(self, quantity: int = 1) -> Optional[Item]:
        """Remove item from slot"""
        if self.is_empty() or quantity > self.quantity:
            return None

        self.quantity -= quantity
        item = self.item

        if self.quantity <= 0:
            self.item = None
            self.quantity = 0
            self.equipped = False

        return item

    def get_total_weight(self) -> float:
        """Get total weight of items in slot"""
        if self.is_empty():
            return 0.0
        return (
            self.item.stats_mod.get("weight", 1.0)
            if hasattr(self.item, "stats_mod")
            else 1.0
        ) * self.quantity


class Inventory:
    """Main inventory class"""

    def __init__(self, max_slots: int = 30, max_weight: float = 100.0):
        self.max_slots = max_slots
        self.max_weight = max_weight
        self.slots: List[InventorySlot] = []
        self.equipped_items: Dict[InventorySlotType, Optional[Item]] = {
            slot_type: None for slot_type in InventorySlotType
        }

        # Initialize empty slots
        for i in range(max_slots):
            self.slots.append(
                InventorySlot(
                    slot_type=InventorySlotType.MISC,
                    max_quantity=99
                    if i >= max_slots - 5
                    else 1,  # Last 5 slots for stackable items
                )
            )

    def get_empty_slots(self) -> List[InventorySlot]:
        """Get all empty slots"""
        return [slot for slot in self.slots if slot.is_empty()]

    def get_slots_with_item(self, item_id: str) -> List[InventorySlot]:
        """Get all slots containing specific item"""
        return [slot for slot in self.slots if slot.item and slot.item.id == item_id]

    def can_add_item(self, item: Item, quantity: int = 1) -> bool:
        """Check if item can be added to inventory"""
        # Check weight limit
        item_weight = (
            item.stats_mod.get("weight", 1.0) if hasattr(item, "stats_mod") else 1.0
        ) * quantity
        if self.get_total_weight() + item_weight > self.max_weight:
            return False

        # Check if item can stack with existing slots
        existing_slots = self.get_slots_with_item(item.id)
        for slot in existing_slots:
            if slot.can_add_item(item, quantity):
                return True

        # Check if there are empty slots
        return len(self.get_empty_slots()) > 0

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """Add item to inventory"""
        if not self.can_add_item(item, quantity):
            return False

        # Try to stack with existing items first
        existing_slots = self.get_slots_with_item(item.id)
        for slot in existing_slots:
            if slot.add_item(item, quantity):
                return True

        # Add to empty slot
        empty_slots = self.get_empty_slots()
        if empty_slots:
            return empty_slots[0].add_item(item, quantity)

        return False

    def remove_item(self, item_id: str, quantity: int = 1) -> Optional[Item]:
        """Remove item from inventory"""
        slots_with_item = self.get_slots_with_item(item_id)
        if not slots_with_item:
            return None

        # Remove from first available slot
        for slot in slots_with_item:
            if slot.quantity >= quantity:
                return slot.remove_item(quantity)
            else:
                # Take what we can from this slot and continue
                remaining = quantity - slot.quantity
                slot.remove_item(slot.quantity)
                quantity = remaining

        return None

    def get_item_count(self, item_id: str) -> int:
        """Get total count of specific item"""
        slots_with_item = self.get_slots_with_item(item_id)
        return sum(slot.quantity for slot in slots_with_item)

    def get_total_weight(self) -> float:
        """Get total weight of all items"""
        return sum(slot.get_total_weight() for slot in self.slots)

    def get_total_value(self) -> int:
        """Get total value of all items"""
        total = 0
        for slot in self.slots:
            if not slot.is_empty():
                total += slot.item.get_total_value() * slot.quantity
        return total

    def equip_item(self, slot: InventorySlot) -> bool:
        """Equip item from slot"""
        if slot.is_empty():
            return False

        item = slot.item
        if not item.can_be_equipped():
            return False

        # Determine slot type based on item type
        if item.type.value == "weapon":
            slot_type = InventorySlotType.WEAPON
        elif item.type.value == "armor":
            slot_type = InventorySlotType.CHEST
        elif item.type.value == "accessory":
            slot_type = InventorySlotType.ACCESSORY
        else:
            return False

        # Unequip current item if any
        current_equipped = self.equipped_items.get(slot_type)
        if current_equipped:
            self.unequip_item(slot_type)

        # Equip new item
        self.equipped_items[slot_type] = item
        slot.equipped = True
        return True

    def unequip_item(self, slot_type: InventorySlotType) -> Optional[Item]:
        """Unequip item from slot type"""
        item = self.equipped_items.get(slot_type)
        if not item:
            return None

        self.equipped_items[slot_type] = None

        # Find slot with this item and unequip it
        for slot in self.slots:
            if slot.item == item:
                slot.equipped = False
                break

        return item

    def get_equipped_items(self) -> Dict[InventorySlotType, Optional[Item]]:
        """Get all equipped items"""
        return self.equipped_items.copy()

    def get_summary(self) -> Dict[str, Any]:
        """Get inventory summary"""
        return {
            "max_slots": self.max_slots,
            "used_slots": len([slot for slot in self.slots if not slot.is_empty()]),
            "max_weight": self.max_weight,
            "current_weight": self.get_total_weight(),
            "total_value": self.get_total_value(),
            "equipped_count": len(
                [item for item in self.equipped_items.values() if item is not None]
            ),
            "unique_items": len(
                set(slot.item.id for slot in self.slots if not slot.is_empty())
            ),
        }
