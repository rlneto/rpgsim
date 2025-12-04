"""
Unit Tests for the CharacterProgressionService.
"""

import pytest
from core.systems.character.services.character_service import CharacterProgressionService
from core.systems.character.domain.character import Character, CharacterClass, CharacterStats

class TestCharacterProgressionService:
    """Test CharacterProgressionService functionality."""

    def test_level_up(self):
        """Test leveling up a character."""
        service = CharacterProgressionService()
        stats = CharacterStats()
        character = Character(
            id="123",
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=1000,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            created=True,
        )
        result = service.level_up(character)
        assert result is True
        assert character.level == 2
        assert character.experience == 1000  # Experience is not reset by the service

    def test_add_experience(self):
        """Test adding experience to a character."""
        service = CharacterProgressionService()
        character = Character()
        result = service.add_experience(character, 100)
        assert result is True
        assert character.experience == 100

    def test_add_experience_invalid(self):
        """Test adding invalid experience to a character."""
        service = CharacterProgressionService()
        character = Character()
        result = service.add_experience(character, -10)
        assert result is False
        assert character.experience == 0
