"""
Core constants for RPGSim
Optimized for LLM agent development with explicit, deterministic values
"""

from typing import Dict, Any
from core.models import (
    CharacterStats,
)

# [CONST_001] - Character class default stats
# Explicit, deterministic mapping for agent understanding
DEFAULT_CHARACTER_STATS: Dict[str, CharacterStats] = {
    "warrior": CharacterStats(
        strength=15,
        dexterity=10,
        intelligence=8,
        wisdom=10,
        charisma=8,
        constitution=14,
    ),
    "mage": CharacterStats(
        strength=8,
        dexterity=12,
        intelligence=16,
        wisdom=14,
        charisma=10,
        constitution=8,
    ),
    "rogue": CharacterStats(
        strength=10,
        dexterity=16,
        intelligence=12,
        wisdom=10,
        charisma=12,
        constitution=8,
    ),
    "cleric": CharacterStats(
        strength=10,
        dexterity=10,
        intelligence=10,
        wisdom=16,
        charisma=12,
        constitution=12,
    ),
    "ranger": CharacterStats(
        strength=12,
        dexterity=14,
        intelligence=10,
        wisdom=12,
        charisma=8,
        constitution=10,
    ),
    "paladin": CharacterStats(
        strength=14,
        dexterity=8,
        intelligence=8,
        wisdom=12,
        charisma=12,
        constitution=14,
    ),
    "warlock": CharacterStats(
        strength=8,
        dexterity=12,
        intelligence=14,
        wisdom=10,
        charisma=16,
        constitution=8,
    ),
    "druid": CharacterStats(
        strength=10,
        dexterity=10,
        intelligence=10,
        wisdom=16,
        charisma=8,
        constitution=12,
    ),
    "monk": CharacterStats(
        strength=12,
        dexterity=14,
        intelligence=10,
        wisdom=12,
        charisma=8,
        constitution=12,
    ),
    "barbarian": CharacterStats(
        strength=16, dexterity=10, intelligence=7, wisdom=8, charisma=7, constitution=15
    ),
    "bard": CharacterStats(
        strength=8,
        dexterity=12,
        intelligence=12,
        wisdom=10,
        charisma=16,
        constitution=10,
    ),
    "sorcerer": CharacterStats(
        strength=6,
        dexterity=10,
        intelligence=14,
        wisdom=10,
        charisma=14,
        constitution=8,
    ),
    "fighter": CharacterStats(
        strength=14,
        dexterity=12,
        intelligence=10,
        wisdom=8,
        charisma=8,
        constitution=12,
    ),
    "necromancer": CharacterStats(
        strength=6,
        dexterity=10,
        intelligence=16,
        wisdom=12,
        charisma=10,
        constitution=8,
    ),
    "illusionist": CharacterStats(
        strength=6,
        dexterity=12,
        intelligence=16,
        wisdom=10,
        charisma=12,
        constitution=8,
    ),
    "alchemist": CharacterStats(
        strength=8,
        dexterity=10,
        intelligence=14,
        wisdom=12,
        charisma=10,
        constitution=10,
    ),
    "berserker": CharacterStats(
        strength=17, dexterity=8, intelligence=6, wisdom=6, charisma=6, constitution=16
    ),
    "assassin": CharacterStats(
        strength=10,
        dexterity=16,
        intelligence=12,
        wisdom=8,
        charisma=10,
        constitution=8,
    ),
    "healer": CharacterStats(
        strength=8,
        dexterity=10,
        intelligence=10,
        wisdom=16,
        charisma=14,
        constitution=10,
    ),
    "summoner": CharacterStats(
        strength=6,
        dexterity=10,
        intelligence=16,
        wisdom=12,
        charisma=12,
        constitution=8,
    ),
    "shapeshifter": CharacterStats(
        strength=10,
        dexterity=12,
        intelligence=10,
        wisdom=12,
        charisma=10,
        constitution=12,
    ),
    "elementalist": CharacterStats(
        strength=8,
        dexterity=10,
        intelligence=16,
        wisdom=12,
        charisma=10,
        constitution=8,
    ),
    "ninja": CharacterStats(
        strength=12,
        dexterity=16,
        intelligence=10,
        wisdom=8,
        charisma=8,
        constitution=10,
    ),
}

