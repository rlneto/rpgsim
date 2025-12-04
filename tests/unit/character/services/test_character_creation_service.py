"""
Unit Tests for the CharacterCreationService.
"""

import pytest
from core.systems.character.services.character_service import CharacterCreationService
from core.systems.character.domain.character import Character, CharacterClass

class TestCharacterCreationService:
    """Test CharacterCreationService functionality."""

    def test_create_character_success(self):
        """Test creating a character with valid parameters."""
        service = CharacterCreationService()
        character = service.create_character("Test", "Warrior")
        assert isinstance(character, Character)
        assert character.name == "Test"
        assert character.class_type == CharacterClass.WARRIOR
        assert character.created is True

    def test_create_character_invalid_class(self):
        """Test creating a character with an invalid class."""
        service = CharacterCreationService()
        character = service.create_character("Test", "InvalidClass")
        assert character.created is False

    def test_parse_class(self):
        """Test the _parse_class method."""
        service = CharacterCreationService()
        assert service._parse_class("Warrior") == CharacterClass.WARRIOR
        with pytest.raises(ValueError):
            service._parse_class("InvalidClass")

    def test_generate_id(self):
        """Test the _generate_id method."""
        service = CharacterCreationService()
        assert isinstance(service._generate_id(), str)
        assert len(service._generate_id()) == 8
