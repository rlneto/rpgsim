"""
Equipment Repository Interface
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
from core.models import Item
from ..domain.equipment import EquipmentSlot, EquipmentSlotInfo


class IEquipmentRepository(ABC):
    """Interface for equipment repository"""

    @abstractmethod
    def get_all_slots(self) -> Dict[EquipmentSlot, EquipmentSlotInfo]:
        """Get all equipment slots"""
        pass

    @abstractmethod
    def get_slot(self, slot: EquipmentSlot) -> Optional[EquipmentSlotInfo]:
        """Get a specific equipment slot"""
        pass

    @abstractmethod
    def equip_item(self, slot: EquipmentSlot, item: Item) -> Tuple[bool, str, Optional[Item]]:
        """Equip an item to a slot"""
        pass

    @abstractmethod
    def unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str, Optional[Item]]:
        """Unequip an item from a slot"""
        pass
