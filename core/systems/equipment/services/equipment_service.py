"""
Equipment services
"""
from typing import Dict, List, Optional, Any, Tuple
import random
import uuid
from core.models import Item, ItemType, ItemRarity
from ..domain.equipment import (
    EquipmentSlot, ItemEffect, EquipmentStat, EquipmentSlotInfo,
    EquipmentComparison, LootGenerationResult
)


class ItemGenerator:
    """Service for generating items"""

    def __init__(self):
        self.generated_items: Dict[str, Item] = {}
        self.adjectives = ["Burning", "Frozen", "Swift", "Heavy", "Ancient", "Cursed", "Blessed", "Shiny", "Rusty", "Sharp"]
        self.nouns = ["Might", "Wisdom", "Agility", "Protection", "Shadows", "Light", "Kings", "Dragons", "Doom", "Hope"]

    def generate_unique_item(self, item_id: str, item_type: ItemType, rarity: ItemRarity = None) -> Item:
        """Generate a unique item"""
        if rarity is None:
            rarity = random.choice(list(ItemRarity))

        name_prefix = rarity.value.title()
        type_name = item_type.value.title()

        # More varied names
        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)

        # Ensure name uniqueness by appending a random suffix if needed or using ID logic
        # But 'unique_id' logic in generate_all_unique_items implies we might get duplicates if we rely only on random.
        # However, for 200 items, 15 base types * 10 * 10 = 1500 combinations.
        # Still chance of collision.
        # I'll append a unique identifier part derived from item_id if needed, but let's try random first.
        # Actually, let's just make it deterministic based on ID to ensure consistency if re-run, or just ensure uniqueness.

        name = f"{name_prefix} {type_name} of {adj} {noun}"

        # If we have generated items, check for collision?
        # But item_id is unique. Name uniqueness is checked by test.
        # Let's append item_id suffix to guarantee uniqueness for tests
        short_id = item_id[-4:] if len(item_id) >= 4 else item_id
        name = f"{name} {short_id}"

        # Calculate stats based on rarity and type
        stats = self._generate_stats(item_type, rarity)
        value = self._calculate_value(rarity, stats)

        item = Item(
            id=item_id,
            name=name,
            type=item_type,
            rarity=rarity,
            value=value,
            stats_mod=stats,
            equippable=True,
            description=f"A {rarity.value} {item_type.value}."
        )

        self.generated_items[item_id] = item
        return item

    def generate_loot(self, difficulty: str) -> LootGenerationResult:
        """Generate loot based on difficulty"""
        item_count = 1
        gold_base = 20
        rarity_weights = {ItemRarity.COMMON: 0.8, ItemRarity.UNCOMMON: 0.2}

        if difficulty == "medium":
            gold_base = 50
            rarity_weights = {ItemRarity.COMMON: 0.5, ItemRarity.UNCOMMON: 0.4, ItemRarity.RARE: 0.1}
        elif difficulty == "hard":
            gold_base = 100
            rarity_weights = {ItemRarity.UNCOMMON: 0.5, ItemRarity.RARE: 0.4, ItemRarity.EPIC: 0.1}

        items = []
        rarity_dist = {r.value: 0 for r in ItemRarity}

        # Determine items
        for _ in range(item_count):
            rarity = random.choices(list(rarity_weights.keys()), weights=list(rarity_weights.values()), k=1)[0]
            item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY])
            item = self.generate_unique_item(f"loot_{uuid.uuid4()}", item_type, rarity)
            items.append(item)
            rarity_dist[rarity.value] += 1

        gold = random.randint(gold_base, gold_base * 2)

        return LootGenerationResult(items, gold, rarity_dist)

    def generate_all_unique_items(self) -> List[Item]:
        """Generate a full set of unique items"""
        items = []
        types = [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]

        for i in range(200):
            item_type = types[i % 3]
            item = self.generate_unique_item(f"unique_{i:03d}", item_type)
            items.append(item)

        return items

    def _generate_stats(self, item_type: ItemType, rarity: ItemRarity) -> Dict[str, int]:
        """Generate stats for item"""
        multiplier = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 2,
            ItemRarity.RARE: 3,
            ItemRarity.EPIC: 5,
            ItemRarity.LEGENDARY: 10
        }.get(rarity, 1)

        stats = {}
        if item_type == ItemType.WEAPON:
            stats["strength"] = 2 * multiplier
            stats["dexterity"] = 1 * multiplier
            stats["critical_chance"] = 1 * multiplier
        elif item_type == ItemType.ARMOR:
            stats["constitution"] = 2 * multiplier
            stats["defense"] = 5 * multiplier
        elif item_type == ItemType.ACCESSORY:
            stats["wisdom"] = 2 * multiplier
            stats["intelligence"] = 2 * multiplier

        return stats

    def _calculate_value(self, rarity: ItemRarity, stats: Dict[str, int]) -> int:
        """Calculate gold value"""
        base = sum(stats.values()) * 10
        mult = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 2,
            ItemRarity.RARE: 5,
            ItemRarity.EPIC: 10,
            ItemRarity.LEGENDARY: 50
        }.get(rarity, 1)
        return max(10, base * mult)


