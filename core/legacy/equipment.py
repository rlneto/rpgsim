"""
Equipment System for RPGSim
Comprehensive equipment management with item generation, stat modifiers,
equipment slots, and inventory management functionality.
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


from core.models import Item, ItemType, ItemRarity


class EquipmentSlot:
    """Equipment slot types"""

    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY1 = "accessory1"
    ACCESSORY2 = "accessory2"


class ItemEffect:
    """Item magical effects"""

    # Damage effects
    FIRE_DAMAGE = "fire_damage"
    ICE_DAMAGE = "ice_damage"
    LIGHTNING_DAMAGE = "lightning_damage"
    POISON_DAMAGE = "poison_damage"
    HOLY_DAMAGE = "holy_damage"
    SHADOW_DAMAGE = "shadow_damage"

    # Combat effects
    LIFE_STEAL = "life_steal"
    CRITICAL_CHANCE = "critical_chance"
    CRITICAL_DAMAGE = "critical_damage"
    STUN_CHANCE = "stun_chance"
    ARMOR_PENETRATION = "armor_penetration"

    # Defensive effects
    EVASION = "evasion"
    MAGIC_RESISTANCE = "magic_resistance"
    DAMAGE_REFLECTION = "damage_reflection"
    THORNS = "thorns"

    # Regeneration effects
    HEALTH_REGENERATION = "health_regeneration"
    MANA_REGENERATION = "mana_regeneration"
    STAMINA_REGENERATION = "stamina_regeneration"

    # Utility effects
    MOVEMENT_SPEED = "movement_speed"
    DETERRENCE = "deterrence"
    GOLD_FIND = "gold_find"
    ITEM_FIND = "item_find"
    EXPERIENCE_BOOST = "experience_boost"


@dataclass
class EquipmentStat:
    """Equipment stat modification"""

    stat_name: str
    bonus_value: int
    source_item_id: str
    is_percentage: bool = False


@dataclass
class EquipmentSlotInfo:
    """Equipment slot information"""

    slot_type: str
    equipped_item: Optional[Item] = None
    allowed_item_types: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Set allowed item types based on slot"""
        if self.slot_type == EquipmentSlot.WEAPON:
            self.allowed_item_types = [ItemType.WEAPON]
        elif self.slot_type == EquipmentSlot.ARMOR:
            self.allowed_item_types = [ItemType.ARMOR]
        elif self.slot_type in [EquipmentSlot.ACCESSORY1, EquipmentSlot.ACCESSORY2]:
            self.allowed_item_types = [ItemType.ACCESSORY]


@dataclass
class EquipmentComparison:
    """Equipment comparison result"""

    current_item: Optional[Item]
    new_item: Item
    slot_type: str
    stat_differences: Dict[str, Tuple[int, int]]  # (current, new)
    power_difference: int
    is_upgrade: bool


@dataclass
class LootGenerationResult:
    """Loot generation result"""

    items: List[Item] = field(default_factory=list)
    gold_amount: int = 0
    rarity_distribution: Dict[str, int] = field(default_factory=dict)


