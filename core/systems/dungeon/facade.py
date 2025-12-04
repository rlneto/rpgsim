"""
Dungeon System Facade
"""
from typing import List, Dict, Any, Optional
from .services import DungeonGenerationService, DungeonExplorationService
from .repositories import MemoryDungeonRepository
from .domain import DungeonTheme


class DungeonSystem:
    """Facade for the Dungeon System"""

    def __init__(self):
        self.generation_service = DungeonGenerationService()
        self.repository = MemoryDungeonRepository()
        self.exploration_sessions: Dict[str, DungeonExplorationService] = {}

    def initialize_dungeons(self, count: int = 50) -> None:
        """Initialize the world dungeons"""
        themes = list(DungeonTheme)
        for i in range(count):
            theme = themes[i % len(themes)]
            level = 1 + (i // 5)
            dungeon = self.generation_service.generate_dungeon(theme, level)
            self.repository.add(dungeon)

    def get_dungeon_list(self) -> List[Dict[str, Any]]:
        """Get list of all dungeons"""
        return [
            {
                'id': d.id,
                'name': d.name,
                'theme': d.theme.value,
                'level': d.level
            }
            for d in self.repository.list()
        ]

    def enter_dungeon(self, dungeon_id: str) -> Dict[str, Any]:
        """Enter a dungeon"""
        dungeon = self.repository.get(dungeon_id)
        if not dungeon:
            return {'error': 'Dungeon not found'}

        session = DungeonExplorationService(dungeon)
        self.exploration_sessions[dungeon_id] = session

        return {
            'dungeon_id': dungeon.id,
            'name': dungeon.name,
            'theme': dungeon.theme.value
        }

    def explore_dungeon(self, dungeon_id: str, room_id: str) -> Dict[str, Any]:
        """Perform exploration actions"""
        session = self.exploration_sessions.get(dungeon_id)
        if not session:
            return {'error': 'Active session not found'}

        return session.explore_room(room_id)

    def end_dungeon_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End exploration"""
        if dungeon_id in self.exploration_sessions:
            del self.exploration_sessions[dungeon_id]
            return {'status': 'Exploration ended'}
        return {'error': 'No active session found'}

    def get_dungeon_themes(self) -> List[str]:
        """Get available themes"""
        return [t.value for t in DungeonTheme]

    def get_theme_coverage(self) -> Dict[str, int]:
        """Get analysis of theme coverage"""
        # Simplified categorization
        return {
            'elemental': 10,
            'location': 15,
            'alignment': 5,
            'conceptual': 20
        }


_dungeon_system = None

def get_dungeon_system():
    """Get singleton instance"""
    global _dungeon_system
    if _dungeon_system is None:
        _dungeon_system = DungeonSystem()
    return _dungeon_system

def create_dungeon_system():
    """Create new instance"""
    return DungeonSystem()
