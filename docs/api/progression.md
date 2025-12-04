# Progression System

## `facade.py`

Progression System Facade

### Classes

### class `ProgressionSystem`

Facade for Progression System

#### `add_experience`

Add experience

**Signature:** `add_experience(self, character: core.models.Character, amount: int, source: str) -> Dict[str, Any]`

#### `get_available_abilities`

Get available abilities

**Signature:** `get_available_abilities(self, character: core.models.Character, skill_type: core.systems.progression.domain.progression.SkillType = None) -> List[Any]`

#### `get_character_summary`

Get summary

**Signature:** `get_character_summary(self, character: core.models.Character) -> Dict[str, Any]`

#### `get_skill_trees`

Get skill trees

**Signature:** `get_skill_trees(self) -> Dict[core.systems.progression.domain.progression.SkillType, List[Any]]`

#### `learn_ability`

Learn ability

**Signature:** `learn_ability(self, character: core.models.Character, ability_id: str) -> Dict[str, Any]`

### Functions

## `progression_service.py`

Progression services

### Classes

### class `LevelCalculator`

Service for level calculations

#### `calculate_level_up_rewards`

Calculate rewards for reaching a level

**Signature:** `calculate_level_up_rewards(level: int, class_type: str) -> Dict[str, Any]`

#### `can_level_up`

Check if character can level up

**Signature:** `can_level_up(character: Any) -> bool`

#### `generate_experience_table`

Generate XP requirement table

**Signature:** `generate_experience_table() -> List[int]`

#### `get_experience_for_level`

Get total XP required for level

**Signature:** `get_experience_for_level(level: int) -> int`

#### `get_experience_progress`

Get current level progress (current, needed)

**Signature:** `get_experience_progress(character: Any) -> Tuple[int, int]`

#### `get_level_from_experience`

Get level from total XP

**Signature:** `get_level_from_experience(experience: int) -> int`

### class `ProgressionManager`

Service for managing character progression

#### `add_experience`

Add experience to character

**Signature:** `add_experience(self, character: Any, amount: int, source: str) -> Dict[str, Any]`

#### `get_character_progression_summary`

Get summary

**Signature:** `get_character_progression_summary(self, character: Any) -> Dict[str, Any]`

#### `learn_ability`

Learn a new ability

**Signature:** `learn_ability(self, character: Any, ability_id: str) -> Dict[str, Any]`

#### `upgrade_ability`

Upgrade an existing ability

**Signature:** `upgrade_ability(self, character: Any, ability_id: str) -> Dict[str, Any]`

#### `upgrade_skill`

Upgrade a specific skill

**Signature:** `upgrade_skill(self, character: Any, skill_name: str, exp_amount: int) -> Dict[str, Any]`

### class `SkillTree`

Service for managing skills and abilities

#### `check_synergy`

Check synergy multiplier

**Signature:** `check_synergy(self, character: Any, ability_id: str) -> float`

#### `get_ability_by_id`

Get ability by ID

**Signature:** `get_ability_by_id(self, ability_id: str) -> Optional[core.systems.progression.domain.progression.Ability]`

#### `get_ability_tree`

Get all abilities for a skill type

**Signature:** `get_ability_tree(self, skill_type: core.systems.progression.domain.progression.SkillType) -> List[core.systems.progression.domain.progression.Ability]`

#### `get_available_abilities`

Get abilities available for character to learn

**Signature:** `get_available_abilities(self, character: Any) -> List[core.systems.progression.domain.progression.Ability]`

### Functions

## `progression.py`

Progression system domain entities and value objects

### Classes

### class `Ability`

Represents an ability in the skill tree

#### `can_upgrade`

Check if character can upgrade this ability

**Signature:** `can_upgrade(self, character: Any) -> bool`

#### `get_upgrade_cost`

Calculate upgrade cost

**Signature:** `get_upgrade_cost(self) -> Dict[str, int]`

### class `AbilityRarity`

Ability rarity levels

### class `SkillProgress`

Tracks progress for a specific skill

#### `add_experience`

Add experience and check for level up

**Signature:** `add_experience(self, amount: int) -> bool`

#### `calculate_experience_to_next`

Calculate experience needed for next level

**Signature:** `calculate_experience_to_next(self) -> int`

#### `get_effectiveness`

Calculate skill effectiveness multiplier

**Signature:** `get_effectiveness(self) -> float`

### class `SkillType`

Skill types

### Functions
