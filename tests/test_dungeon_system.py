"""
Unit tests for Dungeon Exploration System.

Tests dungeon generation, themes, layouts, puzzles, environmental challenges,
secrets, progression, rewards, and strategic decision-making.
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.systems.dungeon.domain.dungeon import (
    DungeonTheme, LayoutType, PuzzleType, EnvironmentalChallenge, RewardTier,
    RoomType, StrategicDecisionType, LoreType, Room, Dungeon, ExplorationSession
)
from core.systems.dungeon.services.dungeon_generation_service import DungeonGenerationService
from core.systems.dungeon.services.dungeon_exploration_service import DungeonExplorationService
from core.systems.dungeon.services.reward_system import RewardSystem
from core.systems.dungeon.facade import DungeonSystem, get_dungeon_system, create_dungeon_system
from core.systems.dungeon.repositories.memory_repository import MemoryDungeonRepository


class TestDungeonEnums(unittest.TestCase):
    """Test dungeon enumeration types."""

    def test_dungeon_theme_count(self):
        """Test there are exactly 50 dungeon themes."""
        self.assertEqual(len(DungeonTheme), 50)

    def test_dungeon_theme_values(self):
        """Test dungeon theme values are valid."""
        themes = list(DungeonTheme)
        for theme in themes:
            self.assertIsInstance(theme.value, str)
            self.assertTrue(len(theme.value) > 0)
            self.assertTrue('_' in theme.value or theme.value.islower())

    def test_layout_types(self):
        """Test layout type enumeration."""
        expected_layouts = ['linear', 'branching', 'circular', 'maze', 'spiral', 'multilevel']
        actual_layouts = [layout.value for layout in LayoutType]
        self.assertEqual(sorted(actual_layouts), sorted(expected_layouts))

    def test_puzzle_types(self):
        """Test puzzle type enumeration."""
        expected_puzzles = ['mechanical', 'magical', 'logical', 'spatial', 'temporal', 'pattern', 'riddle', 'environmental']
        actual_puzzles = [puzzle.value for puzzle in PuzzleType]
        self.assertEqual(sorted(actual_puzzles), sorted(expected_puzzles))

    def test_environmental_challenges(self):
        """Test environmental challenge enumeration."""
        expected_challenges = ['darkness', 'poison', 'fire', 'ice', 'electricity', 'wind', 'gravity', 'time_warp']
        actual_challenges = [challenge.value for challenge in EnvironmentalChallenge]
        self.assertEqual(sorted(actual_challenges), sorted(expected_challenges))

    def test_reward_tiers(self):
        """Test reward tier enumeration."""
        expected_tiers = ['common', 'uncommon', 'rare', 'epic', 'legendary']
        actual_tiers = [tier.value for tier in RewardTier]
        self.assertEqual(sorted(actual_tiers), sorted(expected_tiers))


class TestRoom(unittest.TestCase):
    """Test Room functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.room = Room(
            id="test_room",
            type=RoomType.CHAMBER,
            x=5, y=10,
            contents=["chest", "torch"],
            secrets=["hidden_key"],
            challenge=EnvironmentalChallenge.DARKNESS,
            puzzle=PuzzleType.MECHANICAL,
            lore=LoreType.INSCRIPTIONS
        )

    def test_room_initialization(self):
        """Test room initialization."""
        self.assertEqual(self.room.id, "test_room")
        self.assertEqual(self.room.type, RoomType.CHAMBER)
        self.assertEqual(self.room.x, 5)
        self.assertEqual(self.room.y, 10)
        self.assertFalse(self.room.explored)

    def test_add_connection(self):
        """Test adding room connections."""
        self.room.add_connection("room_2")
        self.assertIn("room_2", self.room.connections)

        # Test duplicate connection not added
        self.room.add_connection("room_2")
        self.assertEqual(self.room.connections.count("room_2"), 1)

    def test_explore_room(self):
        """Test room exploration."""
        result = self.room.explore()

        self.assertTrue(self.room.explored)
        self.assertEqual(result['room_id'], "test_room")
        self.assertEqual(result['type'], "chamber")
        self.assertEqual(result['contents'], ["chest", "torch"])
        self.assertEqual(result['secrets'], ["hidden_key"])
        self.assertEqual(result['challenge'], "darkness")
        self.assertEqual(result['puzzle'], "mechanical")
        self.assertEqual(result['lore'], "inscriptions")

    def test_explore_already_explored(self):
        """Test exploring already explored room."""
        self.room.explored = True
        result = self.room.explore()
        self.assertEqual(result, {})


