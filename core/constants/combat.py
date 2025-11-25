"""
Combat Constants for RPGSim
Optimized for LLM agents with explicit, deterministic combat formulas
"""

from typing import Dict, List, Any
from core.models import CharacterClass, ItemType


# DAMAGE TYPES
DAMAGE_TYPES = {
    "physical": {
        "name": "Physical",
        "description": "Standard physical damage from weapons and attacks",
        "resistance_stat": "constitution",
        "armor_effective": True,
        "spell_resistant": False
    },
    "fire": {
        "name": "Fire",
        "description": "Fire-based damage from spells and abilities",
        "resistance_stat": "intelligence",
        "armor_effective": False,
        "spell_resistant": True
    },
    "ice": {
        "name": "Ice",
        "description": "Ice-based damage from spells and abilities",
        "resistance_stat": "constitution",
        "armor_effective": False,
        "spell_resistant": True
    },
    "lightning": {
        "name": "Lightning",
        "description": "Lightning-based damage from spells and abilities",
        "resistance_stat": "dexterity",
        "armor_effective": False,
        "spell_resistant": True
    },
    "poison": {
        "name": "Poison",
        "description": "Poison-based damage over time",
        "resistance_stat": "constitution",
        "armor_effective": False,
        "spell_resistant": False
    },
    "holy": {
        "name": "Holy",
        "description": "Holy damage from divine spells",
        "resistance_stat": "wisdom",
        "armor_effective": False,
        "spell_resistant": True
    },
    "dark": {
        "name": "Dark",
        "description": "Dark damage from necromantic spells",
        "resistance_stat": "wisdom",
        "armor_effective": False,
        "spell_resistant": True
    },
    "psychic": {
        "name": "Psychic",
        "description": "Psychic damage from mental attacks",
        "resistance_stat": "wisdom",
        "armor_effective": False,
        "spell_resistant": False
    }
}


# SPELL SCHOOLS
SPELL_SCHOOLS = {
    "fire": {
        "name": "Fire Magic",
        "description": "Spells that deal fire damage and create fire effects",
        "primary_stat": "intelligence",
        "secondary_stat": "charisma",
        "damage_type": "fire",
        "difficulty": 3,
        "mana_multiplier": 1.2
    },
    "ice": {
        "name": "Ice Magic",
        "description": "Spells that deal ice damage and create ice effects",
        "primary_stat": "intelligence",
        "secondary_stat": "wisdom",
        "damage_type": "ice",
        "difficulty": 3,
        "mana_multiplier": 1.2
    },
    "lightning": {
        "name": "Lightning Magic",
        "description": "Spells that deal lightning damage and create electric effects",
        "primary_stat": "intelligence",
        "secondary_stat": "dexterity",
        "damage_type": "lightning",
        "difficulty": 4,
        "mana_multiplier": 1.5
    },
    "holy": {
        "name": "Holy Magic",
        "description": "Spells that deal holy damage and provide healing",
        "primary_stat": "wisdom",
        "secondary_stat": "charisma",
        "damage_type": "holy",
        "difficulty": 2,
        "mana_multiplier": 1.0
    },
    "dark": {
        "name": "Dark Magic",
        "description": "Spells that deal dark damage and create undead effects",
        "primary_stat": "intelligence",
        "secondary_stat": "wisdom",
        "damage_type": "dark",
        "difficulty": 5,
        "mana_multiplier": 2.0
    },
    "nature": {
        "name": "Nature Magic",
        "description": "Spells that manipulate nature and provide healing",
        "primary_stat": "wisdom",
        "secondary_stat": "constitution",
        "damage_type": "poison",
        "difficulty": 2,
        "mana_multiplier": 1.0
    },
    "psychic": {
        "name": "Psychic Magic",
        "description": "Spells that manipulate minds and deal psychic damage",
        "primary_stat": "wisdom",
        "secondary_stat": "charisma",
        "damage_type": "psychic",
        "difficulty": 4,
        "mana_multiplier": 1.5
    }
}


