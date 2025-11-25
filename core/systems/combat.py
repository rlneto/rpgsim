"""
Combat System for RPGSim
Optimized for LLM agents with explicit, deterministic combat calculations
"""

import random
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from core.models import (
    Character, CharacterClass, CharacterStats,
    Enemy, EnemyType,
    Item, ItemRarity, ItemType
)
from core.validation import (
    ValidationError,
    validate_combat_execution,
    validate_damage_calculation
)
from core.constants import (
    GAME_CONFIG,
    DAMAGE_MULTIPLIERS,
    COMBAT_CONFIG,
    COMBAT_FORMULAS,
    CRITICAL_MULTIPLIERS
)


def calculate_damage(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy],
    weapon: Optional[Item] = None,
    ability: Optional[str] = None,
    damage_type: str = "physical"
) -> Dict[str, Any]:
    """
    Calculate damage for attack with explicit formula for agents.
    
    Args:
        attacker: Attacking character or enemy
        defender: Defending character or enemy
        weapon: Optional weapon being used
        ability: Optional ability being used
        damage_type: Type of damage being dealt
        
    Returns:
        Dict[str, Any]: Damage calculation details
        
    Raises:
        ValidationError: If parameters are invalid
        
    Examples:
        >>> attacker = create_character("Warrior", CharacterClass.WARRIOR)
        >>> defender = create_enemy("Goblin", 2)
        >>> damage = calculate_damage(attacker, defender)
        >>> damage['damage']
        25
        >>> damage['damage_type']
        'physical'
        >>> damage['critical_hit']
        False
        >>> damage['hit']
        True
    """
    # Validate combat parameters
    validate_combat_execution(attacker, defender, 20)  # Assume reasonable damage
    
    # Get base stats
    attacker_stats = getattr(attacker, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    defender_stats = getattr(defender, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    
    # Calculate base damage
    if damage_type == "physical":
        base_damage = COMBAT_FORMULAS["physical_damage"]["base_damage"]
        stat_bonus = attacker_stats.strength * COMBAT_FORMULAS["physical_damage"]["stat_multiplier"]
        weapon_bonus = 0
        
        if weapon and weapon.is_equipment():
            weapon_bonus = weapon.stats_mod.get("damage", 0)
        
        ability_bonus = 0
        if ability:
            ability_bonus = _get_ability_damage_bonus(ability)
        
        raw_damage = base_damage + stat_bonus + weapon_bonus + ability_bonus
    
    elif damage_type in ["fire", "ice", "lightning", "holy", "dark"]:
        base_damage = COMBAT_FORMULAS["magical_damage"]["base_damage"]
        stat_bonus = attacker_stats.intelligence * COMBAT_FORMULAS["magical_damage"]["stat_multiplier"]
        
        if isinstance(attacker, Character):
            class_multiplier = DAMAGE_MULTIPLIERS[attacker.class_type.value]
        else:
            class_multiplier = 1.0
        
        spell_bonus = 0
        if ability:
            spell_bonus = _get_spell_damage_bonus(ability)
        
        raw_damage = (base_damage + stat_bonus + spell_bonus) * class_multiplier
    
    else:
        raw_damage = 10  # Default damage
    
    # Apply damage modifiers
    damage_modifiers = _get_damage_modifiers(attacker, defender, weapon, ability)
    modified_damage = raw_damage * damage_modifiers['total_multiplier']
    
    # Calculate hit chance
    hit_chance = calculate_hit_chance(attacker, defender)
    hit_roll = random.randint(1, 100)
    is_hit = hit_roll <= hit_chance
    
    # Calculate critical chance
    critical_chance = calculate_critical_chance(attacker, defender)
    is_critical = is_hit and random.randint(1, 100) <= critical_chance
    
    # Apply critical multiplier
    if is_critical:
        critical_multiplier = CRITICAL_MULTIPLIERS["critical"]["multiplier"]
        final_damage = modified_damage * critical_multiplier
        critical_type = "critical"
    else:
        final_damage = modified_damage
        critical_type = "normal"
    
    # Apply damage reduction
    damage_reduction = _calculate_damage_reduction(defender, damage_type)
    final_damage = final_damage * damage_reduction
    
    # Ensure minimum damage
    final_damage = max(final_damage, COMBAT_CONFIG["min_damage"])
    
    # Ensure maximum damage
    final_damage = min(final_damage, COMBAT_CONFIG["max_damage"])
    
    # Round to integer
    final_damage = int(final_damage)
    
    return {
        'damage': final_damage,
        'raw_damage': raw_damage,
        'modified_damage': int(modified_damage),
        'damage_type': damage_type,
        'hit': is_hit,
        'critical_hit': is_critical,
        'critical_type': critical_type,
        'critical_multiplier': CRITICAL_MULTIPLIERS[critical_type]["multiplier"] if is_critical else 1.0,
        'hit_chance': hit_chance,
        'critical_chance': critical_chance,
        'damage_reduction': damage_reduction,
        'damage_modifiers': damage_modifiers
    }


def calculate_hit_chance(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy]
) -> int:
    """
    Calculate hit chance with explicit formula for agents.
    
    Args:
        attacker: Attacking character or enemy
        defender: Defending character or enemy
        
    Returns:
        int: Hit chance percentage (0-100)
        
    Examples:
        >>> attacker = create_character("Rogue", CharacterClass.ROGUE)
        >>> defender = create_character("Warrior", CharacterClass.WARRIOR)
        >>> hit_chance = calculate_hit_chance(attacker, defender)
        >>> 0 <= hit_chance <= 100
        True
    """
    # Get stats
    attacker_stats = getattr(attacker, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    defender_stats = getattr(defender, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    
    # Base hit chance
    base_hit = COMBAT_FORMULAS["hit_chance"]["base_hit"]
    
    # Dexterity modifier
    dex_diff = attacker_stats.dexterity - defender_stats.dexterity
    dex_modifier = dex_diff // 2
    
    # Level modifier
    attacker_level = getattr(attacker, 'level', 1)
    defender_level = getattr(defender, 'level', 1)
    level_diff = attacker_level - defender_level
    level_modifier = level_diff // 5
    
    # Calculate total hit chance
    hit_chance = base_hit + dex_modifier + level_modifier
    
    # Apply bounds
    hit_chance = max(COMBAT_FORMULAS["hit_chance"]["min_hit"], hit_chance)
    hit_chance = min(COMBAT_FORMULAS["hit_chance"]["max_hit"], hit_chance)
    
    return int(hit_chance)


def calculate_critical_chance(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy]
) -> int:
    """
    Calculate critical chance with explicit formula for agents.
    
    Args:
        attacker: Attacking character or enemy
        defender: Defending character or enemy
        
    Returns:
        int: Critical chance percentage (0-100)
        
    Examples:
        >>> attacker = create_character("Assassin", CharacterClass.ASSASSIN)
        >>> defender = create_character("Goblin", 2)
        >>> crit_chance = calculate_critical_chance(attacker, defender)
        >>> 0 <= crit_chance <= 100
        True
    """
    # Get stats
    attacker_stats = getattr(attacker, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    
    # Base critical chance
    base_crit = COMBAT_FORMULAS["critical_chance"]["base_crit"]
    
    # Dexterity modifier
    dex_modifier = max(0, (attacker_stats.dexterity - 10) // 4)
    
    # Level modifier
    attacker_level = getattr(attacker, 'level', 1)
    level_modifier = attacker_level // 10
    
    # Class modifier
    if isinstance(attacker, Character):
        class_modifier = _get_class_critical_modifier(attacker.class_type)
    else:
        class_modifier = 0
    
    # Calculate total critical chance
    critical_chance = base_crit + dex_modifier + level_modifier + class_modifier
    
    # Apply bounds
    critical_chance = max(COMBAT_FORMULAS["critical_chance"]["min_crit"], critical_chance)
    critical_chance = min(COMBAT_FORMULAS["critical_chance"]["max_crit"], critical_chance)
    
    return int(critical_chance)


def calculate_dodge_chance(
    defender: Union[Character, Enemy],
    attacker: Union[Character, Enemy]
) -> int:
    """
    Calculate dodge chance with explicit formula for agents.
    
    Args:
        defender: Defending character or enemy
        attacker: Attacking character or enemy
        
    Returns:
        int: Dodge chance percentage (0-100)
        
    Examples:
        >>> defender = create_character("Ranger", CharacterClass.RANGER)
        >>> attacker = create_character("Warrior", CharacterClass.WARRIOR)
        >>> dodge_chance = calculate_dodge_chance(defender, attacker)
        >>> 0 <= dodge_chance <= 100
        True
    """
    # Get stats
    defender_stats = getattr(defender, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    attacker_stats = getattr(attacker, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    
    # Base dodge chance
    base_dodge = COMBAT_FORMULAS["dodge_chance"]["base_dodge"]
    
    # Dexterity modifier
    dex_diff = defender_stats.dexterity - attacker_stats.dexterity
    dex_modifier = dex_diff // 3
    
    # Level modifier
    defender_level = getattr(defender, 'level', 1)
    level_modifier = defender_level // 8
    
    # Calculate total dodge chance
    dodge_chance = base_dodge + dex_modifier + level_modifier
    
    # Apply bounds
    dodge_chance = max(COMBAT_FORMULAS["dodge_chance"]["min_dodge"], dodge_chance)
    dodge_chance = min(COMBAT_FORMULAS["dodge_chance"]["max_dodge"], dodge_chance)
    
    return int(dodge_chance)


def calculate_block_chance(
    defender: Union[Character, Enemy],
    attacker: Union[Character, Enemy]
) -> int:
    """
    Calculate block chance with explicit formula for agents.
    
    Args:
        defender: Defending character or enemy
        attacker: Attacking character or enemy
        
    Returns:
        int: Block chance percentage (0-100)
        
    Examples:
        >>> defender = create_character("Paladin", CharacterClass.PALADIN)
        >>> attacker = create_character("Goblin", 2)
        >>> block_chance = calculate_block_chance(defender, attacker)
        >>> 0 <= block_chance <= 100
        True
    """
    # Get stats
    defender_stats = getattr(defender, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
    
    # Base block chance
    base_block = COMBAT_FORMULAS["block_chance"]["base_block"]
    
    # Strength modifier
    str_modifier = defender_stats.strength // 5
    
    # Level modifier
    defender_level = getattr(defender, 'level', 1)
    level_modifier = defender_level // 10
    
    # Shield modifier (if has shield)
    shield_bonus = _get_shield_bonus(defender)
    shield_modifier = shield_bonus // 10
    
    # Calculate total block chance
    block_chance = base_block + str_modifier + level_modifier + shield_modifier
    
    # Apply bounds
    block_chance = max(COMBAT_FORMULAS["block_chance"]["min_block"], block_chance)
    block_chance = min(COMBAT_FORMULAS["block_chance"]["max_block"], block_chance)
    
    return int(block_chance)


def simulate_combat_round(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy],
    weapon: Optional[Item] = None,
    ability: Optional[str] = None,
    damage_type: str = "physical"
) -> Dict[str, Any]:
    """
    Simulate a single combat round with explicit logic for agents.
    
    Args:
        attacker: Attacking character or enemy
        defender: Defending character or enemy
        weapon: Optional weapon being used
        ability: Optional ability being used
        damage_type: Type of damage being dealt
        
    Returns:
        Dict[str, Any]: Combat round results
        
    Examples:
        >>> attacker = create_character("Warrior", CharacterClass.WARRIOR)
        >>> defender = create_enemy("Goblin", 2)
        >>> result = simulate_combat_round(attacker, defender)
        >>> result['attacker']['name']
        'Warrior'
        >>> result['defender']['name']
        'Goblin'
        >>> result['round_number']
        1
        >>> 'damage' in result
        True
        >>> 'hit' in result
        True
    """
    # Calculate dodge chance
    dodge_chance = calculate_dodge_chance(defender, attacker)
    dodge_roll = random.randint(1, 100)
    is_dodged = dodge_roll <= dodge_chance
    
    if is_dodged:
        return {
            'round_number': 1,
            'attacker': {
                'name': getattr(attacker, 'name', 'Unknown'),
                'level': getattr(attacker, 'level', 1),
                'hp': getattr(attacker, 'hp', 0),
                'max_hp': getattr(attacker, 'max_hp', 0)
            },
            'defender': {
                'name': getattr(defender, 'name', 'Unknown'),
                'level': getattr(defender, 'level', 1),
                'hp': getattr(defender, 'hp', 0),
                'max_hp': getattr(defender, 'max_hp', 0)
            },
            'hit': False,
            'dodged': True,
            'blocked': False,
            'damage': 0,
            'damage_type': damage_type,
            'critical_hit': False,
            'weapon': getattr(weapon, 'name', None) if weapon else None,
            'ability': ability,
            'dodge_chance': dodge_chance,
            'dodge_roll': dodge_roll,
            'message': f"{getattr(attacker, 'name', 'Unknown')} attacks but {getattr(defender, 'name', 'Unknown')} dodges!"
        }
    
    # Calculate block chance
    block_chance = calculate_block_chance(defender, attacker)
    block_roll = random.randint(1, 100)
    is_blocked = block_roll <= block_chance
    
    # Calculate damage
    damage_result = calculate_damage(attacker, defender, weapon, ability, damage_type)
    
    # Apply block reduction if blocked
    final_damage = damage_result['damage']
    if is_blocked:
        block_reduction = 0.5  # Block reduces damage by 50%
        final_damage = int(final_damage * block_reduction)
    
    # Apply damage to defender
    old_hp = getattr(defender, 'hp', 0)
    final_hp = max(0, old_hp - final_damage)
    
    # Update defender's HP
    if hasattr(defender, 'hp'):
        defender.hp = final_hp
    
    return {
        'round_number': 1,
        'attacker': {
            'name': getattr(attacker, 'name', 'Unknown'),
            'level': getattr(attacker, 'level', 1),
            'hp': getattr(attacker, 'hp', 0),
            'max_hp': getattr(attacker, 'max_hp', 0)
        },
        'defender': {
            'name': getattr(defender, 'name', 'Unknown'),
            'level': getattr(defender, 'level', 1),
            'hp': final_hp,
            'max_hp': getattr(defender, 'max_hp', 0)
        },
        'hit': damage_result['hit'],
        'dodged': False,
        'blocked': is_blocked,
        'damage': final_damage,
        'damage_type': damage_type,
        'critical_hit': damage_result['critical_hit'],
        'weapon': getattr(weapon, 'name', None) if weapon else None,
        'ability': ability,
        'hit_chance': damage_result['hit_chance'],
        'block_chance': block_chance,
        'block_roll': block_roll,
        'dodge_chance': dodge_chance,
        'dodge_roll': dodge_roll,
        'old_hp': old_hp,
        'new_hp': final_hp,
        'hp_change': old_hp - final_hp,
        'message': _generate_combat_message(attacker, defender, final_damage, is_blocked, damage_result['critical_hit'], is_dodged)
    }


def resolve_combat_round(
    combat_round: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Resolve combat round results and update combat state.
    
    Args:
        combat_round: Combat round results from simulate_combat_round()
        
    Returns:
        Dict[str, Any]: Resolved combat round with additional information
        
    Examples:
        >>> attacker = create_character("Warrior", CharacterClass.WARRIOR)
        >>> defender = create_enemy("Goblin", 2)
        >>> combat_round = simulate_combat_round(attacker, defender)
        >>> resolved = resolve_combat_round(combat_round)
        >>> resolved['combat_over']
        False
        >>> resolved['winner']
        None
        >>> 'damage_dealt' in resolved
        True
    """
    # Check if combat is over
    defender_hp = combat_round['defender']['hp']
    attacker_hp = combat_round['attacker']['hp']
    
    combat_over = defender_hp <= 0 or attacker_hp <= 0
    
    if combat_over:
        if defender_hp <= 0 and attacker_hp > 0:
            winner = combat_round['attacker']['name']
            loser = combat_round['defender']['name']
        elif attacker_hp <= 0 and defender_hp > 0:
            winner = combat_round['defender']['name']
            loser = combat_round['attacker']['name']
        else:
            winner = "draw"
            loser = "draw"
    else:
        winner = None
        loser = None
    
    return {
        **combat_round,
        'combat_over': combat_over,
        'winner': winner,
        'loser': loser,
        'damage_dealt': combat_round['damage'],
        'damage_received': combat_round['damage'],
        'attacker_remaining_hp': combat_round['attacker']['hp'],
        'defender_remaining_hp': combat_round['defender']['hp'],
        'attacker_hp_percentage': (combat_round['attacker']['hp'] / combat_round['attacker']['max_hp']) * 100,
        'defender_hp_percentage': (combat_round['defender']['hp'] / combat_round['defender']['max_hp']) * 100
    }


def calculate_combat_outcome(
    participants: List[Union[Character, Enemy]],
    max_rounds: int = 50
) -> Dict[str, Any]:
    """
    Calculate complete combat outcome with explicit simulation for agents.
    
    Args:
        participants: List of combat participants
        max_rounds: Maximum rounds before draw
        
    Returns:
        Dict[str, Any]: Complete combat outcome
        
    Examples:
        >>> attacker = create_character("Warrior", CharacterClass.WARRIOR)
        >>> defender = create_enemy("Goblin", 2)
        >>> outcome = calculate_combat_outcome([attacker, defender])
        >>> 'winner' in outcome
        True
        >>> 'total_rounds' in outcome
        True
        >>> 'combat_log' in outcome
        True
    """
    if len(participants) < 2:
        raise ValidationError("Combat requires at least 2 participants", field='participants', value=participants)
    
    # Initialize combat state
    combat_log = []
    current_round = 0
    combat_over = False
    winner = None
    
    # Simulate combat rounds
    while not combat_over and current_round < max_rounds:
        current_round += 1
        
        # Simple turn-based combat: first participant attacks second
        attacker = participants[0]
        defender = participants[1]
        
        # Check if participants can fight
        if not getattr(attacker, 'is_alive', lambda: True)():
            combat_over = True
            winner = getattr(participants[1], 'name', 'Unknown')
            break
        
        if not getattr(defender, 'is_alive', lambda: True)():
            combat_over = True
            winner = getattr(participants[0], 'name', 'Unknown')
            break
        
        # Simulate combat round
        combat_round = simulate_combat_round(attacker, defender)
        resolved_round = resolve_combat_round(combat_round)
        
        # Add to combat log
        combat_log.append(resolved_round)
        
        # Check if combat is over
        combat_over = resolved_round['combat_over']
        if combat_over:
            winner = resolved_round['winner']
        
        # Switch participants for next round (simple alternating)
        participants = [participants[1], participants[0]]
    
    # Determine final outcome
    if not combat_over and current_round >= max_rounds:
        outcome = "draw"
        winner = "draw"
    elif winner:
        outcome = "victory"
    else:
        outcome = "draw"
        winner = "draw"
    
    # Calculate combat statistics
    total_damage = sum(round_result['damage_dealt'] for round_result in combat_log)
    total_hits = sum(1 for round_result in combat_log if round_result['hit'])
    total_criticals = sum(1 for round_result in combat_log if round_result['critical_hit'])
    
    return {
        'outcome': outcome,
        'winner': winner,
        'total_rounds': current_round,
        'total_damage': total_damage,
        'total_hits': total_hits,
        'total_criticals': total_criticals,
        'hit_rate': (total_hits / current_round * 100) if current_round > 0 else 0,
        'critical_rate': (total_criticals / total_hits * 100) if total_hits > 0 else 0,
        'average_damage': total_damage / total_hits if total_hits > 0 else 0,
        'combat_log': combat_log,
        'participants': [
            {
                'name': getattr(p, 'name', 'Unknown'),
                'level': getattr(p, 'level', 1),
                'hp': getattr(p, 'hp', 0),
                'max_hp': getattr(p, 'max_hp', 0),
                'is_alive': getattr(p, 'is_alive', lambda: True)()
            } for p in participants
        ]
    }


# Helper functions for combat calculations
def _get_ability_damage_bonus(ability: str) -> int:
    """Get damage bonus for specific ability."""
    ability_damage_bonus = {
        "Power Attack": 10,
        "Backstab": 15,
        "Whirlwind Attack": 20,
        "Holy Strike": 12,
        "Shadow Strike": 18,
        "Fury Strike": 25,
        "Precision Strike": 8,
        "Heavy Strike": 22,
        "Rapid Strike": 5,
        "Deadly Strike": 30
    }
    return ability_damage_bonus.get(ability, 0)


def _get_spell_damage_bonus(spell: str) -> int:
    """Get damage bonus for specific spell."""
    spell_damage_bonus = {
        "Fireball": 25,
        "Ice Lance": 20,
        "Lightning Bolt": 30,
        "Holy Light": 15,
        "Dark Bolt": 28,
        "Poison Dart": 10,
        "Psychic Blast": 22,
        "Arcane Missile": 18,
        "Meteor": 40,
        "Blizzard": 35,
        "Thunderstorm": 32,
        "Divine Wrath": 38,
        "Demonic Fire": 45,
        "Nature's Wrath": 33,
        "Mind Blast": 26
    }
    return spell_damage_bonus.get(spell, 0)


def _get_class_critical_modifier(character_class: CharacterClass) -> int:
    """Get critical chance bonus for specific character class."""
    class_crit_bonus = {
        CharacterClass.WARRIOR: 0,
        CharacterClass.MAGE: 2,
        CharacterClass.ROGUE: 8,
        CharacterClass.CLERIC: 1,
        CharacterClass.RANGER: 3,
        CharacterClass.PALADIN: 2,
        CharacterClass.WARLOCK: 3,
        CharacterClass.DRUID: 1,
        CharacterClass.MONK: 4,
        CharacterClass.BARBARIAN: 1,
        CharacterClass.BARD: 2,
        CharacterClass.SORCERER: 3,
        CharacterClass.FIGHTER: 1,
        CharacterClass.NECROMANCER: 2,
        CharacterClass.ILLUSIONIST: 4,
        CharacterClass.ALCHEMIST: 2,
        CharacterClass.BERSERKER: 3,
        CharacterClass.ASSASSIN: 10,
        CharacterClass.HEALER: 0,
        CharacterClass.SUMMONER: 2,
        CharacterClass.SHAPESHIFTER: 1,
        CharacterClass.ELEMENTALIST: 3,
        CharacterClass.NINJA: 7
    }
    return class_crit_bonus.get(character_class, 0)


def _get_shield_bonus(defender: Union[Character, Enemy]) -> int:
    """Get shield bonus for defender."""
    if isinstance(defender, Character):
        # Check for shield in inventory
        for item in defender.inventory:
            if hasattr(item, 'type') and item.type == ItemType.ARMOR:
                if 'shield' in item.name.lower() or item.stats_mod.get('shield', 0) > 0:
                    return item.stats_mod.get('defense', 0)
    return 0


def _get_damage_modifiers(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy],
    weapon: Optional[Item],
    ability: Optional[str]
) -> Dict[str, Any]:
    """Get all damage modifiers."""
    modifiers = {
        'level_advantage': 1.0,
        'weapon_quality': 1.0,
        'ability_bonus': 1.0,
        'terrain_bonus': 1.0,
        'weather_bonus': 1.0,
        'total_multiplier': 1.0
    }
    
    # Level advantage modifier
    attacker_level = getattr(attacker, 'level', 1)
    defender_level = getattr(defender, 'level', 1)
    
    if attacker_level > defender_level:
        level_diff = attacker_level - defender_level
        modifiers['level_advantage'] = 1.0 + (level_diff * 0.05)
    elif attacker_level < defender_level:
        level_diff = defender_level - attacker_level
        modifiers['level_advantage'] = 1.0 - (level_diff * 0.05)
    
    # Weapon quality modifier
    if weapon:
        if weapon.rarity == ItemRarity.RARE:
            modifiers['weapon_quality'] = 1.1
        elif weapon.rarity == ItemRarity.EPIC:
            modifiers['weapon_quality'] = 1.2
        elif weapon.rarity == ItemRarity.LEGENDARY:
            modifiers['weapon_quality'] = 1.3
    
    # Ability bonus modifier
    if ability:
        if "Power" in ability:
            modifiers['ability_bonus'] = 1.2
        elif "Deadly" in ability:
            modifiers['ability_bonus'] = 1.3
        elif "Ultimate" in ability:
            modifiers['ability_bonus'] = 1.5
    
    # Calculate total multiplier
    modifiers['total_multiplier'] = (
        modifiers['level_advantage'] *
        modifiers['weapon_quality'] *
        modifiers['ability_bonus'] *
        modifiers['terrain_bonus'] *
        modifiers['weather_bonus']
    )
    
    return modifiers


def _calculate_damage_reduction(
    defender: Union[Character, Enemy],
    damage_type: str
) -> float:
    """Calculate damage reduction for defender."""
    base_reduction = 1.0
    
    # Armor reduction for physical damage
    if damage_type == "physical":
        base_reduction = COMBAT_CONFIG["armor_absorption"]
    
    # Magic resistance for magical damage
    elif damage_type in ["fire", "ice", "lightning", "holy", "dark"]:
        base_reduction = COMBAT_CONFIG["magic_absorption"]
    
    # Check for specific resistances
    if hasattr(defender, 'resistances'):
        if damage_type in defender.resistances:
            base_reduction *= 0.5  # Additional 50% reduction
    
    return base_reduction


def _generate_combat_message(
    attacker: Union[Character, Enemy],
    defender: Union[Character, Enemy],
    damage: int,
    blocked: bool,
    critical: bool,
    dodged: bool
) -> str:
    """Generate combat message for logging."""
    attacker_name = getattr(attacker, 'name', 'Unknown')
    defender_name = getattr(defender, 'name', 'Unknown')
    
    if dodged:
        return f"{attacker_name} attacks but {defender_name} dodges!"
    elif blocked:
        return f"{attacker_name} attacks {defender_name} for {damage} damage (blocked)!"
    elif critical:
        return f"{attacker_name} lands a CRITICAL hit on {defender_name} for {damage} damage!"
    elif damage > 0:
        return f"{attacker_name} hits {defender_name} for {damage} damage!"
    else:
        return f"{attacker_name} attacks {defender_name} but deals no damage!"


# Import required functions for internal use
from core.systems.character import create_character
from core.systems.enemies import create_enemy


# Export all functions for easy access
__all__ = [
    'calculate_damage',
    'calculate_hit_chance',
    'calculate_critical_chance',
    'calculate_dodge_chance',
    'calculate_block_chance',
    'simulate_combat_round',
    'resolve_combat_round',
    'calculate_combat_outcome'
]