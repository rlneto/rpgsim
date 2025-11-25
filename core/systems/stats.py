"""
Stats System for RPGSim
Optimized for LLM agents with explicit, deterministic calculations
"""

from typing import Dict, List, Any, Optional
from core.models import (
    Character, CharacterClass, CharacterStats,
    Item
)
from core.validation import ValidationError
from core.constants import (
    GAME_CONFIG, BASE_HP_BY_CLASS, DAMAGE_MULTIPLIERS
)


def calculate_base_hp(
    class_type: CharacterClass,
    constitution: int,
    level: int = 1
) -> int:
    """
    Calculate base HP based on class, constitution, and level.
    
    Args:
        class_type: Character class
        constitution: Constitution stat value
        level: Character level (default: 1)
        
    Returns:
        int: Calculated base HP
        
    Examples:
        >>> calculate_base_hp(CharacterClass.WARRIOR, 14, 1)
        60
        >>> calculate_base_hp(CharacterClass.MAGE, 8, 1)
        6
        >>> calculate_base_hp(CharacterClass.WARRIOR, 14, 2)
        68  # Gains HP on level up
    """
    # Get base HP for class
    base_hp = BASE_HP_BY_CLASS[class_type.value]
    
    # Calculate constitution bonus
    constitution_bonus = (constitution - 10) // 2
    if constitution_bonus < 0:
        constitution_bonus = 0
    
    # Calculate level bonus (simple formula: +8 HP per level for warrior class)
    class_hp_per_level = {
        CharacterClass.WARRIOR: 8,
        CharacterClass.MAGE: 2,
        CharacterClass.ROGUE: 4,
        CharacterClass.CLERIC: 6,
        CharacterClass.RANGER: 5,
        CharacterClass.PALADIN: 8,
        CharacterClass.WARLOCK: 3,
        CharacterClass.DRUID: 5,
        CharacterClass.MONK: 6,
        CharacterClass.BARBARIAN: 10,
        CharacterClass.BARD: 4,
        CharacterClass.SORCERER: 2,
        CharacterClass.FIGHTER: 7,
        CharacterClass.NECROMANCER: 2,
        CharacterClass.ILLUSIONIST: 2,
        CharacterClass.ALCHEMIST: 4,
        CharacterClass.BERSERKER: 12,
        CharacterClass.ASSASSIN: 4,
        CharacterClass.HEALER: 5,
        CharacterClass.SUMMONER: 3,
        CharacterClass.SHAPESHIFTER: 6,
        CharacterClass.ELEMENTALIST: 2,
        CharacterClass.NINJA: 4
    }
    
    hp_per_level = class_hp_per_level.get(class_type, 5)
    level_bonus = (level - 1) * hp_per_level
    
    # Calculate total HP
    total_hp = base_hp + constitution_bonus + level_bonus
    
    # Ensure minimum HP
    total_hp = max(total_hp, 1)
    
    return total_hp


def calculate_damage_multiplier(class_type: CharacterClass) -> float:
    """
    Calculate damage multiplier for character class.
    
    Args:
        class_type: Character class
        
    Returns:
        float: Damage multiplier
        
    Examples:
        >>> calculate_damage_multiplier(CharacterClass.WARRIOR)
        1.5
        >>> calculate_damage_multiplier(CharacterClass.MAGE)
        1.0
        >>> calculate_damage_multiplier(CharacterClass.ROGUE)
        1.3
        >>> calculate_damage_multiplier(CharacterClass.BERSERKER)
        1.7
    """
    return DAMAGE_MULTIPLIERS[class_type.value]


def calculate_stat_modifiers(stats: CharacterStats) -> Dict[str, int]:
    """
    Calculate stat modifiers based on stat values.
    
    Args:
        stats: Character stats
        
    Returns:
        Dict[str, int]: Stat modifiers
        
    Examples:
        >>> stats = CharacterStats(strength=15, dexterity=10, intelligence=8, wisdom=10, charisma=8, constitution=14)
        >>> modifiers = calculate_stat_modifiers(stats)
        >>> modifiers['strength']
        2
        >>> modifiers['intelligence']
        -1
        >>> modifiers['constitution']
        2
    """
    return stats.get_stat_modifiers()


