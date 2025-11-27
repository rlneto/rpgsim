"""
UI Repository interfaces
Data access layer abstractions for UI components
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from ..domain.ui import UISession, UIElement, LogMessage, MenuItem, ColorScheme


class UISessionRepository(ABC):
    """Repository for UI session management"""
    
    @abstractmethod
    def save_session(self, session: UISession) -> bool:
        """Save UI session state"""
        pass
    
    @abstractmethod
    def load_session(self) -> Optional[UISession]:
        """Load UI session state"""
        pass
    
    @abstractmethod
    def delete_session(self) -> bool:
        """Delete UI session state"""
        pass


class UIConfigRepository(ABC):
    """Repository for UI configuration"""
    
    @abstractmethod
    def save_color_scheme(self, scheme: ColorScheme) -> bool:
        """Save color scheme"""
        pass
    
    @abstractmethod
    def load_color_scheme(self) -> Optional[ColorScheme]:
        """Load color scheme"""
        pass
    
    @abstractmethod
    def save_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Save theme configuration"""
        pass
    
    @abstractmethod
    def load_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Load theme configuration"""
        pass
    
    @abstractmethod
    def list_themes(self) -> List[str]:
        """List available themes"""
        pass


class LogRepository(ABC):
    """Repository for game log messages"""
    
    @abstractmethod
    def add_message(self, message: LogMessage) -> bool:
        """Add log message"""
        pass
    
    @abstractmethod
    def get_recent_messages(self, count: int = 50) -> List[LogMessage]:
        """Get recent messages"""
        pass
    
    @abstractmethod
    def get_messages_by_type(self, message_type: str) -> List[LogMessage]:
        """Get messages by type"""
        pass
    
    @abstractmethod
    def clear_log(self) -> bool:
        """Clear all log messages"""
        pass
    
    @abstractmethod
    def get_log_size(self) -> int:
        """Get current log size"""
        pass


class MenuRepository(ABC):
    """Repository for menu configurations"""
    
    @abstractmethod
    def save_menu(self, menu_id: str, menu_config: Any) -> bool:
        """Save menu configuration"""
        pass
    
    @abstractmethod
    def load_menu(self, menu_id: str) -> Optional[Any]:
        """Load menu configuration"""
        pass
    
    @abstractmethod
    def list_menus(self) -> List[str]:
        """List available menus"""
        pass


class AssetRepository(ABC):
    """Repository for UI assets (ASCII art, sounds, etc.)"""
    
    @abstractmethod
    def get_ascii_art(self, art_id: str) -> Optional[str]:
        """Get ASCII art by ID"""
        pass
    
    @abstractmethod
    def get_animation_frames(self, animation_id: str) -> List[str]:
        """Get animation frames"""
        pass
    
    @abstractmethod
    def get_sound_effect(self, sound_id: str) -> Optional[Any]:
        """Get sound effect"""
        pass
    
    @abstractmethod
    def list_assets(self, asset_type: str) -> List[str]:
        """List assets by type"""
        pass


class WidgetRepository(ABC):
    """Repository for widget configurations"""
    
    @abstractmethod
    def save_widget(self, widget_id: str, widget_config: Any) -> bool:
        """Save widget configuration"""
        pass
    
    @abstractmethod
    def load_widget(self, widget_id: str) -> Optional[Any]:
        """Load widget configuration"""
        pass
    
    @abstractmethod
    def list_widgets(self) -> List[str]:
        """List available widgets"""
        pass