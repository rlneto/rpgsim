"""
Unit Tests for the Character Model.
"""

import pytest
import uuid
from core.systems.character.domain.character import Character, CharacterClass, CharacterStats

class TestCharacterModel:
    """Test Character model functionality."""

    def test_character_creation(self):
        """Test creating a character with all required fields."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test Character",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            created=True
        )

        assert character.name == "Test Character"
        assert character.class_type == CharacterClass.WARRIOR
        assert character.level == 1
        assert character.hp == 100
        assert character.max_hp == 100
        assert character.gold == 50

    def test_is_alive(self):
        """Test the is_alive method."""
        character = Character(created=True, hp=100)
        assert character.is_alive() is True

        character.hp = 0
        assert character.is_alive() is False

        character.created = False
        assert character.is_alive() is False

    def test_add_to_inventory(self):
        """Test the add_to_inventory method."""
        character = Character()
        assert character.add_to_inventory("sword") is True
        assert "sword" in character.inventory

    def test_add_to_inventory_invalid_item(self):
        """Test adding an invalid item to the inventory."""
        character = Character()
        assert character.add_to_inventory("") is False
        assert character.add_to_inventory("   ") is False
        assert len(character.inventory) == 0

    def test_remove_from_inventory(self):
        """Test the remove_from_inventory method."""
        character = Character(inventory=["sword"])
        assert character.remove_from_inventory("sword") is True
        assert "sword" not in character.inventory

    def test_remove_from_inventory_item_not_found(self):
        """Test removing an item that is not in the inventory."""
        character = Character(inventory=["shield"])
        assert character.remove_from_inventory("sword") is False
        assert "shield" in character.inventory

    def test_level_up(self):
        """Test the level_up method."""
        character = Character(created=True, level=1)
        assert character.level_up() is True
        assert character.level == 2

    def test_level_up_not_created(self):
        """Test leveling up a character that has not been created."""
        character = Character(created=False, level=1)
        assert character.level_up() is False
        assert character.level == 1

    def test_get_class_stats(self):
        """Test the get_class_stats method."""
        character = Character()
        stats = character.get_class_stats("Warrior")
        assert stats["strength"] == 17

    def test_get_class_mechanic(self):
        """Test the get_class_mechanic method."""
        character = Character()
        mechanic = character.get_class_mechanic("Warrior")
        assert mechanic == "Weapon Mastery"

    def test_get_class_abilities(self):
        """Test the get_class_abilities method."""
        character = Character()
        abilities = character.get_class_abilities("Warrior")
        assert "Power Strike" in abilities

    def test_get_all_character_classes(self):
        """Test the get_all_character_classes method."""
        classes = Character.get_all_character_classes()
        assert "Warrior" in classes
        assert "Mage" in classes
        assert "Rogue" in classes
