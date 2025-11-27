"""
Spell System for RPGSim
Optimized for LLM agents with explicit, deterministic spell casting
"""

import random
from typing import Dict, List, Any, Optional, Union
from core.models import (
    Character, CharacterStats,
    Enemy,
    GameState
)
from core.validation import ValidationError


def cast_spell(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy, None],
    spell_name: str,
    spell_school: str,
    spell_power: int,
    mana_cost: int,
    game_state: Optional[GameState] = None
) -> Dict[str, Any]:
    """
    Cast spell with explicit validation and deterministic effects.

    Args:
        caster: Spell caster (character or enemy)
        target: Spell target (character, enemy, or None for area effect)
        spell_name: Name of spell being cast
        spell_school: School of magic for the spell
        spell_power: Base power of the spell
        mana_cost: Mana cost to cast the spell
        game_state: Optional game state for context

    Returns:
        Dict[str, Any]: Spell casting results

    Raises:
        ValidationError: If spell casting parameters are invalid

    Examples:
        >>> caster = create_character("Mage", CharacterClass.MAGE)
        >>> target = create_enemy("Goblin", 2)
        >>> result = cast_spell(caster, target, "Fireball", "fire", 30, 20)
        >>> result['spell_cast']
        True
        >>> result['damage']
        45
        >>> result['mana_used']
        20
        >>> result['spell_name']
        'Fireball'
        >>> result['spell_school']
        'fire'
    """
    # Validate spell casting parameters
    validate_spell_casting(caster, spell_name, spell_school, mana_cost)

    # Check if caster has enough mana
    if hasattr(caster, 'mana'):
        if caster.mana < mana_cost:
            raise ValidationError(
                f"Insufficient mana: need {mana_cost}, have {caster.mana}",
                field='mana', value=caster.mana
            )

    # Check spell requirements
    if not _check_spell_requirements(caster, spell_name, spell_school):
        raise ValidationError(
            f"Spell requirements not met for {spell_name}",
            field='spell_name', value=spell_name
        )

    # Calculate spell hit chance
    hit_chance = _calculate_spell_hit_chance(caster, target, spell_school)
    hit_roll = random.randint(1, 100)
    spell_hits = hit_roll <= hit_chance

    # Calculate spell effects
    spell_effects = _get_spell_effects(spell_name, spell_school, spell_power)

    # Apply spell effects
    total_damage = 0
    total_healing = 0
    status_effects_applied = []

    if spell_hits and target:
        # Calculate damage
        if spell_effects['damage'] > 0:
            damage_result = calculate_spell_damage(caster, target, spell_name, spell_school, spell_power)
            total_damage = damage_result['damage']

            # Apply damage to target
            if hasattr(target, 'hp'):
                target.hp = max(0, target.hp - total_damage)

        # Calculate healing
        if spell_effects['healing'] > 0:
            healing_result = calculate_spell_healing(caster, target, spell_name, spell_school, spell_power)
            total_healing = healing_result['healing']

            # Apply healing to target
            if hasattr(target, 'hp'):
                target.hp = min(target.max_hp, target.hp + total_healing)

        # Apply status effects
        for status_effect in spell_effects['status_effects']:
            if _apply_status_effect(target, status_effect, spell_power):
                status_effects_applied.append(status_effect)

    # Consume mana
    if hasattr(caster, 'mana'):
        caster.mana -= mana_cost

    # Set cooldown
    spell_cooldown = _calculate_spell_cooldown(spell_name, spell_school, spell_power)
    if hasattr(caster, 'spell_cooldowns'):
        caster.spell_cooldowns[spell_name] = spell_cooldown

    return {
        'spell_cast': True,
        'spell_name': spell_name,
        'spell_school': spell_school,
        'spell_power': spell_power,
        'mana_cost': mana_cost,
        'mana_used': mana_cost,
        'spell_hits': spell_hits,
        'hit_chance': hit_chance,
        'hit_roll': hit_roll,
        'target': getattr(target, 'name', None) if target else None,
        'damage': total_damage,
        'healing': total_healing,
        'status_effects_applied': status_effects_applied,
        'spell_cooldown': spell_cooldown,
        'spell_effects': spell_effects,
        'message': _generate_spell_message(caster, target, spell_name, spell_hits, total_damage, total_healing)
    }


