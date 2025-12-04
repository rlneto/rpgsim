"""
Unit Tests for the CharacterSystem Facade.
"""

import pytest
from unittest.mock import MagicMock, patch
from core.systems.character.facade import CharacterSystem, create_character, level_up_character, add_experience, get_all_character_classes, get_class_balance_stats, validate_class_balance, verify_unique_mechanics, verify_minimum_abilities, heal_character, get_default_stats_for_class
from core.systems.character.domain.character import Character, CharacterClass
from core.systems.character.exceptions.character_exceptions import (
    CharacterCreationError,
    CharacterNotFoundError,
)


@pytest.fixture
def mock_repo():
    """Fixture for a mocked character repository."""
    return MagicMock()


@pytest.fixture
def mock_creation_service():
    """Fixture for a mocked character creation service."""
    return MagicMock()


@pytest.fixture
def mock_progression_service():
    """Fixture for a mocked character progression service."""
    return MagicMock()


@pytest.fixture
def mock_inventory_service():
    """Fixture for a mocked character inventory service."""
    return MagicMock()


@pytest.fixture
def mock_balance_service():
    """Fixture for a mocked character balance service."""
    return MagicMock()


@pytest.fixture
def character_system(
    mock_repo,
    mock_creation_service,
    mock_progression_service,
    mock_inventory_service,
    mock_balance_service,
):
    """Fixture for a CharacterSystem with mocked dependencies."""
    with patch(
        "core.systems.character.facade.MemoryCharacterRepository", return_value=mock_repo
    ), patch(
        "core.systems.character.facade.CharacterCreationService",
        return_value=mock_creation_service,
    ), patch(
        "core.systems.character.facade.CharacterProgressionService",
        return_value=mock_progression_service,
    ), patch(
        "core.systems.character.facade.CharacterInventoryService",
        return_value=mock_inventory_service,
    ), patch(
        "core.systems.character.facade.CharacterBalanceService",
        return_value=mock_balance_service,
    ):
        system = CharacterSystem(repository=mock_repo)
        # manually set the services as they are set in the init method of the real class
        system.creation_service = mock_creation_service
        system.progression_service = mock_progression_service
        system.inventory_service = mock_inventory_service
        system.balance_service = mock_balance_service
        yield system


