"""
Game system facade for BDD compatibility
"""

from typing import Dict, Any, Optional, List


# Global game state for BDD scenarios
_game_state = {
    "started": False,
    "player": None,
    "current_location": None,
    "save_data": {}
}


def start_new_game() -> Dict[str, Any]:
    """Start a new game session (BDD compliant)"""
    global _game_state
    _game_state["started"] = True
    _game_state["player"] = None
    _game_state["current_location"] = "starting_area"
    
    return {
        "status": "started",
        "message": "New game started successfully!",
        "player": _game_state["player"],
        "location": _game_state["current_location"]
    }


def save_game(save_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Save game state (BDD compliant)"""
    global _game_state
    
    if data is None:
        data = _game_state.copy()
    
    _game_state["save_data"][save_id] = data
    
    return {
        "status": "saved",
        "save_id": save_id,
        "message": f"Game saved as {save_id}",
        "timestamp": "2023-01-01T12:00:00Z"
    }


def load_game(save_id: str) -> Dict[str, Any]:
    """Load game state (BDD compliant)"""
    global _game_state
    
    if save_id not in _game_state["save_data"]:
        return {
            "status": "error",
            "message": f"Save file {save_id} not found"
        }
    
    _game_state = _game_state["save_data"][save_id].copy()
    
    return {
        "status": "loaded",
        "save_id": save_id,
        "message": f"Game {save_id} loaded successfully",
        "game_state": _game_state
    }


def get_game_state() -> Dict[str, Any]:
    """Get current game state (BDD compliant)"""
    global _game_state
    return _game_state.copy()


def continue_game() -> Dict[str, Any]:
    """Continue existing game (BDD compliant)"""
    global _game_state
    
    if not _game_state["started"]:
        return {
            "status": "error",
            "message": "No saved game found"
        }
    
    return {
        "status": "continued",
        "message": "Game continued successfully",
        "game_state": _game_state
    }