# [CONST_002] - Default abilities by character class
# Explicit mapping for agent understanding
DEFAULT_ABILITIES: Dict[str, list] = {
    "warrior": ["Attack", "Defend", "Power Strike", "Shield Bash", "Intimidate"],
    "mage": [
        "Attack",
        "Defend",
        "Fireball",
        "Magic Missile",
        "Teleport",
        "Mana Shield",
    ],
    "rogue": ["Attack", "Defend", "Backstab", "Pick Lock", "Stealth", "Poison Blade"],
    "cleric": ["Attack", "Defend", "Heal", "Turn Undead", "Bless", "Holy Light"],
    "ranger": [
        "Attack",
        "Defend",
        "Precise Shot",
        "Track",
        "Animal Companion",
        "Nature's Call",
    ],
    "paladin": [
        "Attack",
        "Defend",
        "Holy Strike",
        "Divine Shield",
        "Lay on Hands",
        "Aura of Courage",
    ],
    "warlock": [
        "Attack",
        "Defend",
        "Eldritch Blast",
        "Curse",
        "Pact Boon",
        "Life Drain",
    ],
    "druid": ["Attack", "Defend", "Wild Shape", "Entangle", "Heal", "Call Lightning"],
    "monk": [
        "Attack",
        "Defend",
        "Flurry of Blows",
        "Stunning Strike",
        "Ki Strike",
        "Deflect Missiles",
    ],
    "barbarian": [
        "Attack",
        "Defend",
        "Rage",
        "Reckless Attack",
        "Unarmed Strike",
        "Toughness",
    ],
    "bard": ["Attack", "Defend", "Inspire", "Charm", "Counter Song", "Enthrall"],
    "sorcerer": [
        "Attack",
        "Defend",
        "Spell Surge",
        "Metamagic",
        "Quick Spell",
        "Arcane Power",
    ],
    "fighter": [
        "Attack",
        "Defend",
        "Power Attack",
        "Cleave",
        "Weapon Focus",
        "Combat Expertise",
    ],
    "necromancer": [
        "Attack",
        "Defend",
        "Raise Dead",
        "Curse",
        "Life Drain",
        "Fear Aura",
    ],
    "illusionist": [
        "Attack",
        "Defend",
        "Create Illusion",
        "Invisibility",
        "Phantasm",
        "Confusion",
    ],
    "alchemist": [
        "Attack",
        "Defend",
        "Brew Potion",
        "Throw Bomb",
        "Mutate",
        "Healing Elixir",
    ],
    "berserker": ["Attack", "Defend", "Frenzy", "Blood Rage", "Berserk", "Unstoppable"],
    "assassin": [
        "Attack",
        "Defend",
        "Stealth Kill",
        "Poison",
        "Shadow Walk",
        "Smoke Bomb",
    ],
    "healer": [
        "Attack",
        "Defend",
        "Greater Heal",
        "Regeneration",
        "Cure Disease",
        "Resurrect",
    ],
    "summoner": [
        "Attack",
        "Defend",
        "Summon Demon",
        "Summon Angel",
        "Summon Elemental",
        "Bind Creature",
    ],
    "shapeshifter": [
        "Attack",
        "Defend",
        "Wolf Form",
        "Bear Form",
        "Eagle Form",
        "Aquatic Form",
    ],
    "elementalist": [
        "Attack",
        "Defend",
        "Fire Strike",
        "Ice Blast",
        "Lightning Bolt",
        "Earthquake",
    ],
    "ninja": [
        "Attack",
        "Defend",
        "Shadow Clone",
        "Smoke Bomb",
        "Throwing Stars",
        "Vanish",
    ],
}

# [CONST_003] - Base HP by character class
# Explicit mapping for deterministic HP calculation
BASE_HP_BY_CLASS: Dict[str, int] = {
    "warrior": 12,
    "mage": 6,
    "rogue": 8,
    "cleric": 10,
    "ranger": 9,
    "paladin": 11,
    "warlock": 7,
    "druid": 9,
    "monk": 10,
    "barbarian": 14,
    "bard": 8,
    "sorcerer": 6,
    "fighter": 10,
    "necromancer": 6,
    "illusionist": 6,
    "alchemist": 7,
    "berserker": 15,
    "assassin": 8,
    "healer": 9,
    "summoner": 6,
    "shapeshifter": 10,
    "elementalist": 6,
    "ninja": 8,
}

# [CONST_004] - Damage multipliers by character class
# Explicit mapping for deterministic damage calculation
DAMAGE_MULTIPLIERS: Dict[str, float] = {
    "warrior": 1.5,
    "mage": 1.0,
    "rogue": 1.3,
    "cleric": 1.1,
    "ranger": 1.2,
    "paladin": 1.4,
    "warlock": 1.1,
    "druid": 1.0,
    "monk": 1.1,
    "barbarian": 1.6,
    "bard": 0.9,
    "sorcerer": 1.0,
    "fighter": 1.3,
    "necromancer": 1.0,
    "illusionist": 0.8,
    "alchemist": 0.9,
    "berserker": 1.7,
    "assassin": 1.4,
    "healer": 0.8,
    "summoner": 1.0,
    "shapeshifter": 1.0,
    "elementalist": 1.1,
    "ninja": 1.2,
}

