"""
UI Service interfaces
Business logic layer for UI operations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from ..domain.ui import (
    UISession, UIElement, LogMessage, MenuItem, 
    ColorScheme, UIState, MessageType, AnimationConfig
)
from ..exceptions.ui_exceptions import UIException


class UIService(ABC):
    """Base UI service interface"""
    
    @abstractmethod
    def initialize_ui(self) -> bool:
        """Initialize UI system"""
        pass
    
    @abstractmethod
    def cleanup_ui(self) -> bool:
        """Cleanup UI system"""
        pass
    
    @abstractmethod
    def render_frame(self) -> bool:
        """Render single frame"""
        pass
    
    @abstractmethod
    def handle_input(self, input_data: Any) -> bool:
        """Handle user input"""
        pass


class ScreenService(ABC):
    """Screen management service interface"""
    
    @abstractmethod
    def navigate_to_screen(self, screen_state: UIState) -> bool:
        """Navigate to specific screen"""
        pass
    
    @abstractmethod
    def go_back(self) -> bool:
        """Go back to previous screen"""
        pass
    
    @abstractmethod
    def get_current_screen(self) -> Optional[UIState]:
        """Get current screen state"""
        pass
    
    @abstractmethod
    def get_navigation_stack(self) -> List[UIState]:
        """Get navigation history"""
        pass


class MenuService(ABC):
    """Menu management service interface"""
    
    @abstractmethod
    def show_menu(self, menu_id: str) -> bool:
        """Show specific menu"""
        pass
    
    @abstractmethod
    def hide_menu(self) -> bool:
        """Hide current menu"""
        pass
    
    @abstractmethod
    def select_menu_item(self, index: int) -> bool:
        """Select menu item by index"""
        pass
    
    @abstractmethod
    def activate_selected_item(self) -> bool:
        """Activate currently selected menu item"""
        pass
    
    @abstractmethod
    def get_menu_state(self) -> Optional[Dict[str, Any]]:
        """Get current menu state"""
        pass


class LogService(ABC):
    """Game log service interface"""
    
    @abstractmethod
    def add_message(self, message: str, message_type: MessageType = MessageType.INFO) -> bool:
        """Add message to log"""
        pass
    
    @abstractmethod
    def get_recent_messages(self, count: int = 50) -> List[LogMessage]:
        """Get recent log messages"""
        pass
    
    @abstractmethod
    def clear_log(self) -> bool:
        """Clear log messages"""
        pass
    
    @abstractmethod
    def get_log_stats(self) -> Dict[str, Any]:
        """Get log statistics"""
        pass


class ThemeService(ABC):
    """Theme management service interface"""
    
    @abstractmethod
    def set_color_scheme(self, scheme: ColorScheme) -> bool:
        """Set color scheme"""
        pass
    
    @abstractmethod
    def get_color_scheme(self) -> Optional[ColorScheme]:
        """Get current color scheme"""
        pass
    
    @abstractmethod
    def load_theme(self, theme_name: str) -> bool:
        """Load theme by name"""
        pass
    
    @abstractmethod
    def save_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Save theme configuration"""
        pass
    
    @abstractmethod
    def list_themes(self) -> List[str]:
        """List available themes"""
        pass


class AnimationService(ABC):
    """Animation service interface"""
    
    @abstractmethod
    def start_animation(self, element_id: str, config: AnimationConfig) -> bool:
        """Start animation on element"""
        pass
    
    @abstractmethod
    def stop_animation(self, element_id: str) -> bool:
        """Stop animation on element"""
        pass
    
    @abstractmethod
    def update_animations(self, delta_time: float) -> bool:
        """Update all active animations"""
        pass
    
    @abstractmethod
    def is_animation_running(self, element_id: str) -> bool:
        """Check if animation is running"""
        pass


class InputService(ABC):
    """Input handling service interface"""
    
    @abstractmethod
    def register_key_binding(self, key: str, action: str, description: str = "") -> bool:
        """Register key binding"""
        pass
    
    @abstractmethod
    def unregister_key_binding(self, key: str) -> bool:
        """Unregister key binding"""
        pass
    
    @abstractmethod
    def get_key_bindings(self) -> Dict[str, Any]:
        """Get all key bindings"""
        pass
    
    @abstractmethod
    def handle_key_press(self, key: str) -> bool:
        """Handle key press"""
        pass


class AssetService(ABC):
    """Asset management service interface"""
    
    @abstractmethod
    def load_ascii_art(self, art_id: str) -> Optional[str]:
        """Load ASCII art"""
        pass
    
    @abstractmethod
    def load_animation_frames(self, animation_id: str) -> List[str]:
        """Load animation frames"""
        pass
    
    @abstractmethod
    def preload_assets(self, asset_list: List[str]) -> bool:
        """Preload list of assets"""
        pass
    
    @abstractmethod
    def get_asset_info(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get asset information"""
        pass


class DialogService(ABC):
    """Dialog management service interface"""
    
    @abstractmethod
    def show_dialog(self, dialog_id: str, message: str, 
                   dialog_type: MessageType = MessageType.INFO) -> bool:
        """Show dialog"""
        pass
    
    @abstractmethod
    def hide_dialog(self) -> bool:
        """Hide current dialog"""
        pass
    
    @abstractmethod
    def is_dialog_active(self) -> bool:
        """Check if dialog is active"""
        pass
    
    @abstractmethod
    def get_dialog_result(self) -> Optional[str]:
        """Get dialog result"""
        pass


class WidgetService(ABC):
    """Widget management service interface"""
    
    @abstractmethod
    def create_widget(self, widget_type: str, config: Dict[str, Any]) -> Optional[str]:
        """Create widget and return ID"""
        pass
    
    @abstractmethod
    def update_widget(self, widget_id: str, config: Dict[str, Any]) -> bool:
        """Update widget configuration"""
        pass
    
    @abstractmethod
    def delete_widget(self, widget_id: str) -> bool:
        """Delete widget"""
        pass
    
    @abstractmethod
    def get_widget(self, widget_id: str) -> Optional[Dict[str, Any]]:
        """Get widget configuration"""
        pass
    
    @abstractmethod
    def list_widgets(self) -> List[str]:
        """List all widget IDs"""
        pass


class LayoutService(ABC):
    """Layout management service interface"""
    
    @abstractmethod
    def calculate_layout(self, screen_size: Tuple[int, int]) -> Dict[str, Any]:
        """Calculate layout for screen size"""
        pass
    
    @abstractmethod
    def update_layout(self, layout_config: Dict[str, Any]) -> bool:
        """Update layout configuration"""
        pass
    
    @abstractmethod
    def get_element_position(self, element_id: str) -> Optional[Tuple[int, int]]:
        """Get element position in layout"""
        pass
    
    @abstractmethod
    def resize_elements(self, new_size: Tuple[int, int]) -> bool:
        """Resize elements for new screen size"""
        pass