def calculate_spell_damage(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_name: str,
    spell_school: str,
    spell_power: int
) -> Dict[str, Any]:
    """
    Calculate spell damage with explicit formula for agents.

    Args:
        caster: Spell caster
        target: Spell target
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell

    Returns:
        Dict[str, Any]: Spell damage calculation details

    Examples:
        >>> caster = create_character("Mage", CharacterClass.MAGE)
        >>> target = create_enemy("Goblin", 2)
        >>> damage = calculate_spell_damage(caster, target, "Fireball", "fire", 30)
        >>> damage['damage']
        45
        >>> damage['damage_type']
        'fire'
        >>> damage['resisted']
        False
    """
    # Get caster stats
    caster_stats = getattr(caster, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))

    # Get spell school configuration
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    primary_stat = school_config.get('primary_stat', 'intelligence')
    secondary_stat = school_config.get('secondary_stat', 'intelligence')

    # Calculate base damage
    base_damage = spell_power
    primary_bonus = getattr(caster_stats, primary_stat, 10) // 2
    secondary_bonus = getattr(caster_stats, secondary_stat, 10) // 4

    raw_damage = base_damage + primary_bonus + secondary_bonus

    # Apply school multiplier
    school_multiplier = school_config.get('mana_multiplier', 1.0)
    modified_damage = raw_damage * school_multiplier

    # Apply level scaling
    caster_level = getattr(caster, 'level', 1)
    level_multiplier = 1.0 + (caster_level * 0.05)
    scaled_damage = modified_damage * level_multiplier

    # Apply spell resistance
    target_resistance = _get_spell_resistance(target, spell_school)
    resisted_damage = scaled_damage * target_resistance

    # Calculate final damage
    final_damage = int(resisted_damage)
    final_damage = max(final_damage, 1)  # Minimum 1 damage
    final_damage = min(final_damage, 999)  # Maximum damage cap

    # Get damage type from spell school
    damage_type = school_config.get('damage_type', 'magical')

    return {
        'damage': final_damage,
        'raw_damage': raw_damage,
        'modified_damage': modified_damage,
        'scaled_damage': scaled_damage,
        'resisted_damage': resisted_damage,
        'damage_type': damage_type,
        'resistance': target_resistance,
        'resisted': target_resistance < 1.0,
        'base_damage': base_damage,
        'primary_bonus': primary_bonus,
        'secondary_bonus': secondary_bonus,
        'school_multiplier': school_multiplier,
        'level_multiplier': level_multiplier
    }


