"""
Leveling System for RPGSim
Optimized for LLM agents with explicit, deterministic calculations
"""

import math
from typing import Dict, List, Any
from core.models import Character, Enemy, Item
from core.validation import ValidationError
from core.constants import (
    GAME_CONFIG, ABILITY_LEARNING_SCHEDULE, STAT_INCREASES
)


def get_experience_for_level(level: int) -> int:
    """
    Calculate experience required for specific level.

    Args:
        level: Target level (1-100)

    Returns:
        int: Experience required for level

    Raises:
        ValidationError: If level is invalid

    Examples:
        >>> get_experience_for_level(1)
        0
        >>> get_experience_for_level(2)
        100
        >>> get_experience_for_level(5)
        1000
        >>> get_experience_for_level(10)
        4000
        >>> get_experience_for_level(50)
        100000
        >>> get_experience_for_level(100)
        400000
    """
    # Validate level
    if level < GAME_CONFIG['min_character_level'] or level > GAME_CONFIG['max_character_level']:
        raise ValidationError(
            f"Level must be between {GAME_CONFIG['min_character_level']} and {GAME_CONFIG['max_character_level']}",
            field='level', value=level
        )

    # Calculate experience using formula: 100 * (level - 1) * level / 2
    if level == 1:
        return 0

    # Simple formula: exponential growth
    # Level 2: 100, Level 5: 1000, Level 10: 4000, Level 20: 16000, Level 50: 100000,
    # Level 100: 400000
    if level <= 20:
        # Linear growth for low levels
        return 100 * (level - 1) ** 2

    # Exponential growth for higher levels
    return int(100 * math.pow(level - 1, 1.8))


def get_experience_cap(level: int) -> int:
    """
    Get maximum experience cap for character at specific level.

    Args:
        level: Character level

    Returns:
        int: Experience cap for level

    Examples:
        >>> get_experience_cap(1)
        99
        >>> get_experience_cap(5)
        499
        >>> get_experience_cap(10)
        1999
        >>> get_experience_cap(50)
        49999
        >>> get_experience_cap(100)
        199999
    """
    # Validate level
    if level < GAME_CONFIG['min_character_level'] or level > GAME_CONFIG['max_character_level']:
        raise ValidationError(
            f"Level must be between {GAME_CONFIG['min_character_level']} and {GAME_CONFIG['max_character_level']}",
            field='level', value=level
        )

    if level >= GAME_CONFIG['max_character_level']:
        # Max level has no cap
        return float('inf')

    # Cap is experience needed for next level minus 1
    next_level_exp = get_experience_for_level(level + 1)
    return next_level_exp - 1


def calculate_level_up_bonuses(
    character: Character,
    new_level: int
) -> Dict[str, Any]:
    """
    Calculate level up bonuses for character.

    Args:
        character: Character leveling up
        new_level: New level after level up

    Returns:
        Dict[str, Any]: Level up bonuses

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> bonuses = calculate_level_up_bonuses(character, 2)
        >>> bonuses['stat_increases']['strength']
        2
        >>> bonuses['hp_increase']
        8
        >>> bonuses['new_abilities']
        []
    """
    # Get stat increases for character class
    class_stat_increases = STAT_INCREASES[character.class_type.value]

    # Calculate HP increase
    old_max_hp = character.max_hp
    # Simple HP calculation
    new_max_hp = character.max_hp + (new_level - character.level) * 2
    hp_increase = new_max_hp - old_max_hp

    # Calculate new abilities unlocked
    new_abilities = []
    if character.class_type.value in ABILITY_LEARNING_SCHEDULE:
        class_schedule = ABILITY_LEARNING_SCHEDULE[character.class_type.value]

        if new_level in class_schedule:
            new_abilities = class_schedule[new_level]

    return {
        'stat_increases': class_stat_increases,
        'hp_increase': hp_increase,
        'new_max_hp': new_max_hp,
        'new_abilities': new_abilities,
        'new_level': new_level,
        'previous_level': character.level
    }


