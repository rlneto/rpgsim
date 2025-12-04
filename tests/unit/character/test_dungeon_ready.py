"""
Unit Tests for the Dungeon Ready Monkey Patch.
"""

import pytest
from core.systems.character.domain.character import Character
from core.systems.character.dungeon_ready import add_dungeon_exploration_to_character

class TestDungeonReady:
    """Test DungeonReady functionality."""

    def test_can_enter_dungeon(self):
        """Test the can_enter_dungeon method."""
        character = Character(level=1, hp=100, max_hp=100, created=True)
        assert character.can_enter_dungeon("normal") is True

    def test_can_enter_dungeon_low_level(self):
        """Test the can_enter_dungeon method with a low-level character."""
        character = Character(level=0, hp=100, max_hp=100, created=True)
        assert character.can_enter_dungeon("normal") is False

    def test_can_enter_dungeon_low_hp(self):
        """Test the can_enter_dungeon method with a low-HP character."""
        character = Character(level=1, hp=49, max_hp=100, created=True)
        assert character.can_enter_dungeon("normal") is False

    def test_prepare_for_dungeon(self):
        """Test the prepare_for_dungeon method."""
        character = Character(gold=50, hp=80, max_hp=100, created=True)
        preparation = character.prepare_for_dungeon()
        assert preparation["cost"] == 30
        assert character.gold == 20
        assert character.hp == 100

    def test_prepare_for_dungeon_low_gold(self):
        """Test the prepare_for_dungeon method with low gold."""
        character = Character(gold=20, hp=80, max_hp=100, created=True)
        preparation = character.prepare_for_dungeon()
        assert preparation["cost"] == 15
        assert character.gold == 5

    def test_prepare_for_dungeon_no_gold(self):
        """Test the prepare_for_dungeon method with no gold."""
        character = Character(gold=0, hp=80, max_hp=100, created=True)
        preparation = character.prepare_for_dungeon()
        assert preparation["cost"] == 15
        assert character.gold == 0

    def test_get_dungeon_readiness(self):
        """Test the get_dungeon_readiness method."""
        character = Character(level=1, hp=100, max_hp=100, gold=50, created=True)
        readiness = character.get_dungeon_readiness()
        assert readiness["overall_ready"] is True