def calculate_leveling_stats(
    base_stats: CharacterStats,
    class_type: CharacterClass,
    level: int = 1
) -> CharacterStats:
    """
    Calculate stats after leveling to specific level.
    
    Args:
        base_stats: Starting stats at level 1
        class_type: Character class
        level: Target level (default: 1)
        
    Returns:
        CharacterStats: Stats at target level
        
    Examples:
        >>> base_stats = CharacterStats(strength=15, dexterity=10, intelligence=8, wisdom=10, charisma=8, constitution=14)
        >>> leveled_stats = calculate_leveling_stats(base_stats, CharacterClass.WARRIOR, 2)
        >>> leveled_stats.strength
        17  # Gained +2 strength
        >>> leveled_stats.constitution
        16  # Gained +2 constitution
    """
    if level < 1:
        raise ValidationError("Level must be at least 1", field='level', value=level)
    
    if level == 1:
        return base_stats
    
    # Get stat increases per level for class
    from core.constants import STAT_INCREASES
    class_stat_increases = STAT_INCREASES[class_type.value]
    
    # Calculate total stat increases
    levels_to_gain = level - 1
    total_increases = {
        'strength': class_stat_increases['strength'] * levels_to_gain,
        'dexterity': class_stat_increases['dexterity'] * levels_to_gain,
        'intelligence': class_stat_increases['intelligence'] * levels_to_gain,
        'wisdom': class_stat_increases['wisdom'] * levels_to_gain,
        'charisma': class_stat_increases['charisma'] * levels_to_gain,
        'constitution': class_stat_increases['constitution'] * levels_to_gain
    }
    
    # Apply stat increases to base stats
    new_stats = CharacterStats(
        strength=base_stats.strength + total_increases['strength'],
        dexterity=base_stats.dexterity + total_increases['dexterity'],
        intelligence=base_stats.intelligence + total_increases['intelligence'],
        wisdom=base_stats.wisdom + total_increases['wisdom'],
        charisma=base_stats.charisma + total_increases['charisma'],
        constitution=base_stats.constitution + total_increases['constitution']
    )
    
    # Ensure stats don't exceed maximum
    max_stat = GAME_CONFIG['max_stat_value']
    new_stats.strength = min(new_stats.strength, max_stat)
    new_stats.dexterity = min(new_stats.dexterity, max_stat)
    new_stats.intelligence = min(new_stats.intelligence, max_stat)
    new_stats.wisdom = min(new_stats.wisdom, max_stat)
    new_stats.charisma = min(new_stats.charisma, max_stat)
    new_stats.constitution = min(new_stats.constitution, max_stat)
    
    return new_stats


def calculate_ability_scaling(
    ability_power: int,
    character_level: int,
    primary_stat: int
) -> int:
    """
    Calculate ability damage/healing scaling with stats and level.
    
    Args:
        ability_power: Base ability power
        character_level: Character level
        primary_stat: Primary stat value for ability
        
    Returns:
        int: Scaled ability power
        
    Examples:
        >>> calculate_ability_scaling(50, 1, 10)
        50
        >>> calculate_ability_scaling(50, 2, 10)
        52  # +2 per level
        >>> calculate_ability_scaling(50, 2, 15)
        54  # +2 per level +2 per 5 primary stat
    """
    # Calculate level scaling
    level_scaling = (character_level - 1) * 2
    
    # Calculate primary stat scaling (2 points per 5 stat value above 10)
    stat_scaling = max(0, (primary_stat - 10) // 5) * 2
    
    # Calculate total scaling
    total_scaling = level_scaling + stat_scaling
    
    # Calculate scaled power
    scaled_power = ability_power + total_scaling
    
    return scaled_power


def get_optimal_stats_for_class(class_type: CharacterClass) -> CharacterStats:
    """
    Get optimal stat distribution for character class.
    
    Args:
        class_type: Character class
        
    Returns:
        CharacterStats: Optimal stats for class
        
    Examples:
        >>> stats = get_optimal_stats_for_class(CharacterClass.WARRIOR)
        >>> stats.strength
        20
        >>> stats.constitution
        20
        >>> stats.intelligence
        8
    """
    from core.constants import DEFAULT_CHARACTER_STATS
    
    # Get default stats for class
    class_defaults = DEFAULT_CHARACTER_STATS[class_type.value]
    
    # Optimize for class primary stats
    optimal_stats = CharacterStats(**class_defaults)
    
    # Apply class-specific optimizations
    if class_type in [CharacterClass.WARRIOR, CharacterClass.FIGHTER, CharacterClass.PALADIN]:
        # Physical classes: prioritize strength and constitution
        optimal_stats.strength = GAME_CONFIG['max_stat_value']
        optimal_stats.constitution = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.MAGE, CharacterClass.SORCERER, CharacterClass.WARLOCK]:
        # Magical classes: prioritize intelligence and charisma
        optimal_stats.intelligence = GAME_CONFIG['max_stat_value']
        optimal_stats.charisma = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.ROGUE, CharacterClass.RANGER, CharacterClass.NINJA]:
        # Dexterous classes: prioritize dexterity
        optimal_stats.dexterity = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.CLERIC, CharacterClass.DRUID, CharacterClass.SHAPESHIFTER]:
        # Wisdom-based classes: prioritize wisdom
        optimal_stats.wisdom = GAME_CONFIG['max_stat_value']
        
    elif class_type == CharacterClass.BARD:
        # Social class: prioritize charisma
        optimal_stats.charisma = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.BARBARIAN, CharacterClass.BERSERKER]:
        # Brute classes: maximize strength and constitution
        optimal_stats.strength = GAME_CONFIG['max_stat_value']
        optimal_stats.constitution = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.NECROMANCER, CharacterClass.ELEMENTALIST]:
        # Specialized magical classes: prioritize intelligence
        optimal_stats.intelligence = GAME_CONFIG['max_stat_value']
        
    elif class_type in [CharacterClass.MONK, CharacterClass.ASSASSIN]:
        # Balanced classes: distribute stats evenly
        avg_stat = (GAME_CONFIG['max_stat_value'] + GAME_CONFIG['min_stat_value']) // 2
        optimal_stats.strength = avg_stat
        optimal_stats.dexterity = avg_stat
        optimal_stats.constitution = avg_stat
        optimal_stats.wisdom = avg_stat
        
    return optimal_stats