class TestDungeon(unittest.TestCase):
    """Test Dungeon functionality."""

    def setUp(self):
        """Set up test fixtures."""
        rooms = {
            "entrance": Room("entrance", RoomType.ENTRANCE, 0, 0),
            "chamber1": Room("chamber1", RoomType.CHAMBER, 1, 0),
            "boss": Room("boss", RoomType.BOSS_ROOM, 2, 0)
        }

        self.dungeon = Dungeon(
            id="test_dungeon",
            name="Test Dungeon",
            theme=DungeonTheme.ANCIENT_TEMPLE,
            level=10,
            rooms=rooms,
            layout=LayoutType.LINEAR,
            puzzles=[PuzzleType.RIDDLE, PuzzleType.MAGICAL],
            environmental_challenges=[EnvironmentalChallenge.DARKNESS],
            secrets=5,
            hidden_areas=3,
            lore_elements=10
        )

    def test_dungeon_initialization(self):
        """Test dungeon initialization."""
        self.assertEqual(self.dungeon.id, "test_dungeon")
        self.assertEqual(self.dungeon.theme, DungeonTheme.ANCIENT_TEMPLE)
        self.assertEqual(self.dungeon.level, 10)
        self.assertEqual(len(self.dungeon.rooms), 3)

    def test_get_room(self):
        """Test getting room by ID."""
        room = self.dungeon.get_room("entrance")
        self.assertIsNotNone(room)
        self.assertEqual(room.id, "entrance")

        non_existent = self.dungeon.get_room("non_existent")
        self.assertIsNone(non_existent)

    def test_get_entrance(self):
        """Test getting entrance room."""
        entrance = self.dungeon.get_entrance()
        self.assertIsNotNone(entrance)
        self.assertEqual(entrance.type, RoomType.ENTRANCE)

    def test_get_boss_room(self):
        """Test getting boss room."""
        boss_room = self.dungeon.get_boss_room()
        self.assertIsNotNone(boss_room)
        self.assertEqual(boss_room.type, RoomType.BOSS_ROOM)

    def test_get_explored_percentage(self):
        """Test exploration percentage calculation."""
        self.assertEqual(self.dungeon.get_explored_percentage(), 0.0)

        # Explore one room
        list(self.dungeon.rooms.values())[0].explored = True
        self.assertAlmostEqual(self.dungeon.get_explored_percentage(), 33.33, places=1)

        # Explore all rooms
        for room in self.dungeon.rooms.values():
            room.explored = True
        self.assertEqual(self.dungeon.get_explored_percentage(), 100.0)


class TestExplorationSession(unittest.TestCase):
    """Test ExplorationSession functionality."""

    def setUp(self):
        """Set up test fixtures."""
        rooms = {
            "entrance": Room("entrance", RoomType.ENTRANCE, 0, 0),
            "chamber1": Room("chamber1", RoomType.CHAMBER, 1, 0,
                                   puzzle=PuzzleType.MECHANICAL,
                                   secrets=["secret1"]),
        }

        dungeon = Dungeon(
            id="test_dungeon",
            name="Test Dungeon",
            theme=DungeonTheme.ANCIENT_TEMPLE,
            level=10,
            rooms=rooms,
            layout=LayoutType.LINEAR,
            puzzles=[PuzzleType.RIDDLE],
            environmental_challenges=[EnvironmentalChallenge.DARKNESS],
            secrets=5,
            hidden_areas=3,
            lore_elements=10
        )

        self.session = ExplorationSession(dungeon=dungeon, player_level=10)

    def test_session_initialization(self):
        """Test session initialization."""
        self.assertEqual(self.session.dungeon.id, "test_dungeon")
        self.assertEqual(self.session.player_level, 10)
        self.assertEqual(self.session.rooms_explored, 0)

    def test_explore_room(self):
        """Test room exploration in session."""
        room = self.session.dungeon.get_room("chamber1")
        discovery = self.session.explore_room(room)

        self.assertEqual(self.session.rooms_explored, 1)
        self.assertEqual(self.session.puzzles_solved, 1)
        self.assertEqual(self.session.secrets_found, 1)
        self.assertEqual(len(self.session.discoveries), 1)

    def test_make_strategic_decision(self):
        """Test strategic decision recording."""
        initial_decisions = self.session.strategic_decisions_made
        self.session.make_strategic_decision(StrategicDecisionType.PATH_CHOICE)
        self.assertEqual(self.session.strategic_decisions_made, initial_decisions + 1)

    def test_add_reward(self):
        """Test reward addition."""
        reward = {'tier': 'rare', 'value': 1000}
        self.session.add_reward(reward)
        self.assertIn(reward, self.session.rewards_found)

    def test_calculate_difficulty_multiplier(self):
        """Test difficulty multiplier calculation."""
        base_multiplier = self.session.calculate_difficulty_multiplier(0)
        self.assertEqual(base_multiplier, 1.0)

        depth_multiplier = self.session.calculate_difficulty_multiplier(10)
        self.assertGreater(depth_multiplier, 1.0)


