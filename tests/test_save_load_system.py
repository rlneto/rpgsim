"""
Unit tests for save/load system implementation
Uses pytest with hypothesis for edge and boundary testing
"""

import pytest
import os
import json
import tempfile
import shutil
from unittest.mock import MagicMock, patch, mock_open
from game.save_load import SaveManager, GameState, SaveData
from tests.conftest import create_test_player, create_test_enemy


class TestSaveManager:
    """Test save/load manager functionality"""
    
    @pytest.fixture
    def temp_save_dir(self):
        """Create a temporary directory for save files"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.mark.unit
    def test_save_manager_initialization(self, temp_save_dir):
        """Test that save manager initializes correctly"""
        save_manager = SaveManager(save_directory=temp_save_dir)
        
        assert save_manager.save_directory == temp_save_dir
        assert os.path.exists(temp_save_dir)
        assert save_manager.max_save_slots == 10  # Default value
    
    @pytest.mark.unit
    def test_save_manager_initialization_with_custom_slots(self, temp_save_dir):
        """Test that save manager initializes with custom save slots"""
        save_manager = SaveManager(save_directory=temp_dir, max_save_slots=5)
        
        assert save_manager.max_save_slots == 5
    
    @pytest.mark.unit
    def test_save_manager_creates_directory_if_not_exists(self):
        """Test that save manager creates directory if it doesn't exist"""
        with tempfile.TemporaryDirectory() as parent_dir:
            save_dir = os.path.join(parent_dir, "new_save_dir")
            assert not os.path.exists(save_dir)
            
            save_manager = SaveManager(save_directory=save_dir)
            
            assert os.path.exists(save_dir)
            assert save_manager.save_directory == save_dir
    
    @pytest.mark.unit
    def test_save_game_state(self, temp_save_dir):
        """Test that game state can be saved"""
        save_manager = SaveManager(save_directory=temp_save_dir)
        
        # Create a test game state
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={"quest1": 0.5, "quest2": 0.2}
        )
        
        # Save the game state
        save_path = save_manager.save_game(game_state, slot=1)
        
        # Verify save file was created
        assert os.path.exists(save_path)
        
        # Verify save file contains expected data
        with open(save_path, 'r') as f:
            save_data = json.load(f)
        
        assert save_data['player']['name'] == player.name
        assert save_data['current_location'] == "test_city"
        assert save_data['world_time'] == 12345
        assert 'quest1' in save_data['quest_progress']
    
    @pytest.mark.unit
    def test_load_game_state(self, temp_save_dir):
        """Test that game state can be loaded"""
        save_manager = SaveManager(save_directory=temp_save_dir)
        
        # Create and save a test game state
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={"quest1": 0.5, "quest2": 0.2}
        )
        
        save_manager.save_game(game_state, slot=1)
        
        # Load the game state
        loaded_state = save_manager.load_game(slot=1)
        
        # Verify loaded state matches saved state
        assert loaded_state.player.name == player.name
        assert loaded_state.current_location == "test_city"
        assert loaded_state.world_time == 12345
        assert loaded_state.quest_progress["quest1"] == 0.5
        assert loaded_state.quest_progress["quest2"] == 0.2
    
    @pytest.mark.unit
    def test_save_overwrites_existing_slot(self, temp_save_dir):
        """Test that saving overwrites existing save slot"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Create initial game state and save
        player1 = create_test_player("Warrior", 5)
        game_state1 = GameState(
            player=player1,
            current_location="city1",
            world_time=1000,
            quest_progress={}
        )
        
        save_manager.save_game(game_state1, slot=1)
        
        # Create different game state and save to same slot
        player2 = create_test_player("Mage", 7)
        game_state2 = GameState(
            player=player2,
            current_location="city2",
            world_time=2000,
            quest_progress={}
        )
        
        save_manager.save_game(game_state2, slot=1)
        
        # Load and verify the new state was saved
        loaded_state = save_manager.load_game(slot=1)
        
        assert loaded_state.player.name == player2.name
        assert loaded_state.current_location == "city2"
        assert loaded_state.world_time == 2000
    
    @pytest.mark.unit
    def test_save_with_metadata(self, temp_save_dir):
        """Test that saves include metadata"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        save_path = save_manager.save_game(game_state, slot=1)
        
        # Verify metadata is included
        with open(save_path, 'r') as f:
            save_data = json.load(f)
        
        assert 'metadata' in save_data
        assert 'version' in save_data['metadata']
        assert 'timestamp' in save_data['metadata']
        assert 'player_level' in save_data['metadata']
        assert 'play_time' in save_data['metadata']
    
    @pytest.mark.unit
    def test_load_nonexistent_save_file(self, temp_save_dir):
        """Test loading a save file that doesn't exist"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        with pytest.raises(FileNotFoundError):
            save_manager.load_game(slot=1)
    
    @pytest.mark.unit
    def test_load_corrupted_save_file(self, temp_save_dir):
        """Test loading a corrupted save file"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Create a corrupted save file
        save_path = os.path.join(temp_dir, "save_1.json")
        with open(save_path, 'w') as f:
            f.write("This is not valid JSON")
        
        with pytest.raises(json.JSONDecodeError):
            save_manager.load_game(slot=1)
    
    @pytest.mark.unit
    def test_list_save_files(self, temp_save_dir):
        """Test listing available save files"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Initially no save files
        save_files = save_manager.list_save_files()
        assert len(save_files) == 0
        
        # Save some games
        for slot in [1, 3, 5]:
            player = create_test_player("Warrior", slot)
            game_state = GameState(
                player=player,
                current_location=f"city_{slot}",
                world_time=slot * 1000,
                quest_progress={}
            )
            save_manager.save_game(game_state, slot=slot)
        
        # List save files
        save_files = save_manager.list_save_files()
        
        # Should have 3 save files
        assert len(save_files) == 3
        
        # Should have information for each saved game
        assert save_files[0]['slot'] == 1
        assert save_files[1]['slot'] == 3
        assert save_files[2]['slot'] == 5
    
    @pytest.mark.unit
    def test_delete_save_file(self, temp_save_dir):
        """Test deleting a save file"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Save a game
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        save_path = save_manager.save_game(game_state, slot=1)
        assert os.path.exists(save_path)
        
        # Delete the save file
        result = save_manager.delete_save(slot=1)
        
        assert result is True
        assert not os.path.exists(save_path)
    
    @pytest.mark.unit
    def test_delete_nonexistent_save_file(self, temp_save_dir):
        """Test deleting a save file that doesn't exist"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        result = save_manager.delete_save(slot=1)
        
        assert result is False
    
    @pytest.mark.unit
    def test_auto_save_functionality(self, temp_save_dir):
        """Test auto-save functionality"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        # Enable auto-save with 3-minute interval
        save_manager.enable_auto_save(game_state, interval_seconds=180)
        
        # Auto-save should create a save file
        auto_save_path = os.path.join(temp_dir, "autosave.json")
        
        # Trigger auto-save manually for testing
        save_manager.trigger_auto_save()
        
        assert os.path.exists(auto_save_path)
    
    @pytest.mark.unit
    def test_quick_save_functionality(self, temp_save_dir):
        """Test quick-save functionality"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        # Perform quick save
        save_path = save_manager.quick_save(game_state)
        
        # Verify quick save file was created
        assert os.path.exists(save_path)
        assert "quicksave" in save_path
        
        # Load and verify content
        loaded_state = save_manager.load_quick_save()
        
        assert loaded_state.player.name == player.name
        assert loaded_state.current_location == "test_city"
    
    @pytest.mark.unit
    def test_quick_load_functionality(self, temp_save_dir):
        """Test quick-load functionality"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        # Save and then quick load
        save_manager.quick_save(game_state)
        loaded_state = save_manager.load_quick_save()
        
        assert loaded_state.player.name == player.name
        assert loaded_state.current_location == "test_city"
        assert loaded_state.world_time == 12345
    
    @pytest.mark.unit
    def test_quick_load_without_existing_save(self, temp_save_dir):
        """Test quick-load when no quick save exists"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        with pytest.raises(FileNotFoundError):
            save_manager.load_quick_save()


class TestGameState:
    """Test game state data structures"""
    
    @pytest.mark.unit
    def test_game_state_creation(self):
        """Test game state creation with valid data"""
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={"quest1": 0.5, "quest2": 0.2}
        )
        
        assert game_state.player == player
        assert game_state.current_location == "test_city"
        assert game_state.world_time == 12345
        assert game_state.quest_progress == {"quest1": 0.5, "quest2": 0.2}
    
    @pytest.mark.unit
    def test_game_state_to_dict(self):
        """Test converting game state to dictionary"""
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={"quest1": 0.5, "quest2": 0.2}
        )
        
        state_dict = game_state.to_dict()
        
        assert state_dict['player']['name'] == player.name
        assert state_dict['current_location'] == "test_city"
        assert state_dict['world_time'] == 12345
        assert state_dict['quest_progress'] == {"quest1": 0.5, "quest2": 0.2}
    
    @pytest.mark.unit
    def test_game_state_from_dict(self):
        """Test creating game state from dictionary"""
        state_dict = {
            'player': {
                'name': 'TestWarrior',
                'class': 'Warrior',
                'level': 5,
                'stats': {'strength': 15, 'dexterity': 12}
            },
            'current_location': 'test_city',
            'world_time': 12345,
            'quest_progress': {'quest1': 0.5, 'quest2': 0.2}
        }
        
        game_state = GameState.from_dict(state_dict)
        
        assert game_state.player.name == 'TestWarrior'
        assert game_state.player.class_type == 'Warrior'
        assert game_state.player.level == 5
        assert game_state.current_location == "test_city"
        assert game_state.world_time == 12345
        assert game_state.quest_progress == {'quest1': 0.5, 'quest2': 0.2}
    
    @pytest.mark.unit
    @given(st.integers(min_value=0, max_value=100000))
    def test_game_state_world_time(self, world_time):
        """Test game state with various world times"""
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=world_time,
            quest_progress={}
        )
        
        assert game_state.world_time == world_time
    
    @pytest.mark.unit
    @given(st.dictionaries(keys=st.text(min_size=1), values=st.floats(min_value=0.0, max_value=1.0)))
    def test_game_state_quest_progress(self, quest_progress):
        """Test game state with various quest progress"""
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress=quest_progress
        )
        
        assert game_state.quest_progress == quest_progress
    
    @pytest.mark.unit
    def test_game_state_validation(self):
        """Test game state validation"""
        # Valid state should pass validation
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        assert game_state.is_valid() is True
        
        # Invalid state should fail validation
        invalid_state = GameState(
            player=None,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        assert invalid_state.is_valid() is False


class TestSaveData:
    """Test save data structures"""
    
    @pytest.mark.unit
    def test_save_data_creation(self):
        """Test save data creation with valid data"""
        metadata = {
            'version': '1.0.0',
            'timestamp': '2023-01-01T12:00:00Z',
            'player_level': 5,
            'play_time': 3600
        }
        
        game_data = {
            'player': {'name': 'TestPlayer', 'level': 5},
            'current_location': 'test_city',
            'world_time': 12345
        }
        
        save_data = SaveData(metadata=metadata, game_data=game_data)
        
        assert save_data.metadata == metadata
        assert save_data.game_data == game_data
    
    @pytest.mark.unit
    def test_save_data_to_json(self):
        """Test converting save data to JSON"""
        metadata = {
            'version': '1.0.0',
            'timestamp': '2023-01-01T12:00:00Z',
            'player_level': 5,
            'play_time': 3600
        }
        
        game_data = {
            'player': {'name': 'TestPlayer', 'level': 5},
            'current_location': 'test_city',
            'world_time': 12345
        }
        
        save_data = SaveData(metadata=metadata, game_data=game_data)
        json_data = save_data.to_json()
        
        parsed_data = json.loads(json_data)
        
        assert parsed_data['metadata'] == metadata
        assert parsed_data['game_data'] == game_data
    
    @pytest.mark.unit
    def test_save_data_from_json(self):
        """Test creating save data from JSON"""
        save_json = json.dumps({
            'metadata': {
                'version': '1.0.0',
                'timestamp': '2023-01-01T12:00:00Z',
                'player_level': 5,
                'play_time': 3600
            },
            'game_data': {
                'player': {'name': 'TestPlayer', 'level': 5},
                'current_location': 'test_city',
                'world_time': 12345
            }
        })
        
        save_data = SaveData.from_json(save_json)
        
        assert save_data.metadata['version'] == '1.0.0'
        assert save_data.game_data['player']['name'] == 'TestPlayer'
    
    @pytest.mark.unit
    def test_save_data_validation(self):
        """Test save data validation"""
        # Valid save data should pass validation
        metadata = {
            'version': '1.0.0',
            'timestamp': '2023-01-01T12:00:00Z',
            'player_level': 5,
            'play_time': 3600
        }
        
        game_data = {
            'player': {'name': 'TestPlayer', 'level': 5},
            'current_location': 'test_city',
            'world_time': 12345
        }
        
        save_data = SaveData(metadata=metadata, game_data=game_data)
        
        assert save_data.is_valid() is True
        
        # Invalid save data should fail validation
        invalid_save_data = SaveData(metadata={}, game_data={})
        
        assert invalid_save_data.is_valid() is False


class TestSaveLoadIntegration:
    """Test save/load integration"""
    
    @pytest.fixture
    def temp_save_dir(self):
        """Create a temporary directory for save files"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_complete_save_load_cycle(self, temp_save_dir):
        """Test complete save/load cycle with complex game state"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Create a complex game state
        player = create_test_player("Warrior", 10)
        player.quests['active'] = ['quest1', 'quest2']
        player.quests['completed'] = ['quest0']
        
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=50000,
            quest_progress={
                'quest1': 0.75,
                'quest2': 0.25,
                'quest3': 0.0
            },
            discovered_locations=['city1', 'city2', 'city3'],
            inventory=['sword', 'shield', 'potion'],
            known_spells=['fireball', 'heal']
        )
        
        # Save the game state
        save_path = save_manager.save_game(game_state, slot=1)
        
        # Load the game state
        loaded_state = save_manager.load_game(slot=1)
        
        # Verify all data was preserved
        assert loaded_state.player.name == player.name
        assert loaded_state.player.level == player.level
        assert loaded_state.player.quests == player.quests
        assert loaded_state.current_location == "test_city"
        assert loaded_state.world_time == 50000
        assert loaded_state.quest_progress == {
            'quest1': 0.75,
            'quest2': 0.25,
            'quest3': 0.0
        }
        assert loaded_state.discovered_locations == ['city1', 'city2', 'city3']
        assert loaded_state.inventory == ['sword', 'shield', 'potion']
        assert loaded_state.known_spells == ['fireball', 'heal']
    
    @pytest.mark.integration
    def test_multiple_save_slots(self, temp_save_dir):
        """Test saving and loading from multiple slots"""
        save_manager = SaveManager(save_directory=temp_dir)
        
        # Create and save different game states in different slots
        game_states = []
        for slot in [1, 3, 7]:
            player = create_test_player("Warrior", slot * 2)
            game_state = GameState(
                player=player,
                current_location=f"city_{slot}",
                world_time=slot * 10000,
                quest_progress={}
            )
            game_states.append(game_state)
            save_manager.save_game(game_state, slot=slot)
        
        # Load and verify each state
        for i, slot in enumerate([1, 3, 7]):
            loaded_state = save_manager.load_game(slot=slot)
            original_state = game_states[i]
            
            assert loaded_state.player.name == original_state.player.name
            assert loaded_state.player.level == original_state.player.level
            assert loaded_state.current_location == original_state.current_location
            assert loaded_state.world_time == original_state.world_time
    
    @pytest.mark.integration
    @given(st.integers(min_value=1, max_value=10))
    def test_save_version_compatibility(self, save_version, temp_save_dir):
        """Test save version compatibility"""
        # This test would involve mocking different save format versions
        # For now, we'll just test with the current version
        save_manager = SaveManager(save_directory=temp_dir)
        
        player = create_test_player("Warrior", 5)
        game_state = GameState(
            player=player,
            current_location="test_city",
            world_time=12345,
            quest_progress={}
        )
        
        # Save with current version
        save_manager.save_game(game_state, slot=1)
        
        # Load and verify compatibility
        loaded_state = save_manager.load_game(slot=1)
        
        assert loaded_state.player.name == player.name