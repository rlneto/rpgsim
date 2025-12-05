from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class EquipmentSlot(str, Enum):
    WEAPON = "weapon"
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    HEAD = "head"
    CHEST = "chest"
    LEGS = "legs"
    FEET = "feet"
    HANDS = "hands"
    NECK = "neck"
    RING_1 = "ring_1"
    RING_2 = "ring_2"
    ACCESSORY = "accessory"
    ACCESSORY1 = "accessory1"
    ACCESSORY2 = "accessory2"
    ARMOR = "armor"

    def __str__(self):
        return self.value

class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MATERIAL = "material"

    def __str__(self):
        return self.value

class ItemRarity(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    def __str__(self):
        return self.value

class ItemEffect(str, Enum):
    FIRE_DAMAGE = "fire_damage"
    ICE_DAMAGE = "ice_damage"
    LIGHTNING_DAMAGE = "lightning_damage"
    HEALING = "healing"
    BUFF = "buff"
    LIFE_STEAL = "life_steal"
    CRITICAL_CHANCE = "critical_chance"
    EVASION = "evasion"
    DEFENSE_UP = "defense_up"
    MAGIC_RESISTANCE = "magic_resistance"
    HEALTH_REGENERATION = "health_regeneration"
    MANA_REGENERATION = "mana_regeneration"
    STAMINA_REGENERATION = "stamina_regeneration"

    def __str__(self):
        return self.value

@dataclass
class Item:
    id: str
    name: str
    type: ItemType
    rarity: ItemRarity = ItemRarity.COMMON
    value: int = 0
    stats: dict = field(default_factory=dict)
    stats_mod: dict = field(default_factory=dict)
    equippable: bool = True
    consumable: bool = False
    stackable: bool = False # Added for test

    def __post_init__(self):
        if self.type == ItemType.WEAPON and not self.stats:
            self.stats = self.stats_mod
        if self.stats_mod and not self.stats:
            self.stats = self.stats_mod

    def can_be_equipped(self) -> bool:
        return self.equippable

@dataclass
class Equipment:
    character_id: str
    items: List[Item] = field(default_factory=list)
    equipped_items: dict = field(default_factory=dict)

@dataclass
class LootGenerationResult:
    items: List[Item]
    gold: int = 0
    experience: int = 0
    gold_amount: int = 0
    rarity_distribution: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if self.gold_amount and not self.gold:
            self.gold = self.gold_amount
        if self.gold and not self.gold_amount:
            self.gold_amount = self.gold

@dataclass
class EquipmentStat:
    stat_name: str
    bonus_value: float
    source_item_id: str
    is_percentage: bool = False

@dataclass
class EquipmentSlotInfo:
    slot_type: EquipmentSlot
    is_equipped: bool = False
    item: Optional[Item] = None
    equipped_item: Optional[Item] = None
    allowed_item_types: List[ItemType] = field(default_factory=list)

    def __post_init__(self):
        if self.item and not self.equipped_item:
            self.equipped_item = self.item
        if self.equipped_item and not self.item:
            self.item = self.equipped_item
        if not self.allowed_item_types:
            if self.slot_type == EquipmentSlot.WEAPON:
                self.allowed_item_types = [ItemType.WEAPON]
            elif self.slot_type == EquipmentSlot.ARMOR:
                self.allowed_item_types = [ItemType.ARMOR]
            elif self.slot_type in [EquipmentSlot.ACCESSORY, EquipmentSlot.ACCESSORY1, EquipmentSlot.ACCESSORY2]:
                self.allowed_item_types = [ItemType.ACCESSORY]
            elif self.slot_type == EquipmentSlot.MAIN_HAND:
                self.allowed_item_types = [ItemType.WEAPON]
            elif self.slot_type in [EquipmentSlot.CHEST, EquipmentSlot.HEAD, EquipmentSlot.LEGS, EquipmentSlot.FEET, EquipmentSlot.HANDS]:
                self.allowed_item_types = [ItemType.ARMOR]

@dataclass
class EquipmentComparison:
    current_item: Optional[Item]
    new_item: Item
    slot_type: EquipmentSlot
    stat_differences: Dict[str, tuple]
    power_difference: float
    is_upgrade: bool