class ItemGenerator:
    """Generates unique magic items with proper scaling and effects"""

    # Item name templates
    WEAPON_NAMES = [
        "Sword",
        "Axe",
        "Mace",
        "Dagger",
        "Spear",
        "Bow",
        "Staff",
        "Wand",
        "Hammer",
        "Claymore",
        "Rapier",
        "Scimitar",
        "Halberd",
        "Trident",
        "Flail",
    ]

    ARMOR_NAMES = [
        "Plate",
        "Mail",
        "Leather",
        "Robes",
        "Scale",
        "Chain",
        "Hide",
        "Cloth",
        "Breastplate",
        "Helmet",
        "Gauntlets",
        "Boots",
        "Shield",
        "Bracers",
        "Greeves",
    ]

    ACCESSORY_NAMES = [
        "Ring",
        "Amulet",
        "Necklace",
        "Bracelet",
        "Charm",
        "Talisman",
        "Brooch",
        "Earring",
        "Pendant",
        "Medallion",
        "Circlet",
        "Crown",
        "Diadem",
        "Scepter",
    ]

    # Item suffixes
    MAGIC_SUFFIXES = [
        "Power",
        "Wisdom",
        "Flames",
        "Shadows",
        "Protection",
        "Might",
        "Speed",
        "Accuracy",
        "Defense",
        "Vitality",
        "Intellect",
        "Agility",
        "Endurance",
        "Focus",
        "Clarity",
        "Resilience",
        "Ferocity",
        "Precision",
        "Absorption",
    ]

    # Stat bonuses by rarity
    RARITY_STATS = {
        ItemRarity.COMMON: 1,
        ItemRarity.UNCOMMON: 2,
        ItemRarity.RARE: 3,
        ItemRarity.EPIC: 4,
        ItemRarity.LEGENDARY: 5,
    }

    # Effect chances by rarity
    RARITY_EFFECT_CHANCES = {
        ItemRarity.COMMON: 0.0,
        ItemRarity.UNCOMMON: 0.1,
        ItemRarity.RARE: 0.3,
        ItemRarity.EPIC: 0.6,
        ItemRarity.LEGENDARY: 0.9,
    }

    # Base value ranges by rarity
    RARITY_VALUE_RANGES = {
        ItemRarity.COMMON: (10, 50),
        ItemRarity.UNCOMMON: (50, 150),
        ItemRarity.RARE: (150, 400),
        ItemRarity.EPIC: (400, 800),
        ItemRarity.LEGENDARY: (800, 2000),
    }

    def __init__(self):
        """Initialize item generator"""
        self.generated_items = []

    def generate_unique_item(self, item_id: str, item_type: ItemType) -> Item:
        """Generate a unique magic item"""

        # Generate base name
        if item_type == ItemType.WEAPON:
            name_part = random.choice(self.WEAPON_NAMES)
        elif item_type == ItemType.ARMOR:
            name_part = random.choice(self.ARMOR_NAMES)
        elif item_type == ItemType.ACCESSORY:
            name_part = random.choice(self.ACCESSORY_NAMES)
        else:
            name_part = "Item"

        # Choose rarity with weighted distribution
        rarity = self._choose_rarity()

        # Generate complete name
        name = f"{name_part} of {random.choice(self.MAGIC_SUFFIXES)}"

        # Generate stats
        stats_mod = self._generate_stats(rarity, item_type)

        # Generate effects
        abilities = self._generate_effects(rarity)

        # Generate value
        value_range = self.RARITY_VALUE_RANGES[rarity]
        value = random.randint(*value_range)

        # Generate description
        description = self._generate_description(item_type, rarity, abilities)

        return Item(
            id=item_id,
            name=name,
            type=item_type,
            rarity=rarity,
            value=value,
            stats_mod=stats_mod,
            abilities=abilities,
            description=description,
            equippable=True,
            consumable=False,
            stackable=False,
            max_stack=1,
        )

    def generate_loot(
        self, difficulty: str = "medium", num_items: int = None
    ) -> LootGenerationResult:
        """Generate loot based on difficulty"""

        if num_items is None:
            num_items = random.randint(1, 3)

        result = LootGenerationResult()

        # Difficulty-based rarity chances
        difficulty_chances = {
            "easy": {
                ItemRarity.COMMON: 70,
                ItemRarity.UNCOMMON: 25,
                ItemRarity.RARE: 5,
                ItemRarity.EPIC: 0,
                ItemRarity.LEGENDARY: 0,
            },
            "medium": {
                ItemRarity.COMMON: 40,
                ItemRarity.UNCOMMON: 40,
                ItemRarity.RARE: 15,
                ItemRarity.EPIC: 4,
                ItemRarity.LEGENDARY: 1,
            },
            "hard": {
                ItemRarity.COMMON: 20,
                ItemRarity.UNCOMMON: 35,
                ItemRarity.RARE: 30,
                ItemRarity.EPIC: 12,
                ItemRarity.LEGENDARY: 3,
            },
        }

        # Generate items
        for i in range(num_items):
            rarity = self._choose_rarity_with_chances(difficulty_chances[difficulty])
            item_type = random.choice(
                [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]
            )

            item = self.generate_unique_item(
                f"loot_{i}_{random.randint(1000, 9999)}", item_type
            )
            # Override rarity for this loot generation
            item.rarity = rarity
            # Adjust stats and value based on rarity
            item.stats_mod = self._generate_stats(rarity, item_type)
            item.abilities = self._generate_effects(rarity)
            value_range = self.RARITY_VALUE_RANGES[rarity]
            item.value = random.randint(*value_range)

            result.items.append(item)

            # Track rarity distribution
            rarity_str = rarity.value
            result.rarity_distribution[rarity_str] = (
                result.rarity_distribution.get(rarity_str, 0) + 1
            )

        # Generate gold reward
        base_gold = random.randint(20, 200)
        difficulty_multiplier = {"easy": 1.0, "medium": 2.0, "hard": 3.0}[difficulty]
        result.gold_amount = int(base_gold * difficulty_multiplier)

        return result

    def generate_all_unique_items(self) -> List[Item]:
        """Generate all 200 unique magic items"""

        items = []

        # Distribute items across types and rarities
        for i in range(200):
            item_type = random.choice(
                [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]
            )
            item = self.generate_unique_item(f"unique_{i:03d}", item_type)
            items.append(item)
            self.generated_items.append(item)

        return items

    def _choose_rarity(self) -> ItemRarity:
        """Choose rarity with weighted distribution"""
        weights = [40, 30, 20, 8, 2]  # Common, Uncommon, Rare, Epic, Legendary
        return random.choices(
            [
                ItemRarity.COMMON,
                ItemRarity.UNCOMMON,
                ItemRarity.RARE,
                ItemRarity.EPIC,
                ItemRarity.LEGENDARY,
            ],
            weights=weights,
        )[0]

    def _choose_rarity_with_chances(self, chances: Dict[ItemRarity, int]) -> ItemRarity:
        """Choose rarity with specific chances"""
        rarities = list(chances.keys())
        weights = list(chances.values())
        return random.choices(rarities, weights=weights)[0]

    def _generate_stats(
        self, rarity: ItemRarity, item_type: ItemType
    ) -> Dict[str, int]:
        """Generate stat modifiers based on rarity and item type"""

        num_stats = self.RARITY_STATS[rarity]

        # Define possible stats for each item type
        if item_type == ItemType.WEAPON:
            possible_stats = [
                "strength",
                "dexterity",
                "critical_chance",
                "critical_damage",
            ]
        elif item_type == ItemType.ARMOR:
            possible_stats = ["constitution", "strength", "magic_resistance", "evasion"]
        else:  # ACCESSORY
            possible_stats = [
                "strength",
                "dexterity",
                "intelligence",
                "wisdom",
                "charisma",
                "constitution",
                "health_regeneration",
                "mana_regeneration",
            ]

        # Select random stats
        selected_stats = random.sample(
            possible_stats, min(num_stats, len(possible_stats))
        )

        # Generate bonus values
        stats_mod = {}
        for stat in selected_stats:
            bonus_range = {
                ItemRarity.COMMON: (1, 3),
                ItemRarity.UNCOMMON: (2, 5),
                ItemRarity.RARE: (4, 8),
                ItemRarity.EPIC: (6, 12),
                ItemRarity.LEGENDARY: (10, 20),
            }[rarity]

            bonus = random.randint(*bonus_range)
            stats_mod[stat] = bonus

        return stats_mod

    def _generate_effects(self, rarity: ItemRarity) -> List[str]:
        """Generate magical effects based on rarity"""

        # Chance to have effects based on rarity
        if random.random() > self.RARITY_EFFECT_CHANCES[rarity]:
            return []

        # Number of effects based on rarity
        num_effects = {
            ItemRarity.UNCOMMON: 1,
            ItemRarity.RARE: 1,
            ItemRarity.EPIC: 2,
            ItemRarity.LEGENDARY: 3,
        }.get(rarity, 0)

        # All possible effects
        all_effects = [
            ItemEffect.FIRE_DAMAGE,
            ItemEffect.ICE_DAMAGE,
            ItemEffect.LIGHTNING_DAMAGE,
            ItemEffect.LIFE_STEAL,
            ItemEffect.CRITICAL_CHANCE,
            ItemEffect.EVASION,
            ItemEffect.MAGIC_RESISTANCE,
            ItemEffect.HEALTH_REGENERATION,
            ItemEffect.MANA_REGENERATION,
            ItemEffect.STUN_CHANCE,
            ItemEffect.POISON_DAMAGE,
            ItemEffect.HOLY_DAMAGE,
            ItemEffect.CRITICAL_DAMAGE,
            ItemEffect.ARMOR_PENETRATION,
            ItemEffect.DAMAGE_REFLECTION,
            ItemEffect.THORNS,
            ItemEffect.MOVEMENT_SPEED,
            ItemEffect.GOLD_FIND,
            ItemEffect.ITEM_FIND,
            ItemEffect.EXPERIENCE_BOOST,
        ]

        # Select random effects
        return random.sample(all_effects, min(num_effects, len(all_effects)))

    def _generate_description(
        self, item_type: ItemType, rarity: ItemRarity, abilities: List[str]
    ) -> str:
        """Generate item description based on type, rarity, and effects"""

        quality_descriptors = {
            ItemRarity.COMMON: "A basic",
            ItemRarity.UNCOMMON: "A well-crafted",
            ItemRarity.RARE: "A fine",
            ItemRarity.EPIC: "An exceptional",
            ItemRarity.LEGENDARY: "A legendary",
        }

        type_descriptors = {
            ItemType.WEAPON: "weapon",
            ItemType.ARMOR: "piece of armor",
            ItemType.ACCESSORY: "magical accessory",
        }

        description = f"{quality_descriptors[rarity]} {type_descriptors[item_type]}"

        if abilities:
            effect_descriptions = {
                ItemEffect.FIRE_DAMAGE: "glowing with fiery energy",
                ItemEffect.ICE_DAMAGE: "radiating cold",
                ItemEffect.LIFE_STEAL: "that drains life from foes",
                ItemEffect.CRITICAL_CHANCE: "designed to strike vital points",
                ItemEffect.EVASION: "that enhances agility",
                ItemEffect.MAGIC_RESISTANCE: "resistant to magical harm",
                ItemEffect.HEALTH_REGENERATION: "that promotes healing",
                ItemEffect.MANA_REGENERATION: "that restores magical energy",
            }

            # Add effect descriptions
            described_effects = [
                effect_descriptions.get(ability, "with magical properties")
                for ability in abilities[:2]
            ]  # Limit to 2 effects
            if described_effects:
                description += f", {', '.join(described_effects)}"

        description += "."
        return description


