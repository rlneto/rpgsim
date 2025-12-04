"""
Unit Tests for the CharacterClass Enum.
"""

import pytest
from core.systems.character.domain.character import CharacterClass

class TestCharacterClass:
    """Test CharacterClass enum functionality."""

    def test_all_24_classes_available(self):
        """Test that all 24 required character classes are available."""
        actual_count = len(CharacterClass)
        assert actual_count == 24, f"Expected 24 classes, got {actual_count}"

        # Check specific important classes exist
        assert CharacterClass.WARRIOR in CharacterClass
        assert CharacterClass.MAGE in CharacterClass
        assert CharacterClass.ROGUE in CharacterClass

    def test_class_values_are_strings(self):
        """Test that all class values are proper strings."""
        for character_class in CharacterClass:
            assert isinstance(character_class.value, str)
            assert len(character_class.value.strip()) > 0

    def test_class_conversion(self):
        """Test class enum conversion works correctly."""
        assert CharacterClass.WARRIOR.value == "Warrior"
        assert CharacterClass("Warrior") == CharacterClass.WARRIOR
