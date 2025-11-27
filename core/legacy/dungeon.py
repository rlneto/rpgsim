"""
Dungeon Exploration System - Procedural dungeon generation and exploration mechanics.

Manages dungeon generation, themes, layouts, puzzles, environmental challenges,
secrets, progression, rewards, and strategic decision-making.

Complexity: Very High
Dependencies: Combat, Equipment, Quest, Travel, World Systems
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field


# Core Enums
class DungeonTheme(Enum):
    """Dungeon theme types."""
    ANCIENT_TEMPLE = "ancient_temple"
    CRYSTAL_CAVES = "crystal_caves"
    VOLCANIC_FORTRESS = "volcanic_fortress"
    FLOODED_CATACOMBS = "flooded_catacombs"
    ENCHANTED_FOREST = "enchanted_forest"
    ABANDONED_MINE = "abandoned_mine"
    ICE_PALACE = "ice_palace"
    SHADOW_REALM = "shadow_realm"
    DESERT_PYRAMID = "desert_pyramid"
    SKY_CASTLE = "sky_castle"
    UNDERGROUND_SEA = "underground_sea"
    CURSED_MANOR = "cursed_manor"
    GOBLIN_WARRENS = "goblin_warrens"
    DRAGON_LAIR = "dragon_lair"
    CLOCKWORK_CITY = "clockwork_city"
    POISON_SWAMP = "poison_swamp"
    FROZEN_WASTES = "frozen_wastes"
    FORBIDDEN_LIBRARY = "forbidden_library"
    ELEMENTAL_PLANE = "elemental_plane"
    DWARVEN_STRONGHOLD = "dwarven_stronghold"
    ELVEN_SANCTUARY = "elven_sanctuary"
    DEMON_INFESTED_KEEP = "demon_infested_keep"
    ANGELIC_SPIRE = "angelic_spire"
    TIME_DISTORTED_RUINS = "time_distorted_ruins"
    ILLUSION_MAZE = "illusion_maze"
    BONE_CHURCH = "bone_church"
    MUSHROOM_CAVERNS = "mushroom_caverns"
    MAGNETIC_MINES = "magnetic_mines"
    ECHOING_CHASM = "echoing_chasm"
    FLOATING_ISLANDS = "floating_islands"
    SOUL_PRISON = "soul_prison"
    DREAMSCAPE_NEXUS = "dreamscape_nexus"
    BLOOD_ARENA = "blood_arena"
    ASTRAL_OBSERVATORY = "astral_observatory"
    RUST_WASTELANDS = "rust_wastelands"
    CRYSTALLINE_LABYRINTH = "crystalline_labyrinth"
    WIND_CARVED_CANYONS = "wind_carved_canyons"
    MIRAGE_DESERT = "mirage_desert"
    SUNKEN_PALACE = "sunken_palace"
    STORM_CHAMBER = "storm_chamber"
    WEB_FILLED_LAIRS = "web_filled_lairs"
    LIQUID_METAL_VATS = "liquid_metal_vats"
    INVERTED_CATHEDRAL = "inverted_cathedral"
    LIVING_FOREST = "living_forest"
    QUANTUM_REACTOR = "quantum_reactor"
    MEMORY_PALACE = "memory_palace"
    NIGHTMARE_FUEL = "nightmare_fuel"
    HARMONY_GARDENS = "harmony_gardens"
    DISCORDANT_PLANES = "discordant_planes"
    ORDERED_STRUCTURES = "ordered_structures"


class LayoutType(Enum):
    """Dungeon layout patterns."""
    LINEAR = "linear"
    BRANCHING = "branching"
    CIRCULAR = "circular"
    MAZE = "maze"
    SPIRAL = "spiral"
    MULTILEVEL = "multilevel"


class PuzzleType(Enum):
    """Puzzle types found in dungeons."""
    MECHANICAL = "mechanical"
    MAGICAL = "magical"
    LOGICAL = "logical"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"
    PATTERN = "pattern"
    RIDDLE = "riddle"
    ENVIRONMENTAL = "environmental"


class EnvironmentalChallenge(Enum):
    """Environmental hazard types."""
    DARKNESS = "darkness"
    POISON = "poison"
    FIRE = "fire"
    ICE = "ice"
    ELECTRICITY = "electricity"
    WIND = "wind"
    GRAVITY = "gravity"
    TIME_WARP = "time_warp"


class RewardTier(Enum):
    """Reward quality tiers."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class RoomType(Enum):
    """Room types in dungeons."""
    ENTRANCE = "entrance"
    CHAMBER = "chamber"
    CORRIDOR = "corridor"
    PUZZLE_ROOM = "puzzle_room"
    TRAP_ROOM = "trap_room"
    TREASURE_ROOM = "treasure_room"
    BOSS_ROOM = "boss_room"
    SECRET_ROOM = "secret_room"
    LORE_ROOM = "lore_room"
    REST_AREA = "rest_area"


