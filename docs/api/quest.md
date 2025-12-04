# Quest System

## `facade.py`

Quest System Facade

### Classes

### class `QuestSystem`

Facade for the Quest System

#### `get_available_quests_for_location`

Get available quests for a location

**Signature:** `get_available_quests_for_location(self, location: str) -> List[core.systems.quest.domain.quest.Quest]`

#### `get_npcs_in_location`

Get NPCs in a location

**Signature:** `get_npcs_in_location(self, location: str) -> List[core.systems.quest.domain.quest.NPCProfile]`

#### `initialize_world`

Initialize world with quests and NPCs

**Signature:** `initialize_world(self, locations: List[str], npc_count: int = 20) -> Dict[str, Any]`

#### `start_quest_from_npc`

Start a quest given by an NPC

**Signature:** `start_quest_from_npc(self, player_id: str, quest_id: str, npc_id: str) -> Optional[core.systems.quest.domain.quest.QuestProgress]`

### Functions

## `memory_repository.py`

Memory implementations of quest repositories

### Classes

### class `MemoryQuestProgressRepository`

Helper class that provides a standard way to create an ABC using
inheritance.

#### `get`



**Signature:** `get(self, player_id: str, quest_id: str) -> Optional[core.systems.quest.domain.quest.QuestProgress]`

#### `list_by_player`



**Signature:** `list_by_player(self, player_id: str) -> List[core.systems.quest.domain.quest.QuestProgress]`

#### `save`



**Signature:** `save(self, progress: core.systems.quest.domain.quest.QuestProgress) -> bool`

### class `MemoryQuestRepository`

Helper class that provides a standard way to create an ABC using
inheritance.

#### `get`



**Signature:** `get(self, quest_id: str) -> Optional[core.systems.quest.domain.quest.Quest]`

#### `list_all`



**Signature:** `list_all(self) -> List[core.systems.quest.domain.quest.Quest]`

#### `save`



**Signature:** `save(self, quest: core.systems.quest.domain.quest.Quest) -> bool`

### Functions

## `quest_generator.py`

Quest generation service

### Classes

### class `QuestGenerator`

Service for generating quests

#### `generate_quest`

Generate a random quest

**Signature:** `generate_quest(self, quest_type: core.systems.quest.domain.quest.QuestType = None, difficulty: core.systems.quest.domain.quest.QuestDifficulty = None, location: str = 'Unknown', giver: str = 'Unknown', quest_id: str = None) -> core.systems.quest.domain.quest.Quest`

### Functions

## `npc_manager.py`

NPC Management Service

### Classes

### class `NPCManager`

Service for managing NPCs

#### `create_npc_profile`

Create a new NPC profile

**Signature:** `create_npc_profile(self, npc_id: str, name: str, location: str, personality: core.systems.quest.domain.quest.NPCPersonality = None, quirk: core.systems.quest.domain.quest.NPCQuirk = None) -> core.systems.quest.domain.quest.NPCProfile`

#### `generate_npcs`

Generate a batch of NPCs

**Signature:** `generate_npcs(self, count: int, locations: List[str] = None) -> List[core.systems.quest.domain.quest.NPCProfile]`

#### `get_npc_by_id`

Get NPC by ID

**Signature:** `get_npc_by_id(self, npc_id: str) -> Optional[core.systems.quest.domain.quest.NPCProfile]`

#### `get_npcs_by_location`

Get NPCs in a specific location

**Signature:** `get_npcs_by_location(self, location: str) -> List[core.systems.quest.domain.quest.NPCProfile]`

### Functions

## `quest_manager.py`

Quest Management Service

### Classes

### class `QuestManager`

Service for managing quest state and progress

#### `abandon_quest`

Abandon a quest

**Signature:** `abandon_quest(self, player_id: str, quest_id: str) -> core.systems.quest.domain.quest.QuestProgress`

#### `complete_quest`

Complete a quest

**Signature:** `complete_quest(self, player_id: str, quest_id: str) -> core.systems.quest.domain.quest.QuestProgress`

#### `fail_quest`

Fail a quest

**Signature:** `fail_quest(self, player_id: str, quest_id: str) -> core.systems.quest.domain.quest.QuestProgress`

#### `get_active_quests`

Get all active quests for player

**Signature:** `get_active_quests(self, player_id: str) -> List[core.systems.quest.domain.quest.QuestProgress]`