class TestDungeonGenerationService(unittest.TestCase):
    """Test DungeonGenerationService functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = DungeonGenerationService()

    def test_generator_initialization(self):
        """Test generator initialization."""
        self.assertIsNotNone(self.generator.theme_puzzle_mapping)
        self.assertIsNotNone(self.generator.theme_challenge_mapping)

    def test_generate_dungeon(self):
        """Test dungeon generation."""
        dungeon = self.generator.generate_dungeon(
            "test_dungeon",
            DungeonTheme.ANCIENT_TEMPLE,
            player_level=15
        )

        self.assertEqual(dungeon.id, "test_dungeon")
        self.assertEqual(dungeon.theme, DungeonTheme.ANCIENT_TEMPLE)
        self.assertEqual(dungeon.level, 15)
        self.assertGreater(len(dungeon.rooms), 0)
        self.assertGreater(len(dungeon.puzzles), 0)
        self.assertGreater(dungeon.secrets, 0)
        self.assertGreater(dungeon.lore_elements, 0)

    def test_generate_theme_puzzles(self):
        """Test theme-appropriate puzzle generation."""
        puzzles = self.generator._generate_theme_puzzles(DungeonTheme.ANCIENT_TEMPLE)
        self.assertGreaterEqual(len(puzzles), 2)
        self.assertLessEqual(len(puzzles), 4)

        # Should include theme-appropriate puzzles
        puzzle_values = [p.value for p in puzzles]
        self.assertTrue(any(p in puzzle_values for p in ['riddle', 'magical']))

    def test_generate_theme_challenges(self):
        """Test theme-appropriate challenge generation."""
        challenges = self.generator._generate_theme_challenges(DungeonTheme.VOLCANIC_FORTRESS)
        self.assertGreaterEqual(len(challenges), 1)
        self.assertLessEqual(len(challenges), 3)

        # Should generate valid challenges
        challenge_values = [c.value for c in challenges]
        valid_challenges = ['darkness', 'poison', 'fire', 'ice', 'electricity', 'wind', 'gravity', 'time_warp']
        for challenge in challenge_values:
            self.assertIn(challenge, valid_challenges)

    def test_generate_room_layouts(self):
        """Test different room layout generations."""
        layout_types = list(LayoutType)

        for layout_type in layout_types:
            with self.subTest(layout=layout_type):
                rooms = self.generator._generate_room_layout(
                    "test_dungeon", 10, layout_type, DungeonTheme.ANCIENT_TEMPLE
                )
                self.assertGreater(len(rooms), 0)

                # Check that entrance is included
                entrance_id = "test_dungeon_entrance"
                self.assertIn(entrance_id, rooms)

    def test_connect_rooms_linear(self):
        """Test linear room connections."""
        rooms = {
            "entrance": Room("entrance", RoomType.ENTRANCE, 0, 0),
            "room1": Room("room1", RoomType.CHAMBER, 1, 0),
            "room2": Room("room2", RoomType.CHAMBER, 2, 0),
        }

        self.generator._connect_rooms(rooms, LayoutType.LINEAR)

        # Check connections
        self.assertIn("room1", rooms["entrance"].connections)
        self.assertIn("entrance", rooms["room1"].connections)
        self.assertIn("room2", rooms["room1"].connections)
        self.assertIn("room1", rooms["room2"].connections)

    def test_connect_rooms_circular(self):
        """Test circular room connections."""
        rooms = {
            "room1": Room("room1", RoomType.CHAMBER, 0, 0),
            "room2": Room("room2", RoomType.CHAMBER, 1, 0),
            "room3": Room("room3", RoomType.CHAMBER, 2, 0),
        }

        self.generator._connect_rooms(rooms, LayoutType.CIRCULAR)

        # Check circular connections
        for room_id, room in rooms.items():
            self.assertGreaterEqual(len(room.connections), 2)


class TestRewardSystem(unittest.TestCase):
    """Test RewardSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.reward_system = RewardSystem()

    def test_system_initialization(self):
        """Test reward system initialization."""
        self.assertIn(RewardTier.COMMON, self.reward_system.reward_values)
        self.assertIn(RewardTier.LEGENDARY, self.reward_system.reward_values)

    def test_generate_reward(self):
        """Test reward generation."""
        reward = self.reward_system.generate_reward(depth=5, dungeon_level=10)

        self.assertIn('tier', reward)
        self.assertIn('type', reward)
        self.assertIn('value', reward)
        self.assertIn('rarity', reward)
        self.assertGreater(reward['value'], 0)

    def test_generate_progressive_rewards(self):
        """Test progressive reward generation."""
        rewards = self.reward_system.generate_progressive_rewards(max_depth=20, dungeon_level=15)

        self.assertGreater(len(rewards), 0)

        # Check that rewards increase in value
        values = [r['value'] for r in rewards]
        self.assertEqual(values, sorted(values))  # Should be non-decreasing

    def test_reward_value_ranges(self):
        """Test reward value ranges by tier."""
        for tier in RewardTier:
            min_val, max_val = self.reward_system.reward_values[tier]
            self.assertGreater(min_val, 0)
            self.assertGreater(max_val, min_val)


