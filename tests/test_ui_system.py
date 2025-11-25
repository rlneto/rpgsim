"""
Unit tests for UI system implementation
Tests the modern terminal UI with Rich and Textual components
"""

import pytest
from unittest.mock import MagicMock, patch
from game.ui import TerminalUI, UIState, KeyHandler


class TestUIState:
    """Test UI state data structures"""
    
    @pytest.mark.unit
    def test_ui_state_creation(self):
        """Test UI state creation with default values"""
        state = UIState()
        
        assert state.screen == "main"
        assert state.selected_index == 0
        assert state.menu_items == []
        assert state.data is not None
    
    @pytest.mark.unit
    def test_ui_state_creation_with_values(self):
        """Test UI state creation with custom values"""
        menu_items = ["Option 1", "Option 2"]
        data = {"test": "value"}
        
        state = UIState(
            screen="menu",
            selected_index=1,
            menu_items=menu_items,
            data=data
        )
        
        assert state.screen == "menu"
        assert state.selected_index == 1
        assert state.menu_items == menu_items
        assert state.data == data
    
    @pytest.mark.unit
    def test_ui_state_post_init(self):
        """Test UI state post-initialization"""
        state = UIState(menu_items=None)
        
        assert state.menu_items == []


class TestTerminalUI:
    """Test terminal UI functionality"""
    
    @pytest.mark.unit
    def test_terminal_ui_initialization(self):
        """Test terminal UI initialization"""
        ui = TerminalUI()
        
        assert ui.console is not None
        assert ui.state.screen == "main"
        assert ui.state.selected_index == 0
        assert ui.running is True
        assert ui.game_data == {}
        assert ui.width == 80
        assert ui.height == 24
    
    @pytest.mark.unit
    def test_terminal_ui_clear(self):
        """Test terminal clearing functionality"""
        ui = TerminalUI()
        
        with patch.object(ui.console, 'clear') as mock_clear:
            ui.clear()
            mock_clear.assert_called_once()
    
    @pytest.mark.unit
    def test_get_centered_text(self):
        """Test centered text creation"""
        ui = TerminalUI()
        
        text = ui.get_centered_text("Test", "bold red")
        
        assert text is not None
        assert "Test" in str(text)
    
    @pytest.mark.unit
    def test_create_title(self):
        """Test title panel creation"""
        ui = TerminalUI()
        
        title = ui.create_title("RPGSim")
        
        assert title is not None
        assert "RPGSim" in str(title)
    
    @pytest.mark.unit
    def test_create_menu_table(self):
        """Test menu table creation"""
        ui = TerminalUI()
        items = ["Option 1", "Option 2", "Option 3"]
        
        table = ui.create_menu_table(items, selected=1)
        
        assert table is not None
        # Table should include all items
        table_str = str(table)
        assert "Option 1" in table_str
        assert "Option 2" in table_str
        assert "Option 3" in table_str
    
    @pytest.mark.unit
    def test_create_status_bar(self):
        """Test status bar creation"""
        ui = TerminalUI()
        ui.update_game_data({
            'player': {
                'hp': 50,
                'max_hp': 100,
                'level': 5,
                'gold': 250
            },
            'location': 'Test City'
        })
        
        status_bar = ui.create_status_bar()
        
        assert status_bar is not None
        status_str = str(status_bar)
        assert "HP:" in status_str
        assert "Level:" in status_str
        assert "Gold:" in status_str
        assert "Location:" in status_str
    
    @pytest.mark.unit
    def test_create_main_menu(self):
        """Test main menu layout creation"""
        ui = TerminalUI()
        
        layout = ui.create_main_menu()
        
        assert layout is not None
        # Should have header, body, footer sections
        assert hasattr(layout, 'split_column')
    
    @pytest.mark.unit
    def test_create_character_creation(self):
        """Test character creation screen"""
        ui = TerminalUI()
        ui.state.screen = "character_creation"
        ui.state.data = {"name": "TestChar", "class": "Warrior"}
        
        layout = ui.create_character_creation()
        
        assert layout is not None
        # Should include character creation form elements
    
    @pytest.mark.unit
    def test_create_game_screen(self):
        """Test main game screen"""
        ui = TerminalUI()
        ui.update_game_data({
            'player': {
                'name': 'TestPlayer',
                'level': 5,
                'hp': 80,
                'max_hp': 100,
                'gold': 500
            },
            'location': 'Test City',
            'events': ['Event 1', 'Event 2']
        })
        
        layout = ui.create_game_screen()
        
        assert layout is not None
        # Should include character info and game world
    
    @pytest.mark.unit
    def test_create_inventory_screen(self):
        """Test inventory screen"""
        ui = TerminalUI()
        ui.update_game_data({
            'inventory': [
                {'name': 'Sword', 'type': 'weapon', 'value': 100},
                {'name': 'Shield', 'type': 'armor', 'value': 150}
            ]
        })
        
        layout = ui.create_inventory_screen()
        
        assert layout is not None
        # Should include inventory items
    
    @pytest.mark.unit
    def test_create_save_load_screen(self):
        """Test save/load screen"""
        ui = TerminalUI()
        ui.update_game_data({
            'saves': [
                {'player_name': 'Player1', 'level': 5, 'location': 'City1'},
                {'player_name': 'Player2', 'level': 10, 'location': 'City2'}
            ]
        })
        
        # Test save screen
        save_layout = ui.create_save_load_screen("save")
        assert save_layout is not None
        
        # Test load screen
        load_layout = ui.create_save_load_screen("load")
        assert load_layout is not None
    
    @pytest.mark.unit
    def test_create_combat_screen(self):
        """Test combat screen"""
        ui = TerminalUI()
        ui.update_game_data({
            'player': {'name': 'Hero', 'hp': 75, 'max_hp': 100},
            'combat': {
                'enemy': {'name': 'Dragon', 'hp': 50, 'max_hp': 100},
                'round': 2,
                'status': 'Active',
                'log': ['Hero attacks!', 'Dragon breathes fire!']
            }
        })
        
        layout = ui.create_combat_screen()
        
        assert layout is not None
        # Should include combat elements
    
    @pytest.mark.unit
    def test_update_game_data(self):
        """Test game data updates"""
        ui = TerminalUI()
        initial_data = ui.game_data.copy()
        
        new_data = {'test': 'value', 'number': 42}
        ui.update_game_data(new_data)
        
        assert ui.game_data['test'] == 'value'
        assert ui.game_data['number'] == 42
        assert ui.game_data['player'] == initial_data.get('player')
    
    @pytest.mark.unit
    def test_show_loading_screen(self):
        """Test loading screen display"""
        ui = TerminalUI()
        
        with patch('game.ui.Progress') as mock_progress:
            ui.show_loading_screen("Testing...")
            mock_progress.assert_called()
    
    @pytest.mark.unit
    def test_show_error_message(self):
        """Test error message display"""
        ui = TerminalUI()
        
        with patch.object(ui.console, 'print') as mock_print:
            ui.show_error_message("Test error")
            mock_print.assert_called()
    
    @pytest.mark.unit
    def test_show_success_message(self):
        """Test success message display"""
        ui = TerminalUI()
        
        with patch.object(ui.console, 'print') as mock_print:
            ui.show_success_message("Test success")
            mock_print.assert_called()
    
    @pytest.mark.unit
    def test_get_text_input(self):
        """Test text input functionality"""
        ui = TerminalUI()
        
        with patch('game.ui.Prompt.ask', return_value="Test Input"):
            result = ui.get_text_input("Enter name:")
            assert result == "Test Input"
    
    @pytest.mark.unit
    def test_get_confirmation(self):
        """Test confirmation dialog"""
        ui = TerminalUI()
        
        with patch('game.ui.Confirm.ask', return_value=True):
            result = ui.get_confirmation("Are you sure?")
            assert result is True
    
    @pytest.mark.unit
    def test_handle_main_menu_input(self):
        """Test main menu input handling"""
        ui = TerminalUI()
        ui.state.screen = "main"
        
        initial_index = ui.state.selected_index
        
        # Test down arrow
        ui.handle_input("down")
        assert ui.state.selected_index == (initial_index + 1) % 4
        
        # Test up arrow
        ui.handle_input("up")
        assert ui.state.selected_index == initial_index
        
        # Test enter on New Character
        ui.handle_input("down")
        ui.handle_input("enter")
        assert ui.state.screen == "character_creation"
    
    @pytest.mark.unit
    def test_handle_character_creation_input(self):
        """Test character creation input handling"""
        ui = TerminalUI()
        ui.state.screen = "character_creation"
        ui.state.data = {"name": "", "class": None}
        
        initial_index = ui.state.selected_index
        
        # Test navigation
        ui.handle_input("j")
        assert ui.state.selected_index == initial_index + 1
        
        ui.handle_input("k")
        assert ui.state.selected_index == initial_index
        
        # Test escape
        ui.handle_input("esc")
        assert ui.state.screen == "main"
    
    @pytest.mark.unit
    def test_handle_game_input(self):
        """Test game screen input handling"""
        ui = TerminalUI()
        ui.state.screen = "game"
        
        # Test inventory key
        ui.handle_input("i")
        assert ui.state.screen == "inventory"
        
        # Test escape back to main
        ui.state.screen = "game"
        ui.handle_input("esc")
        assert ui.state.screen == "main"
    
    @pytest.mark.unit
    def test_handle_inventory_input(self):
        """Test inventory input handling"""
        ui = TerminalUI()
        ui.update_game_data({
            'inventory': [
                {'name': 'Sword', 'type': 'weapon', 'value': 100},
                {'name': 'Shield', 'type': 'armor', 'value': 150}
            ]
        })
        ui.state.screen = "inventory"
        
        initial_index = ui.state.selected_index
        
        # Test navigation
        ui.handle_input("j")
        assert ui.state.selected_index == initial_index + 1
        
        ui.handle_input("k")
        assert ui.state.selected_index == initial_index
        
        # Test escape back
        ui.handle_input("esc")
        assert ui.state.screen == "game"
    
    @pytest.mark.unit
    def test_handle_save_load_input(self):
        """Test save/load input handling"""
        ui = TerminalUI()
        ui.update_game_data({
            'saves': [
                {'player_name': 'Player1', 'level': 5},
                {'player_name': 'Player2', 'level': 10}
            ]
        })
        
        # Test save screen
        ui.state.screen = "save"
        initial_index = ui.state.selected_index
        
        ui.handle_input("j")
        assert ui.state.selected_index == initial_index + 1
        
        ui.handle_input("esc")
        assert ui.state.screen == "game"
        
        # Test load screen
        ui.state.screen = "load"
        ui.handle_input("esc")
        assert ui.state.screen == "game"
    
    @pytest.mark.unit
    def test_handle_combat_input(self):
        """Test combat input handling"""
        ui = TerminalUI()
        ui.update_game_data({
            'player': {'name': 'Hero', 'hp': 100, 'max_hp': 100},
            'combat': {
                'enemy': {'name': 'Dragon', 'hp': 100, 'max_hp': 100}
            }
        })
        ui.state.screen = "combat"
        
        initial_index = ui.state.selected_index
        
        # Test navigation
        ui.handle_input("j")
        assert ui.state.selected_index == initial_index + 1
        
        ui.handle_input("k")
        assert ui.state.selected_index == initial_index


