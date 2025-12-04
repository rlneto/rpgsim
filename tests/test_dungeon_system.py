"""
Unit tests for Dungeon Exploration System.

Tests dungeon generation, themes, layouts, puzzles, environmental challenges,
secrets, progression, rewards, and strategic decision-making.
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.systems.dungeon.domain import (
    Dungeon, DungeonTheme, LayoutType,
    Room, RoomType, PuzzleType, EnvironmentalChallenge, LoreType, RewardTier,
    Treasure, Trap, TrapType
)
from core.systems.dungeon.services import (
    DungeonGenerationService,
    DungeonExplorationService,
    RewardService
)
from core.systems.dungeon.repositories import MemoryDungeonRepository
from core.systems.dungeon.facade import DungeonSystem, get_dungeon_system, create_dungeon_system


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
            treasures=[Treasure(id="t1", name="Gold", tier=RewardTier.COMMON, value=10)],
            traps=[Trap(id="tr1", type=TrapType.MECHANICAL, description="Dart trap")],
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
        self.assertEqual(len(result['treasures']), 1)
        self.assertEqual(len(result['traps']), 1)
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

    def test_get_entrance(self):
        """Test getting entrance room."""
        entrance = self.dungeon.get_entrance()
        self.assertIsNotNone(entrance)
        self.assertEqual(entrance.type.value, "entrance")

    def test_get_boss_room(self):
        """Test getting boss room."""
        boss_room = self.dungeon.get_boss_room()
        self.assertIsNotNone(boss_room)
        self.assertEqual(boss_room.type.value, "boss_room")


class TestDungeonExplorationService(unittest.TestCase):
    """Test DungeonExplorationService functionality."""

    def setUp(self):
        """Set up test fixtures."""
        rooms = {
            "entrance": Room("entrance", RoomType.ENTRANCE, 0, 0),
            "chamber1": Room("chamber1", RoomType.CHAMBER, 1, 0, puzzle=PuzzleType.MECHANICAL, secrets=["secret1"]),
        }
        rooms["entrance"].add_connection("chamber1")
        dungeon = Dungeon(id="test_dungeon", name="Test Dungeon", theme=DungeonTheme.ANCIENT_TEMPLE, level=10, rooms=rooms, layout=LayoutType.LINEAR, puzzles=[], environmental_challenges=[], secrets=5, hidden_areas=3, lore_elements=10)
        self.service = DungeonExplorationService(dungeon=dungeon)

    def test_explore_room(self):
        """Test room exploration in session."""
        discovery = self.service.explore_room("chamber1")
        self.assertEqual(self.service.current_room_id, "chamber1")
        self.assertTrue(self.service.dungeon.get_room("chamber1").explored)
        self.assertIn("room_id", discovery)


class TestRewardService(unittest.TestCase):
    """Test RewardService functionality."""

    def setUp(self):
        self.service = RewardService()

    def test_generate_treasure(self):
        treasure = self.service.generate_treasure(1)
        self.assertIsInstance(treasure, Treasure)
        self.assertEqual(treasure.tier, RewardTier.COMMON)

        treasure = self.service.generate_treasure(25)
        self.assertEqual(treasure.tier, RewardTier.LEGENDARY)


class TestDungeonGenerationService(unittest.TestCase):
    """Test DungeonGenerationService functionality."""

    def setUp(self):
        self.service = DungeonGenerationService()

    def test_generate_dungeon_with_treasure(self):
        """Test that treasure rooms contain treasure."""
        dungeon = self.service.generate_dungeon(DungeonTheme.ANCIENT_TEMPLE, player_level=15)
        treasure_room_found = False
        for room in dungeon.rooms.values():
            if room.type == RoomType.TREASURE_ROOM:
                self.assertGreater(len(room.treasures), 0)
                treasure_room_found = True
        if not treasure_room_found:
            print("Warning: No treasure room generated in test dungeon.")

    def test_generate_dungeon_with_traps(self):
        """Test that trap rooms contain traps."""
        dungeon = self.service.generate_dungeon(DungeonTheme.ANCIENT_TEMPLE, player_level=15)
        trap_room_found = False
        for room in dungeon.rooms.values():
            if room.type == RoomType.TRAP_ROOM:
                self.assertGreater(len(room.traps), 0)
                trap_room_found = True
        if not trap_room_found:
            print("Warning: No trap room generated in test dungeon.")


class TestDungeonSystem(unittest.TestCase):
    """Test main DungeonSystem functionality."""

    def setUp(self):
        self.system = DungeonSystem()
        self.system.initialize_dungeons(1)
        self.dungeon_id = self.system.repository.list()[0].id

    def test_get_dungeon_themes(self):
        themes = self.system.get_dungeon_themes()
        self.assertIsInstance(themes, list)
        self.assertGreater(len(themes), 0)

    def test_get_theme_coverage(self):
        coverage = self.system.get_theme_coverage()
        self.assertIsInstance(coverage, dict)
        self.assertIn('elemental', coverage)


class TestSystemIntegration(unittest.TestCase):
    """Test integration between system components."""

    def setUp(self):
        self.system = create_dungeon_system()
        self.system.initialize_dungeons(50)

    def test_full_exploration_workflow(self):
        """Test complete dungeon exploration workflow."""
        dungeon = self.system.repository.list()[0]
        dungeon_id = dungeon.id
        entry_result = self.system.enter_dungeon(dungeon_id)
        self.assertNotIn('error', entry_result)
        room_to_explore = dungeon.get_entrance()
        self.assertIsNotNone(room_to_explore)
        explore_result = self.system.explore_dungeon(dungeon_id, room_to_explore.id)
        self.assertNotIn('error', explore_result)
        self.assertTrue(dungeon.get_room(room_to_explore.id).explored)
        end_result = self.system.end_dungeon_exploration(dungeon_id)
        self.assertIn('status', end_result)


if __name__ == '__main__':
    unittest.main()
