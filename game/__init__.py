"""
UI module using modular architecture pattern
Provides modern terminal interface with ASCII art and animations
"""

from .ui import GameUI
from .modern_ui import run_terminal_ui, create_terminal_ui

__all__ = ['GameUI', 'run_terminal_ui', 'create_terminal_ui']