class StrategicDecisionType(Enum):
    """Types of strategic decisions players make."""
    PATH_CHOICE = "path_choice"
    RESOURCE_MANAGEMENT = "resource_management"
    RISK_ASSESSMENT = "risk_assessment"
    PUZZLE_APPROACH = "puzzle_approach"
    COMBAT_TACTICS = "combat_tactics"
    EXPLORATION_PRIORITY = "exploration_priority"


class LoreType(Enum):
    """Types of lore found in dungeons."""
    HISTORICAL_RECORDS = "historical_records"
    INSCRIPTIONS = "inscriptions"
    ENVIRONMENTAL_STORYTELLING = "environmental_storytelling"
    ITEM_DESCRIPTIONS = "item_descriptions"
    BACKGROUNDS = "boss_backgrounds"
    ARCHITECTURAL_CLUES = "architectural_clues"


# Core Data Classes
@dataclass
class DungeonRoom:
    """Individual room within a dungeon."""
    id: str
    type: RoomType
    x: int
    y: int
    connections: List[str] = field(default_factory=list)
    contents: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    challenge: Optional[EnvironmentalChallenge] = None
    puzzle: Optional[PuzzleType] = None
    lore: Optional[LoreType] = None
    explored: bool = False

    def add_connection(self, room_id: str) -> None:
        """Add connection to another room."""
        if room_id not in self.connections:
            self.connections.append(room_id)

    def explore(self) -> Dict[str, Any]:
        """Explore this room and return discoveries."""
        if self.explored:
            return {}

        self.explored = True
        return {
            'room_id': self.id,
            'type': self.type.value,
            'contents': self.contents.copy(),
            'secrets': self.secrets.copy(),
            'challenge': self.challenge.value if self.challenge else None,
            'puzzle': self.puzzle.value if self.puzzle else None,
            'lore': self.lore.value if self.lore else None
        }


@dataclass
class Dungeon:
    """Complete dungeon definition."""
    id: str
    name: str
    theme: DungeonTheme
    level: int
    rooms: Dict[str, DungeonRoom]
    layout: LayoutType
    puzzles: List[PuzzleType]
    environmental_challenges: List[EnvironmentalChallenge]
    secrets: int
    hidden_areas: int
    lore_elements: int
    difficulty_progression: str = "increasing"
    reward_tiers: List[RewardTier] = field(default_factory=lambda: list(RewardTier))

    def get_room(self, room_id: str) -> Optional[DungeonRoom]:
        """Get room by ID."""
        return self.rooms.get(room_id)

    def get_entrance(self) -> Optional[DungeonRoom]:
        """Get dungeon entrance room."""
        for room in self.rooms.values():
            if room.type == RoomType.ENTRANCE:
                return room
        return None

    def get_boss_room(self) -> Optional[DungeonRoom]:
        """Get boss room."""
        for room in self.rooms.values():
            if room.type == RoomType.BOSS_ROOM:
                return room
        return None

    def get_explored_percentage(self) -> float:
        """Calculate percentage of rooms explored."""
        if not self.rooms:
            return 0.0
        explored_count = sum(1 for room in self.rooms.values() if room.explored)
        return (explored_count / len(self.rooms)) * 100


@dataclass
class ExplorationSession:
    """Current dungeon exploration session."""
    dungeon: Dungeon
    player_level: int
    rooms_explored: int = 0
    puzzles_solved: int = 0
    secrets_found: int = 0
    hidden_areas_discovered: int = 0
    lore_pieces_found: int = 0
    strategic_decisions_made: int = 0
    current_room: Optional[str] = None
    depth_reached: int = 0
    bosses_defeated: int = 0
    time_spent: int = 0  # minutes
    resources_used: Dict[str, int] = field(default_factory=dict)
    discoveries: List[Dict[str, Any]] = field(default_factory=list)
    rewards_found: List[Dict[str, Any]] = field(default_factory=list)

    def explore_room(self, room: DungeonRoom) -> Dict[str, Any]:
        """Explore a room and record discoveries."""
        if room.explored:
            return {}

        self.rooms_explored += 1
        discovery = room.explore()
        self.discoveries.append(discovery)

        # Track specific discoveries
        if room.puzzle:
            self.puzzles_solved += 1
        if room.secrets:
            self.secrets_found += len(room.secrets)
        if room.lore:
            self.lore_pieces_found += 1

        return discovery

    def make_strategic_decision(self, _decision_type: StrategicDecisionType) -> None:
        """Record a strategic decision made by the player."""
        self.strategic_decisions_made += 1

    def add_reward(self, reward: Dict[str, Any]) -> None:
        """Add a reward found during exploration."""
        self.rewards_found.append(reward)

    def calculate_difficulty_multiplier(self, depth: int) -> float:
        """Calculate difficulty multiplier based on depth."""
        base_multiplier = 1.0
        depth_bonus = (depth / 10) * 0.3  # 30% increase per 10 depth
        return base_multiplier + depth_bonus


