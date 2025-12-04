"""
Dungeon system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from .room import Room, PuzzleType, EnvironmentalChallenge


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


@dataclass
class Dungeon:
    """A complete dungeon instance"""
    id: str
    name: str
    theme: DungeonTheme
    level: int
    rooms: Dict[str, Room]
    layout: LayoutType
    puzzles: List[PuzzleType]
    environmental_challenges: List[EnvironmentalChallenge]
    secrets: int
    hidden_areas: int
    lore_elements: int

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by ID"""
        return self.rooms.get(room_id)

    def get_entrance(self) -> Optional[Room]:
        """Get the entrance room"""
        for room in self.rooms.values():
            if room.type.value == "entrance":
                return room
        return None

    def get_boss_room(self) -> Optional[Room]:
        """Get the boss room"""
        for room in self.rooms.values():
            if room.type.value == "boss_room":
                return room
        return None

    def get_explored_percentage(self) -> float:
        """Calculate percentage of explored rooms"""
        if not self.rooms:
            return 0.0
        explored_count = sum(1 for room in self.rooms.values() if room.explored)
        return (explored_count / len(self.rooms)) * 100.0
