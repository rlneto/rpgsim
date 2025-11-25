"""
Character System for RPGSim
Implements character creation, classes, stats, and progression
"""

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


class Character:  # pylint: disable=too-many-instance-attributes
    """
    Represents a character in RPGSim with stats, abilities, and progression
    """

    # Class configurations with unique mechanics and stat distributions
    CLASS_CONFIG = {
        CharacterClass.WARRIOR: {
            "mechanic": "Weapon Mastery",
            "base_stats": {
                "strength": 17,
                "dexterity": 12,
                "intelligence": 10,
                "wisdom": 11,
                "charisma": 10,
                "constitution": 16,
            },
            "primary_stat": "strength",
            "abilities": [
                "Power Strike",
                "Shield Bash",
                "Battle Cry",
                "Weapon Specialization",
                "Armor Training",
                "Combat Stance",
                "Whirlwind Attack",
                "Warrior's Resolve",
                "Weapon Throw",
                "Berserker Rage",
            ],
        },
        CharacterClass.MAGE: {
            "mechanic": "Arcane Spellcasting",
            "base_stats": {
                "strength": 10,
                "dexterity": 12,
                "intelligence": 17,
                "wisdom": 15,
                "charisma": 12,
                "constitution": 12,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Fireball",
                "Frost Armor",
                "Teleport",
                "Mana Shield",
                "Arcane Blast",
                "Spell Mastery",
                "Elemental Focus",
                "Mana Regeneration",
                "Time Warp",
                "Meteor Storm",
            ],
        },
        CharacterClass.ROGUE: {
            "mechanic": "Stealth and Critical Strikes",
            "base_stats": {
                "strength": 12,
                "dexterity": 17,
                "intelligence": 11,
                "wisdom": 12,
                "charisma": 14,
                "constitution": 13,
            },
            "primary_stat": "dexterity",
            "abilities": [
                "Stealth",
                "Backstab",
                "Lockpicking",
                "Disarm Traps",
                "Evasion",
                "Poison Blade",
                "Shadow Step",
                "Critical Strike",
                "Thievery",
                "Assassinate",
            ],
        },
        CharacterClass.CLERIC: {
            "mechanic": "Divine Healing",
            "base_stats": {
                "strength": 13,
                "dexterity": 10,
                "intelligence": 12,
                "wisdom": 17,
                "charisma": 15,
                "constitution": 14,
            },
            "primary_stat": "wisdom",
            "abilities": [
                "Heal",
                "Divine Shield",
                "Turn Undead",
                "Bless",
                "Cure Disease",
                "Resurrection",
                "Divine Light",
                "Holy Strike",
                "Group Heal",
                "Sanctuary",
            ],
        },
        CharacterClass.RANGER: {
            "mechanic": "Beast Companion",
            "base_stats": {
                "strength": 14,
                "dexterity": 16,
                "intelligence": 11,
                "wisdom": 15,
                "charisma": 12,
                "constitution": 14,
            },
            "primary_stat": "dexterity",
            "abilities": [
                "Animal Companion",
                "Track",
                "Precise Shot",
                "Nature Sense",
                "Beast Training",
                "Dual Wield",
                "Survival Instinct",
                "Rapid Fire",
                "Camouflage",
                "Call of the Wild",
            ],
        },
        CharacterClass.PALADIN: {
            "mechanic": "Holy Smite",
            "base_stats": {
                "strength": 16,
                "dexterity": 11,
                "intelligence": 11,
                "wisdom": 15,
                "charisma": 16,
                "constitution": 15,
            },
            "primary_stat": "strength",
            "abilities": [
                "Holy Strike",
                "Divine Protection",
                "Lay on Hands",
                "Aura of Courage",
                "Holy Aura",
                "Crusader Strike",
                "Divine Shield",
                "Blessing of Light",
                "Sacred Oath",
                "Celestial Mount",
            ],
        },
        CharacterClass.WARLOCK: {
            "mechanic": "Pact Magic",
            "base_stats": {
                "strength": 10,
                "dexterity": 12,
                "intelligence": 16,
                "wisdom": 12,
                "charisma": 17,
                "constitution": 12,
            },
            "primary_stat": "charisma",
            "abilities": [
                "Eldritch Blast",
                "Pact Boon",
                "Dark One's Blessing",
                "Otherworldly Patron",
                "Hex",
                "Soul Sacrifice",
                "Demoniac Pacts",
                "Shadow Magic",
                "Void Walker",
                "Demonic Power",
            ],
        },
        CharacterClass.DRUID: {
            "mechanic": "Shape-shifting",
            "base_stats": {
                "strength": 12,
                "dexterity": 13,
                "intelligence": 12,
                "wisdom": 17,
                "charisma": 11,
                "constitution": 14,
            },
            "primary_stat": "wisdom",
            "abilities": [
                "Wild Shape",
                "Nature's Wrath",
                "Healing Touch",
                "Entangle",
                "Regeneration",
                "Elemental Form",
                "Commune with Nature",
                "Forest Guardian",
                "Storm Call",
                "World Tree",
            ],
        },
        CharacterClass.MONK: {
            "mechanic": "Ki Energy",
            "base_stats": {
                "strength": 14,
                "dexterity": 16,
                "intelligence": 11,
                "wisdom": 15,
                "charisma": 12,
                "constitution": 15,
            },
            "primary_stat": "dexterity",
            "abilities": [
                "Ki Strike",
                "Stunning Strike",
                "Flurry of Blows",
                "Dodge",
                "Deflect Arrows",
                "Perfect Self",
                "Quivering Palm",
                "Wholeness of Body",
                "Diamond Soul",
                "Timeless Body",
            ],
        },
        CharacterClass.BARBARIAN: {
            "mechanic": "Rage",
            "base_stats": {
                "strength": 17,
                "dexterity": 13,
                "intelligence": 10,
                "wisdom": 11,
                "charisma": 11,
                "constitution": 17,
            },
            "primary_stat": "strength",
            "abilities": [
                "Rage",
                "Unarmored Defense",
                "Reckless Attack",
                "Danger Sense",
                "Primal Champion",
                "Totemic Warrior",
                "Feral Instinct",
                "Mindless Rage",
                "Brutal Critical",
                "Primal Might",
            ],
        },
        CharacterClass.BARD: {
            "mechanic": "Inspiration",
            "base_stats": {
                "strength": 10,
                "dexterity": 13,
                "intelligence": 13,
                "wisdom": 12,
                "charisma": 17,
                "constitution": 12,
            },
            "primary_stat": "charisma",
            "abilities": [
                "Inspiration",
                "Bardic Music",
                "Performance",
                "Countercharm",
                "Fascinate",
                "Suggestion",
                "Enthralling Performance",
                "Magical Secrets",
                "Superior Inspiration",
                "Song of Rest",
            ],
        },
        CharacterClass.SORCERER: {
            "mechanic": "Innate Magic",
            "base_stats": {
                "strength": 10,
                "dexterity": 12,
                "intelligence": 15,
                "wisdom": 13,
                "charisma": 17,
                "constitution": 11,
            },
            "primary_stat": "charisma",
            "abilities": [
                "Innate Spellcasting",
                "Metamagic",
                "Sorcery Points",
                "Font of Magic",
                "Spell Evocation",
                "Quickened Spell",
                "Twinned Spell",
                "Heightened Spell",
                "Subtle Spell",
                "Magical Aptitude",
            ],
        },
        CharacterClass.FIGHTER: {
            "mechanic": "Combat Specialization",
            "base_stats": {
                "strength": 16,
                "dexterity": 14,
                "intelligence": 11,
                "wisdom": 12,
                "charisma": 11,
                "constitution": 15,
            },
            "primary_stat": "strength",
            "abilities": [
                "Fighting Style",
                "Second Wind",
                "Action Surge",
                "Martial Archetype",
                "Battle Master",
                "Combat Maneuver",
                "Disarming Attack",
                "Trip Attack",
                "Grappling Strike",
                "Combat Rally",
            ],
        },
        CharacterClass.NECROMANCER: {
            "mechanic": "Undead Control",
            "base_stats": {
                "strength": 10,
                "dexterity": 11,
                "intelligence": 17,
                "wisdom": 12,
                "charisma": 13,
                "constitution": 12,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Animate Dead",
                "Necrotic Energy",
                "Life Drain",
                "Undead Servants",
                "Death Touch",
                "Bone Armor",
                "Soul Harvest",
                "Corpse Explosion",
                "Lich Transformation",
                "Army of the Dead",
            ],
        },
        CharacterClass.ILLUSIONIST: {
            "mechanic": "Mind Tricks",
            "base_stats": {
                "strength": 10,
                "dexterity": 12,
                "intelligence": 17,
                "wisdom": 13,
                "charisma": 14,
                "constitution": 11,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Illusion",
                "Invisibility",
                "Mirror Image",
                "Disguise Self",
                "Phantasm",
                "Mind Cloud",
                "Telepathy",
                "Dream Walking",
                "Reality Shift",
                "Master Illusion",
            ],
        },
        CharacterClass.ALCHEMIST: {
            "mechanic": "Potion Brewing",
            "base_stats": {
                "strength": 11,
                "dexterity": 13,
                "intelligence": 17,
                "wisdom": 12,
                "charisma": 11,
                "constitution": 15,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Potion Brewing",
                "Transmutation",
                "Formula Crafting",
                "Explosives",
                "Healing Elixirs",
                "Poison Master",
                "Enhanced Alchemy",
                "Chemical Warfare",
                "Philosopher's Stone",
                "Master Brewer",
            ],
        },
        CharacterClass.BERSERKER: {
            "mechanic": "Battle Fury",
            "base_stats": {
                "strength": 18,
                "dexterity": 13,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 11,
                "constitution": 17,
            },
            "primary_stat": "strength",
            "abilities": [
                "Battle Fury",
                "Bloodlust",
                "Frenzied Assault",
                "Pain Resistance",
                "War Cry",
                "Unstoppable Force",
                "Blood Rage",
                "Destruction Frenzy",
                "Apocalypse Strike",
                "Final Stand",
            ],
        },
        CharacterClass.ASSASSIN: {
            "mechanic": "Instant Kill Techniques",
            "base_stats": {
                "strength": 12,
                "dexterity": 18,
                "intelligence": 12,
                "wisdom": 11,
                "charisma": 13,
                "constitution": 13,
            },
            "primary_stat": "dexterity",
            "abilities": [
                "Instant Kill",
                "Shadow Strike",
                "Death Mark",
                "Silent Kill",
                "Critical Weakness",
                "Poison Master",
                "Stealth Mastery",
                "Precise Targeting",
                "One Shot One Kill",
                "Shadow Assassination",
            ],
        },
        CharacterClass.HEALER: {
            "mechanic": "Restoration Magic",
            "base_stats": {
                "strength": 11,
                "dexterity": 10,
                "intelligence": 13,
                "wisdom": 18,
                "charisma": 14,
                "constitution": 13,
            },
            "primary_stat": "wisdom",
            "abilities": [
                "Major Heal",
                "Group Restoration",
                "Cleanse",
                "Resurrect Allies",
                "Divine Protection",
                "Mass Healing",
                "Life Channel",
                "Purify",
                "Guardian Angel",
                "Miracle Worker",
            ],
        },
        CharacterClass.SUMMONER: {
            "mechanic": "Creature Summoning",
            "base_stats": {
                "strength": 10,
                "dexterity": 11,
                "intelligence": 17,
                "wisdom": 14,
                "charisma": 15,
                "constitution": 12,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Summon Creature",
                "Bind Summoned",
                "Creature Control",
                "Portal Magic",
                "Multiple Summons",
                "Planar Allies",
                "Creature Evolution",
                "Master Summoner",
                "Army Creation",
                "Dimensional Rift",
            ],
        },
        CharacterClass.SHAPESHIFTER: {
            "mechanic": "Form Transformation",
            "base_stats": {
                "strength": 13,
                "dexterity": 15,
                "intelligence": 12,
                "wisdom": 16,
                "charisma": 10,
                "constitution": 15,
            },
            "primary_stat": "wisdom",
            "abilities": [
                "Transform Beast",
                "Transform Humanoid",
                "Transform Elemental",
                "Adapt Form",
                "Hybrid Form",
                "Perfect Mimicry",
                "Form Mastery",
                "Rapid Transformation",
                "Ultimate Form",
                "Primordial Shape",
            ],
        },
        CharacterClass.ELEMENTALIST: {
            "mechanic": "Element Control",
            "base_stats": {
                "strength": 11,
                "dexterity": 12,
                "intelligence": 18,
                "wisdom": 14,
                "charisma": 11,
                "constitution": 13,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Fire Control",
                "Water Control",
                "Earth Control",
                "Air Control",
                "Lightning Strike",
                "Elemental Fusion",
                "Elemental Shield",
                "Storm Calling",
                "Elemental Mastery",
                "Apocalypse Elements",
            ],
        },
        CharacterClass.NINJA: {
            "mechanic": "Shadow Arts",
            "base_stats": {
                "strength": 12,
                "dexterity": 18,
                "intelligence": 11,
                "wisdom": 13,
                "charisma": 12,
                "constitution": 13,
            },
            "primary_stat": "dexterity",
            "abilities": [
                "Shadow Clone",
                "Vanish",
                "Ninjutsu",
                "Smoke Bomb",
                "Kunai Throw",
                "Shadow Walk",
                "Assassination Arts",
                "Stealth Mastery",
                "Perfect Strike",
                "Dark Vision",
            ],
        },
        CharacterClass.DEVELOPER: {
            "mechanic": "Code Manipulation",
            "base_stats": {
                "strength": 11,
                "dexterity": 12,
                "intelligence": 18,
                "wisdom": 15,
                "charisma": 10,
                "constitution": 12,
            },
            "primary_stat": "intelligence",
            "abilities": [
                "Debug Code",
                "System Optimization",
                "API Integration",
                "Database Query",
                "Security Audit",
                "Code Generation",
                "Bug Detection",
                "Performance Tuning",
                "System Architecture",
                "Debug Mode",
            ],
        },
    }

    def __init__(self):
        """Initialize empty character"""
        self.name: str = ""
        self.class_type: Optional[CharacterClass] = None
        self.level: int = 1
        self.experience: int = 0
        self.stats: Dict[str, int] = {}
        self.inventory: List[str] = []
        self.abilities: List[str] = []
        self.created: bool = False
        self.visual_customization: Dict[str, str] = {}

    def create_character(self, name: str, class_type: str) -> bool:
        """
        Create a new character with specified name and class

        Args:
            name: Character name
            class_type: Character class name or enum value

        Returns:
            True if character created successfully, False otherwise
        """
        try:
            # Parse class input (accept string or enum)
            if isinstance(class_type, str):
                class_type = self._parse_class_string(class_type)

            if class_type not in CharacterClass:
                return False

            if not name or len(name.strip()) == 0:
                return False

            self.name = name.strip()
            self.class_type = class_type
            self.level = 1
            self.experience = 0

            # Set class-specific stats
            class_config = self.CLASS_CONFIG[class_type]
            self.stats = class_config["base_stats"].copy()

            # Set class-specific abilities
            self.abilities = class_config["abilities"].copy()

            # Initialize inventory with basic items
            self.inventory = ["Basic Clothes", "Travel Rations"]

            # Set default visual customization
            self.visual_customization = {
                "hair_color": "brown",
                "eye_color": "blue",
                "skin_tone": "fair",
                "build": "medium",
            }

            self.created = True
            return True

        except (ValueError, TypeError, AttributeError, KeyError):
            return False

    def _parse_class_string(self, class_string: str) -> Optional[CharacterClass]:
        """Parse string class name to CharacterClass enum"""
        class_mapping = {
            "warrior": CharacterClass.WARRIOR,
            "mage": CharacterClass.MAGE,
            "rogue": CharacterClass.ROGUE,
            "cleric": CharacterClass.CLERIC,
            "ranger": CharacterClass.RANGER,
            "paladin": CharacterClass.PALADIN,
            "warlock": CharacterClass.WARLOCK,
            "druid": CharacterClass.DRUID,
            "monk": CharacterClass.MONK,
            "barbarian": CharacterClass.BARBARIAN,
            "bard": CharacterClass.BARD,
            "sorcerer": CharacterClass.SORCERER,
            "fighter": CharacterClass.FIGHTER,
            "necromancer": CharacterClass.NECROMANCER,
            "illusionist": CharacterClass.ILLUSIONIST,
            "alchemist": CharacterClass.ALCHEMIST,
            "berserker": CharacterClass.BERSERKER,
            "assassin": CharacterClass.ASSASSIN,
            "healer": CharacterClass.HEALER,
            "summoner": CharacterClass.SUMMONER,
            "shapeshifter": CharacterClass.SHAPESHIFTER,
            "elementalist": CharacterClass.ELEMENTALIST,
            "ninja": CharacterClass.NINJA,
            "developer": CharacterClass.DEVELOPER,
        }

        return class_mapping.get(class_string.lower())

    def get_class_stats(self, class_name: str) -> Optional[Dict[str, int]]:
        """
        Get the stat distribution for a specific class

        Args:
            class_name: Name of the class

        Returns:
            Dictionary of stats or None if class doesn't exist
        """
        try:
            if isinstance(class_name, str):
                class_type = self._parse_class_string(class_name)
            else:
                class_type = class_name

            if class_type and class_type in self.CLASS_CONFIG:
                return self.CLASS_CONFIG[class_type]["base_stats"].copy()
            return None
        except (ValueError, TypeError, AttributeError, KeyError):
            return None

    def get_class_mechanic(self, class_name: str) -> Optional[str]:
        """
        Get the unique mechanic for a specific class

        Args:
            class_name: Name of the class

        Returns:
            Mechanic name or None if class doesn't exist
        """
        try:
            if isinstance(class_name, str):
                class_type = self._parse_class_string(class_name)
            else:
                class_type = class_name

            if class_type and class_type in self.CLASS_CONFIG:
                return self.CLASS_CONFIG[class_type]["mechanic"]
            return None
        except (ValueError, TypeError, AttributeError, KeyError):
            return None

    def get_class_abilities(self, class_name: str) -> Optional[List[str]]:
        """
        Get the abilities for a specific class

        Args:
            class_name: Name of the class

        Returns:
            List of abilities or None if class doesn't exist
        """
        try:
            if isinstance(class_name, str):
                class_type = self._parse_class_string(class_name)
            else:
                class_type = class_name

            if class_type and class_type in self.CLASS_CONFIG:
                return self.CLASS_CONFIG[class_type]["abilities"].copy()
            return None
        except (ValueError, TypeError, AttributeError, KeyError):
            return None

    def get_all_classes(self) -> List[str]:
        """
        Get list of all available character classes

        Returns:
            List of class names
        """
        return [cls.value for cls in CharacterClass]

    def calculate_power_level(self) -> int:
        """
        Calculate character's total power level based on stats

        Returns:
            Total power level (sum of all stats)
        """
        return sum(self.stats.values())

    def get_strengths_and_weaknesses(self) -> Dict[str, List[str]]:
        """
        Get character's strengths and weaknesses based on stats

        Returns:
            Dictionary with 'strengths' and 'weaknesses' lists
        """
        strengths = []
        weaknesses = []

        for stat_name, stat_value in self.stats.items():
            if stat_value >= 15:
                strengths.append(stat_name)
            elif stat_value <= 12:
                weaknesses.append(stat_name)

        return {"strengths": strengths, "weaknesses": weaknesses}

    def add_to_inventory(self, item: str) -> bool:
        """
        Add item to character inventory

        Args:
            item: Item name to add

        Returns:
            True if item added successfully
        """
        try:
            if item and len(item.strip()) > 0:
                self.inventory.append(item.strip())
                return True
            return False
        except (ValueError, TypeError, AttributeError, KeyError):
            return False

    def remove_from_inventory(self, item: str) -> bool:
        """
        Remove item from character inventory

        Args:
            item: Item name to remove

        Returns:
            True if item removed successfully
        """
        try:
            if item in self.inventory:
                self.inventory.remove(item)
                return True
            return False
        except (ValueError, TypeError, AttributeError, KeyError):
            return False

    def get_inventory_count(self) -> int:
        """
        Get number of items in inventory

        Returns:
            Number of items
        """
        return len(self.inventory)

    def level_up(self) -> bool:
        """
        Level up character and improve stats

        Returns:
            True if level up successful
        """
        try:
            if self.level >= 1:
                self.level += 1

                # Improve primary stat by 1
                if self.class_type:
                    primary_stat = self.CLASS_CONFIG[self.class_type]["primary_stat"]
                    self.stats[primary_stat] += 1

                # Improve other stats occasionally
                for stat in self.stats:
                    if stat != primary_stat and self.level % 2 == 0:
                        self.stats[stat] += 1

                return True
            return False
        except (ValueError, TypeError, AttributeError, KeyError):
            return False

    def set_visual_customization(self, customization_type: str, value: str) -> bool:
        """
        Set visual customization option

        Args:
            customization_type: Type of customization (hair_color, eye_color, etc.)
            value: Customization value

        Returns:
            True if customization set successfully
        """
        try:
            if customization_type in ["hair_color", "eye_color", "skin_tone", "build"] and value:
                self.visual_customization[customization_type] = value.strip()
                return True
            return False
        except (ValueError, TypeError, AttributeError, KeyError):
            return False