# ABILITY TYPES
ABILITY_TYPES = {
    "attack": {
        "name": "Attack",
        "description": "Standard physical attack ability",
        "damage_type": "physical",
        "base_damage": 10,
        "stat_scaling": "strength",
        "cooldown": 0,
        "resource_cost": 0,
        "requirements": {"level": 1}
    },
    "power_attack": {
        "name": "Power Attack",
        "description": "Enhanced physical attack with bonus damage",
        "damage_type": "physical",
        "base_damage": 20,
        "stat_scaling": "strength",
        "cooldown": 2,
        "resource_cost": 5,
        "requirements": {"level": 3, "strength": 12}
    },
    "defend": {
        "name": "Defend",
        "description": "Defensive stance that reduces damage taken",
        "damage_type": "none",
        "base_damage": 0,
        "stat_scaling": "constitution",
        "cooldown": 0,
        "resource_cost": 0,
        "requirements": {"level": 1}
    },
    "heal": {
        "name": "Heal",
        "description": "Healing ability that restores HP",
        "damage_type": "holy",
        "base_damage": -15,  # Negative damage = healing
        "stat_scaling": "wisdom",
        "cooldown": 3,
        "resource_cost": 10,
        "requirements": {"level": 2, "wisdom": 10}
    },
    "stealth": {
        "name": "Stealth",
        "description": "Ability to hide and gain surprise attack bonus",
        "damage_type": "none",
        "base_damage": 0,
        "stat_scaling": "dexterity",
        "cooldown": 5,
        "resource_cost": 3,
        "requirements": {"level": 2, "dexterity": 12}
    },
    "backstab": {
        "name": "Backstab",
        "description": "Sneak attack that deals bonus damage from behind",
        "damage_type": "physical",
        "base_damage": 25,
        "stat_scaling": "dexterity",
        "cooldown": 4,
        "resource_cost": 5,
        "requirements": {"level": 4, "dexterity": 14}
    },
    "fireball": {
        "name": "Fireball",
        "description": "Magical fire attack that explodes on impact",
        "damage_type": "fire",
        "base_damage": 30,
        "stat_scaling": "intelligence",
        "cooldown": 3,
        "resource_cost": 20,
        "requirements": {"level": 3, "intelligence": 12}
    },
    "lightning_bolt": {
        "name": "Lightning Bolt",
        "description": "Lightning spell that deals high damage",
        "damage_type": "lightning",
        "base_damage": 40,
        "stat_scaling": "intelligence",
        "cooldown": 4,
        "resource_cost": 25,
        "requirements": {"level": 5, "intelligence": 14}
    },
    "poison_blade": {
        "name": "Poison Blade",
        "description": "Weapon attack with poison damage over time",
        "damage_type": "poison",
        "base_damage": 15,
        "stat_scaling": "dexterity",
        "cooldown": 3,
        "resource_cost": 8,
        "requirements": {"level": 3, "dexterity": 12}
    },
    "holy_strike": {
        "name": "Holy Strike",
        "description": "Divine attack that deals holy damage",
        "damage_type": "holy",
        "base_damage": 25,
        "stat_scaling": "strength",
        "cooldown": 3,
        "resource_cost": 10,
        "requirements": {"level": 3, "wisdom": 12, "strength": 10}
    }
}