def calculate_spell_healing(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_name: str,
    spell_school: str,
    spell_power: int
) -> Dict[str, Any]:
    """
    Calculate spell healing with explicit formula for agents.

    Args:
        caster: Spell caster
        target: Spell target
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell

    Returns:
        Dict[str, Any]: Spell healing calculation details

    Examples:
        >>> caster = create_character("Cleric", CharacterClass.CLERIC)
        >>> target = create_character("Warrior", CharacterClass.WARRIOR)
        >>> target.hp = 50
        >>> target.max_hp = 100
        >>> healing = calculate_spell_healing(caster, target, "Heal", "holy", 25)
        >>> healing['healing']
        35
        >>> healing['healing_type']
        'holy'
    """
    # Get caster stats
    caster_stats = getattr(caster, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))

    # Get spell school configuration
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    primary_stat = school_config.get('primary_stat', 'wisdom')
    secondary_stat = school_config.get('secondary_stat', 'charisma')

    # Calculate base healing
    base_healing = spell_power
    primary_bonus = getattr(caster_stats, primary_stat, 10) // 2
    secondary_bonus = getattr(caster_stats, secondary_stat, 10) // 4

    raw_healing = base_healing + primary_bonus + secondary_bonus

    # Apply school multiplier
    school_multiplier = school_config.get('mana_multiplier', 1.0)
    modified_healing = raw_healing * school_multiplier

    # Apply level scaling
    caster_level = getattr(caster, 'level', 1)
    level_multiplier = 1.0 + (caster_level * 0.03)
    scaled_healing = modified_healing * level_multiplier

    # Apply healing bonus (healing is more effective than damage)
    healing_bonus = 1.2
    final_healing = int(scaled_healing * healing_bonus)

    # Cap healing at target's missing HP
    if hasattr(target, 'hp') and hasattr(target, 'max_hp'):
        missing_hp = target.max_hp - target.hp
        final_healing = min(final_healing, missing_hp)

    final_healing = max(final_healing, 0)  # Minimum 0 healing

    return {
        'healing': final_healing,
        'raw_healing': raw_healing,
        'modified_healing': modified_healing,
        'scaled_healing': scaled_healing,
        'healing_type': school_config.get('damage_type', 'holy'),
        'base_healing': base_healing,
        'primary_bonus': primary_bonus,
        'secondary_bonus': secondary_bonus,
        'school_multiplier': school_multiplier,
        'level_multiplier': level_multiplier,
        'healing_bonus': healing_bonus
    }


