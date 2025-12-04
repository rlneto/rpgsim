"""
Character domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class CharacterClass(Enum):
    """All 23 character classes available in RPGSim"""
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    CLERIC = "Cleric"
    RANGER = "Ranger"
    PALADIN = "Paladin"
    WARLOCK = "Warlock"
    DRUID = "Druid"
    MONK = "Monk"
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    SORCERER = "Sorcerer"
    FIGHTER = "Fighter"
    NECROMANCER = "Necromancer"
    ILLUSIONIST = "Illusionist"
    ALCHEMIST = "Alchemist"
    BERSERKER = "Berserker"
    ASSASSIN = "Assassin"
    HEALER = "Healer"
    SUMMONER = "Summoner"
    SHAPESHIFTER = "Shapeshifter"
    ELEMENTALIST = "Elementalist"
    NINJA = "Ninja"
    DEVELOPER = "Developer"


@dataclass(frozen=True)
class CharacterStats:
    """Character statistics as immutable value object"""
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    constitution: int = 10

    def total_power(self) -> int:
        """Calculate total power level"""
        return (
            self.strength + self.dexterity + self.intelligence +
            self.wisdom + self.charisma + self.constitution
        )

    def primary_stat_value(self, primary_stat: str) -> int:
        """Get value of primary stat"""
        return getattr(self, primary_stat, 10)

    def get_strengths(self) -> List[str]:
        """Get list of character's strong stats (15+ points)"""
        return [
            stat for stat, value in self.__dict__.items()
            if isinstance(value, int) and value >= 15
        ]

    def get_weaknesses(self) -> List[str]:
        """Get list of character's weak stats (12- points)"""
        return [
            stat for stat, value in self.__dict__.items()
            if isinstance(value, int) and value <= 12
        ]


@dataclass
class CharacterClassConfig:
    """Configuration for a character class"""
    mechanic: str
    base_stats: 'CharacterStats'
    primary_stat: str
    abilities: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate configuration after creation"""
        if self.primary_stat not in self.base_stats.__dict__:
            raise ValueError(f"Invalid primary stat: {self.primary_stat}")


@dataclass
class Character:
    """Character aggregate root entity"""
    id: str = ""
    name: str = ""
    class_type: Optional[CharacterClass] = None
    level: int = 1
    experience: int = 0
    stats: 'CharacterStats' = field(default_factory=CharacterStats)
    hp: int = 100
    max_hp: int = 100
    gold: int = 0
    inventory: List[str] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    created: bool = False
    visual_customization: Dict[str, str] = field(default_factory=dict)

    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.created and self.hp > 0

    def add_to_inventory(self, item: str) -> bool:
        """Add item to inventory with validation"""
        if not item or not item.strip():
            return False
        self.inventory.append(item.strip())
        return True

    def remove_from_inventory(self, item: str) -> bool:
        """Remove item from inventory"""
        try:
            self.inventory.remove(item)
            return True
        except ValueError:
            return False

    def level_up(self) -> bool:
        """Level up character with stat improvements"""
        if not self.created or self.level < 1:
            return False

        self.level += 1

        # Improve primary stat
        if self.class_type:
            primary_stat_value = self.stats.primary_stat_value(
                CHARACTER_CLASSES[self.class_type].primary_stat
            )
            primary_stat_value += 1

        return True

    def calculate_power_level(self) -> int:
        """Calculate character's total power level"""
        return self.stats.total_power()

    def __post_init__(self):
        """Post-initialization for dataclass"""
        # Set HP to 0 if not created
        if not self.created:
            self.hp = 0

    # BDD compatibility methods
    def get_class_stats(self, class_name: str) -> Optional[Dict]:
        """Get stats for specific class (BDD compatibility)"""
        try:
            character_class = self._parse_class_for_stats(class_name)
            if character_class in CHARACTER_CLASSES:
                config = CHARACTER_CLASSES[character_class]
                return {
                    "strength": config.base_stats.strength,
                    "dexterity": config.base_stats.dexterity,
                    "intelligence": config.base_stats.intelligence,
                    "wisdom": config.base_stats.wisdom,
                    "charisma": config.base_stats.charisma,
                    "constitution": config.base_stats.constitution
                }
        except (ValueError, AttributeError):
            pass
        return None

    def get_class_mechanic(self, class_name: str) -> Optional[str]:
        """Get mechanic for specific class (BDD compatibility)"""
        try:
            character_class = self._parse_class_for_stats(class_name)
            if character_class in CHARACTER_CLASSES:
                return CHARACTER_CLASSES[character_class].mechanic
        except (ValueError, AttributeError):
            pass
        return None

    def get_class_abilities(self, class_name: str) -> Optional[List[str]]:
        """Get abilities for specific class (BDD compatibility)"""
        try:
            character_class = self._parse_class_for_stats(class_name)
            if character_class in CHARACTER_CLASSES:
                return CHARACTER_CLASSES[character_class].abilities.copy()
        except (ValueError, AttributeError):
            pass
        return None

    def _parse_class_for_stats(self, class_name: str) -> 'CharacterClass':
        """Parse class name string to enum value (BDD compatibility)"""
        class_str = class_name.strip().lower()

        for char_class in CharacterClass:
            if char_class.value.lower() == class_str:
                return char_class

        raise ValueError(f"Unknown character class: {class_name}")

    @classmethod
    def get_all_character_classes(cls) -> List[str]:
        """Get list of all character classes (BDD compatibility)"""
        return [cls.value for cls in CharacterClass]


