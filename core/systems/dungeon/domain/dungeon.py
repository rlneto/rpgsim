"""
Dungeon system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum
import random
from datetime import datetime


class DungeonTheme(Enum):
    """Themes for dungeons"""
    ANCIENT_TEMPLE = "ancient_temple"
    VOLCANIC_FORTRESS = "volcanic_fortress"
    FROZEN_WASTELAND = "frozen_wasteland"
    SUNKEN_CITY = "sunken_city"
    FLOATING_ISLAND = "floating_island"
    CRYSTAL_CAVERN = "crystal_cavern"
    NECROPOLIS = "necropolis"
    ABANDONED_MINE = "abandoned_mine"
    VERDANT_LABYRINTH = "verdant_labyrinth"
    CLOCKWORK_TOWER = "clockwork_tower"
    SHADOW_REALM = "shadow_realm"
    CELESTIAL_PALACE = "celestial_palace"
    UNDERGROUND_JUNGLE = "underground_jungle"
    HAUNTED_MANSION = "haunted_mansion"
    ARCANE_LIBRARY = "arcane_library"
    DESERT_TOMB = "desert_tomb"
    FUNGAL_GROTTO = "fungal_grotto"
    OBSIDIAN_SPIRE = "obsidian_spire"
    CORAL_REEF = "coral_reef"
    STEAM_WORKS = "steam_works"
    PRISMATIC_PRISON = "prismatic_prison"
    VOID_EXPANSE = "void_expanse"
    DRAGON_LAIR = "dragon_lair"
    GOBLIN_WARREN = "goblin_warren"
    ELVEN_RUINS = "elven_ruins"
    DWARVEN_STRONGHOLD = "dwarven_stronghold"
    WIZARD_TOWER = "wizard_tower"
    BEAST_DEN = "beast_den"
    SWAMP_OF_SORROWS = "swamp_of_sorrows"
    THUNDER_PEAK = "thunder_peak"
    MIRROR_HALLS = "mirror_halls"
    SANDSTONE_CANYON = "sandstone_canyon"
    ICE_PALACE = "ice_palace"
    LAVA_TUBES = "lava_tubes"
    ANCIENT_SEWERS = "ancient_sewers"
    CATACOMBS = "catacombs"
    CRYPT = "crypt"
    MAUSOLEUM = "mausoleum"
    GRAVEYARD = "graveyard"
    DUNGEON = "dungeon"
    CELLAR = "cellar"
    CAVE = "cave"
    GROTTO = "grotto"
    CAVERN = "cavern"
    MINE = "mine"
    TUNNEL = "tunnel"
    PASSAGE = "passage"
    MAZE = "maze"
    HALL = "hall"
    CHAMBER = "chamber"


class LayoutType(Enum):
    """Layout types for dungeon generation"""
    LINEAR = "linear"
    BRANCHING = "branching"
    CIRCULAR = "circular"
    MAZE = "maze"
    SPIRAL = "spiral"
    MULTILEVEL = "multilevel"


class PuzzleType(Enum):
    """Types of puzzles encountered"""
    MECHANICAL = "mechanical"
    MAGICAL = "magical"
    LOGICAL = "logical"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"
    PATTERN = "pattern"
    RIDDLE = "riddle"
    ENVIRONMENTAL = "environmental"


class EnvironmentalChallenge(Enum):
    """Environmental hazards"""
    DARKNESS = "darkness"
    POISON = "poison"
    FIRE = "fire"
    ICE = "ice"
    ELECTRICITY = "electricity"
    WIND = "wind"
    GRAVITY = "gravity"
    TIME_WARP = "time_warp"


class RewardTier(Enum):
    """Tiers of rewards"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class RoomType(Enum):
    """Types of rooms"""
    ENTRANCE = "entrance"
    CHAMBER = "chamber"
    CORRIDOR = "corridor"
    BOSS_ROOM = "boss_room"
    TREASURE_ROOM = "treasure_room"
    PUZZLE_ROOM = "puzzle_room"
    TRAP_ROOM = "trap_room"
    SHRINE = "shrine"
    SHOP = "shop"
    REST_AREA = "rest_area"


