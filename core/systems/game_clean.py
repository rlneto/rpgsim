"""
Game system facade for BDD compatibility
"""

from typing import Dict, Any, Optional, List

# Import BDD version
from .game_bdd import (
    start_new_game,
    save_game,
    load_game,
    get_game_state,
    continue_game
)