def calculate_spell_cost(
    spell_name: str,
    spell_school: str,
    spell_power: int,
    caster_level: int = 1
) -> Dict[str, Any]:
    """
    Calculate spell mana cost with explicit formula for agents.

    Args:
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell
        caster_level: Level of spell caster

    Returns:
        Dict[str, Any]: Spell cost calculation details

    Examples:
        >>> cost = calculate_spell_cost("Fireball", "fire", 30, 5)
        >>> cost['mana_cost']
        24
        >>> cost['base_cost']
        30
        >>> cost['level_reduction']
        5
    """
    # Get spell school configuration
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    difficulty = school_config.get('difficulty', 3)
    mana_multiplier = school_config.get('mana_multiplier', 1.0)

    # Calculate base mana cost
    base_cost = spell_power * difficulty

    # Apply school multiplier
    school_cost = int(base_cost * mana_multiplier)

    # Apply level reduction
    level_reduction = max(0, (caster_level - 1) // 5 * 2)
    reduced_cost = school_cost - level_reduction

    # Apply spell-specific cost modifiers
    cost_modifier = _get_spell_cost_modifier(spell_name)
    final_cost = int(reduced_cost * cost_modifier)

    # Ensure minimum cost
    final_cost = max(final_cost, 1)

    # Ensure maximum cost
    final_cost = min(final_cost, 500)

    return {
        'mana_cost': final_cost,
        'base_cost': base_cost,
        'school_cost': school_cost,
        'reduced_cost': reduced_cost,
        'cost_modifier': cost_modifier,
        'level_reduction': level_reduction,
        'difficulty': difficulty,
        'school_multiplier': mana_multiplier
    }


def get_spell_effects(
    spell_name: str,
    spell_school: str,
    spell_power: int
) -> Dict[str, Any]:
    """
    Get spell effects with explicit description for agents.

    Args:
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell

    Returns:
        Dict[str, Any]: Spell effects details

    Examples:
        >>> effects = get_spell_effects("Fireball", "fire", 30)
        >>> effects['damage']
        30
        >>> effects['status_effects']
        ['burn']
        >>> effects['area_of_effect']
        True
    """
    # Get spell configuration
    spell_config = _get_spell_configuration(spell_name, spell_school)

    if spell_config:
        return {
            'damage': spell_config.get('damage', 0),
            'healing': spell_config.get('healing', 0),
            'status_effects': spell_config.get('status_effects', []),
            'area_of_effect': spell_config.get('area_of_effect', False),
            'duration': spell_config.get('duration', 0),
            'range': spell_config.get('range', 1),
            'radius': spell_config.get('radius', 0),
            'description': spell_config.get('description', ''),
            'target_type': spell_config.get('target_type', 'enemy'),
            'casting_time': spell_config.get('casting_time', 1),
            'components': spell_config.get('components', [])
        }

    # Default spell effects
    return {
        'damage': spell_power,
        'healing': 0,
        'status_effects': [],
        'area_of_effect': False,
        'duration': 0,
        'range': 1,
        'radius': 0,
        'description': f'A {spell_school} spell that deals {spell_power} damage',
        'target_type': 'enemy',
        'casting_time': 1,
        'components': ['verbal']
    }


def apply_spell_effects(
    target: Union[Character, Enemy],
    spell_effects: Dict[str, Any],
    spell_power: int,
    caster: Optional[Union[Character, Enemy]] = None
) -> Dict[str, Any]:
    """
    Apply spell effects to target with explicit logic for agents.

    Args:
        target: Spell target
        spell_effects: Spell effects to apply
        spell_power: Power of spell for effect calculation
        caster: Optional spell caster

    Returns:
        Dict[str, Any]: Applied effects details

    Examples:
        >>> target = create_character("Warrior", CharacterClass.WARRIOR)
        >>> effects = get_spell_effects("Poison Cloud", "nature", 20)
        >>> applied = apply_spell_effects(target, effects, 20)
        >>> applied['status_effects_applied']
        ['poison']
    """
    applied_effects = {
        'damage_applied': 0,
        'healing_applied': 0,
        'status_effects_applied': [],
        'failed_effects': []
    }

    # Apply damage
    if spell_effects['damage'] > 0 and target:
        damage_applied = spell_effects['damage']
        if hasattr(target, 'hp'):
            old_hp = target.hp
            target.hp = max(0, target.hp - damage_applied)
            applied_effects['damage_applied'] = damage_applied
            applied_effects['old_hp'] = old_hp
            applied_effects['new_hp'] = target.hp
            applied_effects['hp_change'] = old_hp - target.hp

    # Apply healing
    if spell_effects['healing'] > 0 and target:
        healing_applied = spell_effects['healing']
        if hasattr(target, 'hp') and hasattr(target, 'max_hp'):
            old_hp = target.hp
            target.hp = min(target.max_hp, target.hp + healing_applied)
            applied_effects['healing_applied'] = healing_applied
            applied_effects['old_hp'] = old_hp
            applied_effects['new_hp'] = target.hp
            applied_effects['hp_change'] = target.hp - old_hp

    # Apply status effects
    for status_effect in spell_effects['status_effects']:
        if target and _apply_status_effect(target, status_effect, spell_power, caster):
            applied_effects['status_effects_applied'].append(status_effect)
        else:
            applied_effects['failed_effects'].append(status_effect)

    return applied_effects


def calculate_spell_duration(
    spell_name: str,
    spell_school: str,
    spell_power: int,
    caster_level: int = 1
) -> Dict[str, Any]:
    """
    Calculate spell duration with explicit formula for agents.

    Args:
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell
        caster_level: Level of spell caster

    Returns:
        Dict[str, Any]: Spell duration calculation details

    Examples:
        >>> duration = calculate_spell_duration("Shield", "holy", 15, 5)
        >>> duration['duration']
        3
        >>> duration['base_duration']
        1
        >>> duration['level_bonus']
        2
    """
    # Get spell configuration
    spell_config = _get_spell_configuration(spell_name, spell_school)

    # Base duration
    base_duration = spell_config.get('duration', 0) if spell_config else 0

    # Duration scaling based on spell power
    power_scaling = spell_power // 20

    # Level bonus
    level_bonus = (caster_level - 1) // 3

    # School bonus
    school_bonus = 0
    if spell_school == 'holy':
        school_bonus = 1
    elif spell_school == 'dark':
        school_bonus = 2

    # Calculate total duration
    total_duration = base_duration + power_scaling + level_bonus + school_bonus

    # Apply duration caps
    total_duration = max(total_duration, 0)
    total_duration = min(total_duration, 20)  # Maximum 20 rounds

    return {
        'duration': total_duration,
        'base_duration': base_duration,
        'power_scaling': power_scaling,
        'level_bonus': level_bonus,
        'school_bonus': school_bonus
    }


def get_spell_range(
    spell_name: str,
    spell_school: str,
    spell_power: int
) -> Dict[str, Any]:
    """
    Get spell range with explicit calculation for agents.

    Args:
        spell_name: Name of spell
        spell_school: School of magic
        spell_power: Base power of spell

    Returns:
        Dict[str, Any]: Spell range details

    Examples:
        >>> spell_range = get_spell_range("Fireball", "fire", 30)
        >>> spell_range['range']
        5
        >>> spell_range['range_type']
        'ranged'
    """
    # Get spell configuration
    spell_config = _get_spell_configuration(spell_name, spell_school)

    # Base range
    base_range = spell_config.get('range', 1) if spell_config else 1

    # Range scaling based on spell power
    power_scaling = spell_power // 25

    # School range modifier
    school_modifier = 1.0
    if spell_school == 'fire':
        school_modifier = 1.2  # Fire spells have better range
    elif spell_school == 'ice':
        school_modifier = 0.8  # Ice spells have shorter range
    elif spell_school == 'lightning':
        school_modifier = 1.5  # Lightning spells have excellent range

    # Calculate total range
    total_range = int((base_range + power_scaling) * school_modifier)

    # Apply range caps
    total_range = max(total_range, 1)
    total_range = min(total_range, 50)  # Maximum 50 units

    # Determine range type
    if total_range <= 1:
        range_type = 'melee'
    elif total_range <= 5:
        range_type = 'short'
    elif total_range <= 15:
        range_type = 'medium'
    elif total_range <= 30:
        range_type = 'long'
    else:
        range_type = 'extreme'

    return {
        'range': total_range,
        'base_range': base_range,
        'power_scaling': power_scaling,
        'school_modifier': school_modifier,
        'range_type': range_type
    }


# Helper functions for spell system
def _check_spell_requirements(
    caster: Union[Character, Enemy],
    spell_name: str,
    spell_school: str
) -> bool:
    """Check if caster meets spell requirements."""
    # Check level requirement
    spell_config = _get_spell_configuration(spell_name, spell_school)
    if spell_config:
        level_requirement = spell_config.get('level_requirement', 1)
        caster_level = getattr(caster, 'level', 1)

        if caster_level < level_requirement:
            return False

    # Check class requirement
    if spell_config:
        class_requirement = spell_config.get('class_requirement')
        if class_requirement:
            if isinstance(caster, Character):
                if caster.class_type.value != class_requirement:
                    return False

    # Check stat requirement
    if spell_config:
        stat_requirement = spell_config.get('stat_requirement')
        if stat_requirement:
            caster_stats = getattr(caster, 'stats', CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10))
            stat_name, stat_value = stat_requirement

            if hasattr(caster_stats, stat_name):
                caster_stat_value = getattr(caster_stats, stat_name)
                if caster_stat_value < stat_value:
                    return False

    return True