class EquipmentManager:
    """Manages equipment slots and stat modifications"""

    def __init__(self):
        """Initialize equipment manager"""
        self.equipment_slots = {
            EquipmentSlot.WEAPON: EquipmentSlotInfo(EquipmentSlot.WEAPON),
            EquipmentSlot.ARMOR: EquipmentSlotInfo(EquipmentSlot.ARMOR),
            EquipmentSlot.ACCESSORY1: EquipmentSlotInfo(EquipmentSlot.ACCESSORY1),
            EquipmentSlot.ACCESSORY2: EquipmentSlotInfo(EquipmentSlot.ACCESSORY2),
        }
        self.item_generator = ItemGenerator()

    def equip_item(self, item: Item) -> Tuple[bool, str, Optional[Item]]:
        """Equip an item to the appropriate slot"""

        if not item.can_be_equipped():
            return False, "Item cannot be equipped", None

        # Find appropriate slot
        slot_type = self._get_slot_for_item_type(item.type)
        if not slot_type:
            return False, "No appropriate slot for this item type", None

        slot_info = self.equipment_slots[slot_type]

        # Check if item type is allowed in this slot
        if item.type not in slot_info.allowed_item_types:
            return False, f"Item type {item.type} not allowed in {slot_type}", None

        # Check if slot is occupied
        previous_item = slot_info.equipped_item

        # Equip new item
        slot_info.equipped_item = item

        return True, f"Successfully equipped {item.name} to {slot_type}", previous_item

    def unequip_item(self, slot_type: str) -> Tuple[bool, str, Optional[Item]]:
        """Unequip item from specified slot"""

        if slot_type not in self.equipment_slots:
            return False, f"Invalid slot: {slot_type}", None

        slot_info = self.equipment_slots[slot_type]
        equipped_item = slot_info.equipped_item

        if not equipped_item:
            return False, f"No item equipped in {slot_type}", None

        # Unequip the item
        slot_info.equipped_item = None

        return (
            True,
            f"Successfully unequipped {equipped_item.name} from {slot_type}",
            equipped_item,
        )

    def get_equipped_item(self, slot_type: str) -> Optional[Item]:
        """Get currently equipped item in specified slot"""

        if slot_type not in self.equipment_slots:
            return None

        return self.equipment_slots[slot_type].equipped_item

    def get_all_equipped_items(self) -> Dict[str, Optional[Item]]:
        """Get all currently equipped items"""

        return {
            slot_type: slot_info.equipped_item
            for slot_type, slot_info in self.equipment_slots.items()
        }

    def calculate_equipment_stats(self) -> Dict[str, int]:
        """Calculate total stat bonuses from all equipped items"""

        total_stats = {}

        for slot_info in self.equipment_slots.values():
            if slot_info.equipped_item:
                for stat, bonus in slot_info.equipped_item.stats_mod.items():
                    total_stats[stat] = total_stats.get(stat, 0) + bonus

        return total_stats

    def compare_items(
        self, current_item: Optional[Item], new_item: Item, slot_type: str
    ) -> EquipmentComparison:
        """Compare current item with new item"""

        stat_differences = {}
        power_difference = 0

        # Calculate stats from current item
        current_stats = current_item.stats_mod if current_item else {}

        # Calculate stat differences
        all_stats = set(current_stats.keys()) | set(new_item.stats_mod.keys())

        for stat in all_stats:
            current_value = current_stats.get(stat, 0)
            new_value = new_item.stats_mod.get(stat, 0)
            stat_differences[stat] = (current_value, new_value)
            power_difference += new_value - current_value

        # Determine if it's an upgrade
        is_upgrade = power_difference > 0

        return EquipmentComparison(
            current_item=current_item,
            new_item=new_item,
            slot_type=slot_type,
            stat_differences=stat_differences,
            power_difference=power_difference,
            is_upgrade=is_upgrade,
        )

    def get_equipment_power_level(self) -> int:
        """Calculate total power level of all equipped items"""

        total_power = 0

        for slot_info in self.equipment_slots.values():
            if slot_info.equipped_item:
                item_power = 0
                # Base power from value
                item_power += slot_info.equipped_item.value // 10

                # Power from stat bonuses
                for stat_bonus in slot_info.equipped_item.stats_mod.values():
                    item_power += stat_bonus

                # Power from rarity
                rarity_power = {
                    ItemRarity.COMMON: 1,
                    ItemRarity.UNCOMMON: 2,
                    ItemRarity.RARE: 3,
                    ItemRarity.EPIC: 4,
                    ItemRarity.LEGENDARY: 5,
                }[slot_info.equipped_item.rarity]

                item_power += rarity_power * 10

                total_power += item_power

        return total_power

    def _get_slot_for_item_type(self, item_type: ItemType) -> Optional[str]:
        """Get appropriate equipment slot for item type"""

        if item_type == ItemType.WEAPON:
            return EquipmentSlot.WEAPON
        if item_type == ItemType.ARMOR:
            return EquipmentSlot.ARMOR
        if item_type == ItemType.ACCESSORY:
            # Find first available accessory slot
            if not self.equipment_slots[EquipmentSlot.ACCESSORY1].equipped_item:
                return EquipmentSlot.ACCESSORY1
            if not self.equipment_slots[EquipmentSlot.ACCESSORY2].equipped_item:
                return EquipmentSlot.ACCESSORY2
            return EquipmentSlot.ACCESSORY1  # Default to first slot
        return None