class TestKeyHandler:
    """Test keyboard input handler"""
    
    @pytest.mark.unit
    def test_key_handler_initialization(self):
        """Test key handler initialization"""
        handler = KeyHandler()
        
        assert handler.key_callbacks == {}
    
    @pytest.mark.unit
    def test_register_callback(self):
        """Test callback registration"""
        handler = KeyHandler()
        
        def test_callback():
            pass
        
        handler.register_callback("a", test_callback)
        
        assert "a" in handler.key_callbacks
        assert handler.key_callbacks["a"] == test_callback
    
    @pytest.mark.unit
    def test_handle_key(self):
        """Test key handling"""
        handler = KeyHandler()
        callback_called = False
        
        def test_callback():
            nonlocal callback_called
            callback_called = True
        
        handler.register_callback("a", test_callback)
        handler.handle_key("a")
        
        assert callback_called
    
    @pytest.mark.unit
    def test_handle_unknown_key(self):
        """Test handling unknown key"""
        handler = KeyHandler()
        
        # Should not raise exception for unknown key
        handler.handle_key("unknown_key")
        
        assert True  # If we reach here, no exception was raised


class TestUIIntegration:
    """Test UI integration scenarios"""
    
    @pytest.mark.integration
    def test_complete_ui_navigation_flow(self):
        """Test complete UI navigation flow"""
        ui = TerminalUI()
        ui.state.screen = "main"
        
        # Navigate from main to character creation
        ui.handle_input("down")  # Select New Character
        ui.handle_input("enter")
        assert ui.state.screen == "character_creation"
        
        # Navigate through character creation
        ui.handle_input("down")  # Select class
        ui.handle_input("j")  # Move down in class list
        assert ui.state.selected_index > 1
        
        # Go back to main
        ui.handle_input("esc")
        assert ui.state.screen == "main"
    
    @pytest.mark.integration
    def test_game_state_updates_ui(self):
        """Test that game state updates are reflected in UI"""
        ui = TerminalUI()
        
        # Update player data
        ui.update_game_data({
            'player': {
                'name': 'TestHero',
                'level': 10,
                'hp': 85,
                'max_hp': 100,
                'gold': 750
            },
            'location': 'Test City',
            'events': ['Quest completed', 'Level up!']
        })
        
        # Test that status bar reflects new data
        status_bar = ui.create_status_bar()
        status_str = str(status_bar)
        
        assert "TestHero" in status_str
        assert "Level 10" in status_str
        assert "85/100" in status_str
        assert "750" in status_str
        assert "Test City" in status_str
    
    @pytest.mark.integration
    def test_screen_transitions_with_data(self):
        """Test screen transitions with data preservation"""
        ui = TerminalUI()
        
        # Set up game data
        game_data = {
            'player': {'name': 'Hero', 'level': 5},
            'inventory': [
                {'name': 'Sword', 'type': 'weapon', 'value': 100}
            ],
            'saves': [
                {'player_name': 'Save1', 'level': 3}
            ]
        }
        ui.update_game_data(game_data)
        
        # Transition to inventory
        ui.state.screen = "game"
        ui.handle_input("i")
        assert ui.state.screen == "inventory"
        
        # Inventory should have access to game data
        inventory_layout = ui.create_inventory_screen()
        assert inventory_layout is not None
        
        # Transition to save screen
        ui.state.screen = "game"
        ui.handle_input("F5")  # This would trigger save
        ui.state.screen = "save"
        save_layout = ui.create_save_load_screen("save")
        assert save_layout is not None
    
    @pytest.mark.integration
    def test_error_handling_in_ui(self):
        """Test error handling in UI operations"""
        ui = TerminalUI()
        
        # Test with corrupted data
        corrupted_data = {'player': None}
        ui.update_game_data(corrupted_data)
        
        # Should not crash when creating status bar
        try:
            status_bar = ui.create_status_bar()
            assert status_bar is not None
        except Exception:
            pytest.fail("UI should handle corrupted data gracefully")
    
    @pytest.mark.integration
    def test_ui_responsiveness_with_large_data(self):
        """Test UI responsiveness with large datasets"""
        ui = TerminalUI()
        
        # Test with large inventory
        large_inventory = [
            {'name': f'Item_{i}', 'type': 'misc', 'value': i * 10}
            for i in range(100)
        ]
        ui.update_game_data({'inventory': large_inventory})
        
        # Should handle large inventory without crashing
        try:
            inventory_layout = ui.create_inventory_screen()
            assert inventory_layout is not None
        except Exception:
            pytest.fail("UI should handle large datasets without crashing")
        
        # Test with many save files
        many_saves = [
            {'player_name': f'Player_{i}', 'level': i, 'location': f'City_{i}'}
            for i in range(50)
        ]
        ui.update_game_data({'saves': many_saves})
        
        # Should handle many save files
        try:
            save_layout = ui.create_save_load_screen("load")
            assert save_layout is not None
        except Exception:
            pytest.fail("UI should handle many save files without crashing")