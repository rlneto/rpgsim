"""
Dungeon exploration services
"""
from typing import Dict, Any, Optional
from ..domain.dungeon import Dungeon
from ..domain.room import Room


class DungeonExplorationService:
    """Service for dungeon exploration"""

    def __init__(self, dungeon: Dungeon):
        self.dungeon = dungeon
        self.current_room_id: Optional[str] = None
        entrance = self.dungeon.get_entrance()
        if entrance:
            self.current_room_id = entrance.id

    def explore_room(self, room_id: str) -> Dict[str, Any]:
        """Explore a room"""
        room = self.dungeon.get_room(room_id)
        if not room:
            return {"error": "Room not found"}

        self.current_room_id = room_id
        return room.explore()

    def get_current_room(self) -> Optional[Room]:
        """Get the current room"""
        if self.current_room_id:
            return self.dungeon.get_room(self.current_room_id)
        return None