class TestCharacterSystem:
    def test_create_character_success(self, character_system, mock_creation_service, mock_repo):
        mock_char = MagicMock(spec=Character)
        mock_char.created = True
        mock_creation_service.create_character.return_value = mock_char

        result = character_system.create_character("Test", "warrior")

        assert result == mock_char
        mock_creation_service.create_character.assert_called_once_with("Test", "warrior")
        mock_repo.save.assert_called_once_with(mock_char)

    def test_create_character_failure(self, character_system, mock_creation_service, mock_repo):
        mock_char = MagicMock(spec=Character)
        mock_char.created = False
        mock_creation_service.create_character.return_value = mock_char

        with pytest.raises(CharacterCreationError):
            character_system.create_character("Test", "warrior")

        mock_creation_service.create_character.assert_called_once_with("Test", "warrior")
        mock_repo.save.assert_not_called()

    def test_get_character(self, character_system, mock_repo):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char

        result = character_system.get_character("123")

        assert result == mock_char
        mock_repo.load.assert_called_once_with("123")

    def test_get_character_not_found(self, character_system, mock_repo):
        mock_repo.load.return_value = None

        result = character_system.get_character("123")

        assert result is None
        mock_repo.load.assert_called_once_with("123")

    def test_get_character_by_name(self, character_system, mock_repo):
        mock_char = MagicMock(spec=Character)
        mock_repo.load_by_name.return_value = mock_char

        result = character_system.get_character_by_name("Test")

        assert result == mock_char
        mock_repo.load_by_name.assert_called_once_with("Test")

    def test_level_up_character_success(
        self, character_system, mock_repo, mock_progression_service
    ):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char
        mock_progression_service.level_up.return_value = True

        result = character_system.level_up_character("123")

        assert result is True
        mock_repo.load.assert_called_once_with("123")
        mock_progression_service.level_up.assert_called_once_with(mock_char)
        mock_repo.save.assert_called_once_with(mock_char)

    def test_level_up_character_failure(
        self, character_system, mock_repo, mock_progression_service
    ):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char
        mock_progression_service.level_up.return_value = False

        result = character_system.level_up_character("123")

        assert result is False
        mock_repo.load.assert_called_once_with("123")
        mock_progression_service.level_up.assert_called_once_with(mock_char)
        mock_repo.save.assert_not_called()

    def test_level_up_character_not_found(self, character_system, mock_repo):
        mock_repo.load.return_value = None

        with pytest.raises(CharacterNotFoundError):
            character_system.level_up_character("123")

    def test_add_to_inventory_success(
        self, character_system, mock_repo, mock_inventory_service
    ):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char
        mock_inventory_service.add_item.return_value = True

        result = character_system.add_to_inventory("123", "sword")

        assert result is True
        mock_repo.load.assert_called_once_with("123")
        mock_inventory_service.add_item.assert_called_once_with(mock_char, "sword")
        mock_repo.save.assert_called_once_with(mock_char)

    def test_add_to_inventory_not_found(self, character_system, mock_repo):
        mock_repo.load.return_value = None
        with pytest.raises(CharacterNotFoundError):
            character_system.add_to_inventory("123", "sword")

    def test_remove_from_inventory_success(
        self, character_system, mock_repo, mock_inventory_service
    ):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char
        mock_inventory_service.remove_item.return_value = True

        result = character_system.remove_from_inventory("123", "sword")

        assert result is True
        mock_repo.load.assert_called_once_with("123")
        mock_inventory_service.remove_item.assert_called_once_with(mock_char, "sword")
        mock_repo.save.assert_called_once_with(mock_char)

    def test_remove_from_inventory_not_found(self, character_system, mock_repo):
        mock_repo.load.return_value = None
        with pytest.raises(CharacterNotFoundError):
            character_system.remove_from_inventory("123", "sword")

    def test_get_inventory_count(
        self, character_system, mock_repo, mock_inventory_service
    ):
        mock_char = MagicMock(spec=Character)
        mock_repo.load.return_value = mock_char
        mock_inventory_service.get_inventory_count.return_value = 5

        result = character_system.get_inventory_count("123")

        assert result == 5
        mock_repo.load.assert_called_once_with("123")
        mock_inventory_service.get_inventory_count.assert_called_once_with(mock_char)

    def test_get_inventory_count_not_found(self, character_system, mock_repo):
        mock_repo.load.return_value = None
        with pytest.raises(CharacterNotFoundError):
            character_system.get_inventory_count("123")

    @patch('core.systems.character.facade.MemoryClassConfigRepository')
    def test_get_class_stats(self, mock_config_repo, character_system):
        mock_config_repo.return_value.get_config.return_value = {"mechanic": "rage"}
        stats = character_system.get_class_stats("Warrior")
        assert stats == {"mechanic": "rage"}

    def test_get_class_stats_invalid_class(self, character_system):
        stats = character_system.get_class_stats("InvalidClass")
        assert stats is None

    @patch('core.systems.character.facade.MemoryClassConfigRepository')
    def test_get_class_mechanic(self, mock_config_repo, character_system):
        mock_config_repo.return_value.get_config.return_value = {"mechanic": "rage", "abilities": ["slash"]}
        mechanic = character_system.get_class_mechanic("Warrior")
        assert mechanic == "rage"

    def test_get_class_mechanic_no_stats(self, character_system):
        with patch.object(character_system, 'get_class_stats', return_value=None):
            mechanic = character_system.get_class_mechanic("Warrior")
            assert mechanic is None

    @patch('core.systems.character.facade.MemoryClassConfigRepository')
    def test_get_class_abilities(self, mock_config_repo, character_system):
        mock_config_repo.return_value.get_config.return_value = {"mechanic": "rage", "abilities": ["slash"]}
        abilities = character_system.get_class_abilities("Warrior")
        assert abilities == ["slash"]

    def test_get_class_abilities_no_stats(self, character_system):
        with patch.object(character_system, 'get_class_stats', return_value=None):
            abilities = character_system.get_class_abilities("Warrior")
            assert abilities is None

    def test_get_all_classes(self, character_system):
        classes = character_system.get_all_classes()
        assert "Warrior" in classes
        assert "Mage" in classes
        assert "Rogue" in classes

    def test_validate_class_balance(self, character_system, mock_balance_service):
        mock_balance_service.validate_balance.return_value = True
        assert character_system.validate_class_balance() is True
        mock_balance_service.validate_balance.assert_called_once()

    def test_verify_unique_mechanics(self, character_system, mock_balance_service):
        mock_balance_service.verify_unique_mechanics.return_value = True
        assert character_system.verify_unique_mechanics() is True
        mock_balance_service.verify_unique_mechanics.assert_called_once()

    def test_verify_minimum_abilities(self, character_system, mock_balance_service):
        mock_balance_service.verify_minimum_abilities.return_value = True
        assert character_system.verify_minimum_abilities() is True
        mock_balance_service.verify_minimum_abilities.assert_called_once()

    def test_list_all_characters(self, character_system, mock_repo):
        mock_char1 = MagicMock(spec=Character)
        mock_char2 = MagicMock(spec=Character)
        mock_repo.list_all.return_value = [mock_char1, mock_char2]

        result = character_system.list_all_characters()

        assert result == [mock_char1, mock_char2]
        mock_repo.list_all.assert_called_once()