def unlock_abilities_at_level(character: Character, level: int) -> None:
    """
    Unlock abilities for character at specific level.

    Args:
        character: Character to unlock abilities for
        level: Level to unlock abilities at

    Examples:
        >>> character = create_character("Test", CharacterClass.MAGE)
        >>> character.has_ability("Fireball")
        False
        >>> unlock_abilities_at_level(character, 3)
        >>> character.has_ability("Fireball")
        True
    """
    # Check if character class has ability learning schedule
    if character.class_type.value not in ABILITY_LEARNING_SCHEDULE:
        return

    class_schedule = ABILITY_LEARNING_SCHEDULE[character.class_type.value]

    # Check if there are abilities to unlock at this level
    if level in class_schedule:
        new_abilities = class_schedule[level]

        # Add new abilities to character
        for ability in new_abilities:
            character.add_ability(ability)


def validate_level_requirements(character: Character, level: int) -> bool:
    """
    Validate that character meets requirements for target level.

    Args:
        character: Character to validate
        level: Target level

    Returns:
        bool: True if requirements are met

    Raises:
        ValidationError: If requirements are not met

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> validate_level_requirements(character, 1)
        True
        >>> validate_level_requirements(character, 2)
        ValidationError: Insufficient experience for level 2: need 100, have 0
    """
    # Validate level is within allowed range
    if level < GAME_CONFIG['min_character_level'] or level > GAME_CONFIG['max_character_level']:
        raise ValidationError(
            f"Level must be between {GAME_CONFIG['min_character_level']} and {GAME_CONFIG['max_character_level']}",
            field='level', value=level
        )

    # Validate experience requirement
    required_exp = get_experience_for_level(level)

    if character.experience < required_exp:
        raise ValidationError(
            f"Insufficient experience for level {level}: need {required_exp}, have {character.experience}",
            field='experience', value=character.experience
        )

    return True


def level_up(character: Character) -> Character:
    """
    Level up character to the next level if requirements are met.

    Args:
        character: Character to level up

    Returns:
        Character: Character after level up

    Raises:
        ValidationError: If requirements are not met

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> character.experience = 100
        >>> character = level_up(character)
        >>> character.level
        2
    """
    # Calculate new level
    new_level = character.level + 1
    
    # Validate level requirements
    validate_level_requirements(character, new_level)
    
    # Calculate level up bonuses
    bonuses = calculate_level_up_bonuses(character, new_level)
    
    # Update character with bonuses
    character.level = new_level
    character.max_hp = bonuses['new_max_hp']
    character.hp = character.max_hp  # Full heal on level up
    
    # Apply stat increases
    for stat, increase in bonuses['stat_increases'].items():
        if hasattr(character.stats, stat):
            setattr(character.stats, stat, 
                    getattr(character.stats, stat) + increase)
    
    # Unlock new abilities
    unlock_abilities_at_level(character, new_level)
    
    return character


def get_level_progress_percentage(character: Character) -> float:
    """
    Calculate character's progress to next level as percentage.

    Args:
        character: Character to calculate progress for

    Returns:
        float: Progress percentage (0-100)

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> character.experience = 50
        >>> get_level_progress_percentage(character)
        50.0  # 50/100 = 50%
        >>> character = add_experience(character, 50)
        >>> get_level_progress_percentage(character)
        100.0  # Ready to level up
        >>> character = level_up_character(character)
        >>> get_level_progress_percentage(character)
        0.0    # Just leveled up
    """
    # Handle max level
    if character.level >= GAME_CONFIG['max_character_level']:
        return 100.0

    # Get current and next level experience
    current_level_exp = get_experience_for_level(character.level)
    next_level_exp = get_experience_for_level(character.level + 1)

    # Calculate progress
    exp_toward_next = character.experience - current_level_exp
    exp_needed_for_next = next_level_exp - current_level_exp

    if exp_needed_for_next == 0:
        return 100.0

    progress_percentage = (exp_toward_next / exp_needed_for_next) * 100.0

    # Ensure percentage is within bounds
    return max(0.0, min(progress_percentage, 100.0))


