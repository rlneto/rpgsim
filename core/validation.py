"""
Validation System for RPGSim
Optimized for LLM agents with explicit, deterministic validation
"""

import re
from typing import List, Dict, Any, Optional, Union
from core.models import (
    Character, CharacterClass, CharacterStats,
    Item, ItemRarity, ItemType,
    Enemy, EnemyType,
    Quest, QuestStatus, QuestObjective,
    Location, LocationType,
    GameState
)
from core.constants import (
    GAME_CONFIG, VALIDATION_CONFIG, ERROR_MESSAGES
)


class ValidationError(Exception):
    """Custom validation error with clear messages for agents."""
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class ValidationWarning(Exception):
    """Custom validation warning for non-critical issues."""
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


def validate_character_name(name: str) -> bool:
    """
    Validate character name with explicit rules.
    
    Args:
        name: Character name to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If name is invalid
        
    Examples:
        >>> validate_character_name("Aragorn")
        True
        >>> validate_character_name("")
        ValidationError: Character name cannot be empty
        >>> validate_character_name("  ")
        ValidationError: Character name cannot be only whitespace
        >>> validate_character_name("Name<")
        ValidationError: Character name cannot contain '<'
        >>> validate_character_name("A" * 51)
        ValidationError: Character name cannot exceed 50 characters
    """
    # Check if name is empty
    if not name:
        raise ValidationError(ERROR_MESSAGES['character_name_empty'], field='name', value=name)
    
    # Check if name is only whitespace
    if not name.strip():
        raise ValidationError(ERROR_MESSAGES['character_name_leading_trailing_spaces'], field='name', value=name)
    
    # Check name length
    if len(name.strip()) < VALIDATION_CONFIG['min_character_name_length']:
        raise ValidationError("Character name must be at least 1 character long", field='name', value=name)
    
    if len(name) > VALIDATION_CONFIG['max_character_name_length']:
        raise ValidationError(ERROR_MESSAGES['character_name_too_long'], field='name', value=name)
    
    # Check for leading/trailing spaces
    if name != name.strip():
        raise ValidationError(ERROR_MESSAGES['character_name_leading_trailing_spaces'], field='name', value=name)
    
    # Check for double spaces
    if '  ' in name:
        raise ValidationError(ERROR_MESSAGES['character_name_double_spaces'], field='name', value=name)
    
    # Check for invalid characters
    if not re.match(f'^[{VALIDATION_CONFIG["valid_name_characters"]}]*$', name):
        raise ValidationError(ERROR_MESSAGES['character_name_invalid_chars'], field='name', value=name)
    
    return True


def validate_character_stats(stats: CharacterStats) -> bool:
    """
    Validate character stats with explicit range checking.
    
    Args:
        stats: CharacterStats object to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If stats are invalid
        
    Examples:
        >>> stats = CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> validate_character_stats(stats)
        True
        >>> invalid_stats = CharacterStats(strength=0, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> validate_character_stats(invalid_stats)
        ValidationError: Strength must be between 1 and 20
    """
    # Validate strength
    if stats.strength < GAME_CONFIG['min_stat_value'] or stats.strength > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Strength must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='strength', value=stats.strength
        )
    
    # Validate dexterity
    if stats.dexterity < GAME_CONFIG['min_stat_value'] or stats.dexterity > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Dexterity must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='dexterity', value=stats.dexterity
        )
    
    # Validate intelligence
    if stats.intelligence < GAME_CONFIG['min_stat_value'] or stats.intelligence > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Intelligence must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='intelligence', value=stats.intelligence
        )
    
    # Validate wisdom
    if stats.wisdom < GAME_CONFIG['min_stat_value'] or stats.wisdom > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Wisdom must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='wisdom', value=stats.wisdom
        )
    
    # Validate charisma
    if stats.charisma < GAME_CONFIG['min_stat_value'] or stats.charisma > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Charisma must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='charisma', value=stats.charisma
        )
    
    # Validate constitution
    if stats.constitution < GAME_CONFIG['min_stat_value'] or stats.constitution > GAME_CONFIG['max_stat_value']:
        raise ValidationError(
            f"Constitution must be between {GAME_CONFIG['min_stat_value']} and {GAME_CONFIG['max_stat_value']}",
            field='constitution', value=stats.constitution
        )
    
    return True


