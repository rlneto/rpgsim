"""
Unit Tests for the MemoryCharacterRepository.
"""

import pytest
from core.systems.character.repositories.memory_repository import MemoryCharacterRepository
from core.systems.character.domain.character import Character

class TestMemoryCharacterRepository:
    """Test MemoryCharacterRepository functionality."""

    def test_save_and_load(self):
        """Test saving and loading a character."""
        repo = MemoryCharacterRepository()
        character = Character(id="123", name="Test")
        repo.save(character)
        loaded_character = repo.load("123")
        assert loaded_character == character

    def test_load_not_found(self):
        """Test loading a character that does not exist."""
        repo = MemoryCharacterRepository()
        assert repo.load("123") is None

    def test_load_by_name(self):
        """Test loading a character by name."""
        repo = MemoryCharacterRepository()
        character = Character(id="123", name="Test")
        repo.save(character)
        loaded_character = repo.load_by_name("Test")
        assert loaded_character == character

    def test_load_by_name_not_found(self):
        """Test loading a character by name that does not exist."""
        repo = MemoryCharacterRepository()
        assert repo.load_by_name("Test") is None

    def test_list_all(self):
        """Test listing all characters."""
        repo = MemoryCharacterRepository()
        character1 = Character(id="123", name="Test1")
        character2 = Character(id="456", name="Test2")
        repo.save(character1)
        repo.save(character2)
        all_characters = repo.list_all()
        assert character1 in all_characters
        assert character2 in all_characters

    def test_save_overwrite(self):
        """Test that saving a character with the same id overwrites the old one."""
        repo = MemoryCharacterRepository()
        character1 = Character(id="123", name="Test1")
        character2 = Character(id="123", name="Test2")
        repo.save(character1)
        repo.save(character2)
        loaded_character = repo.load("123")
        assert loaded_character.name == "Test2"
        assert len(repo.list_all()) == 1
