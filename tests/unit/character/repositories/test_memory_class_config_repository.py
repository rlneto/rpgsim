"""
Unit Tests for the MemoryClassConfigRepository.
"""

import pytest
from core.systems.character.repositories.memory_repository import MemoryClassConfigRepository
from core.systems.character.domain.character import CharacterClass

class TestMemoryClassConfigRepository:
    """Test MemoryClassConfigRepository functionality."""

    def test_get_config(self):
        """Test getting a class config."""
        repo = MemoryClassConfigRepository()
        config = repo.get_config(CharacterClass.WARRIOR)
        assert config is not None
        assert config["mechanic"] == "Weapon Mastery"

    def test_get_config_not_found(self):
        """Test getting a class config that does not exist."""
        repo = MemoryClassConfigRepository()
        config = repo.get_config(CharacterClass.DEVELOPER)
        assert config is None