def validate_character_creation(name: str, class_type: CharacterClass, stats: CharacterStats) -> bool:
    """
    Validate complete character creation parameters.
    
    Args:
        name: Character name
        class_type: Character class
        stats: Character statistics
        
    Returns:
        bool: True if all validations pass
        
    Raises:
        ValidationError: If any validation fails
        
    Examples:
        >>> stats = CharacterStats(strength=10, dexterity=10, intelligence=10, wisdom=10, charisma=10, constitution=10)
        >>> validate_character_creation("Aragorn", CharacterClass.WARRIOR, stats)
        True
    """
    # Validate character name
    validate_character_name(name)
    
    # Validate character class
    if class_type not in CharacterClass:
        raise ValidationError(ERROR_MESSAGES['character_class_invalid'], field='class_type', value=class_type)
    
    # Validate character stats
    validate_character_stats(stats)
    
    # Validate class-specific stat requirements (optional)
    validate_class_stat_requirements(class_type, stats)
    
    return True


def validate_class_stat_requirements(class_type: CharacterClass, stats: CharacterStats) -> bool:
    """
    Validate class-specific stat requirements.
    
    Args:
        class_type: Character class
        stats: Character statistics
        
    Returns:
        bool: True if requirements are met
        
    Raises:
        ValidationError: If requirements are not met
    """
    # Define minimum stat requirements for each class
    class_requirements = {
        CharacterClass.WARRIOR: {
            'strength': 12,
            'constitution': 12
        },
        CharacterClass.MAGE: {
            'intelligence': 12,
            'wisdom': 10
        },
        CharacterClass.ROGUE: {
            'dexterity': 12,
            'strength': 8
        },
        CharacterClass.CLERIC: {
            'wisdom': 12,
            'charisma': 10
        },
        CharacterClass.RANGER: {
            'dexterity': 12,
            'wisdom': 10
        },
        CharacterClass.PALADIN: {
            'strength': 12,
            'charisma': 12,
            'wisdom': 10
        },
        # Add other classes as needed
    }
    
    # Check class requirements
    if class_type in class_requirements:
        requirements = class_requirements[class_type]
        
        for stat_name, min_value in requirements.items():
            stat_value = getattr(stats, stat_name)
            
            if stat_value < min_value:
                raise ValidationError(
                    f"{class_type.value.title()} class requires {stat_name} >= {min_value}, got {stat_value}",
                    field=stat_name, value=stat_value
                )
    
    return True


def validate_item_creation(name: str, item_type: ItemType, value: int) -> bool:
    """
    Validate item creation parameters.
    
    Args:
        name: Item name
        item_type: Item type
        value: Item value in gold
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    # Validate item name
    if not name or not name.strip():
        raise ValidationError("Item name cannot be empty", field='name', value=name)
    
    if len(name) > VALIDATION_CONFIG['max_item_name_length']:
        raise ValidationError(ERROR_MESSAGES['item_name_too_long'], field='name', value=name)
    
    # Validate item type
    if item_type not in ItemType:
        raise ValidationError("Invalid item type", field='type', value=item_type)
    
    # Validate item value
    if value < 0:
        raise ValidationError("Item value cannot be negative", field='value', value=value)
    
    if value > 1000000:  # Reasonable upper limit
        raise ValidationWarning("Item value is unusually high", field='value', value=value)
    
    return True


def validate_enemy_creation(name: str, enemy_type: EnemyType, level: int, hp: int, max_hp: int) -> bool:
    """
    Validate enemy creation parameters.
    
    Args:
        name: Enemy name
        enemy_type: Enemy type
        level: Enemy level
        hp: Current HP
        max_hp: Maximum HP
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    # Validate enemy name
    if not name or not name.strip():
        raise ValidationError("Enemy name cannot be empty", field='name', value=name)
    
    if len(name) > VALIDATION_CONFIG['max_enemy_name_length']:
        raise ValidationError("Enemy name is too long", field='name', value=name)
    
    # Validate enemy type
    if enemy_type not in EnemyType:
        raise ValidationError("Invalid enemy type", field='type', value=enemy_type)
    
    # Validate enemy level
    if level < 1 or level > GAME_CONFIG['max_character_level']:
        raise ValidationError(f"Enemy level must be between 1 and {GAME_CONFIG['max_character_level']}", field='level', value=level)
    
    # Validate HP values
    if max_hp <= 0:
        raise ValidationError("Enemy max HP must be positive", field='max_hp', value=max_hp)
    
    if hp < 0:
        raise ValidationError("Enemy HP cannot be negative", field='hp', value=hp)
    
    if hp > max_hp:
        raise ValidationError("Enemy HP cannot exceed max HP", field='hp', value=hp)
    
    return True