def _calculate_spell_hit_chance(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_school: str
) -> int:
    """Calculate spell hit chance."""
    # Get school configuration
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    difficulty = school_config.get('difficulty', 3)

    # Base hit chance depends on difficulty
    base_hit = 100 - (difficulty * 5)

    # Caster level bonus
    caster_level = getattr(caster, 'level', 1)
    level_bonus = min(caster_level, 20)

    # Target resistance
    target_resistance = _get_spell_resistance(target, spell_school)
    resistance_penalty = (1.0 - target_resistance) * 20

    # Calculate final hit chance
    hit_chance = base_hit + level_bonus - resistance_penalty

    # Apply bounds
    hit_chance = max(25, hit_chance)
    hit_chance = min(95, hit_chance)

    return int(hit_chance)


def _get_spell_resistance(
    target: Union[Character, Enemy],
    spell_school: str
) -> float:
    """Get target's resistance to spell school."""
    # Get damage type from spell school
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    damage_type = school_config.get('damage_type', 'magical')

    # Check target's resistances
    if hasattr(target, 'resistances'):
        return target.resistances.get(damage_type, 1.0)

    # Default resistance
    return 1.0


def _apply_status_effect(
    target: Union[Character, Enemy],
    status_effect: str,
    spell_power: int,
    caster: Optional[Union[Character, Enemy]] = None
) -> bool:
    """Apply status effect to target."""
    if not hasattr(target, 'status_effects'):
        return False

    # Get status effect configuration
    effect_config = STATUS_EFFECTS.get(status_effect)
    if not effect_config:
        return False

    # Check immunity
    if isinstance(target, Character):
        immune_classes = effect_config.get('immune_classes', [])
        if target.class_type.value in immune_classes:
            return False

    # Calculate effect duration
    base_duration = effect_config.get('duration', 3)
    power_duration = spell_power // 10
    total_duration = base_duration + power_duration

    # Apply status effect
    target.status_effects[status_effect] = {
        'duration': total_duration,
        'damage_per_round': effect_config.get('damage_per_round', 0),
        'stackable': effect_config.get('stackable', False),
        'applied_by': getattr(caster, 'name', 'Unknown') if caster else 'Unknown',
        'applied_at': None  # Would be timestamp in real implementation
    }

    return True


