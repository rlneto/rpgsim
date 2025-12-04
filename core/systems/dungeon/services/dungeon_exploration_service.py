"""
Dungeon exploration services
"""
from typing import Dict, Any
from ..domain.dungeon import Dungeon, Room, StrategicDecisionType, ExplorationSession
from ..interfaces.repositories import DungeonRepository


class DungeonExplorationService:
    """Service for dungeon exploration"""

    def __init__(self, dungeon_repository: DungeonRepository):
        self._dungeon_repository = dungeon_repository
        self._sessions: Dict[str, ExplorationSession] = {}

    def start_exploration(self, dungeon_id: str, player_level: int) -> ExplorationSession:
        """Start a new exploration session"""
        dungeon = self._dungeon_repository.get_by_id(dungeon_id)
        if not dungeon:
            raise ValueError("Dungeon not found")

        session = ExplorationSession(dungeon, player_level)
        self._sessions[dungeon_id] = session
        return session

    def get_session(self, dungeon_id: str) -> ExplorationSession:
        """Get an active exploration session"""
        return self._sessions.get(dungeon_id)

    def explore_room(self, dungeon_id: str, room_id: str) -> Dict[str, Any]:
        """Explore a room in the dungeon"""
        session = self.get_session(dungeon_id)
        if not session:
            raise ValueError("Active session not found")

        room = session.dungeon.get_room(room_id)
        if not room:
            raise ValueError("Room not found")

        return session.explore_room(room)

    def make_strategic_decision(self, dungeon_id: str, decision_type: StrategicDecisionType) -> None:
        """Make a strategic decision"""
        session = self.get_session(dungeon_id)
        if not session:
            raise ValueError("Active session not found")

        session.make_strategic_decision(decision_type)

    def end_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End an exploration session"""
        session = self.get_session(dungeon_id)
        if not session:
            return {"error": "Session not found"}

        summary = {
            "dungeon_id": dungeon_id,
            "rooms_explored": session.rooms_explored,
            "secrets_found": session.secrets_found,
            "exploration_percentage": session.dungeon.get_explored_percentage(),
        }
        del self._sessions[dungeon_id]
        return summary