def validate_quest_creation(name: str, description: str, objectives: List[QuestObjective]) -> bool:
    """
    Validate quest creation parameters.
    
    Args:
        name: Quest name
        description: Quest description
        objectives: List of quest objectives
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    # Validate quest name
    if not name or not name.strip():
        raise ValidationError("Quest name cannot be empty", field='name', value=name)
    
    if len(name) > VALIDATION_CONFIG['max_quest_name_length']:
        raise ValidationError(ERROR_MESSAGES['quest_name_too_long'], field='name', value=name)
    
    # Validate quest description
    if not description or not description.strip():
        raise ValidationError("Quest description cannot be empty", field='description', value=description)
    
    if len(description) > VALIDATION_CONFIG['max_quest_description_length']:
        raise ValidationError(ERROR_MESSAGES['quest_description_too_long'], field='description', value=description)
    
    # Validate objectives
    if not objectives:
        raise ValidationError("Quest must have at least one objective", field='objectives', value=objectives)
    
    for i, objective in enumerate(objectives):
        if not objective.description or not objective.description.strip():
            raise ValidationError(f"Objective {i+1} description cannot be empty", field=f'objectives[{i}].description', value=objective.description)
        
        if objective.target < 0:
            raise ValidationError(f"Objective {i+1} target cannot be negative", field=f'objectives[{i}].target', value=objective.target)
        
        if objective.progress < 0:
            raise ValidationError(f"Objective {i+1} progress cannot be negative", field=f'objectives[{i}].progress', value=objective.progress)
        
        if objective.progress > objective.target:
            raise ValidationError(f"Objective {i+1} progress cannot exceed target", field=f'objectives[{i}].progress', value=objective.progress)
    
    return True


def validate_combat_execution(attacker: Character, defender: Union[Character, Enemy], damage: int) -> bool:
    """
    Validate combat execution parameters.
    
    Args:
        attacker: Attacking character
        defender: Defending character or enemy
        damage: Damage dealt
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    # Validate attacker
    if not attacker:
        raise ValidationError("Attacker cannot be None", field='attacker', value=attacker)
    
    if not attacker.is_alive():
        raise ValidationError("Attacker must be alive", field='attacker', value=attacker.get_summary())
    
    # Validate defender
    if not defender:
        raise ValidationError("Defender cannot be None", field='defender', value=defender)
    
    if not defender.is_alive():
        raise ValidationError("Defender must be alive", field='defender', value=defender.get_summary())
    
    # Validate damage
    if damage < 0:
        raise ValidationError(ERROR_MESSAGES['damage_negative'], field='damage', value=damage)
    
    if damage > GAME_CONFIG['combat_damage_cap']:
        raise ValidationError(ERROR_MESSAGES['damage_exceeds_cap'], field='damage', value=damage)
    
    # Validate damage calculations (optional)
    validate_damage_calculation(attacker, defender, damage)
    
    return True


def validate_damage_calculation(attacker: Character, defender: Union[Character, Enemy], damage: int) -> bool:
    """
    Validate damage calculation is reasonable.
    
    Args:
        attacker: Attacking character
        defender: Defending character or enemy
        damage: Damage dealt
        
    Returns:
        bool: True if reasonable
    """
    # Get damage multiplier for attacker's class
    from core.constants import DAMAGE_MULTIPLIERS
    damage_mult = DAMAGE_MULTIPLIERS.get(attacker.class_type.value, 1.0)
    
    # Calculate expected damage range
    base_damage = attacker.stats.strength * damage_mult
    min_expected = base_damage * 0.5  # 50% of expected
    max_expected = base_damage * 2.0  # 200% of expected
    
    # Validate damage is in reasonable range
    if damage < min_expected:
        raise ValidationWarning(f"Damage {damage} is below expected range {min_expected:.1f}-{max_expected:.1f}", field='damage', value=damage)
    
    if damage > max_expected:
        raise ValidationWarning(f"Damage {damage} is above expected range {min_expected:.1f}-{max_expected:.1f}", field='damage', value=damage)
    
    return True


def validate_save_load_operation(game_state: GameState, save_data: Optional[str] = None) -> bool:
    """
    Validate save/load operation parameters.
    
    Args:
        game_state: Game state to save or load
        save_data: Save data (for load operations)
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    # Validate game state
    if not game_state:
        raise ValidationError("Game state cannot be None", field='game_state', value=game_state)
    
    # For save operations
    if save_data is None:
        # Validate that game state has required fields for saving
        if not hasattr(game_state, 'save_version'):
            raise ValidationError("Game state missing save_version", field='game_state', value=game_state)
        
        if not hasattr(game_state, 'save_timestamp'):
            raise ValidationError("Game state missing save_timestamp", field='game_state', value=game_state)
    
    # For load operations
    else:
        # Validate save data format
        if not isinstance(save_data, str):
            raise ValidationError("Save data must be a string", field='save_data', type=type(save_data))
        
        if not save_data.strip():
            raise ValidationError("Save data cannot be empty", field='save_data', value=save_data)
        
        # Validate save data can be parsed as JSON
        import json
        try:
            parsed_data = json.loads(save_data)
            
            # Validate required fields in save data
            required_fields = ['game_state', 'save_version', 'save_timestamp']
            for field in required_fields:
                if field not in parsed_data:
                    raise ValidationError(f"Save data missing required field: {field}", field='save_data', value=save_data)
                    
        except json.JSONDecodeError as e:
            raise ValidationError(f"Save data is not valid JSON: {str(e)}", field='save_data', value=save_data)
    
    return True


def validate_character_level(character: Character, level: int) -> bool:
    """
    Validate character level progression.
    
    Args:
        character: Character to validate
        level: Target level
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    if not character:
        raise ValidationError("Character cannot be None", field='character', value=character)
    
    if level < GAME_CONFIG['min_character_level'] or level > GAME_CONFIG['max_character_level']:
        raise ValidationError(
            f"Level must be between {GAME_CONFIG['min_character_level']} and {GAME_CONFIG['max_character_level']}",
            field='level', value=level
        )
    
    if level < character.level:
        raise ValidationError(f"Target level {level} cannot be less than current level {character.level}", field='level', value=level)
    
    # Validate experience requirement for target level
    from core.systems.leveling import get_experience_for_level
    required_exp = get_experience_for_level(level)
    
    if character.experience < required_exp:
        raise ValidationError(
            f"Insufficient experience for level {level}: need {required_exp}, have {character.experience}",
            field='experience', value=character.experience
        )
    
    return True