# Class-level utility functions
def get_all_character_classes() -> List[str]:
    """
    Get list of all available character classes

    Returns:
        List of class names
    """
    return [cls.value for cls in CharacterClass]


def get_class_balance_stats() -> Dict[str, int]:
    """
    Calculate power levels for all classes to verify balance

    Returns:
        Dictionary mapping class names to power levels
    """
    balance_stats = {}

    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            stats = Character.CLASS_CONFIG[char_class]["base_stats"]
            power = sum(stats.values())
            balance_stats[char_class.value] = power

    return balance_stats


def validate_class_balance() -> bool:
    """
    Validate that all classes are balanced within 15% power difference

    Returns:
        True if classes are balanced, False otherwise
    """
    balance_stats = get_class_balance_stats()

    if not balance_stats:
        return False

    max_power = max(balance_stats.values())
    min_power = min(balance_stats.values())

    # Calculate ratio of difference
    balance_ratio = (max_power - min_power) / min_power if min_power > 0 else 0

    # Classes should be within 15% power difference
    return balance_ratio <= 0.15


def verify_unique_mechanics() -> bool:
    """
    Verify that all classes have unique mechanics

    Returns:
        True if all mechanics are unique, False otherwise
    """
    mechanics = []

    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            mechanic = Character.CLASS_CONFIG[char_class]["mechanic"]
            mechanics.append(mechanic)

    # Check if all mechanics are unique
    return len(set(mechanics)) == len(mechanics)


def verify_minimum_abilities() -> bool:
    """
    Verify that all classes have at least 10 unique abilities

    Returns:
        True if all classes meet ability requirements, False otherwise
    """
    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            abilities = Character.CLASS_CONFIG[char_class]["abilities"]
            if len(abilities) < 10:
                return False

            # Check for uniqueness within class
            if len(set(abilities)) != len(abilities):
                return False

    return True
