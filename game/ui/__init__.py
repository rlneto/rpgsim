"""
UI package module exports
"""

from .ui.modular_ui import UISystem, get_ui_system, initialize_ui, run_ui, log_message
from .ui.domain.ui import (
    UISession, UIState, MessageType, ColorScheme,
    LogMessage, ScreenPosition, ScreenSize, MenuItem
)
from .ui.services.ui_service import UIServiceFactory
from .ui.assets.ascii_art import ASCIIArtAssets
from .ui.components.ui_components import (
    CharacterDisplay, LocationDisplay, GameLog,
    MenuDisplay, StatusDisplay, DialogDisplay
)
from .ui.screens.modern_terminal_ui import (
    GameScreen, CharacterCreationScreen, MainMenuScreen,
    GameState, create_terminal_ui, run_terminal_ui
)
from .modern_ui import ModernTerminalUI, create_modern_ui, run_modern_terminal_ui

__all__ = [
    # Core System
    'UISystem',
    'get_ui_system',
    'initialize_ui',
    'run_ui',
    'log_message',
    
    # Domain Models
    'UISession',
    'UIState',
    'MessageType',
    'ColorScheme',
    'LogMessage',
    'ScreenPosition',
    'ScreenSize',
    'MenuItem',
    
    # Services
    'UIServiceFactory',
    
    # Assets
    'ASCIIArtAssets',
    
    # Components
    'CharacterDisplay',
    'LocationDisplay',
    'GameLog',
    'MenuDisplay',
    'StatusDisplay',
    'DialogDisplay',
    
    # Screens
    'GameScreen',
    'CharacterCreationScreen',
    'MainMenuScreen',
    
    # Main Application
    'GameState',
    'ModernTerminalUI',
    'create_terminal_ui',
    'run_terminal_ui',
    'create_modern_ui',
    'run_modern_terminal_ui'
]