"""
Equipment System Facade
"""
from typing import Dict, List, Optional, Any, Tuple
from core.models import Item, ItemType, ItemRarity
from .domain.equipment import (
    EquipmentSlot, EquipmentComparison, LootGenerationResult
)
from .services.equipment_service import (
    ItemGenerator, EquipmentManager, InventoryManager
)


class EquipmentSystem:
    """Facade for Equipment System"""

    def __init__(self):
        self.item_generator = ItemGenerator()
        self.equipment_manager = EquipmentManager()
        self.inventory_manager = InventoryManager()
        self.unique_items = self.item_generator.generate_all_unique_items()

    def generate_combat_loot(self, difficulty: str) -> LootGenerationResult:
        """Generate loot from combat"""
        return self.item_generator.generate_loot(difficulty)

    def generate_quest_reward(self, difficulty: str) -> LootGenerationResult:
        """Generate quest reward"""
        loot = self.item_generator.generate_loot(difficulty)
        # Quests give more items and gold
        loot.gold_amount = int(loot.gold_amount * 1.5)
        extra_item = self.item_generator.generate_unique_item(f"quest_{loot.gold_amount}", ItemType.ACCESSORY)
        loot.items.append(extra_item)
        return loot

    def add_item_to_inventory(self, item: Item) -> bool:
        """Add item to inventory"""
        return self.inventory_manager.add_item(item)

    def equipment_equip_item(self, item: Item, character_stats: Dict[str, int]) -> Tuple[bool, str, Optional[Item]]:
        """Equip an item"""
        # First ensure item is in inventory? Or just equip?
        # Typically you equip FROM inventory.
        # But this method takes an item object.

        success, msg, prev = self.equipment_manager.equip_item(item, character_stats)
        if success:
            # Remove from inventory if present
            self.inventory_manager.remove_item(item.id)
            # Add previous item to inventory if present
            if prev:
                self.inventory_manager.add_item(prev)

        return success, msg, prev

    def equipment_unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str, Optional[Item]]:
        """Unequip item"""
        success, msg, item = self.equipment_manager.unequip_item(slot)
        if success and item:
            self.inventory_manager.add_item(item)
        return success, msg, item

    def get_character_equipment_stats(self) -> Dict[str, int]:
        """Get stats from equipment"""
        return self.equipment_manager.calculate_equipment_stats()

    def get_character_equipment_power(self) -> int:
        """Get power level"""
        return self.equipment_manager.get_equipment_power_level()

    def get_unique_items_by_type(self, item_type: ItemType, rarity: ItemRarity = None) -> List[Item]:
        """Get unique items filtered"""
        items = [i for i in self.unique_items if i.type == item_type]
        if rarity:
            items = [i for i in items if i.rarity == rarity]
        return items

    def get_item_comparison(self, current_item: Optional[Item], new_item: Item, slot: EquipmentSlot) -> EquipmentComparison:
        """Compare items"""
        return self.equipment_manager.compare_items(current_item, new_item, slot)

    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get summary of inventory and equipment"""
        inv_curr, inv_max = self.inventory_manager.get_inventory_space()

        equipped = {}
        for slot, info in self.equipment_manager.equipment_slots.items():
            equipped[slot.value] = info.equipped_item.name if info.equipped_item else None

        return {
            "inventory": {
                "current_size": inv_curr,
                "max_size": inv_max,
                "item_count": inv_curr,
                "total_value": self.inventory_manager.get_inventory_value()
            },
            "equipment": {
                "equipped_items": equipped,
                "stat_bonuses": self.equipment_manager.calculate_equipment_stats(),
                "power_level": self.equipment_manager.get_equipment_power_level()
            },
            "unique_items_available": len(self.unique_items)
        }

    def get_unique_item_count(self) -> int:
        """Get count of unique items"""
        return len(self.unique_items)