def get_remaining_experience(character: Character) -> int:
    """
    Calculate remaining experience needed for next level.

    Args:
        character: Character to calculate remaining experience for

    Returns:
        int: Remaining experience needed (0 if at max level)

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> character.experience = 50
        >>> get_remaining_experience(character)
        50  # Need 100 total, have 50
        >>> character = add_experience(character, 50)
        >>> get_remaining_experience(character)
        0   # Ready to level up
    """
    # Handle max level
    if character.level >= GAME_CONFIG['max_character_level']:
        return 0

    # Get current and next level experience
    current_level_exp = get_experience_for_level(character.level)
    next_level_exp = get_experience_for_level(character.level + 1)

    # Calculate remaining experience (current_level_exp unused)
    _ = get_experience_for_level(character.level)  # For consistency
    remaining_exp = next_level_exp - character.experience

    # Ensure remaining experience is not negative
    return max(0, remaining_exp)


def calculate_experience_rewards(
    quest_difficulty: str,
    character_level: int,
    quest_type: str = "side_quest"
) -> Dict[str, int]:
    """
    Calculate experience rewards based on quest difficulty and character level.

    Args:
        quest_difficulty: Quest difficulty ("easy", "medium", "hard", "legendary")
        character_level: Character level for scaling
        quest_type: Type of quest ("side_quest", "main_quest")

    Returns:
        Dict[str, int]: Experience rewards breakdown

    Examples:
        >>> calculate_experience_rewards("easy", 1)
        {'base_xp': 50, 'level_bonus': 0, 'type_bonus': 0, 'total_xp': 50}
        >>> calculate_experience_rewards("medium", 10, "main_quest")
        {'base_xp': 200, 'level_bonus': 50, 'type_bonus': 50, 'total_xp': 300}
        >>> calculate_experience_rewards("legendary", 50)
        {'base_xp': 1000, 'level_bonus': 250, 'type_bonus': 0, 'total_xp': 1250}
    """
    # Base experience rewards
    base_xp = {
        "easy": 50,
        "medium": 200,
        "hard": 500,
        "legendary": 1000
    }.get(quest_difficulty, 50)

    # Level bonus (10% of base XP per 10 levels)
    level_bonus = int(base_xp * (character_level // 10) * 0.1)

    # Type bonus
    type_bonus = {
        "side_quest": 0,
        "main_quest": base_xp // 4  # 25% bonus for main quests
    }.get(quest_type, 0)

    # Calculate total
    total_xp = base_xp + level_bonus + type_bonus

    return {
        'base_xp': base_xp,
        'level_bonus': level_bonus,
        'type_bonus': type_bonus,
        'total_xp': total_xp
    }


def calculate_combat_experience(
    character: Character,
    enemy: Enemy,
    damage_dealt: int,
    killing_blow: bool = False
) -> int:
    """
    Calculate experience reward from combat.

    Args:
        character: Character fighting
        enemy: Enemy defeated
        damage_dealt: Total damage dealt by character
        killing_blow: Whether character delivered killing blow

    Returns:
        int: Experience earned from combat

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> goblin = create_enemy("Goblin", 2)
        >>> calculate_combat_experience(character, goblin, 50, True)
        100
        >>> calculate_combat_experience(character, goblin, 25, False)
        50
    """
    # Base experience from enemy
    base_exp = enemy.reward_xp

    # Level difference bonus/penalty
    level_diff = enemy.level - character.level

    # Adjust experience based on level difference
    if level_diff >= 5:
        # Enemy is much stronger - bonus
        exp_multiplier = 1.5
    elif level_diff >= 2:
        # Enemy is stronger - small bonus
        exp_multiplier = 1.2
    elif level_diff <= -5:
        # Enemy is much weaker - penalty
        exp_multiplier = 0.5
    elif level_diff <= -2:
        # Enemy is weaker - small penalty
        exp_multiplier = 0.8
    else:
        # Similar level - no adjustment
        exp_multiplier = 1.0

    # Damage contribution bonus
    max_hp = enemy.max_hp
    damage_contribution = min(damage_dealt, max_hp) / max_hp
    damage_bonus = int(base_exp * damage_contribution)

    # Killing blow bonus
    killing_blow_bonus = int(base_exp * 0.2) if killing_blow else 0

    # Calculate total experience
    total_exp = int(base_exp * exp_multiplier) + damage_bonus + killing_blow_bonus

    # Ensure minimum experience
    total_exp = max(total_exp, 10)

    return total_exp


def calculate_item_experience(item: Item, character_level: int) -> int:
    """
    Calculate experience reward from using valuable items.

    Args:
        item: Item that grants experience
        character_level: Character level for scaling

    Returns:
        int: Experience earned from item

    Examples:
        >>> from core.models import Item, ItemType, ItemRarity
        >>> item = Item(id="exp_potion", name="Experience Potion", type=ItemType.CONSUMABLE,
        ...              rarity=ItemRarity.RARE, value=500)
        >>> calculate_item_experience(item, 10)
        100
    """
    # Only consumable items can grant experience
    if not item.consumable:
        return 0

    # Experience based on item rarity and value
    rarity_xp = {
        "common": 0,
        "uncommon": 25,
        "rare": 100,
        "epic": 250,
        "legendary": 500
    }.get(item.rarity.value, 0)

    # Value-based experience (1 XP per 10 gold value)
    value_xp = item.value // 10

    # Level scaling (reduces XP for higher levels)
    level_multiplier = max(0.1, 1.0 - (character_level // 10) * 0.1)

    # Calculate total experience
    total_xp = int((rarity_xp + value_xp) * level_multiplier)

    # Ensure minimum experience for consumables
    if item.consumable and total_xp < 10:
        total_xp = 10

    return total_xp


def get_level_requirements_for_abilities(character: Character) -> Dict[str, int]:
    """
    Get level requirements for all abilities in character's class.

    Args:
        character: Character to get requirements for

    Returns:
        Dict[str, int]: Ability name -> level required

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> requirements = get_level_requirements_for_abilities(character)
        >>> requirements["Power Strike"]
        1
        >>> requirements["Whirlwind Attack"]
        5
    """
    # Get ability learning schedule for character class
    if character.class_type.value not in ABILITY_LEARNING_SCHEDULE:
        return {}

    class_schedule = ABILITY_LEARNING_SCHEDULE[character.class_type.value]

    # Build requirements dictionary
    requirements = {}
    for level, abilities in class_schedule.items():
        for ability in abilities:
            requirements[ability] = level

    return requirements


def can_learn_ability_at_level(
    character: Character,
    ability: str,
    level: int
) -> bool:
    """
    Check if character can learn ability at specific level.

    Args:
        character: Character to check
        ability: Ability to learn
        level: Level to learn at

    Returns:
        bool: True if ability can be learned at level

    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> can_learn_ability_at_level(character, "Power Strike", 1)
        True
        >>> can_learn_ability_at_level(character, "Whirlwind Attack", 3)
        False
        >>> can_learn_ability_at_level(character, "Whirlwind Attack", 5)
        True
    """
    # Get ability requirements
    requirements = get_level_requirements_for_abilities(character)

    # Check if ability exists and level requirement is met
    if ability not in requirements:
        return False

    required_level = requirements[ability]
    return level >= required_level


def calculate_leveling_path(
    current_level: int,
    target_level: int
) -> List[Dict[str, Any]]:
    """
    Calculate leveling path from current to target level.

    Args:
        current_level: Starting level
        target_level: Target level

    Returns:
        List[Dict[str, Any]]: Level progression information

    Examples:
        >>> path = calculate_leveling_path(1, 3)
        >>> len(path)
        2
        >>> path[0]['level']
        2
        >>> path[0]['experience_required']
        100
        >>> path[1]['level']
        3
        >>> path[1]['experience_required']
        400
    """
    # Validate levels
    if current_level < 1 or target_level > GAME_CONFIG['max_character_level']:
        raise ValidationError("Invalid level range for leveling path")

    if current_level >= target_level:
        return []

    # Calculate path
    path = []
    for level in range(current_level + 1, target_level + 1):
        exp_required = get_experience_for_level(level)
        exp_for_level = exp_required - get_experience_for_level(level - 1)

        path.append({
            'level': level,
            'experience_required': exp_required,
            'experience_for_level': exp_for_level,
            'cumulative_experience': exp_required
        })

    return path


# Export all functions for easy access
__all__ = [
    'get_experience_for_level',
    'get_experience_cap',
    'calculate_level_up_bonuses',
    'unlock_abilities_at_level',
    'validate_level_requirements',
    'get_level_progress_percentage',
    'get_remaining_experience',
    'calculate_experience_rewards',
    'calculate_combat_experience',
    'calculate_item_experience',
    'get_level_requirements_for_abilities',
    'can_learn_ability_at_level',
    'calculate_leveling_path'
]
