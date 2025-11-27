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
- exceptions/: Custom exception types
- facade.py: Clean external API

All modules are <500 lines and follow SOLID principles.
"""

# Public API - clean facade interface
from .facade import (
    CharacterSystem,
    create_character,
    level_up_character,
    add_experience,
    get_all_character_classes,
    get_class_balance_stats
)

# Validation functions for BDD compatibility
def validate_class_balance() -> bool:
    """Validate class balance (BDD compatibility)"""
    system = CharacterSystem()
    return system.validate_class_balance()

def verify_unique_mechanics() -> bool:
    """Verify unique mechanics (BDD compatibility)"""
    system = CharacterSystem()
    return system.verify_unique_mechanics()

def verify_minimum_abilities() -> bool:
    """Verify minimum abilities (BDD compatibility)"""
    system = CharacterSystem()
    return system.verify_minimum_abilities()

# Domain exports for advanced usage
from .domain.character import Character, CharacterClass, CharacterStats

__all__ = [
    # Public API
    'CharacterSystem',
    'create_character', 'level_up_character', 'add_experience',
    'get_all_character_classes', 'get_class_balance_stats',
    
    # BDD compatibility
    'validate_class_balance', 'verify_unique_mechanics', 'verify_minimum_abilities',
    
    # Domain objects
    'Character', 'CharacterClass', 'CharacterStats'
]
