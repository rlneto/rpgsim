"""
Dungeon generation services
"""
from typing import Dict, List, Any, Optional
import random
import uuid
from ..domain.dungeon import (
    Dungeon, DungeonRoom, DungeonTheme, LayoutType, PuzzleType,
    EnvironmentalChallenge, RoomType, LoreType
)


class DungeonGenerator:
    """Service for procedural dungeon generation"""

    def __init__(self):
        self.theme_puzzle_mapping = self._initialize_theme_puzzles()
        self.theme_challenge_mapping = self._initialize_theme_challenges()

    def generate_dungeon(self, dungeon_id: str, theme: DungeonTheme, player_level: int) -> Dungeon:
        """Generate a complete dungeon"""
        layout = self._select_layout(theme)
        room_count = 5 + (player_level // 2)  # Scale with level

        rooms = self._generate_room_layout(dungeon_id, room_count, layout, theme)
        self._connect_rooms(rooms, layout)

        # Add content
        puzzles = self._generate_theme_puzzles(theme)
        challenges = self._generate_theme_challenges(theme)

        return Dungeon(
            id=dungeon_id,
            name=f"{theme.value.replace('_', ' ').title()}",
            theme=theme,
            level=player_level,
            rooms=rooms,
            layout=layout,
            puzzles=puzzles,
            environmental_challenges=challenges,
            secrets=max(1, room_count // 3),
            hidden_areas=max(0, room_count // 5),
            lore_elements=max(1, room_count // 2)
        )

    def _initialize_theme_puzzles(self) -> Dict[DungeonTheme, List[PuzzleType]]:
        """Map themes to appropriate puzzles"""
        # Default mapping for all themes
        mapping = {}
        for theme in DungeonTheme:
            mapping[theme] = [PuzzleType.RIDDLE, PuzzleType.MECHANICAL]

        # Specific overrides
        mapping[DungeonTheme.ANCIENT_TEMPLE] = [PuzzleType.RIDDLE, PuzzleType.MAGICAL, PuzzleType.PATTERN]
        mapping[DungeonTheme.CLOCKWORK_TOWER] = [PuzzleType.MECHANICAL, PuzzleType.LOGICAL, PuzzleType.TEMPORAL]
        mapping[DungeonTheme.ARCANE_LIBRARY] = [PuzzleType.MAGICAL, PuzzleType.RIDDLE, PuzzleType.LOGICAL]

        return mapping

    def _initialize_theme_challenges(self) -> Dict[DungeonTheme, List[EnvironmentalChallenge]]:
        """Map themes to environmental challenges"""
        mapping = {}
        for theme in DungeonTheme:
            mapping[theme] = [EnvironmentalChallenge.DARKNESS]

        mapping[DungeonTheme.VOLCANIC_FORTRESS] = [EnvironmentalChallenge.FIRE, EnvironmentalChallenge.POISON]
        mapping[DungeonTheme.FROZEN_WASTELAND] = [EnvironmentalChallenge.ICE, EnvironmentalChallenge.WIND]
        mapping[DungeonTheme.CLOCKWORK_TOWER] = [EnvironmentalChallenge.ELECTRICITY, EnvironmentalChallenge.TIME_WARP]

        return mapping

    def _select_layout(self, theme: DungeonTheme) -> LayoutType:
        """Select appropriate layout for theme"""
        if theme in [DungeonTheme.MAZE, DungeonTheme.VERDANT_LABYRINTH]:
            return LayoutType.MAZE
        elif theme in [DungeonTheme.CLOCKWORK_TOWER, DungeonTheme.WIZARD_TOWER]:
            return LayoutType.SPIRAL
        return LayoutType.LINEAR  # Default

    def _generate_theme_puzzles(self, theme: DungeonTheme) -> List[PuzzleType]:
        """Generate puzzles based on theme"""
        available = self.theme_puzzle_mapping.get(theme, [PuzzleType.RIDDLE])
        count = random.randint(2, 4)
        return random.choices(available, k=count)

    def _generate_theme_challenges(self, theme: DungeonTheme) -> List[EnvironmentalChallenge]:
        """Generate challenges based on theme"""
        available = self.theme_challenge_mapping.get(theme, [EnvironmentalChallenge.DARKNESS])
        count = random.randint(1, 3)
        # Ensure unique challenges
        return list(set(random.choices(available, k=count)))

    def _generate_room_layout(self, dungeon_id: str, count: int,
                             layout: LayoutType, theme: DungeonTheme) -> Dict[str, DungeonRoom]:
        """Generate rooms based on layout"""
        rooms = {}

        # Always create entrance
        entrance_id = f"{dungeon_id}_entrance"
        rooms[entrance_id] = DungeonRoom(
            id=entrance_id,
            type=RoomType.ENTRANCE,
            x=0, y=0
        )

        # Create other rooms
        for i in range(1, count):
            room_id = f"{dungeon_id}_room_{i}"
            room_type = RoomType.CHAMBER

            # Chance for special rooms
            if i == count - 1:
                room_type = RoomType.BOSS_ROOM
            elif random.random() < 0.2:
                room_type = random.choice([RoomType.PUZZLE_ROOM, RoomType.TREASURE_ROOM, RoomType.TRAP_ROOM])

            rooms[room_id] = DungeonRoom(
                id=room_id,
                type=room_type,
                x=i, y=0,  # Simplified coordinates
                contents=self._generate_room_contents(theme, room_type),
                secrets=["Hidden cache"] if random.random() < 0.3 else [],
                challenge=self._get_room_challenge(theme) if random.random() < 0.2 else None,
                puzzle=self._get_room_puzzle(theme) if room_type == RoomType.PUZZLE_ROOM else None
            )

        return rooms

    def _connect_rooms(self, rooms: Dict[str, DungeonRoom], layout: LayoutType) -> None:
        """Connect rooms based on layout"""
        room_ids = list(rooms.keys())

        if layout == LayoutType.LINEAR:
            for i in range(len(room_ids) - 1):
                current_id = room_ids[i]
                next_id = room_ids[i+1]
                rooms[current_id].add_connection(next_id)
                rooms[next_id].add_connection(current_id)

        elif layout == LayoutType.CIRCULAR:
            # Connect linearly first
            for i in range(len(room_ids) - 1):
                current_id = room_ids[i]
                next_id = room_ids[i+1]
                rooms[current_id].add_connection(next_id)
                rooms[next_id].add_connection(current_id)
            # Close the loop
            if len(room_ids) > 2:
                rooms[room_ids[-1]].add_connection(room_ids[0])
                rooms[room_ids[0]].add_connection(room_ids[-1])

        # Fallback for other layouts to linear for now
        else:
            for i in range(len(room_ids) - 1):
                current_id = room_ids[i]
                next_id = room_ids[i+1]
                rooms[current_id].add_connection(next_id)
                rooms[next_id].add_connection(current_id)

    def _generate_room_contents(self, theme: DungeonTheme, room_type: RoomType) -> List[str]:
        """Generate room contents"""
        contents = []
        if room_type == RoomType.TREASURE_ROOM:
            contents.append("Chest")
        elif room_type == RoomType.BOSS_ROOM:
            contents.append("Boss Monster")
        else:
            contents.append("Monster")
            if random.random() < 0.5:
                contents.append("Crate")
        return contents

    def _get_room_challenge(self, theme: DungeonTheme) -> EnvironmentalChallenge:
        """Get challenge for a room"""
        options = self.theme_challenge_mapping.get(theme, [EnvironmentalChallenge.DARKNESS])
        return random.choice(options)

    def _get_room_puzzle(self, theme: DungeonTheme) -> PuzzleType:
        """Get puzzle for a room"""
        options = self.theme_puzzle_mapping.get(theme, [PuzzleType.RIDDLE])
        return random.choice(options)
