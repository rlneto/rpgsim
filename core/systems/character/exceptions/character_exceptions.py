"""
Character-specific exceptions
"""


class CharacterError(Exception):
    """Base exception for character system"""
    pass


class InvalidCharacterClassError(CharacterError):
    """Raised when trying to use invalid character class"""
    pass


class CharacterCreationError(CharacterError):
    """Raised when character creation fails"""
    pass


class CharacterNotFoundError(CharacterError):
    """Raised when character is not found"""
    pass


class InventoryError(CharacterError):
    """Raised when inventory operation fails"""
    pass


class StatValidationError(CharacterError):
    """Raised when stat validation fails"""
    pass
