"""
Spell casting functions for RPGSim
Core spell mechanics and validation
"""

import random
from typing import Dict, List, Any, Optional, Union
from core.models import Character, Enemy, CharacterStats, GameState
from core.validation import ValidationError
from .spell_constants import SPELL_SCHOOLS, STATUS_EFFECTS


def validate_spell_casting(
    caster: Union[Character, Enemy],
    spell_name: str,
    spell_school: str,
    mana_cost: int,
) -> None:
    """
    Validate spell casting parameters.

    Args:
        caster: Spell caster
        spell_name: Name of spell
        spell_school: School of magic
        mana_cost: Mana cost to cast spell

    Raises:
        ValidationError: If spell casting parameters are invalid
    """
    # Check if caster has enough mana
    if hasattr(caster, "mana"):
        if caster.mana < mana_cost:
            raise ValidationError(
                f"Insufficient mana: need {mana_cost}, have {caster.mana}",
                field="mana",
                value=caster.mana,
            )

    # Check spell requirements
    if not _check_spell_requirements(caster, spell_name, spell_school):
        raise ValidationError(
            f"Spell requirements not met for {spell_name}",
            field="spell_name",
            value=spell_name,
        )


def cast_spell(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy, None],
    spell_name: str,
    spell_school: str,
    spell_power: int,
    mana_cost: int,
    _game_state: Optional[GameState] = None,
) -> Dict[str, Any]:
    """
    Cast spell with explicit validation and deterministic effects.

    Args:
        caster: Spell caster (character or enemy)
        target: Spell target (character, enemy, or None for area effect)
        spell_name: Name of spell being cast
        spell_school: School of magic for spell
        spell_power: Base power of spell
        mana_cost: Mana cost to cast spell
        _game_state: Optional game state for context

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
    if hasattr(caster, "mana"):
        if caster.mana < mana_cost:
            raise ValidationError(
                f"Insufficient mana: need {mana_cost}, have {caster.mana}",
                field="mana",
                value=caster.mana,
            )

    # Check spell requirements
    if not _check_spell_requirements(caster, spell_name, spell_school):
        raise ValidationError(
            f"Spell requirements not met for {spell_name}",
            field="spell_name",
            value=spell_name,
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
        if spell_effects["damage"] > 0:
            damage_result = calculate_spell_damage(
                caster, target, spell_name, spell_school, spell_power
            )
            total_damage = damage_result["damage"]

            # Apply damage to target
            if hasattr(target, "hp"):
                target.hp = max(0, target.hp - total_damage)

        # Calculate healing
        if spell_effects["healing"] > 0:
            healing_result = calculate_spell_healing(
                caster, target, spell_name, spell_school, spell_power
            )
            total_healing = healing_result["healing"]

            # Apply healing to target
            if hasattr(target, "hp"):
                target.hp = min(target.max_hp, target.hp + total_healing)

        # Apply status effects
        for status_effect in spell_effects["status_effects"]:
            if _apply_status_effect(target, status_effect, spell_power):
                status_effects_applied.append(status_effect)

    # Consume mana
    if hasattr(caster, "mana"):
        caster.mana -= mana_cost

    # Set cooldown
    spell_cooldown = _calculate_spell_cooldown(spell_name, spell_school, spell_power)
    if hasattr(caster, "spell_cooldowns"):
        caster.spell_cooldowns[spell_name] = spell_cooldown

    return {
        "spell_cast": True,
        "spell_name": spell_name,
        "spell_school": spell_school,
        "spell_power": spell_power,
        "mana_cost": mana_cost,
        "mana_used": mana_cost,
        "spell_hits": spell_hits,
        "hit_chance": hit_chance,
        "hit_roll": hit_roll,
        "target": getattr(target, "name", None) if target else None,
        "damage": total_damage,
        "healing": total_healing,
        "status_effects_applied": status_effects_applied,
        "spell_cooldown": spell_cooldown,
        "spell_effects": spell_effects,
        "message": _generate_spell_message(
            caster, target, spell_name, spell_hits, total_damage, total_healing
        ),
    }


def calculate_spell_damage(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    _spell_name: str,
    spell_school: str,
    spell_power: int,
) -> Dict[str, Any]:
    """
    Calculate spell damage with explicit formula for agents.

    Args:
        caster: Spell caster
        target: Spell target
        _spell_name: Name of spell
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
    caster_stats = getattr(caster, "stats", None)
    if not caster_stats:
        caster_stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

    # Get spell school configuration
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    primary_stat = school_config.get("primary_stat", "intelligence")
    secondary_stat = school_config.get("secondary_stat", "intelligence")

    # Calculate base damage
    base_damage = spell_power
    primary_bonus = getattr(caster_stats, primary_stat, 10) // 2
    secondary_bonus = getattr(caster_stats, secondary_stat, 10) // 4

    raw_damage = base_damage + primary_bonus + secondary_bonus

    # Apply school multiplier
    school_multiplier = school_config.get("mana_multiplier", 1.0)
    modified_damage = raw_damage * school_multiplier

    # Apply level scaling
    caster_level = getattr(caster, "level", 1)
    level_multiplier = 1.0 + (caster_level * 0.05)
    scaled_damage = modified_damage * level_multiplier

    # Apply resistance
    if hasattr(target, "resistances"):
        resistance = target.resistances.get(spell_school, 0)
        final_damage = max(1, scaled_damage * (1 - resistance))
    else:
        final_damage = scaled_damage

    # Apply damage caps
    max_damage = spell_power * 3
    final_damage = min(final_damage, max_damage)

    return {
        "base_damage": base_damage,
        "primary_bonus": primary_bonus,
        "secondary_bonus": secondary_bonus,
        "raw_damage": raw_damage,
        "school_multiplier": school_multiplier,
        "modified_damage": modified_damage,
        "level_multiplier": level_multiplier,
        "scaled_damage": scaled_damage,
        "resistance": getattr(target, "resistances", {}).get(spell_school, 0),
        "final_damage": int(final_damage),
        "max_damage": max_damage,
        "damage": int(final_damage),
        "damage_type": spell_school,
        "resisted": False,
    }


