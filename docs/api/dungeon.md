# Dungeon System

## `facade.py`

Dungeon System Facade

### Classes

### class `DungeonSystem`

Facade for the Dungeon System

#### `end_dungeon_exploration`

End exploration

**Signature:** `end_dungeon_exploration(self, dungeon_id: str) -> Dict[str, Any]`

#### `enter_dungeon`

Enter a dungeon

**Signature:** `enter_dungeon(self, dungeon_id: str, player_level: int) -> Dict[str, Any]`

#### `explore_dungeon`

Perform exploration actions

**Signature:** `explore_dungeon(self, dungeon_id: str, actions: List[str]) -> Dict[str, Any]`

#### `get_dungeon_list`

Get list of all dungeons

**Signature:** `get_dungeon_list(self) -> List[Dict[str, Any]]`

#### `get_dungeon_themes`

Get available themes

**Signature:** `get_dungeon_themes(self) -> List[str]`

#### `get_theme_coverage`

Get analysis of theme coverage

**Signature:** `get_theme_coverage(self) -> Dict[str, int]`

#### `initialize_dungeons`

Initialize the world dungeons

**Signature:** `initialize_dungeons(self, count: int = 50) -> None`

#### `navigate_dungeon`

Navigate deeper into dungeon

**Signature:** `navigate_dungeon(self, dungeon_id: str, depth: int = 0) -> Dict[str, Any]`

### Functions

### `create_dungeon_system`

Create new instance

**Signature:** `create_dungeon_system()`

### `get_dungeon_system`

Get singleton instance

**Signature:** `get_dungeon_system()`

## `dungeon_manager.py`

Dungeon manager service

### Classes

### class `DungeonManager`

Service for managing dungeon state and sessions

#### `end_exploration`

End exploration session

**Signature:** `end_exploration(self, dungeon_id: str) -> Dict[str, Any]`

#### `generate_all_dungeons`

Generate a set of dungeons

**Signature:** `generate_all_dungeons(self, count: int) -> None`

#### `get_all_themes`

Get all used themes

**Signature:** `get_all_themes(self) -> List[core.systems.dungeon.domain.dungeon.DungeonTheme]`

#### `get_dungeon`

Get dungeon by ID

**Signature:** `get_dungeon(self, dungeon_id: str) -> Optional[core.systems.dungeon.domain.dungeon.Dungeon]`

#### `get_dungeons_by_theme`

Get dungeons with specific theme

**Signature:** `get_dungeons_by_theme(self, theme: core.systems.dungeon.domain.dungeon.DungeonTheme) -> List[core.systems.dungeon.domain.dungeon.Dungeon]`

#### `get_session`

Get active session

**Signature:** `get_session(self, dungeon_id: str) -> Optional[core.systems.dungeon.domain.dungeon.ExplorationSession]`

#### `start_exploration`

Start an exploration session

**Signature:** `start_exploration(self, dungeon_id: str, player_level: int) -> Optional[core.systems.dungeon.domain.dungeon.ExplorationSession]`

### Functions

## `dungeon_service.py`

Dungeon generation services

### Classes

### class `DungeonGenerator`

Service for procedural dungeon generation

#### `generate_dungeon`

Generate a complete dungeon

**Signature:** `generate_dungeon(self, dungeon_id: str, theme: core.systems.dungeon.domain.dungeon.DungeonTheme, player_level: int) -> core.systems.dungeon.domain.dungeon.Dungeon`

### Functions

## `reward_system.py`

Reward system service

### Classes

### class `RewardSystem`

Service for generating rewards

#### `generate_progressive_rewards`

Generate a series of rewards increasing in value

**Signature:** `generate_progressive_rewards(self, max_depth: int, dungeon_level: int) -> List[Dict[str, Any]]`

#### `generate_reward`

Generate a single reward

**Signature:** `generate_reward(self, depth: int, dungeon_level: int) -> Dict[str, Any]`

### Functions

## `dungeon.py`

Dungeon system domain entities and value objects

### Classes

### class `Dungeon`

A complete dungeon instance

#### `get_boss_room`

Get the boss room

**Signature:** `get_boss_room(self) -> Optional[core.systems.dungeon.domain.dungeon.DungeonRoom]`

#### `get_entrance`

Get the entrance room

**Signature:** `get_entrance(self) -> Optional[core.systems.dungeon.domain.dungeon.DungeonRoom]`

#### `get_explored_percentage`

Calculate percentage of explored rooms

**Signature:** `get_explored_percentage(self) -> float`

#### `get_room`

Get a room by ID

**Signature:** `get_room(self, room_id: str) -> Optional[core.systems.dungeon.domain.dungeon.DungeonRoom]`

### class `DungeonRoom`

A room within a dungeon

#### `add_connection`

Add a connection to another room

**Signature:** `add_connection(self, room_id: str) -> None`

#### `explore`

Explore the room and return contents

**Signature:** `explore(self) -> Dict[str, Any]`

### class `DungeonTheme`

Themes for dungeons

### class `EnvironmentalChallenge`

Environmental hazards

### class `ExplorationSession`

Active exploration session

#### `add_reward`

Add a found reward

**Signature:** `add_reward(self, reward: Dict[str, Any]) -> None`

#### `calculate_difficulty_multiplier`

Calculate difficulty multiplier based on depth and level

**Signature:** `calculate_difficulty_multiplier(self, depth: int) -> float`

#### `explore_room`

Process room exploration

**Signature:** `explore_room(self, room: core.systems.dungeon.domain.dungeon.DungeonRoom) -> Dict[str, Any]`

#### `make_strategic_decision`

Record a strategic decision

**Signature:** `make_strategic_decision(self, decision_type: core.systems.dungeon.domain.dungeon.StrategicDecisionType) -> None`

### class `LayoutType`

Layout types for dungeon generation

### class `LoreType`

Types of lore elements

### class `PuzzleType`

Types of puzzles encountered

### class `RewardTier`

Tiers of rewards

### class `RoomType`

Types of rooms

### class `StrategicDecisionType`

Types of strategic decisions

### Functions