# STATUS EFFECTS
STATUS_EFFECTS = {
    "poison": {
        "name": "Poison",
        "description": "Takes damage over time",
        "damage_type": "poison",
        "duration": 5,  # rounds
        "damage_per_round": 5,
        "stackable": True,
        "removable": True,
        "immune_classes": ["necromancer", "druid"]
    },
    "burn": {
        "name": "Burn",
        "description": "Takes fire damage over time",
        "damage_type": "fire",
        "duration": 3,
        "damage_per_round": 8,
        "stackable": False,
        "removable": True,
        "immune_classes": ["elementalist", "berserker"]
    },
    "freeze": {
        "name": "Freeze",
        "description": "Cannot move or attack",
        "damage_type": "ice",
        "duration": 2,
        "damage_per_round": 0,
        "stackable": False,
        "removable": True,
        "immune_classes": ["elementalist", "shapeshifter"]
    },
    "stun": {
        "name": "Stun",
        "description": "Cannot act for one round",
        "damage_type": "physical",
        "duration": 1,
        "damage_per_round": 0,
        "stackable": False,
        "removable": True,
        "immune_classes": ["monk", "berserker"]
    },
    "bleed": {
        "name": "Bleed",
        "description": "Takes physical damage over time",
        "damage_type": "physical",
        "duration": 4,
        "damage_per_round": 4,
        "stackable": True,
        "removable": True,
        "immune_classes": ["paladin", "healer"]
    },
    "haste": {
        "name": "Haste",
        "description": "Acts twice per round",
        "damage_type": "none",
        "duration": 3,
        "damage_per_round": 0,
        "stackable": False,
        "removable": False,
        "immune_classes": []
    },
    "regeneration": {
        "name": "Regeneration",
        "description": "Heals damage over time",
        "damage_type": "holy",
        "duration": 5,
        "damage_per_round": -5,  # Negative = healing
        "stackable": False,
        "removable": False,
        "immune_classes": []
    },
    "weakness": {
        "name": "Weakness",
        "description": "Reduced damage output",
        "damage_type": "none",
        "duration": 4,
        "damage_per_round": 0,
        "stackable": False,
        "removable": True,
        "immune_classes": ["berserker", "paladin"]
    },
    "defense_boost": {
        "name": "Defense Boost",
        "description": "Reduced damage taken",
        "damage_type": "none",
        "duration": 3,
        "damage_per_round": 0,
        "stackable": False,
        "removable": False,
        "immune_classes": []
    },
    "blind": {
        "name": "Blind",
        "description": "Reduced hit chance",
        "damage_type": "none",
        "duration": 3,
        "damage_per_round": 0,
        "stackable": False,
        "removable": True,
        "immune_classes": ["ranger", "ninja"]
    }
}


# COMBAT FORMULAS
COMBAT_FORMULAS = {
    "hit_chance": {
        "description": "Base hit chance calculation",
        "formula": "base_hit + (attacker_dexterity - defender_dexterity) // 2",
        "base_hit": 80,  # 80% base hit chance
        "max_hit": 95,   # 95% maximum hit chance
        "min_hit": 25    # 25% minimum hit chance
    },
    "critical_chance": {
        "description": "Critical hit chance calculation",
        "formula": "base_crit + (attacker_dexterity - 10) // 4 + (level_difficulty // 10)",
        "base_crit": 5,  # 5% base critical chance
        "max_crit": 30,  # 30% maximum critical chance
        "min_crit": 0    # 0% minimum critical chance
    },
    "dodge_chance": {
        "description": "Dodge chance calculation",
        "formula": "base_dodge + (defender_dexterity - attacker_dexterity) // 3",
        "base_dodge": 10,  # 10% base dodge chance
        "max_dodge": 40,   # 40% maximum dodge chance
        "min_dodge": 0     # 0% minimum dodge chance
    },
    "block_chance": {
        "description": "Block chance calculation",
        "formula": "base_block + (defender_strength // 5) + (shield_bonus // 10)",
        "base_block": 5,   # 5% base block chance
        "max_block": 35,   # 35% maximum block chance
        "min_block": 0     # 0% minimum block chance
    },
    "physical_damage": {
        "description": "Physical damage calculation",
        "formula": "base_damage + (strength // 2) + (weapon_damage) + (ability_power)",
        "base_damage": 10,  # Base damage for unarmed attacks
        "stat_multiplier": 0.5,  # Strength contributes 50% of stat value
        "weapon_multiplier": 1.0,  # Full weapon damage
        "armor_reduction": 0.8     # Armor reduces damage by 80%
    },
    "magical_damage": {
        "description": "Magical damage calculation",
        "formula": "base_damage + (intelligence // 2) + (spell_power) + (ability_power)",
        "base_damage": 15,  # Base damage for basic spells
        "stat_multiplier": 0.5,  # Intelligence contributes 50% of stat value
        "spell_multiplier": 1.0,  # Full spell power
        "resist_multiplier": 0.5  # Resistance reduces damage by 50%
    },
    "elemental_damage": {
        "description": "Elemental damage calculation with effectiveness",
        "formula": "base_damage * (type_effectiveness) * (resist_modifier)",
        "effectiveness": {
            "fire_vs_ice": 1.5,
            "ice_vs_fire": 1.3,
            "lightning_vs_ice": 1.4,
            "holy_vs_dark": 1.6,
            "dark_vs_holy": 1.6
        },
        "resist_multiplier": 0.6  # Elemental resistance reduces damage by 60%
    }
}


