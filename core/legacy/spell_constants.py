"""
Spell constants for RPGSim
Spell schools, status effects, and spell configurations
"""

# Spell schools configuration
SPELL_SCHOOLS = {
    "fire": {
        "primary_stat": "intelligence",
        "secondary_stat": "wisdom",
        "mana_multiplier": 1.2,
    },
    "water": {
        "primary_stat": "wisdom",
        "secondary_stat": "intelligence",
        "mana_multiplier": 1.1,
    },
    "earth": {
        "primary_stat": "constitution",
        "secondary_stat": "strength",
        "mana_multiplier": 1.0,
    },
    "air": {
        "primary_stat": "dexterity",
        "secondary_stat": "intelligence",
        "mana_multiplier": 1.1,
    },
    "light": {
        "primary_stat": "wisdom",
        "secondary_stat": "charisma",
        "mana_multiplier": 1.3,
    },
    "dark": {
        "primary_stat": "charisma",
        "secondary_stat": "intelligence",
        "mana_multiplier": 1.4,
    },
    "healing": {
        "primary_stat": "wisdom",
        "secondary_stat": "constitution",
        "mana_multiplier": 0.8,
    },
    "protection": {
        "primary_stat": "constitution",
        "secondary_stat": "wisdom",
        "mana_multiplier": 1.0,
    },
    "illusion": {
        "primary_stat": "intelligence",
        "secondary_stat": "charisma",
        "mana_multiplier": 1.1,
    },
}

# Status effects configuration
STATUS_EFFECTS = {
    "stun": {"duration": 2, "immune_classes": ["warrior", "barbarian"]},
    "poison": {
        "duration": 3,
        "damage_per_turn": 2,
        "immune_classes": ["rogue", "ranger"],
    },
    "freeze": {"duration": 1, "immune_classes": ["mage", "wizard"]},
    "burn": {"duration": 2, "damage_per_turn": 1, "immune_classes": ["fire_elemental"]},
    "heal": {"duration": 0, "heal_amount": 5},
    "shield": {"duration": 3, "damage_reduction": 2},
    "haste": {"duration": 2, "speed_bonus": 2},
    "slow": {"duration": 2, "speed_penalty": 1},
}
