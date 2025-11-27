"""
Memory-based UI Repository Implementations
In-memory data storage for UI components
"""

from typing import Dict, Any, List, Optional
from ..domain.ui import UISession, UIElement, LogMessage, MenuItem, ColorScheme
from ..interfaces.repositories import (
    UISessionRepository, UIConfigRepository, LogRepository,
    MenuRepository, AssetRepository, WidgetRepository
)
from ..exceptions.ui_exceptions import UIException


class MemoryUISessionRepository(UISessionRepository):
    """In-memory UI session repository"""
    
    def __init__(self):
        self._session: Optional[UISession] = None
        self._saved_sessions: Dict[str, UISession] = {}
    
    def save_session(self, session: UISession) -> bool:
        """Save UI session state"""
        try:
            self._session = session
            self._saved_sessions[session.current_screen.value] = session
            return True
        except Exception:
            return False
    
    def load_session(self) -> Optional[UISession]:
        """Load UI session state"""
        try:
            return self._session
        except Exception:
            return None
    
    def delete_session(self) -> bool:
        """Delete UI session state"""
        try:
            if self._session:
                screen_value = self._session.current_screen.value
                if screen_value in self._saved_sessions:
                    del self._saved_sessions[screen_value]
                self._session = None
            return True
        except Exception:
            return False


class MemoryUIConfigRepository(UIConfigRepository):
    """In-memory UI configuration repository"""
    
    def __init__(self):
        self._color_schemes: Dict[str, ColorScheme] = {}
        self._themes: Dict[str, Dict[str, Any]] = {}
        self._current_color_scheme: Optional[ColorScheme] = None
        
        # Initialize with default schemes
        self._initialize_default_schemes()
    
    def _initialize_default_schemes(self) -> None:
        """Initialize default color schemes"""
        default_schemes = {
            "default": ColorScheme(),
            "dark": ColorScheme(
                primary="#00ff00",
                secondary="#00ff00",
                accent="#00ff00",
                background="#000000",
                text="#ffffff",
                muted="#808080"
            ),
            "retro": ColorScheme(
                primary="#ffff00",
                secondary="#00ffff",
                accent="#ff00ff",
                background="#000080",
                text="#ffffff",
                muted="#808080"
            ),
            "nature": ColorScheme(
                primary="#228b22",
                secondary="#8fbc8f",
                accent="#2e8b57",
                background="#1a1a1a",
                text="#f5f5dc",
                muted="#a9a9a9"
            ),
            "cyber": ColorScheme(
                primary="#00ffff",
                secondary="#ff00ff",
                accent="#ffff00",
                background="#0a0a0a",
                text="#00ff00",
                muted="#404040"
            )
        }
        
        for name, scheme in default_schemes.items():
            self._color_schemes[name] = scheme
    
    def save_color_scheme(self, scheme: ColorScheme) -> bool:
        """Save color scheme"""
        try:
            self._current_color_scheme = scheme
            return True
        except Exception:
            return False
    
    def load_color_scheme(self) -> Optional[ColorScheme]:
        """Load color scheme"""
        try:
            return self._current_color_scheme or self._color_schemes.get("default")
        except Exception:
            return None
    
    def save_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Save theme configuration"""
        try:
            self._themes[theme_name] = theme_data
            return True
        except Exception:
            return False
    
    def load_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Load theme configuration"""
        try:
            return self._themes.get(theme_name)
        except Exception:
            return None
    
    def list_themes(self) -> List[str]:
        """List available themes"""
        try:
            return list(self._themes.keys())
        except Exception:
            return []


class MemoryLogRepository(LogRepository):
    """In-memory game log repository"""
    
    def __init__(self, max_entries: int = 1000):
        self._messages: List[LogMessage] = []
        self._max_entries = max_entries
    
    def add_message(self, message: LogMessage) -> bool:
        """Add log message"""
        try:
            self._messages.append(message)
            
            # Keep only the most recent messages
            if len(self._messages) > self._max_entries:
                self._messages = self._messages[-self._max_entries:]
            
            return True
        except Exception:
            return False
    
    def get_recent_messages(self, count: int = 50) -> List[LogMessage]:
        """Get recent messages"""
        try:
            return self._messages[-count:] if count > 0 else []
        except Exception:
            return []
    
    def get_messages_by_type(self, message_type: str) -> List[LogMessage]:
        """Get messages by type"""
        try:
            return [
                msg for msg in self._messages
                if msg.message_type.value == message_type
            ]
        except Exception:
            return []
    
    def clear_log(self) -> bool:
        """Clear all log messages"""
        try:
            self._messages.clear()
            return True
        except Exception:
            return False
    
    def get_log_size(self) -> int:
        """Get current log size"""
        try:
            return len(self._messages)
        except Exception:
            return 0


