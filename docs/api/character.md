# Character System

## `dungeon_ready.py`

Character System Update for Dungeon Exploration
FOCUS: Add dungeon-ready features to existing characters

### Classes

### Functions

### `add_dungeon_exploration_to_character`

Add dungeon exploration methods to Character class

**Signature:** `add_dungeon_exploration_to_character()`

## `facade.py`

Facade for character system operations

### Classes

### class `CharacterSystem`

Facade for all character system operations

#### `add_to_inventory`

Add item to character inventory

**Signature:** `add_to_inventory(self, character_id: str, item: str) -> bool`

#### `create_character`

Create a new character

**Signature:** `create_character(self, name: str, class_type: str) -> core.systems.character.domain.character.Character`

#### `get_all_classes`

Get list of all available character classes

**Signature:** `get_all_classes(self) -> List[str]`

#### `get_character`

Get character by ID

**Signature:** `get_character(self, character_id: str) -> Optional[core.systems.character.domain.character.Character]`

#### `get_character_by_name`

Get character by name

**Signature:** `get_character_by_name(self, name: str) -> Optional[core.systems.character.domain.character.Character]`

#### `get_class_abilities`

Get abilities for specific class

**Signature:** `get_class_abilities(self, class_name: str) -> Optional[List[str]]`

#### `get_class_mechanic`

Get mechanic for specific class

**Signature:** `get_class_mechanic(self, class_name: str) -> Optional[str]`

#### `get_class_stats`

Get stats for specific class

**Signature:** `get_class_stats(self, class_name: str) -> Optional[Dict]`

#### `get_inventory_count`

Get character inventory count

**Signature:** `get_inventory_count(self, character_id: str) -> int`

#### `level_up_character`

Level up character by ID

**Signature:** `level_up_character(self, character_id: str) -> bool`

#### `list_all_characters`

List all characters

**Signature:** `list_all_characters(self) -> List[core.systems.character.domain.character.Character]`

#### `remove_from_inventory`

Remove item from character inventory

**Signature:** `remove_from_inventory(self, character_id: str, item: str) -> bool`

#### `validate_class_balance`

Validate that all classes are balanced

**Signature:** `validate_class_balance(self) -> bool`

#### `verify_minimum_abilities`

Verify that all classes have minimum abilities

**Signature:** `verify_minimum_abilities(self) -> bool`

#### `verify_unique_mechanics`

Verify that all classes have unique mechanics

**Signature:** `verify_unique_mechanics(self) -> bool`

### Functions

### `add_experience`

Add experience to character (backward compatibility)

**Signature:** `add_experience(character: core.systems.character.domain.character.Character, exp_amount: int) -> bool`

### `create_character`

Create a character (backward compatibility)

**Signature:** `create_character(name: str, class_type: str) -> core.systems.character.domain.character.Character`

### `get_all_character_classes`

Get all character classes for Select widget (backward compatibility)

**Signature:** `get_all_character_classes() -> List[Tuple[str, str]]`

### `get_class_balance_stats`

Get class balance statistics

**Signature:** `get_class_balance_stats() -> Dict[str, int]`

### `get_default_stats_for_class`

Get default stats for class (BDD compliant)

**Signature:** `get_default_stats_for_class(class_type: str) -> dict`

### `heal_character`

Heal character by amount (BDD compliant)

**Signature:** `heal_character(character: core.systems.character.domain.character.Character, amount: int) -> bool`

### `level_up_character`

Level up character (backward compatibility)

**Signature:** `level_up_character(character: core.systems.character.domain.character.Character) -> bool`

### `validate_class_balance`

Validate class balance (backward compatibility)

**Signature:** `validate_class_balance() -> bool`

### `verify_minimum_abilities`

Verify minimum abilities (backward compatibility)

**Signature:** `verify_minimum_abilities() -> bool`

### `verify_unique_mechanics`

Verify unique mechanics (backward compatibility)

**Signature:** `verify_unique_mechanics() -> bool`

## `memory_repository.py`

Memory repository implementations for character data

### Classes

### class `MemoryCharacterRepository`

In-memory character repository

#### `delete`

Delete character by ID

**Signature:** `delete(self, character_id: str) -> bool`

#### `list_all`

List all characters

**Signature:** `list_all(self) -> List[core.systems.character.domain.character.Character]`

#### `load`

Load character by ID

**Signature:** `load(self, character_id: str) -> Optional[core.systems.character.domain.character.Character]`

#### `load_by_name`

Load character by name

**Signature:** `load_by_name(self, name: str) -> Optional[core.systems.character.domain.character.Character]`

#### `save`

Save character to memory storage

**Signature:** `save(self, character: core.systems.character.domain.character.Character) -> bool`

### class `MemoryClassConfigRepository`

In-memory class configuration repository

#### `get_all_configs`

Get all class configurations

**Signature:** `get_all_configs(self) -> Dict[core.systems.character.domain.character.CharacterClass, Dict]`

#### `get_config`

Get configuration for specific class

**Signature:** `get_config(self, character_class: core.systems.character.domain.character.CharacterClass) -> Optional[Dict]`

### Functions

## `character_exceptions.py`

Character-specific exceptions

### Classes

### class `CharacterCreationError`

Raised when character creation fails

### class `CharacterError`

Base exception for character system

### class `CharacterNotFoundError`