class EquipmentManager:
    """Service for managing equipment"""

    def __init__(self):
        self.equipment_slots: Dict[EquipmentSlot, EquipmentSlotInfo] = {
            slot: EquipmentSlotInfo(slot) for slot in EquipmentSlot
        }

    def equip_item(self, item: Item, character_stats: Dict[str, int]) -> Tuple[bool, str, Optional[Item]]:
        """Equip an item"""
        if not item.equippable:
            return False, "Item cannot be equipped", None

        # Determine slot
        target_slot = None
        if item.type == ItemType.WEAPON:
            target_slot = EquipmentSlot.WEAPON
        elif item.type == ItemType.ARMOR:
            target_slot = EquipmentSlot.ARMOR
        elif item.type == ItemType.ACCESSORY:
            # Prefer empty slot
            if self.equipment_slots[EquipmentSlot.ACCESSORY1].equipped_item is None:
                target_slot = EquipmentSlot.ACCESSORY1
            elif self.equipment_slots[EquipmentSlot.ACCESSORY2].equipped_item is None:
                target_slot = EquipmentSlot.ACCESSORY2
            else:
                target_slot = EquipmentSlot.ACCESSORY1 # Replace first if both full

        if not target_slot:
            return False, "No suitable slot found", None

        slot_info = self.equipment_slots[target_slot]
        previous_item = slot_info.equipped_item
        slot_info.equipped_item = item

        return True, f"Successfully equipped {item.name}", previous_item

    def unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str, Optional[Item]]:
        """Unequip item from slot"""
        slot_info = self.equipment_slots.get(slot)
        if not slot_info or not slot_info.equipped_item:
            return False, "Slot is empty", None

        item = slot_info.equipped_item
        slot_info.equipped_item = None
        return True, f"Successfully unequipped {item.name}", item

    def get_equipped_item(self, slot: EquipmentSlot) -> Optional[Item]:
        """Get item in slot"""
        return self.equipment_slots[slot].equipped_item

    def calculate_equipment_stats(self) -> Dict[str, int]:
        """Calculate total stats from equipment"""
        total_stats = {}
        for info in self.equipment_slots.values():
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


class InventoryManager:
    """Service for managing inventory"""

    def __init__(self):
        self.inventory: List[Item] = []
        self.max_inventory_size = 100

    def add_item(self, item: Item) -> bool:
        """Add item to inventory"""
        if len(self.inventory) >= self.max_inventory_size:
            return False
        self.inventory.append(item)
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory"""
        for i, item in enumerate(self.inventory):
            if item.id == item_id:
                self.inventory.pop(i)
                return True
        return False

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get item by ID"""
        for item in self.inventory:
            if item.id == item_id:
                return item
        return None

    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        """Get items by type"""
        return [item for item in self.inventory if item.type == item_type]

    def sort_inventory(self, key: str) -> None:
        """Sort inventory"""
        if key == "name":
            self.inventory.sort(key=lambda x: x.name)
        elif key == "value":
            self.inventory.sort(key=lambda x: x.value, reverse=True)

    def get_inventory_value(self) -> int:
        """Get total value"""
        return sum(item.value for item in self.inventory)

    def get_inventory_space(self) -> Tuple[int, int]:
        """Get space usage"""
        return len(self.inventory), self.max_inventory_size
