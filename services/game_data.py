SPELL_SCHOOLS_CONFIG = {
    "fire": {"primary_stat": "intelligence", "secondary_stat": "wisdom", "mana_multiplier": 1.2, "cooldown_modifier": 0.8},
    "water": {"primary_stat": "wisdom", "secondary_stat": "intelligence", "mana_multiplier": 1.1, "cooldown_modifier": 1.0},
    "earth": {"primary_stat": "constitution", "secondary_stat": "strength", "mana_multiplier": 1.0, "cooldown_modifier": 1.1},
    "air": {"primary_stat": "dexterity", "secondary_stat": "intelligence", "mana_multiplier": 1.1, "cooldown_modifier": 0.9},
    "light": {"primary_stat": "wisdom", "secondary_stat": "charisma", "mana_multiplier": 1.3, "cooldown_modifier": 1.2},
    "dark": {"primary_stat": "charisma", "secondary_stat": "intelligence", "mana_multiplier": 1.4, "cooldown_modifier": 1.3},
    "healing": {"primary_stat": "wisdom", "secondary_stat": "constitution", "mana_multiplier": 0.8, "cooldown_modifier": 0.7},
    "protection": {"primary_stat": "constitution", "secondary_stat": "wisdom", "mana_multiplier": 1.0, "cooldown_modifier": 1.0},
    "illusion": {"primary_stat": "intelligence", "secondary_stat": "charisma", "mana_multiplier": 1.1, "cooldown_modifier": 1.0},
}

STATUS_EFFECTS_CONFIG = {
    "stun": {"duration": 2, "immune_classes": ["warrior", "barbarian"]},
    "poison": {"duration": 3, "damage_per_turn": 2, "immune_classes": ["rogue", "ranger"]},
    "freeze": {"duration": 1, "immune_classes": ["mage", "wizard"]},
    "burn": {"duration": 2, "damage_per_turn": 1, "immune_classes": ["fire_elemental"]},
    "heal": {"duration": 0, "heal_amount": 5},
    "shield": {"duration": 3, "damage_reduction": 2},
    "haste": {"duration": 2, "speed_bonus": 2},
    "slow": {"duration": 2, "speed_penalty": 1},
}