# CRITICAL MULTIPLIERS
CRITICAL_MULTIPLIERS = {
    "normal": {
        "name": "Normal Hit",
        "multiplier": 1.0,
        "description": "Standard damage"
    },
    "critical": {
        "name": "Critical Hit",
        "multiplier": 2.0,
        "description": "Double damage"
    },
    "devastating": {
        "name": "Devastating Hit",
        "multiplier": 3.0,
        "description": "Triple damage"
    },
    "lethal": {
        "name": "Lethal Hit",
        "multiplier": 4.0,
        "description": "Quadruple damage"
    }
}


# RESISTANCE VALUES
RESISTANCE_VALUES = {
    "none": {
        "name": "No Resistance",
        "multiplier": 1.0,
        "description": "No damage reduction"
    },
    "low": {
        "name": "Low Resistance",
        "multiplier": 0.8,
        "description": "20% damage reduction"
    },
    "medium": {
        "name": "Medium Resistance",
        "multiplier": 0.6,
        "description": "40% damage reduction"
    },
    "high": {
        "name": "High Resistance",
        "multiplier": 0.4,
        "description": "60% damage reduction"
    },
    "immune": {
        "name": "Immune",
        "multiplier": 0.0,
        "description": "No damage taken"
    },
    "vulnerable": {
        "name": "Vulnerable",
        "multiplier": 1.5,
        "description": "50% increased damage"
    }
}


