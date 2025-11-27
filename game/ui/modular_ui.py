"""
Modern Terminal UI Facade
Clean interface for UI operations
"""

from typing import Dict, Any, List, Optional, Callable
from ..ui.domain.ui import (
    UISession, UIState, MessageType, ColorScheme,
    LogMessage, MenuItem, MenuConfig
)
from ..ui.services.ui_service import UIServiceFactory
from ..ui.screens.modern_terminal_ui import (
    GameScreen, CharacterCreationScreen, MainMenuScreen,
    GameState, create_terminal_ui, run_terminal_ui
)


class UISystem:
    """Facade for UI operations with modular architecture"""
    
    def __init__(self):
        self.service_factory = UIServiceFactory()
        self.screen_service = self.service_factory.get_screen_service()
        self.menu_service = self.service_factory.get_menu_service()
        self.log_service = self.service_factory.get_log_service()
        self.asset_service = self.service_factory.get_asset_service()
        
        self.session_repository = self.service_factory.get_session_repository()
        self.game_state: Optional[GameState] = None
        self.ui_app: Optional[Any] = None
        
        # Event callbacks
        self.callbacks: Dict[str, List[Callable]] = {}
    
    def initialize_ui(self) -> bool:
        """Initialize UI system"""
        try:
            # Initialize services
            if not self._initialize_services():
                return False
            
            # Create initial session
            session = self.session_repository.load_session()
            if not session:
                session = UISession()
                self.session_repository.save_session(session)
            
            # Set initial screen
            self.screen_service.navigate_to_screen(UIState.MAIN_MENU)
            
            return True
        except Exception as e:
            self.log_message(f"Failed to initialize UI: {e}", MessageType.ERROR)
            return False
    
    def cleanup_ui(self) -> bool:
        """Cleanup UI system"""
        try:
            self.service_factory.clear_services()
            self.ui_app = None
            self.game_state = None
            return True
        except Exception as e:
            self.log_message(f"Failed to cleanup UI: {e}", MessageType.ERROR)
            return False
    
    def run_ui(self) -> None:
        """Run the terminal UI application"""
        try:
            # Create and run UI
            self.ui_app = create_terminal_ui()
            run_terminal_ui()
        except Exception as e:
            self.log_message(f"Failed to run UI: {e}", MessageType.ERROR)
    
    def set_game_state(self, game_state: GameState) -> bool:
        """Set current game state"""
        try:
            self.game_state = game_state
            
            # Log state change
            self.log_message(f"Game state updated: {game_state.player['name'] if game_state.player else 'Unknown'}", 
                           MessageType.INFO)
            
            return True
        except Exception as e:
            self.log_message(f"Failed to set game state: {e}", MessageType.ERROR)
            return False
    
    def get_game_state(self) -> Optional[GameState]:
        """Get current game state"""
        return self.game_state
    
    # Screen Management
    def navigate_to_screen(self, screen_state: UIState) -> bool:
        """Navigate to specific screen"""
        try:
            success = self.screen_service.navigate_to_screen(screen_state)
            if success:
                self.log_message(f"Navigated to {screen_state.value}", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to navigate to {screen_state.value}: {e}", MessageType.ERROR)
            return False
    
    def go_back(self) -> bool:
        """Go back to previous screen"""
        try:
            success = self.screen_service.go_back()
            if success:
                self.log_message("Went back to previous screen", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to go back: {e}", MessageType.ERROR)
            return False
    
    def get_current_screen(self) -> Optional[UIState]:
        """Get current screen"""
        try:
            return self.screen_service.get_current_screen()
        except Exception as e:
            self.log_message(f"Failed to get current screen: {e}", MessageType.ERROR)
            return None
    
    def get_navigation_stack(self) -> List[UIState]:
        """Get navigation history"""
        try:
            return self.screen_service.get_navigation_stack()
        except Exception as e:
            self.log_message(f"Failed to get navigation stack: {e}", MessageType.ERROR)
            return []
    
    # Menu Management
    def show_menu(self, menu_id: str) -> bool:
        """Show specific menu"""
        try:
            success = self.menu_service.show_menu(menu_id)
            if success:
                self.log_message(f"Showing menu: {menu_id}", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to show menu {menu_id}: {e}", MessageType.ERROR)
            return False
    
    def hide_menu(self) -> bool:
        """Hide current menu"""
        try:
            success = self.menu_service.hide_menu()
            if success:
                self.log_message("Menu hidden", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to hide menu: {e}", MessageType.ERROR)
            return False
    
    def select_menu_item(self, index: int) -> bool:
        """Select menu item by index"""
        try:
            success = self.menu_service.select_menu_item(index)
            if success:
                menu_state = self.menu_service.get_menu_state()
                if menu_state and 'selected_item' in menu_state:
                    item = menu_state['selected_item']
                    self.log_message(f"Selected menu item: {item.label}", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to select menu item {index}: {e}", MessageType.ERROR)
            return False
    
    def activate_selected_item(self) -> Optional[MenuItem]:
        """Activate currently selected menu item"""
        try:
            item = self.menu_service.activate_selected_item()
            if item:
                self.log_message(f"Activated menu item: {item.label}", MessageType.SUCCESS)
                
                # Trigger callback if registered
                self._trigger_callback("menu_item_activated", item)
            return item
        except Exception as e:
            self.log_message(f"Failed to activate selected item: {e}", MessageType.ERROR)
            return None
    
    def get_menu_state(self) -> Optional[Dict[str, Any]]:
        """Get current menu state"""
        try:
            return self.menu_service.get_menu_state()
        except Exception as e:
            self.log_message(f"Failed to get menu state: {e}", MessageType.ERROR)
            return None
    
    # Log Management
    def log_message(self, message: str, message_type: MessageType = MessageType.INFO) -> bool:
        """Add message to log"""
        try:
            success = self.log_service.add_message(message, message_type)
            return success
        except Exception:
            return False
    
    def log_info(self, message: str) -> bool:
        """Log info message"""
        return self.log_message(message, MessageType.INFO)
    
    def log_success(self, message: str) -> bool:
        """Log success message"""
        return self.log_message(message, MessageType.SUCCESS)
    
    def log_warning(self, message: str) -> bool:
        """Log warning message"""
        return self.log_message(message, MessageType.WARNING)
    
    def log_error(self, message: str) -> bool:
        """Log error message"""
        return self.log_message(message, MessageType.ERROR)
    
    def log_combat(self, message: str) -> bool:
        """Log combat message"""
        return self.log_message(message, MessageType.COMBAT)
    
    def log_loot(self, message: str) -> bool:
        """Log loot message"""
        return self.log_message(message, MessageType.LOOT)
    
    def log_quest(self, message: str) -> bool:
        """Log quest message"""
        return self.log_message(message, MessageType.QUEST)
    
    def log_discovery(self, message: str) -> bool:
        """Log discovery message"""
        return self.log_message(message, MessageType.DISCOVERY)
    
    def get_recent_messages(self, count: int = 50) -> List[LogMessage]:
        """Get recent log messages"""
        try:
            return self.log_service.get_recent_messages(count)
        except Exception as e:
            self.log_message(f"Failed to get recent messages: {e}", MessageType.ERROR)
            return []
    
    def clear_log(self) -> bool:
        """Clear log messages"""
        try:
            success = self.log_service.clear_log()
            if success:
                self.log_message("Log cleared", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to clear log: {e}", MessageType.ERROR)
            return False
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get log statistics"""
        try:
            return self.log_service.get_log_stats()
        except Exception as e:
            self.log_message(f"Failed to get log stats: {e}", MessageType.ERROR)
            return {}
    
    # Asset Management
    def get_ascii_art(self, art_id: str) -> Optional[str]:
        """Get ASCII art by ID"""
        try:
            return self.asset_service.load_ascii_art(art_id)
        except Exception as e:
            self.log_message(f"Failed to load ASCII art {art_id}: {e}", MessageType.ERROR)
            return None
    
    def get_animation_frames(self, animation_id: str) -> List[str]:
        """Get animation frames"""
        try:
            return self.asset_service.load_animation_frames(animation_id)
        except Exception as e:
            self.log_message(f"Failed to load animation {animation_id}: {e}", MessageType.ERROR)
            return []
    
    def preload_assets(self, asset_list: List[str]) -> bool:
        """Preload list of assets"""
        try:
            success = self.asset_service.preload_assets(asset_list)
            if success:
                self.log_message(f"Preloaded {len(asset_list)} assets", MessageType.INFO)
            return success
        except Exception as e:
            self.log_message(f"Failed to preload assets: {e}", MessageType.ERROR)
            return False
    
    def get_asset_info(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get asset information"""
        try:
            return self.asset_service.get_asset_info(asset_id)
        except Exception as e:
            self.log_message(f"Failed to get asset info {asset_id}: {e}", MessageType.ERROR)
            return None
    
    # Callback Management
    def register_callback(self, event: str, callback: Callable) -> None:
        """Register callback for event"""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)
    
    def unregister_callback(self, event: str, callback: Callable) -> bool:
        """Unregister callback for event"""
        if event in self.callbacks:
            try:
                self.callbacks[event].remove(callback)
                return True
            except ValueError:
                pass
        return False
    
    def _trigger_callback(self, event: str, data: Any = None) -> None:
        """Trigger callbacks for event"""
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    self.log_message(f"Callback error for {event}: {e}", MessageType.ERROR)
    
    # Game State Management
    def update_player_data(self, player_data: Dict[str, Any]) -> bool:
        """Update player data"""
        try:
            if self.game_state:
                self.game_state.player.update(player_data)
                self.log_message(f"Player data updated: {player_data}", MessageType.INFO)
                return True
            return False
        except Exception as e:
            self.log_message(f"Failed to update player data: {e}", MessageType.ERROR)
            return False
    
    def update_location_data(self, location_data: Dict[str, Any]) -> bool:
        """Update location data"""
        try:
            if self.game_state:
                self.game_state.location.update(location_data)
                self.log_message(f"Location updated: {location_data.get('name', 'Unknown')}", MessageType.INFO)
                return True
            return False
        except Exception as e:
            self.log_message(f"Failed to update location data: {e}", MessageType.ERROR)
            return False
    
    def update_status_data(self, status_data: Dict[str, Any]) -> bool:
        """Update status data"""
        try:
            if self.game_state:
                self.game_state.status.update(status_data)
                self.log_message("Status data updated", MessageType.INFO)
                return True
            return False
        except Exception as e:
            self.log_message(f"Failed to update status data: {e}", MessageType.ERROR)
            return False
    
    def get_player_data(self) -> Optional[Dict[str, Any]]:
        """Get player data"""
        if self.game_state:
            return self.game_state.player
        return None
    
    def get_location_data(self) -> Optional[Dict[str, Any]]:
        """Get location data"""
        if self.game_state:
            return self.game_state.location
        return None
    
    def get_status_data(self) -> Optional[Dict[str, Any]]:
        """Get status data"""
        if self.game_state:
            return self.game_state.status
        return None
    
    # Utility Methods
    def is_ui_initialized(self) -> bool:
        """Check if UI is initialized"""
        try:
            return (self.service_factory is not None and 
                   self.screen_service is not None and
                   self.menu_service is not None and
                   self.log_service is not None and
                   self.asset_service is not None)
        except Exception:
            return False
    
    def get_ui_status(self) -> Dict[str, Any]:
        """Get UI system status"""
        try:
            current_screen = self.get_current_screen()
            navigation_stack = self.get_navigation_stack()
            log_stats = self.get_log_stats()
            
            return {
                "initialized": self.is_ui_initialized(),
                "current_screen": current_screen.value if current_screen else None,
                "navigation_stack_size": len(navigation_stack),
                "log_messages": log_stats.get("total_messages", 0),
                "game_state_loaded": self.game_state is not None,
                "ui_app_loaded": self.ui_app is not None
            }
        except Exception as e:
            self.log_message(f"Failed to get UI status: {e}", MessageType.ERROR)
            return {
                "initialized": False,
                "error": str(e)
            }


# Global UI system instance for easy access
_ui_system = None


def get_ui_system() -> UISystem:
    """Get global UI system instance"""
    global _ui_system
    if _ui_system is None:
        _ui_system = UISystem()
    return _ui_system


# Convenience functions
def initialize_ui() -> bool:
    """Initialize UI system"""
    ui = get_ui_system()
    return ui.initialize_ui()


def run_ui() -> None:
    """Run UI system"""
    ui = get_ui_system()
    ui.run_ui()


def log_message(message: str, message_type: MessageType = MessageType.INFO) -> bool:
    """Log message using global UI system"""
    ui = get_ui_system()
    return ui.log_message(message, message_type)


# Export main classes and functions
__all__ = [
    'UISystem',
    'get_ui_system',
    'initialize_ui', 
    'run_ui',
    'log_message',
    'GameState',
    'UIState',
    'MessageType',
    'create_terminal_ui',
    'run_terminal_ui'
]