class InventoryManager:
    """Manages player inventory and item operations"""

    def __init__(self):
        """Initialize inventory manager"""
        self.max_inventory_size = 100
        self.inventory = []
        self.equipment_manager = EquipmentManager()

    def add_item(self, item: Item) -> bool:
        """Add item to inventory"""

        # Check inventory space
        if len(self.inventory) >= self.max_inventory_size:
            return False

        # For stackable items, try to stack
        if item.stackable and item.max_stack > 1:
            existing_item = self._find_existing_stackable_item(item)
            if (
                existing_item
                and existing_item.max_stack > existing_item.get_total_value()
            ):
                existing_item.max_stack += 1
                return True

        # Add as new item
        self.inventory.append(item)
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove item from inventory by ID"""

        for i, item in enumerate(self.inventory):
            if item.id == item_id:
                del self.inventory[i]
                return True
        return False

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get item from inventory by ID"""

        for item in self.inventory:
            if item.id == item_id:
                return item
        return None

    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        """Get all items of specified type from inventory"""

        return [item for item in self.inventory if item.type == item_type]

    def sort_inventory(self, sort_by: str = "name") -> None:
        """Sort inventory by specified criteria"""

        if sort_by == "name":
            self.inventory.sort(key=lambda x: x.name)
        elif sort_by == "type":
            self.inventory.sort(key=lambda x: x.type.value)
        elif sort_by == "rarity":
            rarity_order = [
                ItemRarity.COMMON,
                ItemRarity.UNCOMMON,
                ItemRarity.RARE,
                ItemRarity.EPIC,
                ItemRarity.LEGENDARY,
            ]
            self.inventory.sort(key=lambda x: rarity_order.index(x.rarity))
        elif sort_by == "value":
            self.inventory.sort(key=lambda x: x.value, reverse=True)

    def get_inventory_value(self) -> int:
        """Calculate total value of all items in inventory"""

        return sum(item.get_total_value() for item in self.inventory)

    def get_inventory_space(self) -> Tuple[int, int]:
        """Get current and maximum inventory space"""

        return len(self.inventory), self.max_inventory_size

    def _find_existing_stackable_item(self, item: Item) -> Optional[Item]:
        """Find existing stackable item of same type"""

        for existing_item in self.inventory:
            if (
                existing_item.stackable
                and existing_item.id == item.id  # Same base item
                and existing_item.max_stack < existing_item.max_stack
            ):
                return existing_item
        return None