#### `get_completed_quests`

Get all completed quests for player

**Signature:** `get_completed_quests(self, player_id: str) -> List[core.systems.quest.domain.quest.QuestProgress]`

#### `get_quest_progress`

Get quest progress

**Signature:** `get_quest_progress(self, player_id: str, quest_id: str) -> Optional[core.systems.quest.domain.quest.QuestProgress]`

#### `is_quest_available`

Check if quest is available for player

**Signature:** `is_quest_available(self, quest: core.systems.quest.domain.quest.Quest, player_data: Dict[str, Any]) -> bool`

#### `start_quest`

Start a quest for a player

**Signature:** `start_quest(self, player_id: str, quest: core.systems.quest.domain.quest.Quest) -> core.systems.quest.domain.quest.QuestProgress`

#### `update_quest_progress`

Update progress on a specific objective

**Signature:** `update_quest_progress(self, player_id: str, quest_id: str, objective_index: int, amount: int) -> core.systems.quest.domain.quest.QuestProgress`

### Functions

## `dialogue_manager.py`

Dialogue Management Service

### Classes

### class `DialogueManager`

Service for managing dialogue

#### `apply_speech_quirk`

Apply NPC speech quirk to text

**Signature:** `apply_speech_quirk(self, text: str, quirk: core.systems.quest.domain.quest.NPCQuirk) -> str`

#### `generate_class_dialogue_options`

Generate dialogue options specific to player class

**Signature:** `generate_class_dialogue_options(self, player_class: str) -> List[core.systems.quest.domain.quest.DialogueOption]`

#### `generate_npc_response`

Generate NPC response based on personality and input

**Signature:** `generate_npc_response(self, npc_profile: core.systems.quest.domain.quest.NPCProfile, player_input: str, player_reputation: int) -> core.systems.quest.domain.quest.DialogueResponse`

#### `generate_quest_dialogue_options`

Generate dialogue options related to quests

**Signature:** `generate_quest_dialogue_options(self, quests: List[Any]) -> List[core.systems.quest.domain.quest.DialogueOption]`

#### `generate_reputation_dialogue_options`

Generate dialogue options based on reputation

**Signature:** `generate_reputation_dialogue_options(self, reputation: int) -> List[core.systems.quest.domain.quest.DialogueOption]`

#### `get_all_dialogue_options`

Get all available dialogue options

**Signature:** `get_all_dialogue_options(self, npc_profile: core.systems.quest.domain.quest.NPCProfile, player_class: str, player_reputation: int, player_quests: List[Any]) -> List[core.systems.quest.domain.quest.DialogueOption]`

### Functions

## `quest.py`

Quest system domain entities and value objects

### Classes

### class `DialogueOption`

Option for player dialogue

### class `DialogueResponse`

NPC response to dialogue

### class `NPCPersonality`

NPC personality types

### class `NPCProfile`

NPC profile data

### class `NPCQuirk`

NPC speech and behavior quirks

### class `Quest`

Active quest data

### class `QuestDifficulty`

Difficulty levels for quests

### class `QuestObjective`

Objective within a quest

### class `QuestProgress`

Player progress on a quest

### class `QuestTemplate`

Template for generating quests

### class `QuestType`

Types of quests

### Functions

## `repositories.py`

Quest repository interfaces

### Classes

### class `QuestProgressRepository`

Helper class that provides a standard way to create an ABC using
inheritance.

#### `get`



**Signature:** `get(self, player_id: str, quest_id: str) -> Optional[core.systems.quest.domain.quest.QuestProgress]`

#### `list_by_player`



**Signature:** `list_by_player(self, player_id: str) -> List[core.systems.quest.domain.quest.QuestProgress]`

#### `save`



**Signature:** `save(self, progress: core.systems.quest.domain.quest.QuestProgress) -> bool`

### class `QuestRepository`

Helper class that provides a standard way to create an ABC using
inheritance.

#### `get`



**Signature:** `get(self, quest_id: str) -> Optional[core.systems.quest.domain.quest.Quest]`

#### `list_all`



**Signature:** `list_all(self) -> List[core.systems.quest.domain.quest.Quest]`

#### `save`



**Signature:** `save(self, quest: core.systems.quest.domain.quest.Quest) -> bool`

### Functions