def test_backward_compatibility_create_character():
    with patch('core.systems.character.facade._character_system') as mock_system:
        create_character("Test", "Warrior")
        mock_system.create_character.assert_called_once_with("Test", "Warrior")

def test_backward_compatibility_level_up_character():
    mock_char = MagicMock(spec=Character)
    level_up_character(mock_char)
    mock_char.level_up.assert_called_once()

def test_backward_compatibility_add_experience():
    mock_char = MagicMock(spec=Character)
    mock_char.experience = 0
    add_experience(mock_char, 100)
    assert mock_char.experience == 100

def test_backward_compatibility_add_experience_negative_exp():
    mock_char = MagicMock(spec=Character)
    mock_char.experience = 50
    result = add_experience(mock_char, -10)
    assert result is False
    assert mock_char.experience == 50

def test_backward_compatibility_get_all_character_classes():
    with patch('core.systems.character.facade._character_system') as mock_system:
        mock_system.get_all_classes.return_value = ["Warrior", "Mage"]
        result = get_all_character_classes()
        assert result == [("Warrior", "Warrior"), ("Mage", "Mage")]

def test_backward_compatibility_get_class_balance_stats():
    result = get_class_balance_stats()
    assert result == {}

def test_backward_compatibility_validate_class_balance():
    with patch('core.systems.character.facade._character_system') as mock_system:
        validate_class_balance()
        mock_system.validate_class_balance.assert_called_once()

def test_backward_compatibility_verify_unique_mechanics():
    with patch('core.systems.character.facade._character_system') as mock_system:
        verify_unique_mechanics()
        mock_system.verify_unique_mechanics.assert_called_once()

def test_backward_compatibility_verify_minimum_abilities():
    with patch('core.systems.character.facade._character_system') as mock_system:
        verify_minimum_abilities()
        mock_system.verify_minimum_abilities.assert_called_once()

def test_backward_compatibility_heal_character():
    mock_char = MagicMock(spec=Character)
    assert heal_character(mock_char, 10) is True
    assert heal_character(mock_char, 0) is False

def test_backward_compatibility_get_default_stats_for_class():
    stats = get_default_stats_for_class("Warrior")
    assert stats["strength"] == 15
    stats = get_default_stats_for_class("Unknown")
    assert stats["strength"] == 10