class TestDungeonSystem(unittest.TestCase):
    """Test main DungeonSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = DungeonSystem()

    def test_system_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.system.repository)
        self.assertIsNotNone(self.system.generation_service)
        self.assertIsNotNone(self.system.exploration_service)
        self.assertIsNotNone(self.system.reward_system)

    def test_initialize_dungeons(self):
        """Test dungeon initialization."""
        self.system.initialize_dungeons()
        self.assertEqual(len(self.system.repository.get_all()), 50)

    def test_get_dungeon_list(self):
        """Test getting dungeon list."""
        self.system.initialize_dungeons()
        dungeon_list = self.system.get_dungeon_list()

        self.assertEqual(len(dungeon_list), 50)
        for dungeon_info in dungeon_list:
            self.assertIn('id', dungeon_info)
            self.assertIn('name', dungeon_info)
            self.assertIn('theme', dungeon_info)

    def test_enter_dungeon(self):
        """Test entering a dungeon."""
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id
        result = self.system.enter_dungeon(dungeon_id, 15)

        self.assertIn('dungeon_id', result)
        self.assertEqual(result['dungeon_id'], dungeon_id)
        self.assertIn('theme', result)
        self.assertIn('puzzles', result)
        self.assertIn('environmental_challenges', result)

    def test_enter_nonexistent_dungeon(self):
        """Test entering non-existent dungeon."""
        result = self.system.enter_dungeon("nonexistent", 10)
        self.assertIn('error', result)

    def test_explore_dungeon(self):
        """Test dungeon exploration."""
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id
        self.system.enter_dungeon(dungeon_id, 10)

        actions = ['explore_room', 'make_strategic_choice', 'face_challenge']
        result = self.system.explore_dungeon(dungeon_id, actions)

        self.assertIn('rooms_explored', result)
        self.assertIn('strategic_decisions', result)
        self.assertIn('discoveries', result)

    def test_navigate_dungeon(self):
        """Test dungeon navigation."""
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id
        self.system.enter_dungeon(dungeon_id, 10)

        result = self.system.navigate_dungeon(dungeon_id, depth=15)

        self.assertIn('depth_reached', result)
        self.assertIn('difficulty_curve', result)
        self.assertIn('rewards_found', result)
        self.assertIn('progress_percentage', result)

    def test_get_dungeon_themes(self):
        """Test getting all dungeon themes."""
        self.system.initialize_dungeons()
        themes = self.system.get_dungeon_themes()
        self.assertEqual(len(themes), 50)

    def test_get_theme_coverage(self):
        """Test theme coverage analysis."""
        self.system.initialize_dungeons()
        coverage = self.system.get_theme_coverage()

        self.assertIn('elemental', coverage)
        self.assertIn('location', coverage)
        self.assertIn('alignment', coverage)
        self.assertIn('conceptual', coverage)

    def test_end_dungeon_exploration(self):
        """Test ending dungeon exploration."""
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id
        self.system.enter_dungeon(dungeon_id, 10)

        result = self.system.end_dungeon_exploration(dungeon_id)
        self.assertIn('dungeon_id', result)
        self.assertIn('rooms_explored', result)
        self.assertIn('exploration_percentage', result)


class TestSystemIntegration(unittest.TestCase):
    """Test integration between system components."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = create_dungeon_system()

    def test_full_exploration_workflow(self):
        """Test complete dungeon exploration workflow."""
        # Initialize dungeons
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id

        # Enter dungeon
        entry_result = self.system.enter_dungeon(dungeon_id, 20)
        self.assertNotIn('error', entry_result)

        # Explore
        explore_result = self.system.explore_dungeon(dungeon_id, [
            'explore_room', 'explore_room', 'make_strategic_choice'
        ])
        self.assertGreater(explore_result['rooms_explored'], 0)

        # Navigate
        nav_result = self.system.navigate_dungeon(dungeon_id, depth=20)
        self.assertGreater(nav_result['depth_reached'], 0)
        self.assertGreater(len(nav_result['rewards_found']), 0)

        # End exploration
        end_result = self.system.end_dungeon_exploration(dungeon_id)
        self.assertIn('exploration_percentage', end_result)

    def test_theme_puzzle_consistency(self):
        """Test that themes have appropriate puzzles."""
        self.system.initialize_dungeons()

        # Test ancient temple has appropriate puzzles
        ancient_temple = None
        for dungeon in self.system.repository.get_all():
            if dungeon.theme == DungeonTheme.ANCIENT_TEMPLE:
                ancient_temple = dungeon
                break

        self.assertIsNotNone(ancient_temple)
        puzzle_values = [p.value for p in ancient_temple.puzzles]

        # Should have riddle or magical puzzle
        self.assertTrue(
            any(p in puzzle_values for p in ['riddle', 'magical']),
            f"Ancient temple should have riddle or magical puzzles, got: {puzzle_values}"
        )

    def test_difficulty_progression(self):
        """Test difficulty progression mechanics."""
        session = ExplorationSession(
            dungeon=Mock(secrets=5, rooms={}),
            player_level=10
        )

        # Test difficulty increases with depth
        depth_0 = session.calculate_difficulty_multiplier(0)
        depth_10 = session.calculate_difficulty_multiplier(10)
        depth_20 = session.calculate_difficulty_multiplier(20)

        self.assertEqual(depth_0, 1.0)
        self.assertGreater(depth_10, depth_0)
        self.assertGreater(depth_20, depth_10)

    def test_reward_scaling(self):
        """Test reward scaling with depth and level."""
        low_reward = self.system.reward_system.generate_reward(5, 10)
        high_reward = self.system.reward_system.generate_reward(25, 50)

        # Higher depth and level should give better rewards
        self.assertGreaterEqual(high_reward['value'], low_reward['value'])

    def test_distinct_themes(self):
        """Test that all dungeons have distinct themes."""
        self.system.initialize_dungeons()
        themes = [d.theme for d in self.system.repository.get_all()]
        unique_themes = set(themes)

        self.assertEqual(len(themes), 50)
        self.assertEqual(len(unique_themes), 50)