class StrategicDecisionType(Enum):
    """Types of strategic decisions"""
    PATH_CHOICE = "path_choice"
    RESOURCE_USE = "resource_use"
    COMBAT_TACTIC = "combat_tactic"
    PUZZLE_APPROACH = "puzzle_approach"
    RISK_ASSESSMENT = "risk_assessment"


class LoreType(Enum):
    """Types of lore elements"""
    INSCRIPTIONS = "inscriptions"
    BOOKS = "books"
    SCROLLS = "scrolls"
    MURALS = "murals"
    STATUES = "statues"
    GHOSTS = "ghosts"
    ARTIFACTS = "artifacts"


@dataclass
class DungeonRoom:
    """A room within a dungeon"""
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
        """Add a connection to another room"""
        if room_id not in self.connections:
            self.connections.append(room_id)

    def explore(self) -> Dict[str, Any]:
        """Explore the room and return contents"""
        if self.explored:
            return {}

        self.explored = True
        return {
            'room_id': self.id,
            'type': self.type.value if hasattr(self.type, 'value') else str(self.type),
            'contents': self.contents,
            'secrets': self.secrets,
            'challenge': self.challenge.value if self.challenge else None,
            'puzzle': self.puzzle.value if self.puzzle else None,
            'lore': self.lore.value if self.lore else None
        }


@dataclass
class Dungeon:
    """A complete dungeon instance"""
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

    def get_room(self, room_id: str) -> Optional[DungeonRoom]:
        """Get a room by ID"""
        return self.rooms.get(room_id)

    def get_entrance(self) -> Optional[DungeonRoom]:
        """Get the entrance room"""
        for room in self.rooms.values():
            if room.type == RoomType.ENTRANCE:
                return room
        return None

    def get_boss_room(self) -> Optional[DungeonRoom]:
        """Get the boss room"""
        for room in self.rooms.values():
            if room.type == RoomType.BOSS_ROOM:
                return room
        return None

    def get_explored_percentage(self) -> float:
        """Calculate percentage of explored rooms"""
        if not self.rooms:
            return 0.0
        explored_count = sum(1 for room in self.rooms.values() if room.explored)
        return (explored_count / len(self.rooms)) * 100.0


class ExplorationSession:
    """Active exploration session"""
    def __init__(self, dungeon: Dungeon, player_level: int):
        self.dungeon = dungeon
        self.player_level = player_level
        self.rooms_explored = 0
        self.puzzles_solved = 0
        self.secrets_found = 0
        self.strategic_decisions_made = 0
        self.rewards_found: List[Dict[str, Any]] = []
        self.discoveries: List[Dict[str, Any]] = []
        self.current_room_id: Optional[str] = None

        # Initialize current room to entrance
        entrance = dungeon.get_entrance()
        if entrance:
            self.current_room_id = entrance.id

    def explore_room(self, room: DungeonRoom) -> Dict[str, Any]:
        """Process room exploration"""
        result = room.explore()
        if result:
            self.rooms_explored += 1
            if room.puzzle:
                self.puzzles_solved += 1
            if room.secrets:
                self.secrets_found += 1

            self.discoveries.append(result)
            self.current_room_id = room.id

        return result

    def make_strategic_decision(self, decision_type: StrategicDecisionType) -> None:
        """Record a strategic decision"""
        self.strategic_decisions_made += 1

    def add_reward(self, reward: Dict[str, Any]) -> None:
        """Add a found reward"""
        self.rewards_found.append(reward)

    def calculate_difficulty_multiplier(self, depth: int) -> float:
        """Calculate difficulty multiplier based on depth and level"""
        # Base multiplier starts at 1.0 and increases with depth
        depth_factor = 1.0 + (depth * 0.1)

        # Level scaling (simplified)
        level_factor = 1.0

        return depth_factor * level_factor