# COMBAT CONFIG
COMBAT_CONFIG = {
    "max_combat_rounds": 50,  # Maximum rounds before draw
    "base_hit_chance": 80,   # Base hit chance percentage
    "base_crit_chance": 5,   # Base critical chance percentage
    "base_dodge_chance": 10, # Base dodge chance percentage
    "base_block_chance": 5,  # Base block chance percentage
    "min_damage": 1,         # Minimum damage per hit
    "max_damage": 9999,      # Maximum damage per hit
    "armor_absorption": 0.8,  # Armor damage absorption rate
    "magic_absorption": 0.5, # Magic damage absorption rate
    "resistance_absorption": 0.6,  # Resistance damage absorption rate
    "level_advantage_damage": 1.1,  # Damage bonus per level advantage
    "level_disadvantage_damage": 0.9, # Damage penalty per level disadvantage
    "critical_threshold": 95, # Hit roll for critical hit
    "fumble_threshold": 5,   # Hit roll for fumble
    "status_effect_duration": 5,  # Default duration for status effects
    "cooldown_reduction_per_level": 0.1,  # Cooldown reduction per 5 levels
    "mana_cost_reduction_per_level": 0.05,  # Mana cost reduction per 5 levels
    "equipment_damage_bonus": 0.1,  # Damage bonus per equipment tier
    "equipment_defense_bonus": 0.1,  # Defense bonus per equipment tier
    "status_effect_damage_cap": 50,  # Maximum damage per status effect tick
    "boss_damage_reduction": 0.25,  # Damage reduction for boss enemies
    "boss_hp_multiplier": 5.0,  # HP multiplier for boss enemies
    "multi_enemy_damage_reduction": 0.1,  # Damage reduction per additional enemy
    "stealth_attack_bonus": 1.5,  # Damage bonus for stealth attacks
    "backstab_bonus": 2.0,  # Damage bonus for backstab attacks
    "power_attack_cost": 5,  # Resource cost for power attacks
    "defend_damage_reduction": 0.5,  # Damage reduction while defending
    "healing_multiplier": 1.0,  # Base healing multiplier
    "mana_cost_per_damage": 0.5,  # Mana cost per damage point
    "stamina_cost_per_damage": 0.3,  # Stamina cost per damage point
    "combo_attack_bonus": 1.2,  # Damage bonus for combo attacks
    "flanking_bonus": 1.3,  # Damage bonus for flanking attacks
    "height_advantage_bonus": 1.1,  # Damage bonus for height advantage
    "range_penalty": 0.8,  # Damage penalty for long-range attacks
    "environment_damage_bonus": 1.1,  # Damage bonus for environmental attacks
    "weather_damage_modifier": 0.9,  # Weather damage modifier
    "time_of_day_damage_modifier": 1.0,  # Time of day damage modifier
    "fatigue_damage_penalty": 0.8,  # Damage penalty from fatigue
    "morale_damage_bonus": 1.1,  # Damage bonus from high morale
    "fear_damage_penalty": 0.7,  # Damage penalty from fear
    "berserk_damage_multiplier": 1.5,  # Damage multiplier for berserk state
    "guard_stance_defense_bonus": 0.7,  # Defense bonus for guard stance
    "rage_stance_offense_bonus": 1.3,  # Offense bonus for rage stance
    "counter_attack_damage": 0.5,  # Damage percentage for counter attacks
    "opportunity_attack_damage": 0.3,  # Damage percentage for opportunity attacks
    "aid_another_attack_bonus": 0.2,  # Attack bonus for aid another
    "aid_another_defense_bonus": 0.2,  # Defense bonus for aid another
    "trip_attack_duration": 2,  # Duration for trip attack
    "disarm_duration": 3,  # Duration for disarm
    "sunder_armor_penetration": 0.3,  # Armor penetration for sunder
    "bull_rush_distance": 10,  # Distance for bull rush
    "grapple_escape_difficulty": 15,  # Difficulty for grapple escape
    "suicide_attack_multiplier": 3.0,  # Damage multiplier for suicide attacks
    "last_stand_bonus": 2.0,  # Damage bonus for last stand
    "desperation_healing": 1.5,  # Healing multiplier for desperation
    "revenge_damage_bonus": 1.4,  # Damage bonus for revenge attacks
    "protection_damage_share": 0.5,  # Damage percentage shared by protection
    "sacrifice_healing": 2.0,  # Healing multiplier for sacrifice
    "resurrection_healing": 1.0,  # Healing multiplier for resurrection
    "revival_cooldown": 100,  # Cooldown for revival abilities
    "immunity_duration": 10,  # Duration for status immunity after removal
    "resistance_cooldown": 5,  # Cooldown for resistance abilities
    "buff_stacking_limit": 3,  # Maximum stacks for buff effects
    "debuff_stacking_limit": 5,  # Maximum stacks for debuff effects
    "area_of_effect_radius": 5,  # Radius for area of effect abilities
    "chain_lightning_jumps": 3,  # Maximum jumps for chain lightning
    "multishot_projectiles": 5,  # Maximum projectiles for multishot
    "meteor_impact_radius": 10,  # Radius for meteor impact
    "blizzard_area_radius": 15,  # Radius for blizzard area
    "earthquake_radius": 20,  # Radius for earthquake
    "volcano_eruption_radius": 25,  # Radius for volcano eruption
    "tornado_path_length": 30,  # Path length for tornado
    "tsunami_wave_length": 40,  # Wave length for tsunami
    "solar_flare_radius": 50,  # Radius for solar flare
    "black_hole_pull_radius": 60,  # Pull radius for black hole
    "time_freeze_duration": 3,  # Duration for time freeze
    "reality_warp_duration": 5,  # Duration for reality warp
    "dimension_shift_duration": 7,  # Duration for dimension shift
    "cosmic_power_multiplier": 3.0,  # Multiplier for cosmic powers
    "divine_intervention_healing": 100,  # Healing for divine intervention
    "demonic_pact_damage": 50,  # Damage for demonic pact
    "angelic_blessing_bonus": 1.5,  # Bonus for angelic blessing
    "demonic_curse_penalty": 0.5,  # Penalty for demonic curse
    "holy_water_damage": 25,  # Damage for holy water
    "unholy_blight_damage": 30,  # Damage for unholy blight
    "sacred_ground_healing": 10,  # Healing for sacred ground
    "desecrated_ground_damage": 15,  # Damage for desecrated ground
    "blessed_armor_defense": 20,  # Defense for blessed armor
    "cursed_weapon_damage": 25,  # Damage for cursed weapon
    "purification_healing": 20,  # Healing for purification
    "corruption_damage": 30,  # Damage for corruption
    "divine_wrath_damage": 50,  # Damage for divine wrath
    "demonic_fury_damage": 45,  # Damage for demonic fury
    "angelic_vengeance_damage": 40,  # Damage for angelic vengeance
    "demonic_retribution_damage": 35,  # Damage for demonic retribution
    "holy_sanctum_protection": 100,  # Protection for holy sanctum
    "demonic_sanctum_corruption": 50,  # Corruption for demonic sanctum
    "divine_judgment_damage": 75,  # Damage for divine judgment
    "demonic_condemnation_damage": 65,  # Damage for demonic condemnation
    "angelic_salvation_healing": 150,  # Healing for angelic salvation
    "damic_damnation_damage": 85,  # Damage for demonic damnation
    "holy_revelation_bonus": 2.0,  # Bonus for holy revelation
    "damic_revelation_bonus": 1.8,  # Bonus for demonic revelation
    "divine_ascension_power": 3.0,  # Power for divine ascension
    "damic_descension_power": 2.8,  # Power for demonic descension
    "heavenly_gate_duration": 10,  # Duration for heavenly gate
    "hellish_gate_duration": 8,   # Duration for hellish gate
    "divine_mercy_healing": 200,  # Healing for divine mercy
    "damic_cruelty_damage": 100,  # Damage for demonic cruelty
    "angelic_purification_cleanse": 50,  # Cleanse for angelic purification
    "damic_contamination_poison": 75,  # Poison for demonic contamination
    "holy_light_blind_duration": 5,  # Duration for holy light blind
    "damic_darkness_fear_duration": 6,  # Duration for demonic darkness fear
    "divine_protection_shield": 500,  # Shield for divine protection
    "damic_destruction_blast": 400,  # Blast for demonic destruction
    "angelic_resurrection_cooldown": 1000,  # Cooldown for angelic resurrection
    "damic_reincarnation_cooldown": 800,  # Cooldown for demonic reincarnation
    "holy_avalanche_damage": 150,  # Damage for holy avalanche
    "damic_tsunami_damage": 140,  # Damage for demonic tsunami
    "divine_earthquake_damage": 130,  # Damage for divine earthquake
    "damic_volcano_damage": 160,  # Damage for demonic volcano
    "heavenly_comet_damage": 170,  # Damage for heavenly comet
    "hellish_meteor_damage": 180,  # Damage for hellish meteor
    "divine_tornado_damage": 190,  # Damage for divine tornado
    "damic_hurricane_damage": 200,  # Damage for demonic hurricane
    "holy_solar_flare_damage": 210,  # Damage for holy solar flare
    "damic_black_hole_damage": 220,  # Damage for demonic black hole
    "angelic_nova_damage": 250,  # Damage for angelic nova
    "damic_implosion_damage": 240,  # Damage for demonic implosion
    "divine_big_bang_damage": 300,  # Damage for divine big bang
    "damic_heat_death_damage": 290  # Damage for demonic heat death
}


# Export all constants for easy access
__all__ = [
    'DAMAGE_TYPES',
    'SPELL_SCHOOLS',
    'ABILITY_TYPES',
    'STATUS_EFFECTS',
    'COMBAT_FORMULAS',
    'CRITICAL_MULTIPLIERS',
    'RESISTANCE_VALUES',
    'COMBAT_CONFIG'
]