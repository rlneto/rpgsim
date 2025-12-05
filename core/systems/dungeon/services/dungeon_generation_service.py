from typing import Dict, List, Optional
import random
import uuid
from ..domain.dungeon import (
    Dungeon, DungeonTheme, LayoutType, Room, RoomType,
    PuzzleType, EnvironmentalChallenge, Trap, TrapType, Treasure, RewardTier
)
from .reward_service import RewardService

class DungeonGenerationService:
    """Service for procedural dungeon generation"""

    def __init__(self):
        self.theme_puzzle_mapping = self._initialize_theme_puzzles()
        self.theme_challenge_mapping = self._initialize_theme_challenges()
        self.reward_service = RewardService()

    def generate_dungeon(self, theme: DungeonTheme, player_level: int) -> Dungeon:
        """Generate a complete dungeon"""
        dungeon_id = str(uuid.uuid4())
        layout = self._select_layout(theme)
        room_count = 5 + (player_level // 2)

        rooms = self._generate_room_layout(dungeon_id, room_count, layout, theme, player_level)
        self._connect_rooms(rooms, layout)

        puzzles = self._generate_theme_puzzles(theme)
        challenges = self._generate_theme_challenges(theme)

        return Dungeon(
            id=dungeon_id,
            name=f"{theme.value.replace('_', ' ').title()}",
            theme=theme,
            level=player_level,
            rooms=rooms, # Pass dict
            layout=layout,
            puzzles=puzzles,
            environmental_challenges=challenges,
            secrets=max(1, room_count // 3),
            hidden_areas=max(0, room_count // 5),
            lore_elements=max(1, room_count // 2),
            difficulty=player_level
        )

    def _initialize_theme_puzzles(self) -> Dict[DungeonTheme, List[PuzzleType]]:
        """Map themes to appropriate puzzles"""
        mapping = {}
        for theme in DungeonTheme:
            mapping[theme] = [PuzzleType.RIDDLE, PuzzleType.MECHANICAL]

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
        return LayoutType.LINEAR

    def _generate_theme_puzzles(self, theme: DungeonTheme) -> List[PuzzleType]:
        """Generate puzzles based on theme"""
        available = self.theme_puzzle_mapping.get(theme, [PuzzleType.RIDDLE])
        count = random.randint(2, 4)
        return random.choices(available, k=count)

    def _generate_theme_challenges(self, theme: DungeonTheme) -> List[EnvironmentalChallenge]:
        """Generate challenges based on theme"""
        available = self.theme_challenge_mapping.get(theme, [EnvironmentalChallenge.DARKNESS])
        count = random.randint(1, 3)
        return list(set(random.choices(available, k=count)))

    def _generate_room_layout(self, dungeon_id: str, count: int,
                             layout: LayoutType, theme: DungeonTheme, level: int) -> Dict[str, Room]:
        """Generate rooms based on layout"""
        rooms = {}
        entrance_id = f"{dungeon_id}_entrance"
        rooms[entrance_id] = Room(
            id=entrance_id,
            type=RoomType.ENTRANCE,
            x=0, y=0,
            name="Entrance Hall",
            description="The entrance to the dungeon."
        )
        for i in range(1, count):
            room_id = f"{dungeon_id}_room_{i}"
            room_type = RoomType.CHAMBER
            if i == count - 1:
                room_type = RoomType.BOSS_ROOM
            elif random.random() < 0.2:
                room_type = random.choice([RoomType.PUZZLE_ROOM, RoomType.TREASURE_ROOM, RoomType.TRAP_ROOM])

            traps = []
            if room_type == RoomType.TRAP_ROOM or random.random() < 0.3:
                traps.append(self._generate_trap())

            treasures = []
            if room_type == RoomType.TREASURE_ROOM:
                treasures.append(self.reward_service.generate_treasure(level))

            rooms[room_id] = Room(
                id=room_id,
                type=room_type,
                x=i, y=0,
                name=f"Room {i}",
                description=f"A generic {room_type.value}.",
                contents=self._generate_room_contents(theme, room_type),
                secrets=["Hidden cache"] if random.random() < 0.3 else [],
                traps=traps,
                treasures=treasures,
                challenge=self._get_room_challenge(theme) if random.random() < 0.2 else None,
                puzzle=self._get_room_puzzle(theme) if room_type == RoomType.PUZZLE_ROOM else None
            )

        if count > 3:
            keys = list(rooms.keys())
            if len(keys) >= 3:
                r1 = rooms[keys[1]]
                if not r1.traps:
                    r1.type = RoomType.TRAP_ROOM
                    r1.traps.append(self._generate_trap())

                r2 = rooms[keys[2]]
                if not r2.treasures:
                    r2.type = RoomType.TREASURE_ROOM
                    r2.treasures.append(self.reward_service.generate_treasure(level))

        return rooms

    def _connect_rooms(self, rooms: Dict[str, Room], layout: LayoutType) -> None:
        """Connect rooms based on layout"""
        room_ids = list(rooms.keys())
        if layout == LayoutType.LINEAR:
            for i in range(len(room_ids) - 1):
                current_id, next_id = room_ids[i], room_ids[i+1]
                rooms[current_id].exits[next_id] = "north"
                rooms[next_id].exits[current_id] = "south"
        else:
             for i in range(len(room_ids) - 1):
                current_id, next_id = room_ids[i], room_ids[i+1]
                rooms[current_id].exits[next_id] = "north"
                rooms[next_id].exits[current_id] = "south"

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

    def _generate_trap(self) -> Trap:
        """Generate a trap"""
        trap_type = random.choice(list(TrapType))
        return Trap(
            id=str(uuid.uuid4()),
            type=trap_type,
            damage=10,
            description=f"A {trap_type.value} trap."
        )

    def _get_room_challenge(self, theme: DungeonTheme) -> EnvironmentalChallenge:
        """Get challenge for a room"""
        options = self.theme_challenge_mapping.get(theme, [EnvironmentalChallenge.DARKNESS])
        return random.choice(options)

    def _get_room_puzzle(self, theme: DungeonTheme) -> PuzzleType:
        """Get puzzle for a room"""
        options = self.theme_puzzle_mapping.get(theme, [PuzzleType.RIDDLE])
        return random.choice(options)