Raised when character is not found

### class `InvalidCharacterClassError`

Raised when trying to use invalid character class

### class `InventoryError`

Raised when inventory operation fails

### class `StatValidationError`

Raised when stat validation fails

### Functions

## `character_service.py`

Character business logic services

### Classes

### class `CharacterBalanceService`

Service for character class balance analysis

#### `get_balance_stats`

Calculate power levels for all classes

**Signature:** `get_balance_stats(self) -> Dict[str, int]`

#### `validate_balance`

Check if all classes are within 15% power difference

**Signature:** `validate_balance(self) -> bool`

#### `verify_minimum_abilities`

Check if all classes have at least 10 abilities

**Signature:** `verify_minimum_abilities(self) -> bool`

#### `verify_unique_mechanics`

Check if all classes have unique mechanics

**Signature:** `verify_unique_mechanics(self) -> bool`

### class `CharacterCreationService`

Service for character creation logic

#### `create_character`

Create a new character with given name and class

**Signature:** `create_character(self, name: str, class_name: str) -> core.systems.character.domain.character.Character`

### class `CharacterInventoryService`

Service for character inventory management

#### `add_item`

Add item to character inventory

**Signature:** `add_item(self, character: core.systems.character.domain.character.Character, item: str) -> bool`

#### `get_inventory_count`

Get number of items in inventory

**Signature:** `get_inventory_count(self, character: core.systems.character.domain.character.Character) -> int`

#### `remove_item`

Remove item from character inventory

**Signature:** `remove_item(self, character: core.systems.character.domain.character.Character, item: str) -> bool`

### class `CharacterProgressionService`

Service for character progression logic

#### `add_experience`

Add experience to character

**Signature:** `add_experience(self, character: core.systems.character.domain.character.Character, exp_amount: int) -> bool`

#### `level_up`

Level up character with stat improvements

**Signature:** `level_up(self, character: core.systems.character.domain.character.Character) -> bool`

### Functions

## `character.py`

Character domain entities and value objects

### Classes

### class `Character`

Character aggregate root entity

#### `add_to_inventory`

Add item to inventory with validation

**Signature:** `add_to_inventory(self, item: str) -> bool`

#### `calculate_power_level`

Calculate character's total power level

**Signature:** `calculate_power_level(self) -> int`

#### `can_enter_dungeon`

Check if character can enter dungeon

**Signature:** `can_enter_dungeon(self, difficulty: str) -> bool`

#### `get_class_abilities`

Get abilities for specific class (BDD compatibility)

**Signature:** `get_class_abilities(self, class_name: str) -> Optional[List[str]]`

#### `get_class_mechanic`

Get mechanic for specific class (BDD compatibility)

**Signature:** `get_class_mechanic(self, class_name: str) -> Optional[str]`

#### `get_class_stats`

Get stats for specific class (BDD compatibility)

**Signature:** `get_class_stats(self, class_name: str) -> Optional[Dict]`

#### `get_dungeon_readiness`

Get character's readiness for dungeon

**Signature:** `get_dungeon_readiness(self) -> Dict`

#### `is_alive`

Check if character is alive

**Signature:** `is_alive(self) -> bool`

#### `level_up`

Level up character with stat improvements

**Signature:** `level_up(self) -> bool`

#### `prepare_for_dungeon`

Prepare character for dungeon exploration

**Signature:** `prepare_for_dungeon(self) -> Dict`

#### `remove_from_inventory`

Remove item from inventory

**Signature:** `remove_from_inventory(self, item: str) -> bool`

### class `CharacterClass`

All 23 character classes available in RPGSim

### class `CharacterClassConfig`

Configuration for a character class

### class `CharacterStats`

Character statistics as immutable value object

#### `get_strengths`

Get list of character's strong stats (15+ points)

**Signature:** `get_strengths(self) -> List[str]`

#### `get_weaknesses`

Get list of character's weak stats (12- points)

**Signature:** `get_weaknesses(self) -> List[str]`

#### `primary_stat_value`

Get value of primary stat

**Signature:** `primary_stat_value(self, primary_stat: str) -> int`

#### `total_power`

Calculate total power level

**Signature:** `total_power(self) -> int`

### Functions

## `repositories.py`

Character data repository interfaces

### Classes

### class `CharacterRepository`

Repository interface for character data access

#### `delete`

Delete character by ID

**Signature:** `delete(self, character_id: str) -> bool`

#### `list_all`

List all characters

**Signature:** `list_all(self) -> List[core.systems.character.domain.character.Character]`

#### `load`

Load character by ID

**Signature:** `load(self, character_id: str) -> Optional[core.systems.character.domain.character.Character]`

#### `load_by_name`

Load character by name

**Signature:** `load_by_name(self, name: str) -> Optional[core.systems.character.domain.character.Character]`

#### `save`

Save character to storage

**Signature:** `save(self, character: core.systems.character.domain.character.Character) -> bool`

### class `ClassConfigRepository`

Repository interface for class configuration data

#### `get_all_configs`

Get all class configurations

**Signature:** `get_all_configs(self) -> Dict[core.systems.character.domain.character.CharacterClass, Dict]`

#### `get_config`

Get configuration for specific class

**Signature:** `get_config(self, character_class: core.systems.character.domain.character.CharacterClass) -> Optional[Dict]`

### Functions