def validate_stat_ranges(stats: CharacterStats) -> bool:
    """
    Validate that all stats are within allowed ranges.
    
    Args:
        stats: Character stats to validate
        
    Returns:
        bool: True if all stats are valid
        
    Raises:
        ValidationError: If any stat is out of range
        
    Examples:
        >>> valid_stats = CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> validate_stat_ranges(valid_stats)
        True
        >>> invalid_stats = CharacterStats(strength=25, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> validate_stat_ranges(invalid_stats)
        ValidationError: Strength must be between 1 and 20
    """
    # Validate each stat is within allowed range
    min_stat = GAME_CONFIG['min_stat_value']
    max_stat = GAME_CONFIG['max_stat_value']
    
    if stats.strength < min_stat or stats.strength > max_stat:
        raise ValidationError(
            f"Strength must be between {min_stat} and {max_stat}",
            field='strength', value=stats.strength
        )
    
    if stats.dexterity < min_stat or stats.dexterity > max_stat:
        raise ValidationError(
            f"Dexterity must be between {min_stat} and {max_stat}",
            field='dexterity', value=stats.dexterity
        )
    
    if stats.intelligence < min_stat or stats.intelligence > max_stat:
        raise ValidationError(
            f"Intelligence must be between {min_stat} and {max_stat}",
            field='intelligence', value=stats.intelligence
        )
    
    if stats.wisdom < min_stat or stats.wisdom > max_stat:
        raise ValidationError(
            f"Wisdom must be between {min_stat} and {max_stat}",
            field='wisdom', value=stats.wisdom
        )
    
    if stats.charisma < min_stat or stats.charisma > max_stat:
        raise ValidationError(
            f"Charisma must be between {min_stat} and {max_stat}",
            field='charisma', value=stats.charisma
        )
    
    if stats.constitution < min_stat or stats.constitution > max_stat:
        raise ValidationError(
            f"Constitution must be between {min_stat} and {max_stat}",
            field='constitution', value=stats.constitution
        )
    
    return True


def apply_stat_bonuses(
    base_stats: CharacterStats,
    bonuses: Dict[str, int]
) -> CharacterStats:
    """
    Apply stat bonuses to base stats with validation.
    
    Args:
        base_stats: Base character stats
        bonuses: Stat bonuses to apply
        
    Returns:
        CharacterStats: Stats with bonuses applied
        
    Raises:
        ValidationError: If bonuses are invalid
        
    Examples:
        >>> base_stats = CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> bonuses = {'strength': 2, 'constitution': 1}
        >>> boosted_stats = apply_stat_bonuses(base_stats, bonuses)
        >>> boosted_stats.strength
        12
        >>> boosted_stats.constitution
        11
    """
    # Validate bonuses
    for stat_name, bonus_value in bonuses.items():
        if stat_name not in ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']:
            raise ValidationError(f"Invalid stat name: {stat_name}", field='stat_name', value=stat_name)
        
        if bonus_value < 0:
            raise ValidationError(f"Stat bonus cannot be negative: {stat_name}={bonus_value}", field=stat_name, value=bonus_value)
    
    # Apply bonuses
    new_stats = CharacterStats(
        strength=base_stats.strength + bonuses.get('strength', 0),
        dexterity=base_stats.dexterity + bonuses.get('dexterity', 0),
        intelligence=base_stats.intelligence + bonuses.get('intelligence', 0),
        wisdom=base_stats.wisdom + bonuses.get('wisdom', 0),
        charisma=base_stats.charisma + bonuses.get('charisma', 0),
        constitution=base_stats.constitution + bonuses.get('constitution', 0)
    )
    
    # Ensure stats don't exceed maximum
    max_stat = GAME_CONFIG['max_stat_value']
    new_stats.strength = min(new_stats.strength, max_stat)
    new_stats.dexterity = min(new_stats.dexterity, max_stat)
    new_stats.intelligence = min(new_stats.intelligence, max_stat)
    new_stats.wisdom = min(new_stats.wisdom, max_stat)
    new_stats.charisma = min(new_stats.charisma, max_stat)
    new_stats.constitution = min(new_stats.constitution, max_stat)
    
    return new_stats