# [CONST_005] - Stat increases per level by character class
# Explicit mapping for deterministic stat progression
STAT_INCREASES: Dict[str, CharacterStats] = {
    "warrior": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "mage": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "rogue": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "cleric": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "ranger": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "paladin": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "warlock": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "druid": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "monk": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "barbarian": CharacterStats(
        strength=2, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=2
    ),
    "bard": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "sorcerer": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "fighter": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "necromancer": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "illusionist": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "alchemist": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "berserker": CharacterStats(
        strength=2, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=2
    ),
    "assassin": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "healer": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "summoner": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "shapeshifter": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "elementalist": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
    "ninja": CharacterStats(
        strength=1, dexterity=1, intelligence=1, wisdom=1, charisma=1, constitution=1
    ),
}

# [CONST_006] - Ability learning schedule
# Explicit mapping for deterministic ability acquisition
ABILITY_LEARNING_SCHEDULE: Dict[str, Dict[int, list]] = {
    "warrior": {
        5: ["Whirlwind Attack"],
        10: ["Battle Cry"],
        15: ["Heroic Strike"],
        20: ["Blade Storm"],
        25: ["Warrior's Resolve"],
        30: ["Cleave"],
        35: ["Berserker Rage"],
        40: ["Final Stand"],
        50: ["Supreme Warrior"],
    },
    "mage": {
        5: ["Lightning Bolt"],
        10: ["Fire Shield"],
        15: ["Chain Lightning"],
        20: ["Meteor Strike"],
        25: ["Time Warp"],
        30: ["Arcane Power"],
        35: ["Disintegrate"],
        40: ["Ritual of Power"],
        50: ["Archmage"],
    },
    "rogue": {
        5: ["Sneak Attack"],
        10: ["Evasion"],
        15: ["Shadow Strike"],
        20: ["Assassinate"],
        25: ["Cloak of Shadows"],
        30: ["Death Strike"],
        35: ["Vanish"],
        40: ["Silent Death"],
        50: ["Shadow Master"],
    },
    # Add other classes as needed
}

# [CONST_007] - Game configuration constants
# Explicit configuration for agent understanding
GAME_CONFIG: Dict[str, Any] = {
    "max_character_level": 100,
    "max_stat_value": 20,
    "min_stat_value": 1,
    "max_character_name_length": 50,
    "min_character_name_length": 1,
    "starting_gold": 100,
    "max_inventory_size": 50,
    "max_abilities": 20,
    "experience_formula_multiplier": 100,
    "experience_formula_exponent": 1.5,
    "combat_damage_cap": 1000,
    "max_gold": 1000000,
    "max_experience": 1000000,
    "min_character_level": 1,
}

# [CONST_008] - UI constants
# Explicit UI configuration for agent understanding
UI_CONFIG: Dict[str, Any] = {
    "terminal_width": 80,
    "terminal_height": 24,
    "border_style": "single",
    "title_color": "cyan",
    "success_color": "green",
    "error_color": "red",
    "warning_color": "yellow",
    "info_color": "white",
    "menu_highlight_color": "blue",
    "stats_display_format": "table",
    "combat_log_max_entries": 100,
    "menu_max_items": 10,
}

# [CONST_009] - Validation constants
# Explicit validation rules for agent understanding
VALIDATION_CONFIG: Dict[str, Any] = {
    "valid_name_characters": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '-",
    "invalid_name_patterns": ["  ", "  "],  # Double spaces, leading/trailing spaces
    "valid_id_characters": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-",
    "min_character_name_length": 1,
    "max_character_name_length": 50,
    "max_item_name_length": 100,
    "max_item_description_length": 500,
    "max_quest_name_length": 100,
    "max_quest_description_length": 1000,
    "max_location_name_length": 100,
    "max_location_description_length": 500,
}

# [CONST_010] - Performance constants
# Explicit performance targets for agent understanding
PERFORMANCE_CONFIG: Dict[str, Any] = {
    "max_test_execution_time": 1.0,  # seconds
    "max_test_suite_time": 5.0,  # seconds
    "max_character_creation_time": 0.1,  # seconds
    "max_combat_calculation_time": 0.01,  # seconds
    "max_save_load_time": 1.0,  # seconds
    "max_ui_render_time": 0.1,  # seconds
    "functions_per_hour_target": 10,
    "test_generation_per_hour_target": 5,
    "error_rate_target": 0.08,  # 8%
    "code_generation_success_rate_target": 0.95,  # 95%
}

# [CONST_011] - File path constants
# Explicit file paths for agent understanding
FILE_PATHS: Dict[str, str] = {
    "data_directory": "data",
    "saves_directory": "saves",
    "logs_directory": "logs",
    "characters_file": "data/characters.json",
    "items_file": "data/items.json",
    "quests_file": "data/quests.json",
    "enemies_file": "data/enemies.json",
    "locations_file": "data/locations.json",
    "config_file": "config.json",
    "game_log_file": "logs/game.log",
    "error_log_file": "logs/error.log",
}

