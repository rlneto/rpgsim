"""
Dungeon manager service
"""
from typing import Dict, List, Optional, Any, Set
import random
from ..domain.dungeon import (
    Dungeon, ExplorationSession, DungeonTheme, StrategicDecisionType
)
from .dungeon_service import DungeonGenerator


class DungeonManager:
    """Service for managing dungeon state and sessions"""

    def __init__(self):
        self.dungeons: Dict[str, Dungeon] = {}
        self.active_sessions: Dict[str, ExplorationSession] = {}
        self.generator = DungeonGenerator()
        self.themes_used: Set[DungeonTheme] = set()

    def generate_all_dungeons(self, count: int) -> None:
        """Generate a set of dungeons"""
        themes = list(DungeonTheme)

        for i in range(count):
            dungeon_id = f"dungeon_{i}"
            theme = themes[i % len(themes)]
            level = 1 + (i // 5)

            dungeon = self.generator.generate_dungeon(dungeon_id, theme, level)
            self.dungeons[dungeon_id] = dungeon
            self.themes_used.add(theme)

    def get_dungeon(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get dungeon by ID"""
        return self.dungeons.get(dungeon_id)

    def start_exploration(self, dungeon_id: str, player_level: int) -> Optional[ExplorationSession]:
        """Start an exploration session"""
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return None

        session = ExplorationSession(dungeon, player_level)
        self.active_sessions[dungeon_id] = session
        return session

    def get_session(self, dungeon_id: str) -> Optional[ExplorationSession]:
        """Get active session"""
        return self.active_sessions.get(dungeon_id)

    def end_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End exploration session"""
        session = self.get_session(dungeon_id)
        if not session:
            return {}

        results = {
            'dungeon_id': dungeon_id,
            'rooms_explored': session.rooms_explored,
            'puzzles_solved': session.puzzles_solved,
            'secrets_found': session.secrets_found,
            'rewards': session.rewards_found,
            'exploration_percentage': session.dungeon.get_explored_percentage()
        }

        del self.active_sessions[dungeon_id]
        return results

    def get_all_themes(self) -> List[DungeonTheme]:
        """Get all used themes"""
        return list(self.themes_used)

    def get_dungeons_by_theme(self, theme: DungeonTheme) -> List[Dungeon]:
        """Get dungeons with specific theme"""
        return [d for d in self.dungeons.values() if d.theme == theme]