class MemoryMenuRepository(MenuRepository):
    """In-memory menu configuration repository"""
    
    def __init__(self):
        self._menus: Dict[str, Any] = {}
        self._initialize_default_menus()
    
    def _initialize_default_menus(self) -> None:
        """Initialize default menu configurations"""
        # This would contain default menu data
        # For now, it's empty
        pass
    
    def save_menu(self, menu_id: str, menu_config: Any) -> bool:
        """Save menu configuration"""
        try:
            self._menus[menu_id] = menu_config
            return True
        except Exception:
            return False
    
    def load_menu(self, menu_id: str) -> Optional[Any]:
        """Load menu configuration"""
        try:
            return self._menus.get(menu_id)
        except Exception:
            return None
    
    def list_menus(self) -> List[str]:
        """List available menus"""
        try:
            return list(self._menus.keys())
        except Exception:
            return []


class MemoryAssetRepository(AssetRepository):
    """In-memory asset repository"""
    
    def __init__(self):
        self._ascii_art: Dict[str, str] = {}
        self._animations: Dict[str, List[str]] = {}
        self._sound_effects: Dict[str, Any] = {}
        self._assets_loaded: bool = False
        
        self._load_default_assets()
    
    def _load_default_assets(self) -> None:
        """Load default ASCII art assets"""
        if self._assets_loaded:
            return
        
        # Load from ASCIIArtAssets
        try:
            from ..assets.ascii_art import ASCIIArtAssets
            
            # Load character art
            for char_class in ASCIIArtAssets.get_all_character_classes():
                art = ASCIIArtAssets.get_character_art(char_class)
                if art:
                    self._ascii_art[f"character_{char_class}"] = art
            
            # Load location art
            for loc_type in ASCIIArtAssets.get_all_location_types():
                art = ASCIIArtAssets.get_location_art(loc_type)
                if art:
                    self._ascii_art[f"location_{loc_type}"] = art
            
            # Load combat art
            for combat_type in ["sword", "shield", "magic"]:
                art = ASCIIArtAssets.get_combat_art(combat_type)
                if art:
                    self._ascii_art[f"combat_{combat_type}"] = art
            
            # Load item art
            for item_type in ASCIIArtAssets.get_all_item_types():
                art = ASCIIArtAssets.get_item_art(item_type)
                if art:
                    self._ascii_art[f"item_{item_type}"] = art
            
            self._assets_loaded = True
        except Exception:
            pass
    
    def get_ascii_art(self, art_id: str) -> Optional[str]:
        """Get ASCII art by ID"""
        try:
            return self._ascii_art.get(art_id)
        except Exception:
            return None
    
    def get_animation_frames(self, animation_id: str) -> List[str]:
        """Get animation frames"""
        try:
            return self._animations.get(animation_id, [])
        except Exception:
            return []
    
    def get_sound_effect(self, sound_id: str) -> Optional[Any]:
        """Get sound effect"""
        try:
            return self._sound_effects.get(sound_id)
        except Exception:
            return None
    
    def list_assets(self, asset_type: str) -> List[str]:
        """List assets by type"""
        try:
            if asset_type == "ascii":
                return list(self._ascii_art.keys())
            elif asset_type == "animation":
                return list(self._animations.keys())
            elif asset_type == "sound":
                return list(self._sound_effects.keys())
            return []
        except Exception:
            return []


class MemoryWidgetRepository(WidgetRepository):
    """In-memory widget configuration repository"""
    
    def __init__(self):
        self._widgets: Dict[str, Any] = {}
        self._widget_templates: Dict[str, Any] = {}
        self._initialize_default_widgets()
    
    def _initialize_default_widgets(self) -> None:
        """Initialize default widget templates"""
        # This would contain default widget templates
        # For now, it's empty
        pass
    
    def save_widget(self, widget_id: str, widget_config: Any) -> bool:
        """Save widget configuration"""
        try:
            self._widgets[widget_id] = widget_config
            return True
        except Exception:
            return False
    
    def load_widget(self, widget_id: str) -> Optional[Any]:
        """Load widget configuration"""
        try:
            return self._widgets.get(widget_id)
        except Exception:
            return None
    
    def list_widgets(self) -> List[str]:
        """List available widgets"""
        try:
            return list(self._widgets.keys())
        except Exception:
            return []