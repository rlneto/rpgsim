"""
Equipment Management Service
"""
from typing import Dict, Optional, Tuple
from core.models import Item, ItemType
from ..domain.equipment import EquipmentSlot, EquipmentComparison
from ..interfaces.iequipment_repository import IEquipmentRepository


class EquipmentManagementService:
    """Service for managing equipment"""

    def __init__(self, equipment_repository: IEquipmentRepository):
        self.equipment_repository = equipment_repository

    def equip_item(self, item: Item, character_stats: Dict[str, int]) -> Tuple[bool, str, Optional[Item]]:
        """Equip an item"""
        if not item.equippable:
            return False, "Item cannot be equipped", None

        target_slot = self._determine_target_slot(item)
        if not target_slot:
            return False, "No suitable slot found", None

        return self.equipment_repository.equip_item(target_slot, item)

    def unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str, Optional[Item]]:
        """Unequip item from slot"""
        return self.equipment_repository.unequip_item(slot)

    def get_equipped_item(self, slot: EquipmentSlot) -> Optional[Item]:
        """Get item in slot"""
        slot_info = self.equipment_repository.get_slot(slot)
        return slot_info.equipped_item if slot_info else None

    def calculate_equipment_stats(self) -> Dict[str, int]:
        """Calculate total stats from equipment"""
        total_stats = {}
        slots = self.equipment_repository.get_all_slots()
        for info in slots.values():
            if info.equipped_item and info.equipped_item.stats_mod:
                for stat, val in info.equipped_item.stats_mod.items():
                    total_stats[stat] = total_stats.get(stat, 0) + val
        return total_stats

    def compare_items(self, current_item: Optional[Item], new_item: Item, slot: EquipmentSlot) -> EquipmentComparison:
        """Compare two items"""
        diffs = {}

        current_stats = current_item.stats_mod if current_item else {}
        new_stats = new_item.stats_mod if new_item else {}

        all_stats = set(current_stats.keys()) | set(new_stats.keys())

        for stat in all_stats:
            old_val = current_stats.get(stat, 0)
            new_val = new_stats.get(stat, 0)
            diffs[stat] = (old_val, new_val)

        current_power = sum(current_stats.values())
        new_power = sum(new_stats.values())

        return EquipmentComparison(
            current_item=current_item,
            new_item=new_item,
            slot_type=slot,
            stat_differences=diffs,
            power_difference=new_power - current_power,
            is_upgrade=new_power > current_power
        )

    def get_equipment_power_level(self) -> int:
        """Calculate total equipment power level"""
        stats = self.calculate_equipment_stats()
        return sum(stats.values())

    def get_equipped_items_summary(self) -> Dict[str, Optional[str]]:
        """Get a summary of equipped items."""
        equipped = {}
        slots = self.equipment_repository.get_all_slots()
        for slot, info in slots.items():
            equipped[slot.value] = info.equipped_item.name if info.equipped_item else None
        return equipped

    def _determine_target_slot(self, item: Item) -> Optional[EquipmentSlot]:
        """Determine the target slot for an item"""
        if item.type == ItemType.WEAPON:
            return EquipmentSlot.WEAPON
        elif item.type == ItemType.ARMOR:
            return EquipmentSlot.ARMOR
        elif item.type == ItemType.ACCESSORY:
            slots = self.equipment_repository.get_all_slots()
            if slots.get(EquipmentSlot.ACCESSORY1).equipped_item is None:
                return EquipmentSlot.ACCESSORY1
            elif slots.get(EquipmentSlot.ACCESSORY2).equipped_item is None:
                return EquipmentSlot.ACCESSORY2
            else:
                return EquipmentSlot.ACCESSORY1
        return None