# Dungeon Generator
class DungeonGenerator:
    """Generates random dungeons with various themes and layouts."""

    def __init__(self):
        self.theme_puzzle_mapping = {
            DungeonTheme.ANCIENT_TEMPLE: [PuzzleType.RIDDLE, PuzzleType.MAGICAL, PuzzleType.LOGICAL],
            DungeonTheme.CRYSTAL_CAVES: [PuzzleType.SPATIAL, PuzzleType.PATTERN, PuzzleType.ENVIRONMENTAL],
            DungeonTheme.VOLCANIC_FORTRESS: [PuzzleType.MECHANICAL, PuzzleType.ENVIRONMENTAL],
            DungeonTheme.FLOODED_CATACOMBS: [PuzzleType.ENVIRONMENTAL, PuzzleType.SPATIAL],
            DungeonTheme.ENCHANTED_FOREST: [PuzzleType.MAGICAL, PuzzleType.LOGICAL],
            DungeonTheme.ABANDONED_MINE: [PuzzleType.MECHANICAL, PuzzleType.ENVIRONMENTAL],
            DungeonTheme.ICE_PALACE: [PuzzleType.SPATIAL, PuzzleType.TEMPORAL],
            DungeonTheme.SHADOW_REALM: [PuzzleType.LOGICAL, PuzzleType.MAGICAL],
            DungeonTheme.DESERT_PYRAMID: [PuzzleType.RIDDLE, PuzzleType.MECHANICAL],
            DungeonTheme.SKY_CASTLE: [PuzzleType.SPATIAL, PuzzleType.MAGICAL],
            DungeonTheme.CLOCKWORK_CITY: [PuzzleType.MECHANICAL, PuzzleType.PATTERN, PuzzleType.TEMPORAL],
            DungeonTheme.FORBIDDEN_LIBRARY: [PuzzleType.RIDDLE, PuzzleType.LOGICAL, PuzzleType.MAGICAL],
            DungeonTheme.DRAGON_LAIR: [PuzzleType.ENVIRONMENTAL, PuzzleType.RIDDLE]
        }

        self.theme_challenge_mapping = {
            DungeonTheme.VOLCANIC_FORTRESS: [EnvironmentalChallenge.FIRE, EnvironmentalChallenge.POISON],
            DungeonTheme.ICE_PALACE: [EnvironmentalChallenge.ICE, EnvironmentalChallenge.WIND],
            DungeonTheme.SHADOW_REALM: [EnvironmentalChallenge.DARKNESS, EnvironmentalChallenge.TIME_WARP],
            DungeonTheme.FLOODED_CATACOMBS: [EnvironmentalChallenge.POISON, EnvironmentalChallenge.DARKNESS],
            DungeonTheme.DESERT_PYRAMID: [EnvironmentalChallenge.FIRE, EnvironmentalChallenge.GRAVITY],
            DungeonTheme.SKY_CASTLE: [EnvironmentalChallenge.WIND, EnvironmentalChallenge.GRAVITY],
            DungeonTheme.STORM_CHAMBER: [EnvironmentalChallenge.ELECTRICITY, EnvironmentalChallenge.WIND],
            DungeonTheme.POISON_SWAMP: [EnvironmentalChallenge.POISON, EnvironmentalChallenge.DARKNESS]
        }

    def generate_dungeon(self, dungeon_id: str, theme: DungeonTheme,
                        player_level: int) -> Dungeon:
        """Generate a complete dungeon."""
        # Generate base properties
        room_count = random.randint(10, 50)
        layout = random.choice(list(LayoutType))

        # Theme-appropriate elements
        puzzles = self._generate_theme_puzzles(theme)
        challenges = self._generate_theme_challenges(theme)

        # Generate rooms
        rooms = self._generate_room_layout(dungeon_id, room_count, layout, theme)

        # Determine secrets and lore
        secrets = random.randint(3, 15)
        hidden_areas = random.randint(2, 8)
        lore_elements = random.randint(5, 20)

        return Dungeon(
            id=dungeon_id,
            name=f"Dungeon: {theme.value.replace('_', ' ').title()}",
            theme=theme,
            level=player_level,
            rooms=rooms,
            layout=layout,
            puzzles=puzzles,
            environmental_challenges=challenges,
            secrets=secrets,
            hidden_areas=hidden_areas,
            lore_elements=lore_elements,
            reward_tiers=list(RewardTier)
        )

    def _generate_theme_puzzles(self, theme: DungeonTheme) -> List[PuzzleType]:
        """Generate theme-appropriate puzzle types."""
        theme_puzzles = self.theme_puzzle_mapping.get(theme, [])
        all_puzzles = list(PuzzleType)

        if theme_puzzles:
            # Select 2-8 puzzles, with preference for theme-appropriate ones
            puzzle_count = random.randint(2, 8)
            puzzles = []

            # Ensure at least one theme-appropriate puzzle
            if theme_puzzles and random.random() < 0.8:
                puzzles.append(random.choice(theme_puzzles))

            # Fill remaining slots with any puzzle types
            while len(puzzles) < puzzle_count:
                puzzle = random.choice(all_puzzles)
                if puzzle not in puzzles:
                    puzzles.append(puzzle)

            return puzzles

        # Random puzzles if no theme mapping
        puzzle_count = random.randint(2, 8)
        return random.sample(all_puzzles, min(puzzle_count, len(all_puzzles)))

    def _generate_theme_challenges(self, theme: DungeonTheme) -> List[EnvironmentalChallenge]:
        """Generate theme-appropriate environmental challenges."""
        theme_challenges = self.theme_challenge_mapping.get(theme, [])
        all_challenges = list(EnvironmentalChallenge)

        if theme_challenges:
            # Select 1-4 challenges, with preference for theme-appropriate ones
            challenge_count = random.randint(1, 4)
            challenges = []

            # Ensure at least one theme-appropriate challenge
            if theme_challenges and random.random() < 0.7:
                challenges.append(random.choice(theme_challenges))

            # Fill remaining slots
            while len(challenges) < challenge_count:
                challenge = random.choice(all_challenges)
                if challenge not in challenges:
                    challenges.append(challenge)

            return challenges

        # Random challenges if no theme mapping
        challenge_count = random.randint(1, 4)
        return random.sample(all_challenges, min(challenge_count, len(all_challenges)))

    def _generate_room_layout(self, dungeon_id: str, room_count: int,
                             layout: LayoutType, theme: DungeonTheme) -> Dict[str, DungeonRoom]:
        """Generate room layout based on layout type."""
        rooms = {}

        # Generate entrance room
        entrance_id = f"{dungeon_id}_entrance"
        rooms[entrance_id] = DungeonRoom(
            id=entrance_id,
            type=RoomType.ENTRANCE,
            x=0, y=0
        )

        # Generate rooms based on layout type
        if layout == LayoutType.LINEAR:
            rooms.update(self._generate_linear_layout(dungeon_id, room_count - 1))
        elif layout == LayoutType.BRANCHING:
            rooms.update(self._generate_branching_layout(dungeon_id, room_count - 1))
        elif layout == LayoutType.CIRCULAR:
            rooms.update(self._generate_circular_layout(dungeon_id, room_count - 1))
        elif layout == LayoutType.MAZE:
            rooms.update(self._generate_maze_layout(dungeon_id, room_count - 1))
        elif layout == LayoutType.SPIRAL:
            rooms.update(self._generate_spiral_layout(dungeon_id, room_count - 1))
        elif layout == LayoutType.MULTILEVEL:
            rooms.update(self._generate_multilevel_layout(dungeon_id, room_count - 1))

        # Add special rooms
        rooms.update(self._generate_special_rooms(dungeon_id, room_count, theme))

        # Connect rooms
        self._connect_rooms(rooms, layout)

        return rooms

    def _generate_linear_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate linear room layout."""
        rooms = {}
        for i in range(room_count):
            room_id = f"{dungeon_id}_{i:02d}"
            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=RoomType.CHAMBER,
                x=i + 1, y=0
            )
        return rooms

    def _generate_branching_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate branching room layout."""
        rooms = {}
        positions = set()

        # Create branching pattern
        for i in range(room_count):
            room_id = f"{dungeon_id}_{i:02d}"

            if i == 0:
                x, y = 1, 0
            elif i % 3 == 0:
                x = i // 3 + 1
                y = (i % 6) - 2
            elif i % 3 == 1:
                x = i // 3 + 1
                y = 0
            else:
                x = i // 3 + 1
                y = -(i % 6) + 2

            # Ensure unique positions
            while (x, y) in positions:
                x += 1
            positions.add((x, y))

            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=RoomType.CHAMBER,
                x=x, y=y
            )

        return rooms

    def _generate_circular_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate circular room layout."""
        rooms = {}
        radius = max(2, room_count // 6)

        for i in range(room_count):
            room_id = f"{dungeon_id}_{i:02d}"

            # Arrange in circle
            angle = (2 * 3.14159 * i) / room_count
            x = int(radius * (angle / 3.14159))
            y = int(radius * (1 - abs(angle / 3.14159 - 1) * 2))

            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=RoomType.CHAMBER,
                x=x, y=y
            )

        return rooms

    def _generate_maze_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate maze-like room layout."""
        rooms = {}
        grid_size = max(5, int(room_count ** 0.5) + 2)
        positions = []

        # Generate positions
        for i, _ in enumerate(range(room_count)):
            room_id = f"{dungeon_id}_{i:02d}"

            # Random walk positions
            if positions:
                last_x, last_y = positions[-1]
                direction = random.choice(['N', 'S', 'E', 'W'])

                if direction == 'N':
                    x, y = last_x, last_y - 1
                elif direction == 'S':
                    x, y = last_x, last_y + 1
                elif direction == 'E':
                    x, y = last_x + 1, last_y
                else:  # W
                    x, y = last_x - 1, last_y
            else:
                x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)

            positions.append((x, y))

            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=RoomType.CHAMBER,
                x=x, y=y
            )

        return rooms

    def _generate_spiral_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate spiral room layout."""
        rooms = {}
        x, y = 0, 0
        dx, dy = 1, 0

        for i in range(room_count):
            room_id = f"{dungeon_id}_{i:02d}"

            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=RoomType.CHAMBER,
                x=x, y=y
            )

            # Spiral movement
            if random.random() < 0.2:  # 20% chance to turn
                dx, dy = -dy, dx  # Turn left

            x += dx
            y += dy

        return rooms

    def _generate_multilevel_layout(self, dungeon_id: str, room_count: int) -> Dict[str, DungeonRoom]:
        """Generate multi-level room layout."""
        rooms = {}
        rooms_per_level = max(3, room_count // 3)

        for level in range(3):
            start_idx = level * rooms_per_level
            end_idx = min(start_idx + rooms_per_level, room_count)

            for i in range(start_idx, end_idx):
                room_id = f"{dungeon_id}_L{level}_{i:02d}"

                # Position based on level
                x = (i - start_idx) % 5
                y = level * 3 + (i - start_idx) // 5

                rooms[room_id] = DungeonRoom(
                    id=room_id,
                    type=RoomType.CHAMBER,
                    x=x, y=y
                )

        return rooms

    def _generate_special_rooms(self, dungeon_id: str, room_count: int,
                               _theme: DungeonTheme) -> Dict[str, DungeonRoom]:
        """Generate special rooms like boss room, treasure rooms, etc."""
        special_rooms = {}

        # Boss room
        boss_id = f"{dungeon_id}_boss"
        special_rooms[boss_id] = DungeonRoom(
            id=boss_id,
            type=RoomType.BOSS_ROOM,
            x=room_count, y=0
        )

        # Treasure rooms (1-3)
        treasure_count = random.randint(1, 3)
        for i in range(treasure_count):
            treasure_id = f"{dungeon_id}_treasure_{i}"
            special_rooms[treasure_id] = DungeonRoom(
                id=treasure_id,
                type=RoomType.TREASURE_ROOM,
                x=room_count + i + 1, y=0
            )

        # Secret rooms (1-2)
        secret_count = random.randint(1, 2)
        for i in range(secret_count):
            secret_id = f"{dungeon_id}_secret_{i}"
            special_rooms[secret_id] = DungeonRoom(
                id=secret_id,
                type=RoomType.SECRET_ROOM,
                x=room_count + treasure_count + i + 1, y=0,
                secrets=[f"secret_item_{i}", f"hidden_lore_{i}"]
            )

        return special_rooms

    def _connect_rooms(self, rooms: Dict[str, DungeonRoom], layout: LayoutType) -> None:
        """Connect rooms based on layout type."""
        room_list = list(rooms.values())

        if layout == LayoutType.LINEAR:
            # Connect rooms in sequence
            for i in range(len(room_list) - 1):
                room_list[i].add_connection(room_list[i + 1].id)
                room_list[i + 1].add_connection(room_list[i].id)

        elif layout == LayoutType.BRANCHING:
            # Create branching connections
            entrance = rooms.get(f"{room_list[0].id.split('_')[0]}_entrance")
            if entrance:
                # Connect entrance to main branches
                for i in range(1, min(4, len(room_list))):
                    entrance.add_connection(room_list[i].id)
                    room_list[i].add_connection(entrance.id)

        elif layout == LayoutType.CIRCULAR:
            # Connect in circular pattern
            for i in range(len(room_list)):
                next_i = (i + 1) % len(room_list)
                room_list[i].add_connection(room_list[next_i].id)
                room_list[next_i].add_connection(room_list[i].id)

        else:
            # Connect nearby rooms for other layouts
            for room in room_list:
                # Find 2-3 nearest rooms
                def distance_to_room(r):
                    return abs(r.x - room.x) + abs(r.y - room.y)

                nearby_rooms = sorted(
                    [r for r in room_list if r.id != room.id],
                    key=distance_to_room
                )[:3]

                for nearby in nearby_rooms:
                    if len(room.connections) < 4:  # Limit connections
                        room.add_connection(nearby.id)
                        nearby.add_connection(room.id)


# Dungeon Manager
class DungeonManager:
    """Manages multiple dungeons and exploration sessions."""

    def __init__(self):
        self.generator = DungeonGenerator()
        self.dungeons: Dict[str, Dungeon] = {}
        self.active_sessions: Dict[str, ExplorationSession] = {}
        self.themes_used: Set[DungeonTheme] = set()

    def generate_all_dungeons(self, count: int = 50) -> None:
        """Generate all dungeons with unique themes."""
        themes = list(DungeonTheme)

        for i in range(min(count, len(themes))):
            theme = themes[i]
            dungeon_id = f"dungeon_{i}"

            # Random level for each dungeon
            level = random.randint(1, 50)

            dungeon = self.generator.generate_dungeon(dungeon_id, theme, level)
            self.dungeons[dungeon_id] = dungeon
            self.themes_used.add(theme)

    def get_dungeon(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get dungeon by ID."""
        return self.dungeons.get(dungeon_id)

    def start_exploration(self, dungeon_id: str, player_level: int) -> Optional[ExplorationSession]:
        """Start exploring a dungeon."""
        dungeon = self.get_dungeon(dungeon_id)
        if not dungeon:
            return None

        session = ExplorationSession(dungeon=dungeon, player_level=player_level)
        self.active_sessions[dungeon_id] = session

        # Start at entrance
        entrance = dungeon.get_entrance()
        if entrance:
            session.current_room = entrance.id

        return session

    def get_session(self, dungeon_id: str) -> Optional[ExplorationSession]:
        """Get active exploration session."""
        return self.active_sessions.get(dungeon_id)

    def end_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End exploration and return results."""
        session = self.get_session(dungeon_id)
        if not session:
            return {}

        # Calculate final statistics
        results = {
            'dungeon_id': dungeon_id,
            'dungeon_name': session.dungeon.name,
            'theme': session.dungeon.theme.value,
            'rooms_explored': session.rooms_explored,
            'total_rooms': len(session.dungeon.rooms),
            'puzzles_solved': session.puzzles_solved,
            'secrets_found': session.secrets_found,
            'hidden_areas_discovered': session.hidden_areas_discovered,
            'lore_pieces_found': session.lore_pieces_found,
            'strategic_decisions_made': session.strategic_decisions_made,
            'depth_reached': session.depth_reached,
            'bosses_defeated': session.bosses_defeated,
            'time_spent': session.time_spent,
            'resources_used': session.resources_used,
            'rewards_found': session.rewards_found,
            'exploration_percentage': session.dungeon.get_explored_percentage()
        }

        # Clean up session
        del self.active_sessions[dungeon_id]

        return results

    def get_all_themes(self) -> List[str]:
        """Get list of all used themes."""
        return [theme.value for theme in self.themes_used]

    def get_dungeons_by_theme(self, theme: DungeonTheme) -> List[Dungeon]:
        """Get all dungeons with specific theme."""
        return [d for d in self.dungeons.values() if d.theme == theme]

    def get_dungeons_by_level_range(self, min_level: int, max_level: int) -> List[Dungeon]:
        """Get dungeons within level range."""
        return [d for d in self.dungeons.values()
                if min_level <= d.level <= max_level]


# Reward System
class RewardSystem:
    """Manages reward generation and progression."""

    def __init__(self):
        """Initialize reward system with value ranges."""
        self.reward_values = {
            RewardTier.COMMON: (50, 200),
            RewardTier.UNCOMMON: (200, 500),
            RewardTier.RARE: (500, 1000),
            RewardTier.EPIC: (1000, 2500),
            RewardTier.LEGENDARY: (2500, 10000)
        }

    def get_reward_range(self, tier: RewardTier) -> Tuple[int, int]:
        """Get value range for a specific reward tier."""
        return self.reward_values[tier]

    def generate_reward(self, depth: int, dungeon_level: int) -> Dict[str, Any]:
        """Generate reward based on depth and dungeon level."""
        # Determine reward tier
        tier_index = min(depth // 10, len(RewardTier) - 1)
        tier = list(RewardTier)[tier_index]

        # Calculate value
        min_val, max_val = self.reward_values[tier]
        base_value = random.randint(min_val, max_val)

        # Apply dungeon level multiplier
        level_multiplier = 1 + (dungeon_level / 100)
        final_value = int(base_value * level_multiplier)

        return {
            'tier': tier.value,
            'type': random.choice(['weapon', 'armor', 'accessory', 'consumable', 'material']),
            'value': final_value,
            'rarity': tier.value
        }

    def generate_progressive_rewards(self, max_depth: int, dungeon_level: int) -> List[Dict[str, Any]]:
        """Generate rewards that increase with progression."""
        rewards = []

        # Generate rewards at different depths
        reward_depths = [5, 10, 15, 20, 25]
        reward_depths = [d for d in reward_depths if d <= max_depth]

        for depth in reward_depths:
            reward = self.generate_reward(depth, dungeon_level)
            rewards.append(reward)

        # Sort rewards by value to ensure progression
        rewards.sort(key=lambda r: r['value'])

        # Add final boss reward if applicable
        if max_depth >= 25:
            boss_reward = self.generate_reward(max_depth, dungeon_level)
            boss_reward['tier'] = RewardTier.LEGENDARY.value
            boss_reward['type'] = 'weapon'
            boss_reward['value'] *= max(rewards, key=lambda r: r['value'])['value'] if rewards else 1000
            rewards.append(boss_reward)

        return rewards


# Main Dungeon System
class DungeonSystem:
    """Main interface for the Dungeon Exploration System."""

    def __init__(self):
        self.manager = DungeonManager()
        self.reward_system = RewardSystem()
        self.generator = DungeonGenerator()

    def initialize_dungeons(self) -> None:
        """Initialize all 50 dungeons with unique themes."""
        self.manager.generate_all_dungeons(50)

    def get_dungeon_list(self) -> List[Dict[str, Any]]:
        """Get list of all available dungeons."""
        return [
            {
                'id': dungeon.id,
                'name': dungeon.name,
                'theme': dungeon.theme.value,
                'level': dungeon.level,
                'room_count': len(dungeon.rooms),
                'layout': dungeon.layout.value,
                'puzzle_count': len(dungeon.puzzles),
                'challenge_count': len(dungeon.environmental_challenges),
                'secrets': dungeon.secrets,
                'hidden_areas': dungeon.hidden_areas,
                'lore_elements': dungeon.lore_elements
            }
            for dungeon in self.manager.dungeons.values()
        ]

    def enter_dungeon(self, dungeon_id: str, player_level: int) -> Dict[str, Any]:
        """Enter a dungeon for exploration."""
        session = self.manager.start_exploration(dungeon_id, player_level)
        if not session:
            return {'error': 'Dungeon not found'}

        dungeon = session.dungeon

        return {
            'dungeon_id': dungeon_id,
            'dungeon_name': dungeon.name,
            'theme': dungeon.theme.value,
            'level': dungeon.level,
            'layout': dungeon.layout.value,
            'total_rooms': len(dungeon.rooms),
            'puzzles': [p.value for p in dungeon.puzzles],
            'environmental_challenges': [c.value for c in dungeon.environmental_challenges],
            'secrets': dungeon.secrets,
            'hidden_areas': dungeon.hidden_areas,
            'lore_elements': dungeon.lore_elements,
            'reward_tiers': [t.value for t in dungeon.reward_tiers],
            'entrance_room': dungeon.get_entrance().id if dungeon.get_entrance() else None
        }

    def explore_dungeon(self, dungeon_id: str, actions: List[str]) -> Dict[str, Any]:
        """Explore a dungeon with specified actions."""
        session = self.manager.get_session(dungeon_id)
        if not session:
            return {'error': 'No active exploration session'}

        results = {
            'rooms_explored': 0,
            'puzzles_solved': 0,
            'secrets_found': 0,
            'hidden_areas_discovered': 0,
            'lore_pieces_found': 0,
            'challenges_faced': [],
            'strategic_decisions': 0,
            'layout_pattern': session.dungeon.layout.value,
            'discoveries': []
        }

        # Process exploration actions
        for action in actions:
            if action == 'explore_room':
                # Explore current room or find new room
                unexplored_rooms = [r for r in session.dungeon.rooms.values() if not r.explored]
                if unexplored_rooms:
                    room = random.choice(unexplored_rooms)
                    discovery = session.explore_room(room)

                    results['rooms_explored'] += 1
                    if room.puzzle:
                        results['puzzles_solved'] += 1
                    if room.secrets:
                        results['secrets_found'] += len(room.secrets)
                    if room.lore:
                        results['lore_pieces_found'] += 1

                    results['discoveries'].append(discovery)
                    session.depth_reached = max(session.depth_reached,
                                              abs(room.x) + abs(room.y))

            elif action == 'make_strategic_choice':
                session.make_strategic_decision(StrategicDecisionType.PATH_CHOICE)
                results['strategic_decisions'] += 1

            elif action == 'face_challenge':
                if session.dungeon.environmental_challenges:
                    challenge = random.choice(session.dungeon.environmental_challenges)
                    results['challenges_faced'].append(challenge.value)

        # Add environmental challenges from dungeon
        results['challenges_faced'].extend([c.value for c in session.dungeon.environmental_challenges])
        results['challenges_faced'] = list(set(results['challenges_faced']))  # Remove duplicates

        return results

    def navigate_dungeon(self, dungeon_id: str, depth: int = 10) -> Dict[str, Any]:
        """Navigate through dungeon with progression."""
        session = self.manager.get_session(dungeon_id)
        if not session:
            return {'error': 'No active exploration session'}

        dungeon = session.dungeon

        # Simulate navigation
        session.depth_reached = min(depth, len(dungeon.rooms) // 2)
        session.strategic_decisions_made = random.randint(5, 15)
        session.time_spent = random.randint(30, 180)

        # Generate difficulty curve
        difficulty_curve = []
        for i in range(min(5, session.depth_reached)):
            difficulty_multiplier = session.calculate_difficulty_multiplier(i * 2)
            difficulty_curve.append(difficulty_multiplier)

        # Generate rewards
        rewards = self.reward_system.generate_progressive_rewards(session.depth_reached, dungeon.level)
        session.rewards_found.extend(rewards)

        # Calculate resources used
        session.resources_used = {
            'health_potions': random.randint(0, 5),
            'mana_potions': random.randint(0, 5),
            'special_items': random.randint(0, 3)
        }

        # Calculate lore discovered
        session.lore_pieces_found = random.randint(1, min(session.depth_reached, dungeon.lore_elements))

        return {
            'depth_reached': session.depth_reached,
            'total_rooms': len(dungeon.rooms),
            'difficulty_curve': difficulty_curve,
            'rewards_found': rewards,
            'strategic_choices_made': session.strategic_decisions_made,
            'lore_discovered': session.lore_pieces_found,
            'bosses_defeated': session.bosses_defeated,
            'time_spent': session.time_spent,
            'resources_used': session.resources_used,
            'progress_percentage': (session.depth_reached / len(dungeon.rooms)) * 100
        }

    def get_dungeon_themes(self) -> List[str]:
        """Get all distinct dungeon themes."""
        return self.manager.get_all_themes()

    def get_theme_coverage(self) -> Dict[str, bool]:
        """Check which thematic categories are covered."""
        themes = [d.theme for d in self.manager.dungeons.values()]

        categories = {
            'elemental': any(theme in [
                DungeonTheme.VOLCANIC_FORTRESS, DungeonTheme.ICE_PALACE,
                DungeonTheme.STORM_CHAMBER, DungeonTheme.ELEMENTAL_PLANE
            ] for theme in themes),
            'location': any(theme in [
                DungeonTheme.ANCIENT_TEMPLE, DungeonTheme.CRYSTAL_CAVES,
                DungeonTheme.FLOODED_CATACOMBS, DungeonTheme.ENCHANTED_FOREST
            ] for theme in themes),
            'alignment': any(theme in [
                DungeonTheme.SHADOW_REALM, DungeonTheme.CURSED_MANOR,
                DungeonTheme.DEMON_INFESTED_KEEP, DungeonTheme.ANGELIC_SPIRE
            ] for theme in themes),
            'conceptual': any(theme in [
                DungeonTheme.TIME_DISTORTED_RUINS, DungeonTheme.ILLUSION_MAZE,
                DungeonTheme.DREAMSCAPE_NEXUS, DungeonTheme.QUANTUM_REACTOR
            ] for theme in themes)
        }

        return categories

    def end_dungeon_exploration(self, dungeon_id: str) -> Dict[str, Any]:
        """End dungeon exploration and return complete results."""
        return self.manager.end_exploration(dungeon_id)


# Create global instance
_dungeon_system = None

def get_dungeon_system() -> DungeonSystem:
    """Get global dungeon system instance."""
    global _dungeon_system
    if _dungeon_system is None:
        _dungeon_system = DungeonSystem()
    return _dungeon_system

def create_dungeon_system() -> DungeonSystem:
    """Create new dungeon system instance."""
    return DungeonSystem()