def validate_ability_learning(character: Character, ability: str, required_level: int) -> bool:
    """
    Validate ability learning conditions.
    
    Args:
        character: Character learning ability
        ability: Ability to learn
        required_level: Level required for ability
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    if not character:
        raise ValidationError("Character cannot be None", field='character', value=character)
    
    if not ability or not ability.strip():
        raise ValidationError("Ability name cannot be empty", field='ability', value=ability)
    
    if character.level < required_level:
        raise ValidationError(
            f"Character level {character.level} insufficient for ability '{ability}' (requires {required_level})",
            field='level', value=character.level
        )
    
    if character.has_ability(ability):
        raise ValidationError(f"Character already knows ability '{ability}'", field='ability', value=ability)
    
    return True


def validate_item_equipment(character: Character, item: Item) -> bool:
    """
    Validate item equipment conditions.
    
    Args:
        character: Character equipping item
        item: Item to equip
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    if not character:
        raise ValidationError("Character cannot be None", field='character', value=character)
    
    if not item:
        raise ValidationError("Item cannot be None", field='item', value=item)
    
    if not item.equippable:
        raise ValidationError(f"Item '{item.name}' is not equippable", field='item', value=item)
    
    if not item.is_equipment():
        raise ValidationError(f"Item '{item.name}' is not equipment", field='item', value=item)
    
    # Check if character meets item requirements (if any)
    validate_item_requirements(character, item)
    
    return True


def validate_item_requirements(character: Character, item: Item) -> bool:
    """
    Validate character meets item requirements.
    
    Args:
        character: Character to check
        item: Item with requirements
        
    Returns:
        bool: True if requirements are met
        
    Raises:
        ValidationError: If requirements are not met
    """
    # Check stat requirements
    for stat_name, required_value in item.stats_mod.items():
        if required_value > 0:  # Only check positive requirements
            character_stat = getattr(character.stats, stat_name)
            
            if character_stat < required_value:
                raise ValidationError(
                    f"Item requires {stat_name} >= {required_value}, character has {character_stat}",
                    field=stat_name, value=character_stat
                )
    
    return True


def validate_character_gold_transaction(character: Character, amount: int, transaction_type: str) -> bool:
    """
    Validate character gold transaction.
    
    Args:
        character: Character making transaction
        amount: Gold amount
        transaction_type: 'add' or 'subtract'
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If invalid
    """
    if not character:
        raise ValidationError("Character cannot be None", field='character', value=character)
    
    if amount < 0:
        raise ValidationError("Transaction amount cannot be negative", field='amount', value=amount)
    
    if transaction_type not in ['add', 'subtract']:
        raise ValidationError("Transaction type must be 'add' or 'subtract'", field='transaction_type', value=transaction_type)
    
    if transaction_type == 'subtract' and amount > character.gold:
        raise ValidationError(
            ERROR_MESSAGES['character_insufficient_gold'],
            field='gold', value=f"{character.gold} - {amount}"
        )
    
    return True


# Export all validation functions for easy access
__all__ = [
    'ValidationError',
    'ValidationWarning',
    'validate_character_name',
    'validate_character_stats',
    'validate_character_creation',
    'validate_class_stat_requirements',
    'validate_item_creation',
    'validate_enemy_creation',
    'validate_quest_creation',
    'validate_combat_execution',
    'validate_damage_calculation',
    'validate_save_load_operation',
    'validate_character_level',
    'validate_ability_learning',
    'validate_item_equipment',
    'validate_item_requirements',
    'validate_character_gold_transaction'
]