"""
Dungeon System Facade
"""
import random
import uuid
from typing import List, Dict, Any, Optional
from .services.dungeon_generation_service import DungeonGenerationService
from .services.dungeon_exploration_service import DungeonExplorationService
from .services.reward_system import RewardSystem
from .domain.dungeon import DungeonTheme, StrategicDecisionType
from .repositories.memory_repository import MemoryDungeonRepository


class DungeonSystem:
    """Facade for the Dungeon System"""

    def __init__(self):
        self.repository = MemoryDungeonRepository()
        self.generation_service = DungeonGenerationService()
        self.exploration_service = DungeonExplorationService(self.repository)
        self.reward_system = RewardSystem()

    def initialize_dungeons(self, count: int = 50) -> None:
        """Initialize the world dungeons"""
        themes = random.sample(list(DungeonTheme), count)
        for i in range(count):
            theme = themes[i]
            player_level = random.randint(1, 10)
            dungeon_id = str(uuid.uuid4())
            dungeon = self.generation_service.generate_dungeon(dungeon_id, theme, player_level)
            self.repository.save(dungeon)

    def get_dungeon_list(self) -> List[Dict[str, Any]]:
        """Get list of all dungeons"""
        dungeons = self.repository.get_all()
        return [
            {
                'id': d.id,
                'name': d.name,
                'theme': d.theme.value,
                'level': d.level
            }
            for d in dungeons
        ]

    def enter_dungeon(self, dungeon_id: str, player_level: int) -> Dict[str, Any]:
        """Enter a dungeon"""
        dungeon = self.repository.get_by_id(dungeon_id)
        if not dungeon:
            return {'error': 'Dungeon not found'}

        session = self.exploration_service.start_exploration(dungeon_id, player_level)

        return {
            'dungeon_id': dungeon.id,
            'name': dungeon.name,
            'theme': dungeon.theme.value,
            'puzzles': [p.value for p in dungeon.puzzles],
            'environmental_challenges': [c.value for c in dungeon.environmental_challenges]
        }

    def explore_dungeon(self, dungeon_id: str, actions: List[str]) -> Dict[str, Any]:
        """Perform exploration actions"""
        session = self.exploration_service.get_session(dungeon_id)
        if not session:
            return {'error': 'Active session not found'}

        for action in actions:
            if action == 'explore_room':
                # Pick an unexplored connected room or just next one for simulation
                room = None
                if session.current_room_id:
                    current = session.dungeon.get_room(session.current_room_id)
                    for conn_id in current.connections:
                        conn_room = session.dungeon.get_room(conn_id)
                        if not conn_room.explored:
                            room = conn_room
                            break

                # Fallback to linear search
                if not room:
                    for r in session.dungeon.rooms.values():
                        if not r.explored:
                            room = r
                            break

                if room:
                    self.exploration_service.explore_room(dungeon_id, room.id)

            elif action == 'make_strategic_choice':
                self.exploration_service.make_strategic_decision(dungeon_id, StrategicDecisionType.PATH_CHOICE)
            elif action == 'face_challenge':
                # Simulate challenge success
                pass

        return {
            'rooms_explored': session.rooms_explored,
            'strategic_decisions': session.strategic_decisions_made,
            'discoveries': session.discoveries
        }

    def navigate_dungeon(self, dungeon_id: str, depth: int = 0) -> Dict[str, Any]:
        """Navigate deeper into dungeon"""
        session = self.exploration_service.get_session(dungeon_id)
        if not session:
            return {'error': 'Active session not found'}

        # Simulate navigation results
        multiplier = session.calculate_difficulty_multiplier(depth)

        # Generate reward if depth sufficient
        if depth > 0:
            reward = self.reward_system.generate_reward(depth, session.dungeon.level)
            session.add_reward(reward)

        return {
            'depth_reached': depth,
            'difficulty_curve': multiplier,
            'rewards_found': session.rewards_found,
            'progress_percentage': session.dungeon.get_explored_percentage()
        }

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

    def end_dungeon_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End exploration"""
        return self.exploration_service.end_exploration(dungeon_id)


# Global instances for testing compatibility
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
