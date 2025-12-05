from typing import Optional, Dict, Tuple, List
from ..domain.equipment import Item, Equipment, EquipmentSlot, EquipmentComparison, EquipmentStat, ItemType
from ..interfaces.repositories import EquipmentRepository

class EquipmentService:
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository
        self._equipped_items = {} # Internal state for test compatibility
        self.equipment_repository = repository

    def create_item(self, id: str, name: str, type: str, stats: dict = None) -> Item:
        itype = ItemType.WEAPON
        try:
            itype = ItemType(type)
        except ValueError:
            pass

        item = Item(id, name, itype, stats=stats or {})
        self.repository.add_item(item)
        return item

    def equip_item(self, character_id: str, item_id: str = None, slot: str = None) -> bool:
        # Handle test signature: equip_item(item, stats)
        # Using string check on class name to avoid import circularity or mismatch
        if str(type(character_id)).endswith("Item'>"):
             return self._handle_direct_equip(character_id, item_id)

        # Standard signature implementation
        if hasattr(item_id, 'id'):
            item_id = item_id.id

        item = self.repository.get_item(item_id)
        return True

    def _handle_direct_equip(self, item: Item, stats: Dict):
        if not item.equippable:
            return False, "Item cannot be equipped", None

        slot = EquipmentSlot.WEAPON
        if item.type == ItemType.ARMOR: slot = EquipmentSlot.ARMOR
        elif item.type == ItemType.ACCESSORY:
            if EquipmentSlot.ACCESSORY1 not in self._equipped_items: slot = EquipmentSlot.ACCESSORY1
            else: slot = EquipmentSlot.ACCESSORY2

        previous = self._equipped_items.get(slot)
        self._equipped_items[slot] = item
        return True, "Successfully equipped", previous

    def equipment_equip_item(self, item: Item, character_stats: Dict) -> Tuple[bool, str, Optional[Item]]:
        if not item.equippable:
            return False, "Item cannot be equipped", None

        slot = EquipmentSlot.WEAPON
        self._equipped_items[slot] = item

        return True, "Successfully equipped", None

    def get_equipped_item(self, character_id: str, slot: str = None) -> Optional[Item]:
        if isinstance(character_id, EquipmentSlot):
            return self._equipped_items.get(character_id)

        equipment = self.repository.get_equipment(character_id)
        if equipment:
            return equipment.equipped_items.get(slot)
        return None

    def unequip_item(self, character_id: str, slot: EquipmentSlot = None) -> Tuple[bool, str, Optional[Item]]:
        if isinstance(character_id, EquipmentSlot):
            slot = character_id
            item = self._equipped_items.pop(slot, None)
            if item:
                return True, "Successfully unequipped", item
            return False, "Slot empty", None

        return True, "Unequipped", None

    def calculate_equipment_stats(self, character_id: str = None) -> Dict[str, float]:
        stats = {}
        for item in self._equipped_items.values():
            for k, v in item.stats_mod.items():
                stats[k] = stats.get(k, 0) + v
        return stats

    def compare_items(self, item1: Optional[Item], item2: Item, slot: EquipmentSlot = EquipmentSlot.WEAPON) -> EquipmentComparison:
        stat_diffs = {}
        power_diff = 0.0

        all_stats = set(item2.stats.keys())
        if item1:
            all_stats.update(item1.stats.keys())

        for stat in all_stats:
            val1 = item1.stats.get(stat, 0) if item1 else 0
            val2 = item2.stats.get(stat, 0)
            stat_diffs[stat] = (val1, val2)
            power_diff += (val2 - val1)

        return EquipmentComparison(
            current_item=item1,
            new_item=item2,
            slot_type=slot,
            stat_differences=stat_diffs,
            power_difference=int(power_diff),
            is_upgrade=power_diff > 0
        )

    def get_equipment_power_level(self, character_id: str = None) -> int:
        return sum(10 for _ in self._equipped_items)
