"""
Unit Tests for the CharacterBalanceService.
"""

import pytest
from core.systems.character.services.character_service import CharacterBalanceService

class TestCharacterBalanceService:
    """Test CharacterBalanceService functionality."""

    def test_get_balance_stats(self):
        """Test the get_balance_stats method."""
        service = CharacterBalanceService()
        stats = service.get_balance_stats()
        assert "Warrior" in stats
        assert stats["Warrior"] == 76

    def test_validate_balance(self):
        """Test the validate_balance method."""
        service = CharacterBalanceService()
        assert service.validate_balance() is True

    def test_validate_balance_empty_stats(self):
        """Test the validate_balance method with empty stats."""
        service = CharacterBalanceService()
        with pytest.MonkeyPatch.context() as m:
            m.setattr(service, "get_balance_stats", lambda: {})
            assert service.validate_balance() is False

    def test_verify_unique_mechanics(self):
        """Test the verify_unique_mechanics method."""
        service = CharacterBalanceService()
        assert service.verify_unique_mechanics() is True

    def test_verify_minimum_abilities(self):
        """Test the verify_minimum_abilities method."""
        service = CharacterBalanceService()
        assert service.verify_minimum_abilities() is True

    def test_verify_minimum_abilities_fails(self):
        """Test the verify_minimum_abilities method when a class has too few abilities."""
        service = CharacterBalanceService()
        with pytest.MonkeyPatch.context() as m:
            m.setattr(service.class_configs[list(service.class_configs.keys())[0]], "abilities", [])
            assert service.verify_minimum_abilities() is False
