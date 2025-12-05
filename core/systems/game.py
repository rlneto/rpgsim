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


class GameSystem:
    """Game system facade for BDD compatibility"""
    
    def __init__(self):
        from .character import CharacterSystem
        from .world import WorldSystem
        from .city import CitySystem
        from .shop import ShopSystem
        from .dungeon import DungeonSystem
        from .quest import QuestSystem
        from .equipment import EquipmentSystem
        from .gamification import GamificationSystem
        
        self.character_system = CharacterSystem()
        self.world_system = WorldSystem()
        self.city_system = CitySystem()
        self.shop_system = ShopSystem()
        self.dungeon_system = DungeonSystem()
        self.quest_system = QuestSystem()
        self.equipment_system = EquipmentSystem()
        self.gamification_system = GamificationSystem()
        
        self._game_state = {}

    def start_new_game(self) -> Dict[str, Any]:
        """Start a new game"""
        try:
            start_location = "riverdale"
            self._game_state = {
                "current_location": {"id": start_location, "name": "Riverdale"},
                "player": None,
                "time": 0,
            }
            return {
                "status": "success",
                "message": "New game started successfully",
                "starting_location": start_location,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to start game: {str(e)}"}

    def create_character(self, name: str, character_class: str) -> Dict[str, Any]:
        """Create a new character"""
        try:
            character = self.character_system.create_character(name, character_class)
            if character:
                self._game_state["player"] = character
                return {
                    "status": "success",
                    "message": f"Character {name} created successfully",
                    "character": character,
                }
            else:
                return {"status": "error", "message": "Failed to create character"}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create character: {str(e)}",
            }

    def travel_to_location(self, location_id: str) -> Dict[str, Any]:
        """Travel to a location"""
        try:
            if not self._game_state.get("player"):
                return {"status": "error", "message": "No character created"}

            # Get character data for travel validation
            character_data = {
                "level": getattr(self._game_state["player"], "level", 1),
                "gold": getattr(self._game_state["player"], "gold", 0),
                "inventory": getattr(self._game_state["player"], "inventory", []),
            }

            current_loc = (self._game_state.get("current_location") or {}).get(
                "id", "riverdale"
            )

            if self.world_system.can_travel(current_loc, location_id, character_data):
                travel_time = self.world_system.calculate_travel_time(
                    current_loc, location_id, character_data
                )
                location_details = self.world_system.get_location_details(location_id)

                # Update game state
                self._game_state["current_location"] = location_details
                self.world_system.advance_time(travel_time)

                return {
                    "status": "success",
                    "message": f"Traveled to {location_details.get('name', location_id)}",
                    "travel_time": travel_time,
                    "location": location_details,
                }
            else:
                return {"status": "error", "message": f"Cannot travel to {location_id}"}
        except Exception as e:
            return {"status": "error", "message": f"Travel failed: {str(e)}"}

    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return self._game_state.copy()


# Global instance for BDD compatibility
_game_system = GameSystem()


# BDD compatibility functions
def get_game_instance() -> GameSystem:
    """Get the game system instance"""
    return _game_system


def start_new_game() -> Dict[str, Any]:
    """Start a new game (BDD compatibility)"""
    return _game_system.start_new_game()


def create_character(name: str, character_class: str) -> Dict[str, Any]:
    """Create a character (BDD compatibility)"""
    return _game_system.create_character(name, character_class)


def travel_to_location(location_id: str) -> Dict[str, Any]:
    """Travel to location (BDD compatibility)"""
    return _game_system.travel_to_location(location_id)


def start_combat(enemy_type: str) -> Dict[str, Any]:
    """Start combat (BDD compatibility)"""
    try:
        if not _game_system._game_state.get("player"):
            return {"status": "error", "message": "No character created"}

        # Simple combat implementation for BDD
        return {
            "status": "success",
            "message": f"Combat started with {enemy_type}",
            "enemy": enemy_type,
            "combat_active": True,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to start combat: {str(e)}"}


def _get_available_classes(self) -> List[str]:
    """Get available character classes (BDD compatibility)"""
    return self.character_system.get_all_classes()


# Export for BDD
__all__ = [
    "GameSystem",
    "get_game_instance",
    "start_new_game",
    "create_character",
    "travel_to_location",
    "start_combat",
]
