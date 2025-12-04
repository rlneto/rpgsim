"""
Unit Tests for the CharacterStats Model.
"""

import pytest
from core.systems.character.domain.character import CharacterStats, CharacterClassConfig

class TestCharacterStats:
    """Test CharacterStats model functionality."""

    def test_default_stats_creation(self):
        """Test creating character stats with default values."""
        stats = CharacterStats()
        assert stats.strength == 10
        assert stats.dexterity == 10
        assert stats.intelligence == 10
        assert stats.wisdom == 10
        assert stats.charisma == 10
        assert stats.constitution == 10

    def test_custom_stats_creation(self):
        """Test creating character stats with custom values."""
        stats = CharacterStats(
            strength=15,
            dexterity=12,
            intelligence=8,
            wisdom=14,
            charisma=10,
            constitution=13,
        )
        assert stats.strength == 15
        assert stats.dexterity == 12
        assert stats.intelligence == 8
        assert stats.wisdom == 14
        assert stats.charisma == 10
        assert stats.constitution == 13

    def test_total_power(self):
        """Test total power calculation."""
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )
        assert stats.total_power() == 60

    def test_get_strengths(self):
        """Test the get_strengths method."""
        stats = CharacterStats(strength=15, dexterity=16)
        strengths = stats.get_strengths()
        assert "strength" in strengths
        assert "dexterity" in strengths
        assert "intelligence" not in strengths

    def test_get_weaknesses(self):
        """Test the get_weaknesses method."""
        stats = CharacterStats(strength=15, intelligence=8, wisdom=10)
        weaknesses = stats.get_weaknesses()
        assert "intelligence" in weaknesses
        assert "wisdom" in weaknesses
        assert "strength" not in weaknesses

class TestCharacterClassConfig:
    """Test CharacterClassConfig model functionality."""

    def test_post_init_valid(self):
        """Test the __post_init__ method with valid data."""
        stats = CharacterStats(strength=10)
        config = CharacterClassConfig(
            mechanic="test",
            base_stats=stats,
            primary_stat="strength",
        )
        assert config.primary_stat == "strength"

    def test_post_init_invalid(self):
        """Test the __post_init__ method with invalid data."""
        stats = CharacterStats(strength=10)
        with pytest.raises(ValueError):
            CharacterClassConfig(
                mechanic="test",
                base_stats=stats,
                primary_stat="invalid",
            )