def calculate_effective_stats(
    base_stats: CharacterStats,
    equipped_items: List[Item]
) -> CharacterStats:
    """
    Calculate effective stats with item bonuses applied.
    
    Args:
        base_stats: Base character stats
        equipped_items: List of equipped items
        
    Returns:
        CharacterStats: Effective stats with item bonuses
        
    Examples:
        >>> base_stats = CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> from core.models import Item, ItemType, ItemRarity
        >>> sword = Item(id="sword", name="Sword", type=ItemType.WEAPON, rarity=ItemRarity.COMMON,
        ...                value=100, stats_mod={"strength": 2})
        >>> effective_stats = calculate_effective_stats(base_stats, [sword])
        >>> effective_stats.strength
        12
    """
    # Start with base stats
    effective_stats = base_stats
    
    # Apply item bonuses
    total_bonuses = {}
    for item in equipped_items:
        if item.is_equipment():
            for stat_name, bonus_value in item.stats_mod.items():
                if stat_name not in total_bonuses:
                    total_bonuses[stat_name] = 0
                total_bonuses[stat_name] += bonus_value
    
    # Apply total bonuses
    effective_stats = apply_stat_bonuses(base_stats, total_bonuses)
    
    return effective_stats


def get_stat_comparative_ranking(
    character_stats: CharacterStats,
    class_type: CharacterClass
) -> Dict[str, str]:
    """
    Get comparative ranking of character stats vs class average.
    
    Args:
        character_stats: Character's current stats
        class_type: Character class for comparison
        
    Returns:
        Dict[str, str]: Ranking for each stat
        
    Examples:
        >>> character_stats = CharacterStats(strength=15, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=14)
        >>> ranking = get_stat_comparative_ranking(character_stats, CharacterClass.WARRIOR)
        >>> ranking['strength']
        'High'
        >>> ranking['intelligence']
        'Low'
    """
    # Get class average stats
    from core.constants import DEFAULT_CHARACTER_STATS
    class_stats = DEFAULT_CHARACTER_STATS[class_type.value]
    
    # Calculate rankings
    rankings = {}
    for stat_name in ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']:
        character_value = getattr(character_stats, stat_name)
        class_value = class_stats.get(stat_name, 10)
        
        if character_value >= class_value + 3:
            ranking[stat_name] = 'Very High'
        elif character_value >= class_value + 1:
            ranking[stat_name] = 'High'
        elif character_value >= class_value - 1:
            ranking[stat_name] = 'Average'
        elif character_value >= class_value - 3:
            ranking[stat_name] = 'Low'
        else:
            ranking[stat_name] = 'Very Low'
    
    return rankings


def calculate_stat_growth_potential(
    character: Character,
    target_level: int
) -> Dict[str, int]:
    """
    Calculate stat growth potential from current to target level.
    
    Args:
        character: Character to analyze
        target_level: Target level to calculate growth to
        
    Returns:
        Dict[str, int]: Potential growth for each stat
        
    Examples:
        >>> character = create_character("Test", CharacterClass.WARRIOR)
        >>> growth = calculate_stat_growth_potential(character, 2)
        >>> growth['strength']
        2
        >>> growth['constitution']
        2
    """
    if target_level <= character.level:
        return {'strength': 0, 'dexterity': 0, 'intelligence': 0, 'wisdom': 0, 'charisma': 0, 'constitution': 0}
    
    # Calculate target level stats
    target_stats = calculate_leveling_stats(character.stats, character.class_type, target_level)
    
    # Calculate growth potential
    growth = {
        'strength': target_stats.strength - character.stats.strength,
        'dexterity': target_stats.dexterity - character.stats.dexterity,
        'intelligence': target_stats.intelligence - character.stats.intelligence,
        'wisdom': target_stats.wisdom - character.stats.wisdom,
        'charisma': target_stats.charisma - character.stats.charisma,
        'constitution': target_stats.constitution - character.stats.constitution
    }
    
    return growth


# Export all functions for easy access
__all__ = [
    'calculate_base_hp',
    'calculate_damage_multiplier',
    'calculate_stat_modifiers',
    'calculate_leveling_stats',
    'calculate_ability_scaling',
    'get_optimal_stats_for_class',
    'validate_stat_ranges',
    'apply_stat_bonuses',
    'calculate_effective_stats',
    'get_stat_comparative_ranking',
    'calculate_stat_growth_potential'
]