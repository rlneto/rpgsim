# Combat System

## `facade.py`

Facade for combat system operations

### Classes

### class `ActionConfig`

Configuration for combat action creation

### class `AttackConfig`

Configuration for attack creation

### class `CombatSystem`

Facade for all combat system operations

#### `add_combatant`

Add combatant to combat

**Signature:** `add_combatant(self, combat_id: str, combatant: core.systems.combat.domain.combat.Combatant) -> bool`

#### `calculate_damage`

Calculate damage for attack

**Signature:** `calculate_damage(self, attack_id: str, attacker_stats: core.systems.combat.domain.combat.CombatStats, defender_stats: core.systems.combat.domain.combat.CombatStats) -> int`

#### `can_use_attack`

Check if attack can be used with given stats

**Signature:** `can_use_attack(self, attack_id: str, stats: core.systems.combat.domain.combat.CombatStats) -> bool`

#### `cleanup_completed_combats`

Remove completed combats and return count

**Signature:** `cleanup_completed_combats(self) -> int`

#### `create_action`

Create a combat action

**Signature:** `create_action(self, config: core.systems.combat.facade.ActionConfig) -> core.systems.combat.domain.combat.CombatAction`

#### `create_attack`

Create a new attack

**Signature:** `create_attack(self, config: core.systems.combat.facade.AttackConfig) -> Optional[core.systems.combat.domain.combat.Attack]`

#### `create_combat`

Create a new combat encounter

**Signature:** `create_combat(self, combat_id: str, name: str, location: str, environment: Optional[Dict[str, Any]] = None) -> Optional[core.systems.combat.domain.combat.Combat]`

#### `create_combatant`

Create a new combatant

**Signature:** `create_combatant(self, config: core.systems.combat.facade.CombatantConfig) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `end_combat`

End combat with result

**Signature:** `end_combat(self, combat_id: str, result: str) -> bool`

#### `execute_action`

Execute a combat action

**Signature:** `execute_action(self, combat_id: str, action: core.systems.combat.domain.combat.CombatAction) -> Dict[str, Any]`

#### `execute_ai_turns`

Execute all AI turns in combat

**Signature:** `execute_ai_turns(self, combat_id: str) -> List[Dict[str, Any]]`

#### `get_actions`

Get combat actions

**Signature:** `get_actions(self, combat_id: str, limit: int = 100) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `get_active_combats`

Get all active combats

**Signature:** `get_active_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_ai_action`

Get AI action for combatant

**Signature:** `get_ai_action(self, combat_id: str, combatant_id: str) -> Optional[core.systems.combat.domain.combat.CombatAction]`

#### `get_alive_combatants`

Get alive combatants in combat

**Signature:** `get_alive_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_all_attacks`

Get all attacks

**Signature:** `get_all_attacks(self) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_all_combats`

Get all combats

**Signature:** `get_all_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_attack`

Get attack by ID

**Signature:** `get_attack(self, attack_id: str) -> Optional[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_damage_type`

Get attacks by damage type

**Signature:** `get_attacks_by_damage_type(self, damage_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_type`

Get attacks by type

**Signature:** `get_attacks_by_type(self, attack_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_combat`

Get combat by ID

**Signature:** `get_combat(self, combat_id: str) -> Optional[core.systems.combat.domain.combat.Combat]`

#### `get_combat_history`

Get combat history

**Signature:** `get_combat_history(self, combat_id: str, limit: int = 50) -> List[Dict[str, Any]]`

#### `get_combat_status`

Get complete combat status

**Signature:** `get_combat_status(self, combat_id: str) -> Optional[Dict[str, Any]]`

#### `get_combat_summary`

Get combat summary

**Signature:** `get_combat_summary(self, combat_id: str) -> Optional[Dict[str, Any]]`

#### `get_combatant`

Get combatant by ID

