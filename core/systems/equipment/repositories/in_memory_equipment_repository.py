"""
In-Memory Equipment Repository
"""
from typing import Dict, Optional, Tuple
from core.models import Item
from ..domain.equipment import EquipmentSlot, EquipmentSlotInfo
from ..interfaces.iequipment_repository import IEquipmentRepository


class InMemoryEquipmentRepository(IEquipmentRepository):
    """In-memory implementation of the equipment repository"""

    def __init__(self):
        self._slots: Dict[EquipmentSlot, EquipmentSlotInfo] = {
            slot: EquipmentSlotInfo(slot) for slot in EquipmentSlot
        }

    def get_all_slots(self) -> Dict[EquipmentSlot, EquipmentSlotInfo]:
        return self._slots

    def get_slot(self, slot: EquipmentSlot) -> Optional[EquipmentSlotInfo]:
        return self._slots.get(slot)

    def equip_item(self, slot: EquipmentSlot, item: Item) -> Tuple[bool, str, Optional[Item]]:
        slot_info = self._slots.get(slot)
        if not slot_info:
            return False, "Invalid slot", None

        previous_item = slot_info.equipped_item
        slot_info.equipped_item = item
        return True, f"Successfully equipped {item.name}", previous_item

    def unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str, Optional[Item]]:
        slot_info = self._slots.get(slot)
        if not slot_info or not slot_info.equipped_item:
            return False, "Slot is empty", None

        item = slot_info.equipped_item
        slot_info.equipped_item = None
        return True, f"Successfully unequipped {item.name}", item
