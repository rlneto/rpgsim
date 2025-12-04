"""
Character System Package - Modular Architecture

This package provides a complete character management system with:
- Domain entities and value objects
- Business logic services
- Repository interfaces and implementations
- Clean facades for external access
- Proper exception handling
- Dependency injection support

Architecture:
- domain/: Business entities (Character, CharacterClass, etc.)
- services/: Business logic (creation, progression, inventory)
- interfaces/: Repository and service contracts
- repositories/: Data access implementations
"""

from .domain.character import Character, CharacterClass, CharacterStats
from .facade import (
    CharacterSystem,
    create_character,
    heal_character,
    get_default_stats_for_class,
    level_up_character,
    add_experience,
    get_all_character_classes,
    get_class_balance_stats,
    validate_class_balance,
    verify_unique_mechanics,
    verify_minimum_abilities,
)

# Legacy functions for backward compatibility
def damage_character(character: Character, amount: int) -> int:
    """Damage character by specified amount"""
    return character.damage(amount)

def calculate_max_hp(character: Character) -> int:
    """Calculate maximum HP for character"""
    return character.max_hp

__all__ = [
    # Public API
    "CharacterSystem",
    "create_character",
    "level_up_character",
    "add_experience",
    "get_all_character_classes",
    "get_class_balance_stats",
    "validate_class_balance",
    "verify_unique_mechanics",
    "verify_minimum_abilities",
    # Legacy compatibility
    "damage_character",
    "calculate_max_hp",
    # Domain objects
    "Character",
    "CharacterClass",
    "CharacterStats",
]
