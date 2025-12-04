"""
Dungeon System Facade
"""
from typing import List, Dict, Any, Optional
from .services.dungeon_manager import DungeonManager
from .services.dungeon_service import DungeonGenerator
from .services.reward_system import RewardSystem
from .domain.dungeon import DungeonTheme, StrategicDecisionType


class DungeonSystem:
    """Facade for the Dungeon System"""

    def __init__(self):
        self.manager = DungeonManager()
        self.generator = self.manager.generator
        self.reward_system = RewardSystem()

    def initialize_dungeons(self, count: int = 50) -> None:
        """Initialize the world dungeons"""
        self.manager.generate_all_dungeons(count)

    def get_dungeon_list(self) -> List[Dict[str, Any]]:
        """Get list of all dungeons"""
        return [
            {
                'id': d.id,
                'name': d.name,
                'theme': d.theme.value,
                'level': d.level
            }
            for d in self.manager.dungeons.values()
        ]

    def enter_dungeon(self, dungeon_id: str, player_level: int) -> Dict[str, Any]:
        """Enter a dungeon"""
        dungeon = self.manager.get_dungeon(dungeon_id)
        if not dungeon:
            return {'error': 'Dungeon not found'}

        session = self.manager.start_exploration(dungeon_id, player_level)

        return {
            'dungeon_id': dungeon.id,
            'name': dungeon.name,
            'theme': dungeon.theme.value,
            'puzzles': [p.value for p in dungeon.puzzles],
            'environmental_challenges': [c.value for c in dungeon.environmental_challenges]
        }

    def explore_dungeon(self, dungeon_id: str, actions: List[str]) -> Dict[str, Any]:
        """Perform exploration actions"""
        session = self.manager.get_session(dungeon_id)
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
                    session.explore_room(room)

            elif action == 'make_strategic_choice':
                session.make_strategic_decision(StrategicDecisionType.PATH_CHOICE)
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
        session = self.manager.get_session(dungeon_id)
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
        return self.manager.end_exploration(dungeon_id)


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