**Signature:** `get_combatant(self, combat_id: str, combatant_id: str) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `get_combatant_status`

Get combatant status

**Signature:** `get_combatant_status(self, combat_id: str, combatant_id: str) -> Optional[Dict[str, Any]]`

#### `get_combatants`

Get all combatants in combat

**Signature:** `get_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants_by_team`

Get combatants by team

**Signature:** `get_combatants_by_team(self, combat_id: str, team: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combats_by_location`

Get combats by location

**Signature:** `get_combats_by_location(self, location: str) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_distance`

Calculate distance between two combatants

**Signature:** `get_distance(self, combat_id: str, combatant1_id: str, combatant2_id: str) -> Optional[float]`

#### `is_in_range`

Check if target is in range

**Signature:** `is_in_range(self, combat_id: str, attacker_id: str, target_id: str, range_distance: int) -> bool`

#### `start_combat`

Start combat encounter

**Signature:** `start_combat(self, combat_id: str) -> bool`

#### `validate_combat_state`

Validate combat state and return issues

**Signature:** `validate_combat_state(self, combat_id: str) -> Dict[str, Any]`

### class `CombatantConfig`

Configuration for combatant creation

### Functions

### `add_combatant`

Add combatant (backward compatibility)

**Signature:** `add_combatant(combat_id: str, combatant: core.systems.combat.domain.combat.Combatant) -> bool`

### `create_combat`

Create combat (backward compatibility)

**Signature:** `create_combat(combat_id: str, name: str, location: str) -> Optional[core.systems.combat.domain.combat.Combat]`

### `execute_action`

Execute action (backward compatibility)

**Signature:** `execute_action(combat_id: str, action: core.systems.combat.domain.combat.CombatAction) -> Dict[str, Any]`

### `get_combat`

Get combat (backward compatibility)

**Signature:** `get_combat(combat_id: str) -> Optional[core.systems.combat.domain.combat.Combat]`

### `start_combat`

Start combat (backward compatibility)

**Signature:** `start_combat(combat_id: str) -> bool`

## `memory_repository.py`

Memory repository implementations for combat data

### Classes

### class `MemoryAttackRepository`

In-memory attack repository

#### `attack_exists`

Check if attack exists

**Signature:** `attack_exists(self, attack_id: str) -> bool`

#### `delete_attack`

Delete attack by ID

**Signature:** `delete_attack(self, attack_id: str) -> bool`

#### `get_all_attacks`

Get all attacks

**Signature:** `get_all_attacks(self) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_damage_type`

Get attacks by damage type

**Signature:** `get_attacks_by_damage_type(self, damage_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_type`

Get attacks by type

**Signature:** `get_attacks_by_type(self, attack_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `load_attack`

Load attack by ID

**Signature:** `load_attack(self, attack_id: str) -> Optional[core.systems.combat.domain.combat.Attack]`

#### `save_attack`

Save attack to memory storage

**Signature:** `save_attack(self, attack: core.systems.combat.domain.combat.Attack) -> bool`

### class `MemoryCombatActionRepository`

In-memory combat action repository

#### `delete_action`

Delete combat action

**Signature:** `delete_action(self, combat_id: str, action_id: str) -> bool`

#### `get_actions`

Get combat actions

**Signature:** `get_actions(self, combat_id: str, limit: int = 100) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `get_actions_by_combatant`

Get actions by combatant

**Signature:** `get_actions_by_combatant(self, combat_id: str, combatant_id: str, limit: int = 50) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `get_actions_by_round`

Get actions by round

**Signature:** `get_actions_by_round(self, combat_id: str, round_number: int) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `save_action`

Save combat action

**Signature:** `save_action(self, combat_id: str, action: core.systems.combat.domain.combat.CombatAction) -> bool`

### class `MemoryCombatLogRepository`

In-memory combat log repository

#### `delete_log_entries`

Delete all log entries for combat

**Signature:** `delete_log_entries(self, combat_id: str) -> bool`

#### `get_entries_by_combatant`

Get log entries by combatant

**Signature:** `get_entries_by_combatant(self, combat_id: str, combatant_id: str, limit: int = 50) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `get_entries_by_round`

Get log entries by round

**Signature:** `get_entries_by_round(self, combat_id: str, round_number: int) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `get_log_entries`

Get combat log entries

**Signature:** `get_log_entries(self, combat_id: str, limit: int = 100) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `save_log_entry`

Save combat log entry

**Signature:** `save_log_entry(self, combat_id: str, entry: core.systems.combat.domain.combat.CombatLog) -> bool`

### class `MemoryCombatRepository`

In-memory combat repository

#### `combat_exists`

Check if combat exists

**Signature:** `combat_exists(self, combat_id: str) -> bool`

#### `delete_combat`

Delete combat by ID

**Signature:** `delete_combat(self, combat_id: str) -> bool`

#### `get_active_combats`

Get all active combats

**Signature:** `get_active_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_all_combats`

Get all combats

**Signature:** `get_all_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_combats_by_location`

Get combats by location

**Signature:** `get_combats_by_location(self, location: str) -> List[core.systems.combat.domain.combat.Combat]`

#### `load_combat`

Load combat by ID

**Signature:** `load_combat(self, combat_id: str) -> Optional[core.systems.combat.domain.combat.Combat]`

#### `save_combat`

Save combat to memory storage

**Signature:** `save_combat(self, combat: core.systems.combat.domain.combat.Combat) -> bool`

### class `MemoryCombatSystemRepository`

Combined memory repository for combat system

#### `get_action_repository`

Get action repository

**Signature:** `get_action_repository(self) -> core.systems.combat.interfaces.repositories.CombatActionRepositoryInterface`

#### `get_attack_repository`

Get attack repository

**Signature:** `get_attack_repository(self) -> core.systems.combat.interfaces.repositories.AttackRepositoryInterface`

#### `get_combat_repository`

Get combat repository

**Signature:** `get_combat_repository(self) -> core.systems.combat.interfaces.repositories.CombatRepositoryInterface`

#### `get_combatant_repository`

Get combatant repository

**Signature:** `get_combatant_repository(self) -> core.systems.combat.interfaces.repositories.CombatantRepositoryInterface`

#### `get_log_repository`

Get log repository

**Signature:** `get_log_repository(self) -> core.systems.combat.interfaces.repositories.CombatLogRepositoryInterface`

### class `MemoryCombatantRepository`

In-memory combatant repository

#### `combatant_exists`

Check if combatant exists in combat

**Signature:** `combatant_exists(self, combat_id: str, combatant_id: str) -> bool`

#### `delete_combatant`

Delete combatant from combat

**Signature:** `delete_combatant(self, combat_id: str, combatant_id: str) -> bool`

#### `get_alive_combatants`

Get alive combatants in a combat

**Signature:** `get_alive_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants`

Get all combatants in a combat

**Signature:** `get_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants_by_team`

Get combatants by team

**Signature:** `get_combatants_by_team(self, combat_id: str, team: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `load_combatant`

Load combatant from combat

**Signature:** `load_combatant(self, combat_id: str, combatant_id: str) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `save_combatant`

Save combatant to combat

**Signature:** `save_combatant(self, combat_id: str, combatant: core.systems.combat.domain.combat.Combatant) -> bool`

### Functions

## `combat_service.py`

Combat service implementations

### Classes

### class `CombatAIService`

Service for AI combat behavior

#### `get_ai_action`

Get AI action for combatant

**Signature:** `get_ai_action(self, combat: core.systems.combat.domain.combat.Combat, combatant: core.systems.combat.domain.combat.Combatant) -> Optional[core.systems.combat.domain.combat.CombatAction]`

### class `CombatCreationService`

Service for creating combat encounters

#### `add_combatant`

Add combatant to combat

**Signature:** `add_combatant(self, combat_id: str, combatant: core.systems.combat.domain.combat.Combatant) -> bool`

#### `create_combat`

Create a new combat encounter

**Signature:** `create_combat(self, combat_id: str, name: str, location: str, environment: Optional[Dict[str, Any]] = None) -> Optional[core.systems.combat.domain.combat.Combat]`

#### `create_combatant`

Create a new combatant

**Signature:** `create_combatant(self, combatant_id: str, name: str, team: str, stats: core.systems.combat.domain.combat.CombatStats, controller: str = 'player', position: Tuple[int, int] = (0, 0), abilities: Optional[List[str]] = None, ai_type: str = 'balanced') -> Optional[core.systems.combat.domain.combat.Combatant]`

### class `CombatExecutionService`

Service for executing combat actions

#### `execute_action`

Execute a combat action

**Signature:** `execute_action(self, combat_id: str, action: core.systems.combat.domain.combat.CombatAction) -> Dict[str, Any]`

#### `start_combat`

Start combat encounter

**Signature:** `start_combat(self, combat_id: str) -> bool`

### class `CombatStatusService`

Service for combat status and information

#### `get_combat_history`

Get combat history

**Signature:** `get_combat_history(self, combat_id: str, limit: int = 50) -> List[Dict[str, Any]]`

#### `get_combat_status`

Get complete combat status

**Signature:** `get_combat_status(self, combat_id: str) -> Optional[Dict[str, Any]]`

#### `get_combatant_status`

Get combatant status

**Signature:** `get_combatant_status(self, combat_id: str, combatant_id: str) -> Optional[Dict[str, Any]]`

### Functions

## `combat_service_bdd.py`

Combat Service BDD Implementation

### Classes

### class `CombatAIService`

Simplified combat AI service for BDD

#### `get_enemy_action`

Get enemy action

**Signature:** `get_enemy_action(self, enemy: Dict, character: Dict) -> Dict`

### class `CombatCreationService`

Simplified combat creation service for BDD

#### `create_combat`

Create combat encounter

**Signature:** `create_combat(self, character_id: str, enemy_id: str) -> Dict`

### class `CombatExecutionService`

Simplified combat execution service for BDD

#### `calculate_damage`

Calculate damage

**Signature:** `calculate_damage(self, attacker: Dict, defender: Dict) -> Dict`

#### `resolve_combat`

Resolve combat

**Signature:** `resolve_combat(self, character: Dict, enemy: Dict) -> Dict`

### class `CombatStatusService`

Simplified combat status service for BDD

#### `get_combat_status`

Get combat status

**Signature:** `get_combat_status(self, combat_id: str) -> Dict`

### Functions

### `calculate_damage`

Calculate damage for BDD testing

**Signature:** `calculate_damage(attacker: dict, defender: dict, attack_type: str = 'basic') -> dict`

### `resolve_combat`

Resolve combat between character and enemy (BDD compliant)

**Signature:** `resolve_combat(character: dict, enemy: dict) -> dict`

## `combat.py`

Domain entities for combat system

### Classes

### class `Attack`

Attack definition

#### `calculate_damage`

Calculate damage against defender

**Signature:** `calculate_damage(self, attacker_stats: core.systems.combat.domain.combat.CombatStats, defender_stats: core.systems.combat.domain.combat.CombatStats) -> int`

#### `can_use`

Check if attack can be used with given stats

**Signature:** `can_use(self, stats: core.systems.combat.domain.combat.CombatStats) -> bool`

#### `get_summary`

Get attack summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

### class `AttackType`

Types of attacks

### class `Combat`

Combat encounter

#### `add_combatant`

Add combatant to combat

**Signature:** `add_combatant(self, combatant: core.systems.combat.domain.combat.Combatant) -> None`

#### `add_log_entry`

Add entry to combat log

**Signature:** `add_log_entry(self, entry: core.systems.combat.domain.combat.CombatLog) -> None`

#### `check_victory_conditions`

Check if victory or defeat conditions are met

**Signature:** `check_victory_conditions(self) -> Optional[str]`

#### `end_combat`

End combat with result

**Signature:** `end_combat(self, result: str) -> bool`

#### `get_alive_combatants`

Get all alive combatants

**Signature:** `get_alive_combatants(self) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_alive_combatants_by_team`

Get alive combatants by team

**Signature:** `get_alive_combatants_by_team(self, team: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatant`

Get combatant by ID

**Signature:** `get_combatant(self, combatant_id: str) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants_by_team`

Get combatants by team

**Signature:** `get_combatants_by_team(self, team: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_current_combatant`

Get current combatant

**Signature:** `get_current_combatant(self) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `get_recent_logs`

Get recent log entries

**Signature:** `get_recent_logs(self, limit: int = 10) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `get_summary`

Get combat summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `next_turn`

Move to next turn

**Signature:** `next_turn(self) -> bool`

#### `remove_combatant`

Remove combatant from combat

**Signature:** `remove_combatant(self, combatant_id: str) -> bool`

#### `start_combat`

Start combat

**Signature:** `start_combat(self) -> bool`

### class `CombatAction`

Action taken in combat

#### `get_summary`

Get action summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

### class `CombatLog`

Combat log entry

#### `get_summary`

Get log entry summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

### class `CombatState`

Combat states

### class `CombatStats`

Combat statistics for a character

#### `get_health_percentage`

Get health as percentage

**Signature:** `get_health_percentage(self) -> float`

#### `get_mana_percentage`

Get mana as percentage

**Signature:** `get_mana_percentage(self) -> float`

#### `heal`

Heal character and return actual amount healed

**Signature:** `heal(self, amount: int) -> int`

#### `is_alive`

Check if character is alive

**Signature:** `is_alive(self) -> bool`

#### `restore_mana`

Restore mana and return actual amount restored

**Signature:** `restore_mana(self, amount: int) -> int`

#### `take_damage`

Apply damage and return actual damage dealt

**Signature:** `take_damage(self, damage: int) -> int`

#### `use_mana`

Use mana and return success

**Signature:** `use_mana(self, amount: int) -> bool`

### class `Combatant`

Combat participant

#### `add_status_effect`

Add status effect

**Signature:** `add_status_effect(self, effect: core.systems.combat.domain.combat.StatusEffectInstance) -> None`

#### `can_act`

Check if combatant can act

**Signature:** `can_act(self) -> bool`

#### `get_distance_to`

Calculate distance to another combatant

**Signature:** `get_distance_to(self, other: 'Combatant') -> float`

#### `get_status_effects`

Get active status effect types

**Signature:** `get_status_effects(self) -> List[str]`

#### `get_summary`

Get combatant summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `has_status_effect`

Check if has specific status effect

**Signature:** `has_status_effect(self, effect: str) -> bool`

#### `is_ai_controlled`

Check if combatant is AI controlled

**Signature:** `is_ai_controlled(self) -> bool`

#### `is_alive`

Check if combatant is alive

**Signature:** `is_alive(self) -> bool`

#### `is_player_controlled`

Check if combatant is player controlled

**Signature:** `is_player_controlled(self) -> bool`

#### `move_to`

Move combatant to position

**Signature:** `move_to(self, position: Tuple[int, int]) -> None`

#### `remove_status_effect`

Remove status effect by type

**Signature:** `remove_status_effect(self, effect: str) -> bool`

#### `update_status_effects`

Update status effects and return expired ones

**Signature:** `update_status_effects(self) -> List[str]`

### class `DamageType`

Types of damage

### class `StatusEffect`

Status effects in combat

### class `StatusEffectInstance`

Instance of a status effect on a character

#### `decrement_duration`

Decrement duration and return if expired

**Signature:** `decrement_duration(self) -> bool`

#### `get_summary`

Get effect summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `is_expired`

Check if effect has expired

**Signature:** `is_expired(self) -> bool`

### Functions

## `repositories.py`

Repository interfaces for combat system

### Classes

### class `AttackRepositoryInterface`

Interface for attack data persistence

#### `attack_exists`

Check if attack exists

**Signature:** `attack_exists(self, attack_id: str) -> bool`

#### `delete_attack`

Delete attack from repository

**Signature:** `delete_attack(self, attack_id: str) -> bool`

#### `get_all_attacks`

Get all attacks

**Signature:** `get_all_attacks(self) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_damage_type`

Get attacks by damage type

**Signature:** `get_attacks_by_damage_type(self, damage_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `get_attacks_by_type`

Get attacks by type

**Signature:** `get_attacks_by_type(self, attack_type: str) -> List[core.systems.combat.domain.combat.Attack]`

#### `load_attack`

Load attack from repository

**Signature:** `load_attack(self, attack_id: str) -> Optional[core.systems.combat.domain.combat.Attack]`

#### `save_attack`

Save attack to repository

**Signature:** `save_attack(self, attack: core.systems.combat.domain.combat.Attack) -> bool`

### class `CombatActionRepositoryInterface`

Interface for combat action data persistence

#### `delete_action`

Delete combat action

**Signature:** `delete_action(self, combat_id: str, action_id: str) -> bool`

#### `get_actions`

Get combat actions

**Signature:** `get_actions(self, combat_id: str, limit: int = 100) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `get_actions_by_combatant`

Get actions by combatant

**Signature:** `get_actions_by_combatant(self, combat_id: str, combatant_id: str, limit: int = 50) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `get_actions_by_round`

Get actions by round

**Signature:** `get_actions_by_round(self, combat_id: str, round_number: int) -> List[core.systems.combat.domain.combat.CombatAction]`

#### `save_action`

Save combat action

**Signature:** `save_action(self, combat_id: str, action: core.systems.combat.domain.combat.CombatAction) -> bool`

### class `CombatLogRepositoryInterface`

Interface for combat log data persistence

#### `delete_log_entries`

Delete all log entries for combat

**Signature:** `delete_log_entries(self, combat_id: str) -> bool`

#### `get_entries_by_combatant`

Get log entries by combatant

**Signature:** `get_entries_by_combatant(self, combat_id: str, combatant_id: str, limit: int = 50) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `get_entries_by_round`

Get log entries by round

**Signature:** `get_entries_by_round(self, combat_id: str, round_number: int) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `get_log_entries`

Get combat log entries

**Signature:** `get_log_entries(self, combat_id: str, limit: int = 100) -> List[core.systems.combat.domain.combat.CombatLog]`

#### `save_log_entry`

Save combat log entry

**Signature:** `save_log_entry(self, combat_id: str, entry: core.systems.combat.domain.combat.CombatLog) -> bool`

### class `CombatRepositoryInterface`

Interface for combat data persistence

#### `combat_exists`

Check if combat exists

**Signature:** `combat_exists(self, combat_id: str) -> bool`

#### `delete_combat`

Delete combat from repository

**Signature:** `delete_combat(self, combat_id: str) -> bool`

#### `get_active_combats`

Get all active combats

**Signature:** `get_active_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_all_combats`

Get all combats

**Signature:** `get_all_combats(self) -> List[core.systems.combat.domain.combat.Combat]`

#### `get_combats_by_location`

Get combats by location

**Signature:** `get_combats_by_location(self, location: str) -> List[core.systems.combat.domain.combat.Combat]`

#### `load_combat`

Load combat from repository

**Signature:** `load_combat(self, combat_id: str) -> Optional[core.systems.combat.domain.combat.Combat]`

#### `save_combat`

Save combat to repository

**Signature:** `save_combat(self, combat: core.systems.combat.domain.combat.Combat) -> bool`

### class `CombatSystemRepositoryInterface`

Combined interface for all combat system repositories

#### `get_action_repository`

Get action repository

**Signature:** `get_action_repository(self) -> core.systems.combat.interfaces.repositories.CombatActionRepositoryInterface`

#### `get_attack_repository`

Get attack repository

**Signature:** `get_attack_repository(self) -> core.systems.combat.interfaces.repositories.AttackRepositoryInterface`

#### `get_combat_repository`

Get combat repository

**Signature:** `get_combat_repository(self) -> core.systems.combat.interfaces.repositories.CombatRepositoryInterface`

#### `get_combatant_repository`

Get combatant repository

**Signature:** `get_combatant_repository(self) -> core.systems.combat.interfaces.repositories.CombatantRepositoryInterface`

#### `get_log_repository`

Get log repository

**Signature:** `get_log_repository(self) -> core.systems.combat.interfaces.repositories.CombatLogRepositoryInterface`

### class `CombatantRepositoryInterface`

Interface for combatant data persistence

#### `combatant_exists`

Check if combatant exists in combat

**Signature:** `combatant_exists(self, combat_id: str, combatant_id: str) -> bool`

#### `delete_combatant`

Delete combatant from combat

**Signature:** `delete_combatant(self, combat_id: str, combatant_id: str) -> bool`

#### `get_alive_combatants`

Get alive combatants in a combat

**Signature:** `get_alive_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants`

Get all combatants in a combat

**Signature:** `get_combatants(self, combat_id: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `get_combatants_by_team`

Get combatants by team

**Signature:** `get_combatants_by_team(self, combat_id: str, team: str) -> List[core.systems.combat.domain.combat.Combatant]`

#### `load_combatant`

Load combatant from combat

**Signature:** `load_combatant(self, combat_id: str, combatant_id: str) -> Optional[core.systems.combat.domain.combat.Combatant]`

#### `save_combatant`

Save combatant to combat

**Signature:** `save_combatant(self, combat_id: str, combatant: core.systems.combat.domain.combat.Combatant) -> bool`

### Functions