class EquipmentSystem:
    """Main equipment system that integrates all equipment functionality"""

    def __init__(self):
        """Initialize equipment system"""
        self.inventory_manager = InventoryManager()
        self.equipment_manager = EquipmentManager()  # Separate instance for general use
        self.item_generator = ItemGenerator()
        self.unique_items = []

        # Generate all unique items on initialization
        self.unique_items = self.item_generator.generate_all_unique_items()

    def generate_combat_loot(
        self, enemy_difficulty: str = "medium"
    ) -> LootGenerationResult:
        """Generate loot after combat"""

        return self.item_generator.generate_loot(enemy_difficulty)

    def generate_quest_reward(
        self, quest_difficulty: str = "medium"
    ) -> LootGenerationResult:
        """Generate quest rewards"""

        # Quest rewards are generally better than combat loot
        result = self.item_generator.generate_loot(
            quest_difficulty, random.randint(2, 4)
        )

        # Bonus gold for quests
        result.gold_amount = int(result.gold_amount * 1.5)

        return result

    def equipment_equip_item(
        self, item: Item, character_stats: Dict[str, int]
    ) -> Tuple[bool, str, Optional[Item]]:
        """Equip item using inventory manager's equipment manager"""

        return self.inventory_manager.equipment_manager.equip_item(
            item, character_stats
        )

    def equipment_unequip_item(
        self, slot_type: str
    ) -> Tuple[bool, str, Optional[Item]]:
        """Unequip item using inventory manager's equipment manager"""

        return self.inventory_manager.equipment_manager.unequip_item(slot_type)

    def add_item_to_inventory(self, item: Item) -> bool:
        """Add item to inventory"""

        return self.inventory_manager.add_item(item)

    def remove_item_from_inventory(self, item_id: str) -> bool:
        """Remove item from inventory"""

        return self.inventory_manager.remove_item(item_id)

    def get_character_equipment_stats(self) -> Dict[str, int]:
        """Get total equipment stats for character"""

        return self.inventory_manager.equipment_manager.calculate_equipment_stats()

    def get_character_equipment_power(self) -> int:
        """Get character's total equipment power level"""

        return self.inventory_manager.equipment_manager.get_equipment_power_level()

    def get_unique_items_by_type(
        self, item_type: ItemType, rarity: Optional[ItemRarity] = None
    ) -> List[Item]:
        """Get unique items filtered by type and optionally rarity"""

        items = [item for item in self.unique_items if item.type == item_type]

        if rarity:
            items = [item for item in items if item.rarity == rarity]

        return items

    def get_item_comparison(
        self, current_item: Optional[Item], new_item: Item, slot_type: str
    ) -> EquipmentComparison:
        """Compare items for equipment decisions"""

        return self.inventory_manager.equipment_manager.compare_items(
            current_item, new_item, slot_type
        )

    def get_unique_item_count(self) -> int:
        """Get total count of unique items in system"""

        return len(self.unique_items)

    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get summary of player inventory and equipment"""

        equipped_items = (
            self.inventory_manager.equipment_manager.get_all_equipped_items()
        )
        equipment_stats = (
            self.inventory_manager.equipment_manager.calculate_equipment_stats()
        )

        current_space, max_space = self.inventory_manager.get_inventory_space()

        return {
            "inventory": {
                "current_size": current_space,
                "max_size": max_space,
                "total_value": self.inventory_manager.get_inventory_value(),
                "item_count": len(self.inventory_manager.inventory),
            },
            "equipment": {
                "equipped_items": {
                    slot: item.name if item else None
                    for slot, item in equipped_items.items()
                },
                "stat_bonuses": equipment_stats,
                "power_level": self.inventory_manager.equipment_manager.get_equipment_power_level(),
            },
            "unique_items_available": len(self.unique_items),
        }
