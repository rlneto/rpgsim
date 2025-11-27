"""
RPGSim Game Engine
Main entry point for the console-based RPG game
"""

import os
import sys
import json
import time
from typing import Optional, Dict, Any

# Add core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.models import Character, CharacterStats, CharacterClass, GameState
from core.validation import validate_character_creation

class GameEngine:
    """Main game engine that coordinates all game systems"""

    def __init__(self):
        self.state: Optional[GameState] = None
        self.running = False
        # self.nav_engine = NavigationEngine()  # Temporarily disabled
        # self.combat_engine = CombatEngine()  # Temporarily disabled

    def start_new_game(self) -> Dict[str, Any]:
        """Initialize a new game session"""
        try:
            # Create initial game state
            self.state = GameState(
                player=None,
                current_location="starter_city",
                game_time=0,
                difficulty="normal"
            )

            return {
                "status": "success",
                "message": "New game initialized successfully",
                "game_state": self.state.to_dict()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to start new game: {str(e)}"
            }

    def create_player_character(self, name: str, character_class: str) -> Dict[str, Any]:
        """Create the main player character"""
        try:
            # Validate inputs
            if not name or len(name.strip()) < 2:
                return {
                    "status": "error",
                    "message": "Character name must be at least 2 characters long"
                }

            if character_class not in self._get_available_classes():
                return {
                    "status": "error",
                    "message": f"Invalid character class: {character_class}"
                }

            # Create character (temporary placeholder)
            player = Character(
                name=name.strip(),
                class_type=CharacterClass[character_class.upper()],
                level=1,
                xp=0,
                stats=CharacterStats(strength=10, dexterity=10, intelligence=10,
                                    wisdom=10, charisma=10, constitution=10)
            )

            # Validate character data (simplified validation)
            validation_result = validate_character_creation(
                player.name,
                player.class_type,
                player.stats
            )
            if not validation_result:
                return {
                    "status": "error",
                    "message": "Character validation failed"
                }

            # Update game state
            if self.state:
                self.state.player = player

            return {
                "status": "success",
                "message": f"Character '{name}' created successfully as {character_class}",
                "character": player.to_dict()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create character: {str(e)}"
            }

    def save_game(self, slot: int = 1) -> Dict[str, Any]:
        """Save current game state to file"""
        try:
            if not self.state or not self.state.player:
                return {
                    "status": "error",
                    "message": "No game in progress to save"
                }

            # Create save directory if it doesn't exist
            save_dir = "saves"
            os.makedirs(save_dir, exist_ok=True)

            # Prepare save data
            save_data = {
                "game_state": self.state.to_dict(),
                "timestamp": time.time(),
                "version": "1.0.0"
            }

            # Write to save file
            save_file = os.path.join(save_dir, f"save_slot_{slot}.json")
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)

            return {
                "status": "success",
                "message": f"Game saved to slot {slot}",
                "file": save_file
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to save game: {str(e)}"
            }

    def load_game(self, slot: int = 1) -> Dict[str, Any]:
        """Load game state from file"""
        try:
            save_file = os.path.join("saves", f"save_slot_{slot}.json")

            if not os.path.exists(save_file):
                return {
                    "status": "error",
                    "message": f"Save file {slot} not found"
                }

            # Load save data
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Restore game state
            self.state = GameState.from_dict(save_data["game_state"])

            return {
                "status": "success",
                "message": f"Game loaded from slot {slot}",
                "game_state": self.state.to_dict()
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to load game: {str(e)}"
            }

    def get_game_status(self) -> Dict[str, Any]:
        """Get current game status"""
        if not self.state:
            return {
                "status": "error",
                "message": "No active game session"
            }

        return {
            "status": "success",
            "game_active": True,
            "has_character": self.state.player is not None,
            "current_location": self.state.current_location,
            "game_time": self.state.game_time
        }

    def travel_to_location(self, location_name: str) -> Dict[str, Any]:
        """Handle player travel between locations"""
        try:
            if not self.state or not self.state.player:
                return {
                    "status": "error",
                    "message": "No active character for travel"
                }

            # Simplified travel system - will be replaced with full implementation
            return {
                "status": "success",
                "message": f"Traveled to {location_name}",
                "location": location_name,
                "travel_time": 15
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Travel failed: {str(e)}"
            }

    def start_combat(self, enemy_id: str) -> Dict[str, Any]:
        """Initiate combat with an enemy"""
        try:
            if not self.state or not self.state.player:
                return {
                    "status": "error",
                    "message": "No active character for combat"
                }

            # Simplified combat system - will be replaced with full implementation
            return {
                "status": "success",
                "message": f"Combat started with {enemy_id}",
                "combat_id": f"combat_{enemy_id}_{time.time()}",
                "enemy": {
                    "id": enemy_id,
                    "name": f"Wild_{enemy_id}",
                    "hp": 100,
                    "level": 1
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to start combat: {str(e)}"
            }

    def _get_available_classes(self) -> list:
        """Get list of available character classes"""
        return [
            "warrior", "mage", "rogue", "cleric", "ranger",
            "paladin", "monk", "bard", "druid", "warlock",
            "barbarian", "sorcerer", "alchemist", "engineer",
            "necromancer", "shaman", "witch", "assassin",
            "templar", "battlemage", "developer", "elementalist",
            "deathknight"
        ]

# Global game instance for easy access
_game_instance: Optional[GameEngine] = None

def get_game_instance() -> GameEngine:
    """Get or create the global game instance"""
    global _game_instance
    if _game_instance is None:
        _game_instance = GameEngine()
    return _game_instance

def start_new_game() -> Dict[str, Any]:
    """Start a new game session"""
    game = get_game_instance()
    return game.start_new_game()

def save_game(slot: int = 1) -> Dict[str, Any]:
    """Save the current game"""
    game = get_game_instance()
    return game.save_game(slot)

def load_game(slot: int = 1) -> Dict[str, Any]:
    """Load a saved game"""
    game = get_game_instance()
    return game.load_game(slot)

def create_character(name: str, character_class: str) -> Dict[str, Any]:
    """Create a new player character"""
    game = get_game_instance()
    return game.create_player_character(name, character_class)

def travel_to_location(location_name: str) -> Dict[str, Any]:
    """Travel to a new location"""
    game = get_game_instance()
    return game.travel_to_location(location_name)

def start_combat(enemy_id: str) -> Dict[str, Any]:
    """Start combat with an enemy"""
    game = get_game_instance()
    return game.start_combat(enemy_id)
