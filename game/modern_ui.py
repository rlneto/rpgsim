"""
Modern Terminal UI - Refactored Modular Version
Rich ASCII art, animations, and immersive RPG experience
"""

from typing import Dict, Any, Optional
from .ui.modular_ui import (
    UISystem,
    get_ui_system,
    initialize_ui,
    run_ui,
    log_message,
    GameState,
    UIState,
    MessageType,
)
from .ui.domain.ui import (
    UISession,
    LogMessage,
    ColorScheme,
    ScreenPosition,
    ScreenSize,
    MenuItem,
)
from .ui.services.ui_service import UIServiceFactory

# from .ui.assets.ascii_art import ASCIIArtAssets
from .ui.components.ui_components import (
    CharacterDisplay,
    LocationDisplay,
    GameLog,
    MenuDisplay,
    StatusDisplay,
    DialogDisplay,
)
from .ui.screens.modern_terminal_ui import (
    GameScreen,
    CharacterCreationScreen,
    MainMenuScreen,
    create_terminal_ui,
    run_terminal_ui,
)


# Backward compatibility aliases
class ModernTerminalUI:
    """Backward compatibility wrapper for modular UI"""

    def __init__(self):
        self.ui_system = get_ui_system()
        self.game_state = GameState()

    def initialize(self) -> bool:
        """Initialize UI"""
        return self.ui_system.initialize_ui()

    def run(self) -> None:
        """Run UI application"""
        self.ui_system.set_game_state(self.game_state)
        self.ui_system.run_ui()

    def set_game_state(
        self,
        player_data: Dict[str, Any],
        location_data: Dict[str, Any],
        status_data: Dict[str, Any],
    ) -> bool:
        """Set game state"""
        self.game_state.player = player_data
        self.game_state.location = location_data
        self.game_state.status = status_data
        return self.ui_system.set_game_state(self.game_state)

    def log_message(self, message: str, message_type: str = "info") -> bool:
        """Log message"""
        msg_type = MessageType.INFO
        if message_type == "success":
            msg_type = MessageType.SUCCESS
        elif message_type == "warning":
            msg_type = MessageType.WARNING
        elif message_type == "error":
            msg_type = MessageType.ERROR
        elif message_type == "combat":
            msg_type = MessageType.COMBAT
        elif message_type == "loot":
            msg_type = MessageType.LOOT
        elif message_type == "quest":
            msg_type = MessageType.QUEST
        elif message_type == "discovery":
            msg_type = MessageType.DISCOVERY

        return self.ui_system.log_message(message, msg_type)

    def get_ascii_art(self, art_id: str) -> Optional[str]:
        """Get ASCII art"""
        return self.ui_system.get_ascii_art(art_id)

    def navigate_to_screen(self, screen_name: str) -> bool:
        """Navigate to screen"""
        screen_map = {
            "main_menu": UIState.MAIN_MENU,
            "character_creation": UIState.CHARACTER_CREATION,
            "game": UIState.GAME_SCREEN,
            "inventory": UIState.INVENTORY,
            "combat": UIState.COMBAT,
            "shop": UIState.SHOP,
            "map": UIState.MAP,
            "quest_journal": UIState.QUEST_JOURNAL,
        }

        screen_state = screen_map.get(screen_name.lower())
        if screen_state:
            return self.ui_system.navigate_to_screen(screen_state)
        return False


# Factory functions for easy access
def create_modern_ui() -> ModernTerminalUI:
    """Create modern terminal UI instance"""
    return ModernTerminalUI()


def run_modern_terminal_ui() -> None:
    """Run modern terminal UI"""
    ui = create_modern_ui()
    ui.initialize()
    ui.run()


# Legacy function names for backward compatibility are imported from modular_terminal_ui


# Export main classes and functions
__all__ = [
    "ModernTerminalUI",
    "create_modern_ui",
    "run_modern_terminal_ui",
    "create_terminal_ui",  # Legacy from modular_terminal_ui
    "run_terminal_ui",  # Legacy from modular_terminal_ui
    "UISystem",
    "get_ui_system",
    "initialize_ui",
    "DialogDisplay",
    "GameScreen",
    "CharacterCreationScreen",
    "MainMenuScreen",
]