def _get_spell_configuration(spell_name: str, spell_school: str) -> Optional[Dict[str, Any]]:
    """Get spell configuration."""
    # Spell configurations database
    spell_configurations = {
        "fireball": {
            'damage': 30,
            'status_effects': ['burn'],
            'area_of_effect': True,
            'duration': 0,
            'range': 5,
            'radius': 2,
            'description': 'Hurls a fiery explosion at target',
            'target_type': 'enemy',
            'casting_time': 2,
            'components': ['verbal', 'somatic'],
            'level_requirement': 3,
            'class_requirement': None,
            'stat_requirement': None
        },
        "ice_lance": {
            'damage': 25,
            'status_effects': ['freeze'],
            'area_of_effect': False,
            'duration': 2,
            'range': 4,
            'radius': 0,
            'description': 'Launches a shard of ice at target',
            'target_type': 'enemy',
            'casting_time': 1,
            'components': ['verbal', 'somatic'],
            'level_requirement': 2,
            'class_requirement': None,
            'stat_requirement': None
        },
        "lightning_bolt": {
            'damage': 40,
            'status_effects': ['stun'],
            'area_of_effect': False,
            'duration': 1,
            'range': 8,
            'radius': 0,
            'description': 'Calls down a bolt of lightning',
            'target_type': 'enemy',
            'casting_time': 1,
            'components': ['verbal', 'somatic'],
            'level_requirement': 5,
            'class_requirement': None,
            'stat_requirement': None
        },
        "heal": {
            'damage': 0,
            'healing': 25,
            'status_effects': [],
            'area_of_effect': False,
            'duration': 0,
            'range': 1,
            'radius': 0,
            'description': 'Restores health to target',
            'target_type': 'ally',
            'casting_time': 1,
            'components': ['verbal', 'somatic'],
            'level_requirement': 2,
            'class_requirement': None,
            'stat_requirement': None
        },
        "holy_light": {
            'damage': 35,
            'healing': 20,
            'status_effects': [],
            'area_of_effect': True,
            'duration': 0,
            'range': 6,
            'radius': 3,
            'description': 'Radiant holy light damages enemies and heals allies',
            'target_type': 'both',
            'casting_time': 2,
            'components': ['verbal', 'somatic', 'divine_focus'],
            'level_requirement': 4,
            'class_requirement': 'cleric',
            'stat_requirement': None
        },
        "poison_cloud": {
            'damage': 20,
            'status_effects': ['poison'],
            'area_of_effect': True,
            'duration': 3,
            'range': 3,
            'radius': 2,
            'description': 'Creates a cloud of poisonous gas',
            'target_type': 'enemy',
            'casting_time': 2,
            'components': ['verbal', 'somatic', 'material'],
            'level_requirement': 3,
            'class_requirement': None,
            'stat_requirement': None
        },
        "shield": {
            'damage': 0,
            'healing': 0,
            'status_effects': ['defense_boost'],
            'area_of_effect': False,
            'duration': 5,
            'range': 1,
            'radius': 0,
            'description': 'Creates a magical shield that reduces damage',
            'target_type': 'ally',
            'casting_time': 1,
            'components': ['verbal', 'somatic'],
            'level_requirement': 1,
            'class_requirement': None,
            'stat_requirement': None
        },
        "teleport": {
            'damage': 0,
            'healing': 0,
            'status_effects': [],
            'area_of_effect': False,
            'duration': 0,
            'range': 10,
            'radius': 0,
            'description': 'Instantly transports caster to another location',
            'target_type': 'self',
            'casting_time': 3,
            'components': ['verbal', 'somatic'],
            'level_requirement': 6,
            'class_requirement': 'mage',
            'stat_requirement': ('intelligence', 15)
        }
    }

    return spell_configurations.get(spell_name)