# [CONST_012] - Error message constants
# Explicit error messages for agent understanding
ERROR_MESSAGES: Dict[str, str] = {
    "character_name_empty": "Character name cannot be empty",
    "character_name_too_long": (
        f"Character name cannot exceed {GAME_CONFIG['max_character_name_length']} characters"
    ),
    "character_name_invalid_chars": (
        "Character name can only contain letters, numbers, spaces, hyphens, and apostrophes"
    ),
    "character_name_double_spaces": "Character name cannot contain consecutive spaces",
    "character_name_leading_trailing_spaces": "Character name cannot start or end with spaces",
    "character_class_invalid": "Invalid character class",
    "character_level_too_low": (
        f"Character level must be at least {GAME_CONFIG['min_character_level']}"
    ),
    "character_level_too_high": (
        f"Character level cannot exceed {GAME_CONFIG['max_character_level']}"
    ),
    "character_hp_negative": "Character HP cannot be negative",
    "character_hp_exceeds_max": "Character HP cannot exceed maximum HP",
    "character_max_hp_negative": "Character max HP must be positive",
    "character_gold_negative": "Character gold cannot be negative",
    "character_insufficient_gold": "Insufficient gold",
    "character_experience_negative": "Character experience cannot be negative",
    "character_defeated": "Character is defeated",
    "damage_negative": "Damage cannot be negative",
    "damage_exceeds_cap": (f"Damage cannot exceed {GAME_CONFIG['combat_damage_cap']}"),
    "healing_negative": "Healing amount cannot be negative",
    "item_id_invalid": "Invalid item ID",
    "item_name_too_long": (
        f"Item name cannot exceed {VALIDATION_CONFIG['max_item_name_length']} characters"
    ),
    "item_description_too_long": (
        f"Item description cannot exceed "
        f"{VALIDATION_CONFIG['max_item_description_length']} characters"
    ),
    "quest_id_invalid": "Invalid quest ID",
    "quest_name_too_long": (
        f"Quest name cannot exceed {VALIDATION_CONFIG['max_quest_name_length']} characters"
    ),
    "quest_description_too_long": (
        f"Quest description cannot exceed "
        f"{VALIDATION_CONFIG['max_quest_description_length']} characters"
    ),
    "location_id_invalid": "Invalid location ID",
    "location_name_too_long": (
        f"Location name cannot exceed "
        f"{VALIDATION_CONFIG['max_location_name_length']} characters"
    ),
    "location_description_too_long": (
        f"Location description cannot exceed "
        f"{VALIDATION_CONFIG['max_location_description_length']} characters"
    ),
}

# [CONST_009] - Combat configuration constants
# Explicit combat multipliers for deterministic agent calculations
COMBAT_CONFIG = {
    "base_damage": 10,
    "min_damage": 1,
    "max_damage": 100,
    "critical_chance": 0.05,
    "miss_chance": 0.05,
    "defense_reduction_factor": 0.3,
    "armor_absorption": 0.2,
    "max_combat_rounds": 50,
    "initiative_bonus_per_dex": 0.1,
}

COMBAT_FORMULAS = {
    "damage_formula": "base_damage * strength * multiplier - defense",
    "hp_formula": "base_hp + constitution * 5",
    "initiative_formula": "dexterity * 0.1 + random(1, 10)",
    "defense_formula": "dexterity * 0.5",
    "physical_damage": {"base_damage": 5, "stat_multiplier": 0.5},
    "magical_damage": {"base_damage": 3, "stat_multiplier": 0.7},
    "hit_chance": {"base_hit": 75, "min_hit": 10, "max_hit": 95},
    "dodge_chance": {"base_dodge": 10, "min_dodge": 5, "max_dodge": 50},
    "critical_chance": {"base_crit": 5, "min_crit": 1, "max_crit": 25},
    "block_chance": {"base_block": 15, "min_block": 5, "max_block": 40},
}

CRITICAL_MULTIPLIERS = {"normal": 1.0, "critical": 2.0, "glancing": 0.5, "miss": 0.0}

# Export all constants for easy access
__all__ = [
    "DEFAULT_CHARACTER_STATS",
    "DEFAULT_ABILITIES",
    "BASE_HP_BY_CLASS",
    "DAMAGE_MULTIPLIERS",
    "STAT_INCREASES",
    "ABILITY_LEARNING_SCHEDULE",
    "GAME_CONFIG",
    "COMBAT_CONFIG",
    "COMBAT_FORMULAS",
    "CRITICAL_MULTIPLIERS",
    "UI_CONFIG",
    "VALIDATION_CONFIG",
    "PERFORMANCE_CONFIG",
    "FILE_PATHS",
    "ERROR_MESSAGES",
]
