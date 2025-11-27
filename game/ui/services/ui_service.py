"""
UI Services Implementation
Business logic layer for UI operations
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple, Callable
from ..domain.ui import (
    UISession, UIElement, LogMessage, MenuItem, 
    ColorScheme, UIState, MessageType, AnimationConfig,
    ScreenPosition, ScreenSize, MenuConfig, DialogConfig,
    ProgressConfig, TabConfig
)
from ..interfaces.services import (
    UIService, ScreenService, MenuService, LogService,
    ThemeService, AnimationService, InputService,
    AssetService, DialogService, WidgetService, LayoutService
)
from ..exceptions.ui_exceptions import (
    UIException, UIStateError, ScreenNotFoundError,
    InvalidNavigationError, AnimationError, RenderError,
    InputError, ThemeError, ResourceError
)
from ..assets.ascii_art import ASCIIArtAssets
from ..repositories.memory_ui_repository import (
    MemoryUISessionRepository, MemoryLogRepository,
    MemoryUIConfigRepository, MemoryAssetRepository
)


class BaseUIService(UIService):
    """Base UI service implementation"""
    
    def __init__(self):
        self.session_repository = MemoryUISessionRepository()
        self.asset_service = MemoryAssetService()
        self.is_initialized = False
        self.running = False
        self.frame_rate = 60
        self.last_frame_time = 0
    
    def initialize_ui(self) -> bool:
        """Initialize UI system"""
        try:
            # Load session or create new one
            session = self.session_repository.load_session()
            if not session:
                session = UISession()
                self.session_repository.save_session(session)
            
            # Preload essential assets
            self.asset_service.preload_assets([
                "character_classes", "locations", "combat", "ui_elements"
            ])
            
            self.is_initialized = True
            return True
        except Exception as e:
            raise UIException(f"Failed to initialize UI: {e}")
    
    def cleanup_ui(self) -> bool:
        """Cleanup UI system"""
        try:
            self.running = False
            self.is_initialized = False
            return True
        except Exception as e:
            raise UIException(f"Failed to cleanup UI: {e}")
    
    def render_frame(self) -> bool:
        """Render single frame"""
        try:
            if not self.is_initialized:
                return False
            
            current_time = time.time()
            delta_time = current_time - self.last_frame_time
            
            # Limit frame rate
            if delta_time < 1.0 / self.frame_rate:
                return False
            
            self.last_frame_time = current_time
            # Rendering logic to be implemented by subclasses
            return True
        except Exception as e:
            raise RenderError(f"Failed to render frame: {e}")
    
    def handle_input(self, input_data: Any) -> bool:
        """Handle user input"""
        try:
            # Input handling logic to be implemented by subclasses
            return True
        except Exception as e:
            raise InputError(f"Failed to handle input: {e}")


class ScreenServiceImpl(ScreenService):
    """Screen management service implementation"""
    
    def __init__(self, session_repository: MemoryUISessionRepository):
        self.session_repository = session_repository
    
    def navigate_to_screen(self, screen_state: UIState) -> bool:
        """Navigate to specific screen"""
        try:
            session = self.session_repository.load_session()
            if not session:
                raise UIStateError("No active session")
            
            session.navigate_to_screen(screen_state)
            self.session_repository.save_session(session)
            return True
        except Exception as e:
            raise InvalidNavigationError(f"Failed to navigate to {screen_state}: {e}")
    
    def go_back(self) -> bool:
        """Go back to previous screen"""
        try:
            session = self.session_repository.load_session()
            if not session:
                return False
            
            success = session.go_back()
            if success:
                self.session_repository.save_session(session)
            return success
        except Exception as e:
            raise InvalidNavigationError(f"Failed to go back: {e}")
    
    def get_current_screen(self) -> Optional[UIState]:
        """Get current screen state"""
        try:
            session = self.session_repository.load_session()
            return session.current_screen if session else None
        except Exception as e:
            raise UIStateError(f"Failed to get current screen: {e}")
    
    def get_navigation_stack(self) -> List[UIState]:
        """Get navigation history"""
        try:
            session = self.session_repository.load_session()
            return session.get_navigation_stack() if session else []
        except Exception as e:
            raise UIStateError(f"Failed to get navigation stack: {e}")


class MenuServiceImpl(MenuService):
    """Menu management service implementation"""
    
    def __init__(self, asset_service: AssetService):
        self.asset_service = asset_service
        self.current_menu_id = None
        self.selected_index = 0
        self.menu_configs = {}
    
    def show_menu(self, menu_id: str) -> bool:
        """Show specific menu"""
        try:
            # Load menu configuration
            menu_config = self._load_menu_config(menu_id)
            if not menu_config:
                raise UIException(f"Menu not found: {menu_id}")
            
            self.current_menu_id = menu_id
            self.selected_index = 0
            self.menu_configs[menu_id] = menu_config
            return True
        except Exception as e:
            raise UIException(f"Failed to show menu {menu_id}: {e}")
    
    def hide_menu(self) -> bool:
        """Hide current menu"""
        self.current_menu_id = None
        self.selected_index = 0
        return True
    
    def select_menu_item(self, index: int) -> bool:
        """Select menu item by index"""
        if not self.current_menu_id:
            return False
        
        menu_config = self.menu_configs.get(self.current_menu_id)
        if not menu_config:
            return False
        
        if 0 <= index < len(menu_config.items):
            self.selected_index = index
            return True
        return False
    
    def activate_selected_item(self) -> Optional[MenuItem]:
        """Activate currently selected menu item"""
        if not self.current_menu_id:
            return None
        
        menu_config = self.menu_configs.get(self.current_menu_id)
        if not menu_config:
            return None
        
        if 0 <= self.selected_index < len(menu_config.items):
            item = menu_config.items[self.selected_index]
            if item.enabled:
                return item
        return None
    
    def get_menu_state(self) -> Optional[Dict[str, Any]]:
        """Get current menu state"""
        if not self.current_menu_id:
            return None
        
        menu_config = self.menu_configs.get(self.current_menu_id)
        if not menu_config:
            return None
        
        return {
            "menu_id": self.current_menu_id,
            "title": menu_config.title,
            "items": menu_config.items,
            "selected_index": self.selected_index,
            "selected_item": menu_config.items[self.selected_index] if 0 <= self.selected_index < len(menu_config.items) else None
        }
    
    def _load_menu_config(self, menu_id: str) -> Optional[MenuConfig]:
        """Load menu configuration"""
        # In a real implementation, this would load from files or repositories
        # For now, return basic configs
        if menu_id == "main":
            return MenuConfig(
                id="main",
                title="🎮 RPGSim - Main Menu",
                items=[
                    MenuItem("new_char", "New Character", "🎭", "Start a new adventure"),
                    MenuItem("load_game", "Load Game", "💾", "Continue a saved game"),
                    MenuItem("settings", "Settings", "⚙️", "Configure game options"),
                    MenuItem("help", "Help", "📖", "View help and instructions"),
                    MenuItem("quit", "Quit", "🚪", "Exit the game")
                ]
            )
        elif menu_id == "character_creation":
            return MenuConfig(
                id="character_creation",
                title="🎭 Character Creation",
                items=[
                    MenuItem("warrior", "Warrior", "⚔️", "Strong melee fighter"),
                    MenuItem("mage", "Mage", "🔮", "Powerful spellcaster"),
                    MenuItem("rogue", "Rogue", "🗡️", "Stealthy assassin"),
                    MenuItem("cleric", "Cleric", "✨", "Divine healer"),
                    MenuItem("back", "Back", "⬅️", "Return to main menu")
                ]
            )
        return None


class LogServiceImpl(LogService):
    """Game log service implementation"""
    
    def __init__(self, log_repository: MemoryLogRepository):
        self.log_repository = log_repository
        self.max_log_entries = 1000
    
    def add_message(self, message: str, message_type: MessageType = MessageType.INFO) -> bool:
        """Add message to log"""
        try:
            log_message = LogMessage(
                message=message,
                message_type=message_type
            )
            return self.log_repository.add_message(log_message)
        except Exception as e:
            raise UIException(f"Failed to add log message: {e}")
    
    def get_recent_messages(self, count: int = 50) -> List[LogMessage]:
        """Get recent log messages"""
        try:
            return self.log_repository.get_recent_messages(count)
        except Exception as e:
            raise UIException(f"Failed to get recent messages: {e}")
    
    def clear_log(self) -> bool:
        """Clear log messages"""
        try:
            return self.log_repository.clear_log()
        except Exception as e:
            raise UIException(f"Failed to clear log: {e}")
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get log statistics"""
        try:
            all_messages = self.log_repository.get_recent_messages(self.max_log_entries)
            stats = {
                "total_messages": len(all_messages),
                "by_type": {},
                "latest_timestamp": None
            }
            
            for message in all_messages:
                msg_type = message.message_type.value
                stats["by_type"][msg_type] = stats["by_type"].get(msg_type, 0) + 1
                
                if not stats["latest_timestamp"] or message.timestamp > stats["latest_timestamp"]:
                    stats["latest_timestamp"] = message.timestamp
            
            return stats
        except Exception as e:
            raise UIException(f"Failed to get log stats: {e}")


