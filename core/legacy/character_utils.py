"""
Character system utility functions
"""

from typing import Dict, List
from core.systems.character import Character, CharacterClass


def get_all_character_classes() -> List[str]:
    """
    Get list of all available character classes

    Returns:
        List of class names
    """
    return [cls.value for cls in CharacterClass]


def get_class_balance_stats() -> Dict[str, int]:
    """
    Calculate power levels for all classes to verify balance

    Returns:
        Dictionary mapping class names to power levels
    """
    balance_stats = {}

    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            stats = Character.CLASS_CONFIG[char_class]["base_stats"]
            power = sum(stats.values())
            balance_stats[char_class.value] = power

    return balance_stats


def validate_class_balance() -> bool:
    """
    Validate that all classes are balanced within 15% power difference

    Returns:
        True if classes are balanced, False otherwise
    """
    balance_stats = get_class_balance_stats()

    if not balance_stats:
        return False

    max_power = max(balance_stats.values())
    min_power = min(balance_stats.values())

    # Calculate ratio of difference
    balance_ratio = (max_power - min_power) / min_power if min_power > 0 else 0

    # Classes should be within 15% power difference
    return balance_ratio <= 0.15


def verify_unique_mechanics() -> bool:
    """
    Verify that all classes have unique mechanics

    Returns:
        True if all mechanics are unique, False otherwise
    """
    mechanics = []

    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            mechanic = Character.CLASS_CONFIG[char_class]["mechanic"]
            mechanics.append(mechanic)

    # Check if all mechanics are unique
    return len(set(mechanics)) == len(mechanics)


def verify_minimum_abilities() -> bool:
    """
    Verify that all classes have at least 10 unique abilities

    Returns:
        True if all classes meet ability requirements, False otherwise
    """
    for char_class in CharacterClass:
        if char_class in Character.CLASS_CONFIG:
            abilities = Character.CLASS_CONFIG[char_class]["abilities"]
            if len(abilities) < 10:
                return False

            # Check for uniqueness within class
            if len(set(abilities)) != len(abilities):
                return False

    return True


# Convenience functions for external use
def create_character(name: str, class_type: str) -> Character:
    """Create a character with the given name and class type."""
    character = Character()
    success = character.create_character(name, class_type)
    if not success:
        raise ValueError(f"Failed to create character: {name} ({class_type})")
    return character


def level_up_character(character: Character) -> bool:
    """Level up a character by one level."""
    # Simple implementation - placeholder
    character.level += 1
    return True


def add_experience(character: Character, exp_amount: int) -> bool:
    """Add experience to a character."""
    if exp_amount <= 0:
        return False

    character.experience += exp_amount
    return True


# Export all functions for easy access
__all__ = [
    'create_character',
    'level_up_character', 'add_experience', 'get_all_character_classes',
    'get_class_balance_stats', 'validate_class_balance',
    'verify_unique_mechanics', 'verify_minimum_abilities'
]