def _get_spell_cost_modifier(spell_name: str) -> float:
    """Get spell cost modifier."""
    cost_modifiers = {
        "fireball": 1.2,
        "lightning_bolt": 1.5,
        "holy_light": 1.3,
        "teleport": 2.0,
        "shield": 0.8,
        "heal": 0.9
    }

    return cost_modifiers.get(spell_name, 1.0)


def _calculate_spell_cooldown(spell_name: str, spell_school: str, spell_power: int) -> int:
    """Calculate spell cooldown."""
    # Base cooldown
    base_cooldown = 3

    # Spell-specific cooldowns
    spell_cooldowns = {
        "fireball": 2,
        "lightning_bolt": 3,
        "heal": 1,
        "shield": 4,
        "teleport": 10
    }

    base_cooldown = spell_cooldowns.get(spell_name, base_cooldown)

    # Power scaling
    power_cooldown = spell_power // 50

    # School modifier
    school_modifier = 1.0
    if spell_school == 'fire':
        school_modifier = 0.8  # Fire spells have shorter cooldown
    elif spell_school == 'holy':
        school_modifier = 1.2  # Holy spells have longer cooldown

    # Calculate final cooldown
    final_cooldown = int((base_cooldown + power_cooldown) * school_modifier)

    # Apply bounds
    final_cooldown = max(final_cooldown, 1)
    final_cooldown = min(final_cooldown, 20)

    return final_cooldown


def _generate_spell_message(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_name: str,
    spell_hits: bool,
    damage: int,
    healing: int
) -> str:
    """Generate spell casting message."""
    caster_name = getattr(caster, 'name', 'Unknown')
    target_name = getattr(target, 'name', None) if target else None

    if not spell_hits:
        return f"{caster_name} casts {spell_name} but it misses!"
    elif damage > 0 and healing > 0:
        return f"{caster_name} casts {spell_name}! Deals {damage} damage and heals {healing} HP to {target_name}!"
    elif damage > 0:
        return f"{caster_name} casts {spell_name}! Deals {damage} damage to {target_name}!"
    elif healing > 0:
        return f"{caster_name} casts {spell_name}! Heals {healing} HP to {target_name}!"
    else:
        return f"{caster_name} casts {spell_name}! The spell takes effect."


# Import required functions for internal use
from core.systems.character import create_character
from core.systems.enemies import create_enemy


# Export all functions for easy access
__all__ = [
    'cast_spell',
    'calculate_spell_damage',
    'calculate_spell_healing',
    'calculate_spell_cost',
    'get_spell_effects',
    'apply_spell_effects',
    'calculate_spell_duration',
    'get_spell_range'
]