# Class configurations database
CHARACTER_CLASSES: Dict[CharacterClass, CharacterClassConfig] = {
    CharacterClass.WARRIOR: CharacterClassConfig(
        mechanic="Weapon Mastery",
        base_stats=CharacterStats(
            strength=17, dexterity=12, intelligence=10,
            wisdom=11, charisma=10, constitution=16
        ),
        primary_stat="strength",
        abilities=[
            "Power Strike", "Shield Bash", "Battle Cry", "Weapon Specialization",
            "Armor Training", "Combat Stance", "Whirlwind Attack",
            "Warrior's Resolve", "Weapon Throw", "Berserker Rage"
        ]
    ),
    CharacterClass.MAGE: CharacterClassConfig(
        mechanic="Arcane Spellcasting",
        base_stats=CharacterStats(
            strength=10, dexterity=12, intelligence=17,
            wisdom=15, charisma=12, constitution=12
        ),
        primary_stat="intelligence",
        abilities=[
            "Fireball", "Frost Armor", "Teleport", "Mana Shield",
            "Arcane Blast", "Spell Mastery", "Elemental Focus",
            "Mana Regeneration", "Time Warp", "Meteor Storm"
        ]
    ),
    CharacterClass.ROGUE: CharacterClassConfig(
        mechanic="Stealth and Critical Strikes",
        base_stats=CharacterStats(
            strength=12, dexterity=17, intelligence=11,
            wisdom=12, charisma=14, constitution=12
        ),
        primary_stat="dexterity",
        abilities=[
            "Stealth", "Backstab", "Lockpicking", "Disarm Traps",
            "Evasion", "Poison Blade", "Shadow Step", "Precise Targeting",
            "One Shot One Kill", "Shadow Assassination"
        ]
    ),
    # Adding a few more key classes for demonstration
    CharacterClass.CLERIC: CharacterClassConfig(
        mechanic="Divine Healing and Support",
        base_stats=CharacterStats(
            strength=12, dexterity=11, intelligence=13,
            wisdom=17, charisma=14, constitution=13
        ),
        primary_stat="wisdom",
        abilities=[
            "Heal", "Bless", "Cure Poison", "Resurrect",
            "Holy Light", "Divine Shield", "Turn Undead",
            "Group Heal", "Blessing of Protection", "Divine Intervention"
        ]
    ),
    CharacterClass.RANGER: CharacterClassConfig(
        mechanic="Wilderness Survival and Animal Companions",
        base_stats=CharacterStats(
            strength=13, dexterity=16, intelligence=12,
            wisdom=15, charisma=11, constitution=13
        ),
        primary_stat="dexterity",
        abilities=[
            "Animal Companion", "Track", "Wilderness Lore", "Archery",
            "Dual Wield", "Beast Taming", "Nature's Wrath",
            "Camouflage", "Hunt", "Pack Tactics"
        ]
    ),
    CharacterClass.PALADIN: CharacterClassConfig(
        mechanic="Divine Smite and Auras",
        base_stats=CharacterStats(
            strength=16, dexterity=11, intelligence=12,
            wisdom=14, charisma=16, constitution=15
        ),
        primary_stat="strength",
        abilities=[
            "Smite", "Lay on Hands", "Divine Sense", "Aura of Protection",
            "Divine Health", "Sacred Oath", "Crusader's Mantle",
            "Holy Avenger", "Righteous Cause", "Vindicator's Shield"
        ]
    )
}