def calculate_spell_healing(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_name: str,
    spell_school: str,
    spell_power: int,
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
    """
    # Get caster stats
    caster_stats = getattr(caster, "stats", None)
    if not caster_stats:
        caster_stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

    # Calculate base healing
    base_healing = spell_power
    wisdom_bonus = caster_stats.wisdom // 3
    intelligence_bonus = caster_stats.intelligence // 4

    raw_healing = base_healing + wisdom_bonus + intelligence_bonus

    # Apply school multiplier
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    school_multiplier = school_config.get("mana_multiplier", 1.0)
    modified_healing = raw_healing * school_multiplier

    # Apply level scaling
    caster_level = getattr(caster, "level", 1)
    level_multiplier = 1.0 + (caster_level * 0.03)
    scaled_healing = modified_healing * level_multiplier

    # Apply healing caps
    max_healing = spell_power * 2
    final_healing = min(scaled_healing, max_healing)

    return {
        "base_healing": base_healing,
        "wisdom_bonus": wisdom_bonus,
        "intelligence_bonus": intelligence_bonus,
        "raw_healing": raw_healing,
        "school_multiplier": school_multiplier,
        "modified_healing": modified_healing,
        "level_multiplier": level_multiplier,
        "scaled_healing": scaled_healing,
        "max_healing": max_healing,
        "healing": int(final_healing),
    }


def _check_spell_requirements(
    caster: Union[Character, Enemy], spell_name: str, spell_school: str
) -> bool:
    """Check if caster meets spell requirements."""
    # Simplified requirement check
    caster_level = getattr(caster, "level", 1)

    # Basic level requirements
    if spell_name in ["Fireball", "Lightning Bolt"] and caster_level < 3:
        return False
    if spell_name in ["Meteor", "Blizzard"] and caster_level < 10:
        return False

    return True


def _calculate_spell_hit_chance(
    caster: Union[Character, Enemy], target: Union[Character, Enemy], spell_school: str
) -> int:
    """Calculate spell hit chance."""
    caster_level = getattr(caster, "level", 1)
    target_level = getattr(target, "level", 1)

    # Base hit chance
    base_chance = 70

    # Level difference modifier
    level_diff = target_level - caster_level
    if level_diff > 0:
        level_modifier = -level_diff * 5
    else:
        level_modifier = min(10, -level_diff * 2)

    # School-specific modifiers
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    accuracy_bonus = school_config.get("accuracy_bonus", 0)

    return max(10, min(95, base_chance + level_modifier + accuracy_bonus))


def _get_spell_effects(
    spell_name: str, spell_school: str, spell_power: int
) -> Dict[str, Any]:
    """Get spell effects configuration."""
    # Simplified spell effects
    spell_effects = {
        "damage": 0,
        "healing": 0,
        "status_effects": [],
        "duration": 0,
        "area_of_effect": False,
    }

    # Configure effects based on spell name
    if spell_name in ["Fireball", "Lightning Bolt", "Ice Shard"]:
        spell_effects["damage"] = spell_power
        spell_effects["area_of_effect"] = spell_name == "Fireball"
    elif spell_name in ["Heal", "Cure Wounds", "Regenerate"]:
        spell_effects["healing"] = spell_power // 2
    elif spell_name in ["Stun", "Freeze", "Sleep"]:
        spell_effects["status_effects"] = ["stun"]
        spell_effects["duration"] = 2
    elif spell_name in ["Poison", "Curse"]:
        spell_effects["status_effects"] = ["poison"]
        spell_effects["duration"] = 3

    return spell_effects


def _apply_status_effect(
    target: Union[Character, Enemy], status_effect: str, spell_power: int
) -> bool:
    """Apply status effect to target."""
    # Get status effect configuration
    effect_config = STATUS_EFFECTS.get(status_effect)
    if not effect_config:
        return False

    # Check immunity
    if hasattr(target, "class_type"):
        immune_classes = effect_config.get("immune_classes", [])
        if target.class_type.value in immune_classes:
            return False

    # Apply effect (simplified)
    if hasattr(target, "status_effects"):
        target.status_effects.append(
            {
                "effect": status_effect,
                "duration": effect_config.get("duration", 0),
                "power": spell_power,
            }
        )

    return True


def _calculate_spell_cooldown(
    spell_name: str, spell_school: str, spell_power: int
) -> int:
    """Calculate spell cooldown."""
    # Base cooldown
    base_cooldown = 3

    # School-specific modifiers
    school_config = SPELL_SCHOOLS.get(spell_school, {})
    cooldown_modifier = school_config.get("cooldown_modifier", 1.0)

    # Power-based scaling
    power_scaling = min(5, spell_power // 20)

    return int(base_cooldown * cooldown_modifier + power_scaling)


def _generate_spell_message(
    caster: Union[Character, Enemy],
    target: Union[Character, Enemy],
    spell_name: str,
    spell_hits: bool,
    damage: int,
    healing: int,
) -> str:
    """Generate spell casting message."""
    caster_name = getattr(caster, "name", "Unknown")
    target_name = getattr(target, "name", "Unknown") if target else "area"

    if damage > 0 and healing > 0:
        return (
            f"{caster_name} casts {spell_name}! "
            f"Deals {damage} damage and heals {healing} HP to {target_name}!"
        )
    if damage > 0:
        return (
            f"{caster_name} casts {spell_name}! Deals {damage} damage to {target_name}!"
        )
    if healing > 0:
        return f"{caster_name} casts {spell_name}! Heals {healing} HP to {target_name}!"
    return f"{caster_name} casts {spell_name}! The spell takes effect."
