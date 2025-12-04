"""
Equipment system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from core.models import Item, ItemType, ItemRarity


class EquipmentSlot(str, Enum):
    """Equipment slots"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY1 = "accessory1"
    ACCESSORY2 = "accessory2"

    def __str__(self):
        return self.value


class ItemEffect(str, Enum):
    """Item effects"""
    FIRE_DAMAGE = "fire_damage"
    ICE_DAMAGE = "ice_damage"
    LIGHTNING_DAMAGE = "lightning_damage"
    LIFE_STEAL = "life_steal"
    CRITICAL_CHANCE = "critical_chance"
    EVASION = "evasion"
    MAGIC_RESISTANCE = "magic_resistance"
    HEALTH_REGENERATION = "health_regeneration"
    MANA_REGENERATION = "mana_regeneration"

    def __str__(self):
        return self.value


@dataclass
class EquipmentStat:
    """Represents a stat bonus from equipment"""
    stat_name: str
    bonus_value: int
    source_item_id: str
    is_percentage: bool = False


@dataclass
class EquipmentSlotInfo:
    """Information about an equipment slot"""
    slot_type: EquipmentSlot
    equipped_item: Optional[Item] = None
    allowed_item_types: List[ItemType] = field(default_factory=list)

    def __post_init__(self):
        if not self.allowed_item_types:
            if self.slot_type == EquipmentSlot.WEAPON:
                self.allowed_item_types = [ItemType.WEAPON]
            elif self.slot_type == EquipmentSlot.ARMOR:
                self.allowed_item_types = [ItemType.ARMOR]
            elif self.slot_type in [EquipmentSlot.ACCESSORY1, EquipmentSlot.ACCESSORY2]:
                self.allowed_item_types = [ItemType.ACCESSORY]


@dataclass
class EquipmentComparison:
    """Result of comparing two items"""
    current_item: Optional[Item]
    new_item: Item
    slot_type: EquipmentSlot
    stat_differences: Dict[str, Any]  # tuple (old, new)
    power_difference: int
    is_upgrade: bool


@dataclass
class LootGenerationResult:
    """Result of loot generation"""
    items: List[Item]
    gold_amount: int
    rarity_distribution: Dict[str, int]
