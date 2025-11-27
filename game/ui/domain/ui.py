"""
UI Domain entities and value objects
Core data structures for the interface
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class UIState(str, Enum):
    """UI state enumeration"""
    MAIN_MENU = "main_menu"
    CHARACTER_CREATION = "character_creation"
    GAME_SCREEN = "game_screen"
    INVENTORY = "inventory"
    COMBAT = "combat"
    DIALOG = "dialog"
    SHOP = "shop"
    MAP = "map"
    QUEST_JOURNAL = "quest_journal"
    SETTINGS = "settings"
    PAUSE = "pause"


class AnimationType(str, Enum):
    """Animation type enumeration"""
    NONE = "none"
    PULSE = "pulse"
    FLASH = "flash"
    ROTATE = "rotate"
    SLIDE = "slide"
    FADE = "fade"
    BOUNCE = "bounce"


class MessageType(str, Enum):
    """Message type enumeration"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    COMBAT = "combat"
    LOOT = "loot"
    QUEST = "quest"
    DISCOVERY = "discovery"
    SYSTEM = "system"


@dataclass(frozen=True)
class ScreenPosition:
    """Screen position coordinate"""
    x: int = 0
    y: int = 0
    
    def distance_to(self, other: 'ScreenPosition') -> float:
        """Calculate distance to another position"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True)
class ScreenSize:
    """Screen dimensions"""
    width: int = 80
    height: int = 24
    
    @property
    def center_x(self) -> int:
        """Get center x coordinate"""
        return self.width // 2
    
    @property
    def center_y(self) -> int:
        """Get center y coordinate"""
        return self.height // 2
    
    def contains(self, position: ScreenPosition) -> bool:
        """Check if position is within screen bounds"""
        return (0 <= position.x < self.width and 
                0 <= position.y < self.height)


@dataclass(frozen=True)
class ColorScheme:
    """UI color scheme"""
    primary: str = "#00ff00"
    secondary: str = "#ffff00"
    accent: str = "#ff00ff"
    success: str = "#00ff00"
    warning: str = "#ffff00"
    error: str = "#ff0000"
    info: str = "#00ffff"
    background: str = "#000000"
    text: str = "#ffffff"
    muted: str = "#808080"


@dataclass(frozen=True)
class AnimationConfig:
    """Animation configuration"""
    animation_type: AnimationType = AnimationType.NONE
    duration: float = 1.0
    loop: bool = False
    easing: str = "linear"
    start_value: float = 0.0
    end_value: float = 1.0
    
    @property
    def is_animated(self) -> bool:
        """Check if animation is enabled"""
        return self.animation_type != AnimationType.NONE


@dataclass(frozen=True)
class UIElement:
    """Base UI element"""
    id: str
    type: str
    position: ScreenPosition = ScreenPosition()
    size: ScreenSize = ScreenSize()
    visible: bool = True
    enabled: bool = True
    animation: AnimationConfig = AnimationConfig()
    color: str = "#ffffff"
    background: str = "#000000"
    border: bool = True
    title: str = ""
    content: str = ""
    z_index: int = 0
    
    def is_visible_at(self, position: ScreenPosition) -> bool:
        """Check if element is visible at position"""
        if not self.visible:
            return False
        
        return (self.size.contains(position - self.position) and
                self.size.x > position.x >= 0 and
                self.size.y > position.y >= 0)
    
    def get_bounds(self) -> Tuple[ScreenPosition, ScreenPosition]:
        """Get element bounds"""
        top_left = self.position
        bottom_right = ScreenPosition(
            self.position.x + self.size.width - 1,
            self.position.y + self.size.height - 1
        )
        return top_left, bottom_right


@dataclass(frozen=True)
class LogMessage:
    """Game log message"""
    message: str
    message_type: MessageType = MessageType.INFO
    timestamp: float = field(default_factory=lambda: __import__('time').time())
    icon: str = "📝"
    color: str = "#ffffff"
    is_persistent: bool = False
    
    def __post_init__(self):
        # Set default icon and color based on message type
        if not self.icon or self.icon == "📝":
            icon_map = {
                MessageType.INFO: "📝",
                MessageType.SUCCESS: "✅",
                MessageType.WARNING: "⚠️",
                MessageType.ERROR: "❌",
                MessageType.COMBAT: "⚔️",
                MessageType.LOOT: "💰",
                MessageType.QUEST: "📜",
                MessageType.DISCOVERY: "🔍",
                MessageType.SYSTEM: "⚙️"
            }
            object.__setattr__(self, 'icon', icon_map.get(self.message_type, "📝"))
        
        if self.color == "#ffffff":
            color_map = {
                MessageType.INFO: "#00ffff",
                MessageType.SUCCESS: "#00ff00",
                MessageType.WARNING: "#ffff00",
                MessageType.ERROR: "#ff0000",
                MessageType.COMBAT: "#ff6600",
                MessageType.LOOT: "#ffff00",
                MessageType.QUEST: "#ff00ff",
                MessageType.DISCOVERY: "#00ffff",
                MessageType.SYSTEM: "#808080"
            }
            object.__setattr__(self, 'color', color_map.get(self.message_type, "#ffffff"))
    
    def get_timestamp_string(self) -> str:
        """Get formatted timestamp"""
        import time
        return time.strftime("%H:%M:%S", time.localtime(self.timestamp))


@dataclass(frozen=True)
class MenuItem:
    """Menu item"""
    id: str
    label: str
    icon: str = ""
    description: str = ""
    enabled: bool = True
    shortcut: str = ""
    submenu: Optional[str] = None
    
    def get_display_label(self) -> str:
        """Get label with icon"""
        if self.icon:
            return f"{self.icon} {self.label}"
        return self.label


@dataclass(frozen=True)
class MenuConfig:
    """Menu configuration"""
    id: str
    title: str
    items: List[MenuItem] = field(default_factory=list)
    position: ScreenPosition = ScreenPosition()
    size: ScreenSize = ScreenSize(40, 10)
    multi_select: bool = False
    cancelable: bool = True
    background: str = "#1a1a1a"
    border: str = "#4a4a4a"
    title_color: str = "#ffff00"
    item_color: str = "#ffffff"
    selected_color: str = "#00ff00"
    disabled_color: str = "#808080"


@dataclass(frozen=True)
class TabConfig:
    """Tab configuration"""
    id: str
    label: str
    icon: str = ""
    content: str = ""
    active: bool = False
    closable: bool = False
    badge: Optional[str] = None


@dataclass(frozen=True)
class ProgressConfig:
    """Progress bar configuration"""
    id: str
    current: int = 0
    maximum: int = 100
    label: str = ""
    show_percentage: bool = True
    show_text: bool = True
    color: str = "#00ff00"
    background_color: str = "#404040"
    border: bool = True
    animated: bool = True


@dataclass(frozen=True)
class DialogConfig:
    """Dialog configuration"""
    id: str
    title: str = ""
    message: str = ""
    type: MessageType = MessageType.INFO
    buttons: List[MenuItem] = field(default_factory=list)
    modal: bool = True
    closable: bool = True
    width: int = 60
    max_height: int = 20
    auto_close: Optional[float] = None


@dataclass
class UISession:
    """UI session state"""
    current_screen: UIState = UIState.MAIN_MENU
    previous_screen: Optional[UIState] = None
    screen_history: List[UIState] = field(default_factory=list)
    focused_element: Optional[str] = None
    selected_menu_index: int = 0
    active_tab: str = ""
    color_scheme: ColorScheme = ColorScheme()
    animations_enabled: bool = True
    sound_enabled: bool = True
    auto_save: bool = True
    debug_mode: bool = False
    
    def navigate_to_screen(self, screen: UIState) -> None:
        """Navigate to a new screen"""
        if self.current_screen != screen:
            self.previous_screen = self.current_screen
            self.screen_history.append(self.current_screen)
            self.current_screen = screen
    
    def go_back(self) -> bool:
        """Go back to previous screen"""
        if self.screen_history:
            previous_screen = self.screen_history.pop()
            self.previous_screen = self.current_screen
            self.current_screen = previous_screen
            return True
        return False
    
    def get_navigation_stack(self) -> List[UIState]:
        """Get current navigation stack"""
        stack = self.screen_history.copy()
        stack.append(self.current_screen)
        return stack
    
    def can_go_back(self) -> bool:
        """Check if can go back"""
        return len(self.screen_history) > 0
    
    def reset_navigation(self) -> None:
        """Reset navigation history"""
        self.screen_history.clear()
        self.previous_screen = None
    
    def toggle_setting(self, setting: str) -> Any:
        """Toggle a setting"""
        if hasattr(self, setting):
            current_value = getattr(self, setting)
            if isinstance(current_value, bool):
                setattr(self, setting, not current_value)
            return getattr(self, setting)
        return None


# Default configurations
DEFAULT_COLOR_SCHEME = ColorScheme()

DEFAULT_MENUS = {
    "main": MenuConfig(
        id="main",
        title="🎮 RPGSim - Main Menu",
        items=[
            MenuItem("new_char", "New Character", "🎭", "Start a new adventure"),
            MenuItem("load_game", "Load Game", "💾", "Continue a saved game"),
            MenuItem("settings", "Settings", "⚙️", "Configure game options"),
            MenuItem("help", "Help", "📖", "View help and instructions"),
            MenuItem("quit", "Quit", "🚪", "Exit the game")
        ]
    ),
    "character_creation": MenuConfig(
        id="character_creation",
        title="🎭 Character Creation",
        items=[
            MenuItem("warrior", "Warrior", "⚔️", "Strong melee fighter"),
            MenuItem("mage", "Mage", "🔮", "Powerful spellcaster"),
            MenuItem("rogue", "Rogue", "🗡️", "Stealthy assassin"),
            MenuItem("cleric", "Cleric", "✨", "Divine healer"),
            MenuItem("back", "Back", "⬅️", "Return to main menu")
        ]
    ),
    "game_menu": MenuConfig(
        id="game_menu",
        title="Game Menu",
        items=[
            MenuItem("inventory", "Inventory", "🎒", "View your items"),
            MenuItem("quests", "Quest Journal", "📜", "Active and completed quests"),
            MenuItem("map", "World Map", "🗺️", "Explore the world"),
            MenuItem("save", "Save Game", "💾", "Save your progress"),
            MenuItem("load", "Load Game", "📂", "Load a saved game"),
            MenuItem("settings", "Settings", "⚙️", "Configure options"),
            MenuItem("main_menu", "Main Menu", "🏠", "Return to main menu")
        ]
    )
}

DEFAULT_DIALOGS = {
    "quit_confirm": DialogConfig(
        id="quit_confirm",
        title="Confirm Quit",
        message="Are you sure you want to quit RPGSim?",
        type=MessageType.WARNING,
        buttons=[
            MenuItem("yes", "Yes", "✅", "Quit the game"),
            MenuItem("no", "No", "❌", "Continue playing")
        ]
    ),
    "save_success": DialogConfig(
        id="save_success",
        title="Game Saved",
        message="Your game has been saved successfully!",
        type=MessageType.SUCCESS,
        buttons=[MenuItem("ok", "OK", "✅")],
        auto_close=3.0
    ),
    "error": DialogConfig(
        id="error",
        title="Error",
        message="An error occurred while performing this action.",
        type=MessageType.ERROR,
        buttons=[MenuItem("ok", "OK", "✅")]
    )
}