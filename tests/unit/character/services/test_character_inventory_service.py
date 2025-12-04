"""
Unit Tests for the CharacterInventoryService.
"""

import pytest
from core.systems.character.services.character_service import CharacterInventoryService
from core.systems.character.domain.character import Character, CharacterClass, CharacterStats

class TestCharacterInventoryService:
    """Test CharacterInventoryService functionality."""

    def test_add_item(self):
        """Test adding an item to a character's inventory."""
        service = CharacterInventoryService()
        stats = CharacterStats()
        character = Character(
            id="123",
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
        )
        result = service.add_item(character, "sword")
        assert result is True
        assert "sword" in character.inventory

    def test_add_item_invalid(self):
        """Test adding an invalid item to a character's inventory."""
        service = CharacterInventoryService()
        stats = CharacterStats()
        character = Character(
            id="123",
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
        )
        result = service.add_item(character, "")
        assert result is False
        assert "" not in character.inventory

    def test_remove_item(self):
        """Test removing an item from a character's inventory."""
        service = CharacterInventoryService()
        stats = CharacterStats()
        character = Character(
            id="123",
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=["sword"],
        )
        result = service.remove_item(character, "sword")
        assert result is True
        assert "sword" not in character.inventory
