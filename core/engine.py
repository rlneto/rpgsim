"""
Game Engine Module for RPGSim
Central game engine that orchestrates all systems
"""

from typing import Optional, Dict, Any
import uuid
from datetime import datetime

from .models import GameState, Character, CharacterClass, CharacterStats


class GameEngine:
    """Central game engine that manages all game state"""

    def __init__(self):
        """Initialize game engine"""
        self.game_state: Optional[GameState] = None
        self.is_running = False

    def start_new_game(self, character_name: str, character_class: str) -> bool:
        """Start a new game with character creation"""
        try:
            # Create basic character stats
            stats = CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            )

            # Create character
            try:
                class_enum = CharacterClass(character_class.lower())
            except ValueError:
                # Fallback to warrior if invalid class
                class_enum = CharacterClass.WARRIOR

            character = Character(
                id=str(uuid.uuid4()),
                name=character_name,
                class_type=class_enum,
                level=1,
                experience=0,
                stats=stats,
                hp=100,
                max_hp=100,
                gold=50,
                abilities=[],
                inventory=[],
                quests_completed=[],
                skills={},
            )

            # Initialize game state
            self.game_state = GameState(
                current_location="town_square",
                player=character,
                world_time=480,  # 8:00 AM
                day=1,
                difficulty="normal",
            )

            self.is_running = True
            return True

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"Failed to start new game: {e}")
            return False

    def load_game(self, save_data: Dict[str, Any]) -> bool:
        """Load game from save data"""
        try:
            self.game_state = GameState(**save_data)
            self.is_running = True
            return True
        except (ValueError, KeyError, RuntimeError) as e:
            print(f"Failed to load game: {e}")
            return False

    def save_game(self) -> Optional[Dict[str, Any]]:
        """Save current game state"""
        if not self.game_state:
            return None

        try:
            self.game_state.save_timestamp = datetime.now().isoformat()
            return self.game_state.model_dump()
        except (ValueError, KeyError, RuntimeError) as e:
            print(f"Failed to save game: {e}")
            return None

    def get_game_status(self) -> Dict[str, Any]:
        """Get current game status"""
        if not self.game_state:
            return {"status": "no_game"}

        return {
            "status": "running" if self.is_running else "paused",
            "game_state": self.game_state.get_game_progress(),
        }

    def advance_time(self, minutes: int) -> bool:
        """Advance game time"""
        if not self.game_state or not self.is_running:
            return False

        try:
            self.game_state.advance_world_time(minutes)
            return True
        except (ValueError, KeyError, RuntimeError) as e:
            print(f"Failed to advance time: {e}")
            return False

    def travel_to_location(self, location_id: str) -> bool:
        """Travel to a new location"""
        if not self.game_state or not self.is_running:
            return False

        try:
            # Update current location
            self.game_state.current_location = location_id

            # Add travel time (30 minutes default)
            self.advance_time(30)

            return True
        except (ValueError, KeyError, RuntimeError) as e:
            print(f"Failed to travel: {e}")
            return False

    def shutdown(self):
        """Shutdown game engine"""
        self.is_running = False
        self.game_state = None


# Singleton instance for global access
_game_engine: Optional[GameEngine] = None


def get_game_engine() -> GameEngine:
    """Get global game engine instance"""
    global _game_engine
    if _game_engine is None:
        _game_engine = GameEngine()
    return _game_engine


def reset_game_engine():
    """Reset global game engine instance"""
    global _game_engine
    if _game_engine:
        _game_engine.shutdown()
    _game_engine = None