class AssetServiceImpl(AssetService):
    """Asset management service implementation"""
    
    def __init__(self):
        self.ascii_assets = ASCIIArtAssets()
        self.loaded_assets = {}
        self.animation_frames = {}
    
    def load_ascii_art(self, art_id: str) -> Optional[str]:
        """Load ASCII art"""
        try:
            # Try to get from loaded assets first
            if art_id in self.loaded_assets:
                return self.loaded_assets[art_id]
            
            # Load from ASCII assets
            art = None
            
            # Check if it's a character class
            if art_id in self.ascii_assets.get_all_character_classes():
                art = self.ascii_assets.get_character_art(art_id)
            
            # Check if it's a location type
            elif art_id in self.ascii_assets.get_all_location_types():
                art = self.ascii_assets.get_location_art(art_id)
            
            # Check if it's an item type
            elif art_id in self.ascii_assets.get_all_item_types():
                art = self.ascii_assets.get_item_art(art_id)
            
            # Check if it's an effect type
            elif art_id in self.ascii_assets.get_all_effect_types():
                art = self.ascii_assets.get_effect_art(art_id)
            
            # Cache the loaded art
            if art:
                self.loaded_assets[art_id] = art
            
            return art
        except Exception as e:
            raise ResourceError(f"Failed to load ASCII art {art_id}: {e}")
    
    def load_animation_frames(self, animation_id: str) -> List[str]:
        """Load animation frames"""
        try:
            if animation_id in self.animation_frames:
                return self.animation_frames[animation_id]
            
            frames = self.ascii_assets.get_animation_frames("location", animation_id)
            if not frames:
                frames = self.ascii_assets.get_animation_frames("combat", animation_id)
            
            if frames:
                self.animation_frames[animation_id] = frames
            
            return frames
        except Exception as e:
            raise ResourceError(f"Failed to load animation {animation_id}: {e}")
    
    def preload_assets(self, asset_list: List[str]) -> bool:
        """Preload list of assets"""
        try:
            for asset_id in asset_list:
                self.load_ascii_art(asset_id)
            return True
        except Exception as e:
            raise ResourceError(f"Failed to preload assets: {e}")
    
    def get_asset_info(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get asset information"""
        try:
            info = {
                "id": asset_id,
                "loaded": asset_id in self.loaded_assets,
                "type": "unknown"
            }
            
            # Determine asset type
            if asset_id in self.ascii_assets.get_all_character_classes():
                info["type"] = "character"
            elif asset_id in self.ascii_assets.get_all_location_types():
                info["type"] = "location"
            elif asset_id in self.ascii_assets.get_all_item_types():
                info["type"] = "item"
            elif asset_id in self.ascii_assets.get_all_effect_types():
                info["type"] = "effect"
            
            return info
        except Exception as e:
            raise ResourceError(f"Failed to get asset info {asset_id}: {e}")


# Service factory for easy dependency injection
class UIServiceFactory:
    """Factory for creating UI services with proper dependencies"""
    
    def __init__(self):
        self.session_repository = MemoryUISessionRepository()
        self.log_repository = MemoryLogRepository()
        self.config_repository = MemoryUIConfigRepository()
        self.asset_repository = MemoryAssetRepository()
        
        self._services = {}
    
    def get_screen_service(self) -> ScreenService:
        """Get screen service instance"""
        if "screen" not in self._services:
            self._services["screen"] = ScreenServiceImpl(self.session_repository)
        return self._services["screen"]
    
    def get_menu_service(self) -> MenuService:
        """Get menu service instance"""
        if "menu" not in self._services:
            self._services["menu"] = MenuServiceImpl(self.asset_repository)
        return self._services["menu"]
    
    def get_log_service(self) -> LogService:
        """Get log service instance"""
        if "log" not in self._services:
            self._services["log"] = LogServiceImpl(self.log_repository)
        return self._services["log"]
    
    def get_asset_service(self) -> AssetService:
        """Get asset service instance"""
        if "asset" not in self._services:
            self._services["asset"] = AssetServiceImpl()
        return self._services["asset"]
    
    def get_session_repository(self) -> MemoryUISessionRepository:
        """Get session repository instance"""
        return self.session_repository
    
    def get_log_repository(self) -> MemoryLogRepository:
        """Get log repository instance"""
        return self.log_repository
    
    def clear_services(self) -> None:
        """Clear all service instances"""
        self._services.clear()