class TestGlobalFunctions(unittest.TestCase):
    """Test global functions."""

    def test_get_dungeon_system(self):
        """Test global dungeon system getter."""
        system1 = get_dungeon_system()
        system2 = get_dungeon_system()
        self.assertIs(system1, system2)  # Should return same instance

    def test_create_dungeon_system(self):
        """Test global dungeon system creator."""
        system1 = create_dungeon_system()
        system2 = create_dungeon_system()
        self.assertIsNot(system1, system2)  # Should return different instances


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = DungeonSystem()

    def test_enter_nonexistent_dungeon(self):
        """Test entering non-existent dungeon."""
        result = self.system.enter_dungeon("invalid_id", 10)
        self.assertIn('error', result)

    def test_explore_without_session(self):
        """Test exploring without active session."""
        result = self.system.explore_dungeon("invalid_id", [])
        self.assertIn('error', result)

    def test_navigate_without_session(self):
        """Test navigating without active session."""
        result = self.system.navigate_dungeon("invalid_id")
        self.assertIn('error', result)

    def test_end_without_session(self):
        """Test ending exploration without active session."""
        result = self.system.end_dungeon_exploration("invalid_id")
        self.assertEqual(result, {'error': 'Session not found'})

    def test_empty_dungeon_list(self):
        """Test getting dungeon list without initialization."""
        dungeon_list = self.system.get_dungeon_list()
        self.assertEqual(dungeon_list, [])

    def test_zero_exploration_actions(self):
        """Test exploration with no actions."""
        self.system.initialize_dungeons()
        dungeons = self.system.repository.get_all()
        dungeon_id = dungeons[0].id
        self.system.enter_dungeon(dungeon_id, 10)

        result = self.system.explore_dungeon(dungeon_id, [])
        self.assertEqual(result['rooms_explored'], 0)
        self.assertEqual(result['strategic_decisions'], 0)


if __name__ == '__main__':
    unittest.main()
