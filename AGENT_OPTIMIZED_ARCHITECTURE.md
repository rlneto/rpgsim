# LLM Agent-Optimized RPGSim Architecture

## Overview
This architecture is specifically designed for LLM agents like GPT-4, prioritizing:
- **Deterministic behavior** over user experience
- **Explicit code** over clever abstractions
- **Agent productivity** over human usability
- **Code generation efficiency** over feature richness
- **Predictable patterns** over innovative solutions

## Core Design Principles for LLM Agents

### 1. **Explicit State Management** (Priority: 1)
- All state changes are visible and traceable
- No hidden magic or reactive behavior
- State mutations are explicit functions
- Every function has predictable input/output

### 2. **Deterministic Functions** (Priority: 2)
- Pure functions wherever possible
- No random behavior in core logic
- Input always produces same output
- Side effects are explicitly declared

### 3. **Type Safety & Validation** (Priority: 3)
- Strong typing throughout
- Input validation at function boundaries
- Clear error messages with specific guidance
- Type hints for all public APIs

### 4. **Minimal Dependencies** (Priority: 4)
- Prefer built-in Python libraries
- Simple, predictable dependencies
- Avoid complex framework magic
- Minimal version conflicts

### 5. **Linear Execution Flow** (Priority: 5)
- No hidden event loops
- Explicit function call chains
- No coroutines or async complexity
- Straight-line execution paths

---

## Agent-Optimized Project Structure

```
rpgsim/
├── core/                    # Core deterministic systems
│   ├── __init__.py
│   ├── models.py            # Data models with Pydantic
│   ├── state.py             # Explicit state management
│   ├── validation.py        # Input validation functions
│   └── constants.py         # Game constants and enums
├── systems/                 # Game systems (explicit functions)
│   ├── __init__.py
│   ├── character.py         # Character system
│   ├── combat.py           # Combat system
│   ├── quest.py            # Quest system
│   ├── inventory.py        # Inventory management
│   ├── save_load.py        # Save/load system
│   └── world.py            # World management
├── ui/                      # Simple UI (curses-based)
│   ├── __init__.py
│   ├── renderer.py          # Explicit UI rendering
│   ├── components.py        # UI components
│   └── input.py            # Input handling
├── data/                    # Game data (JSON)
│   ├── characters.json
│   ├── items.json
│   ├── quests.json
│   ├── enemies.json
│   └── world.json
├── tests/                    # Deterministic tests
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── tools/                    # Agent development tools
│   ├── code_generator.py    # Code generation helpers
│   ├── validator.py         # Code validation
│   └── formatters.py       # Code formatting
├── main.py                  # Entry point
├── config.py                # Configuration
└── requirements.txt         # Minimal dependencies
```

---

## Core Data Models (Deterministic)

### 1. Character Model
```python
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Optional
from enum import Enum

class CharacterClass(str, Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    # ... 20 more classes

class CharacterStats(BaseModel):
    strength: int = Field(ge=1, le=20, description="Strength stat (1-20)")
    dexterity: int = Field(ge=1, le=20, description="Dexterity stat (1-20)")
    intelligence: int = Field(ge=1, le=20, description="Intelligence stat (1-20)")
    wisdom: int = Field(ge=1, le=20, description="Wisdom stat (1-20)")
    charisma: int = Field(ge=1, le=20, description="Charisma stat (1-20)")
    constitution: int = Field(ge=1, le=20, description="Constitution stat (1-20)")

class Character(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Character name")
    class_type: CharacterClass = Field(description="Character class")
    level: int = Field(ge=1, le=100, description="Character level (1-100)")
    stats: CharacterStats = Field(description="Character stats")
    hp: int = Field(ge=0, description="Current hit points")
    max_hp: int = Field(ge=1, description="Maximum hit points")
    gold: int = Field(ge=0, description="Gold amount")
    abilities: List[str] = Field(default_factory=list, description="Character abilities")
    inventory: List[str] = Field(default_factory=list, description="Inventory items")
    
    @validator('hp')
    def hp_not_exceed_max(cls, v, values):
        if 'max_hp' in values and v > values['max_hp']:
            return values['max_hp']
        return v
    
    @validator('max_hp')
    def max_hp_positive(cls, v):
        if v <= 0:
            raise ValueError('Max HP must be positive')
        return v
```

### 2. Game State Model
```python
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class GameState(BaseModel):
    """Explicit game state - no hidden magic"""
    player: Character = Field(description="Player character")
    current_location: str = Field(default="start", description="Current location")
    world_time: int = Field(default=0, description="World time in seconds")
    quests_active: List[str] = Field(default_factory=list, description="Active quest IDs")
    quests_completed: List[str] = Field(default_factory=list, description="Completed quest IDs")
    inventory: List[str] = Field(default_factory=list, description="Inventory item IDs")
    known_locations: List[str] = Field(default_factory=list, description="Known location IDs")
    game_version: str = Field(default="1.0.0", description="Game version")
    last_save: Optional[datetime] = Field(default=None, description="Last save timestamp")
    
    def update_location(self, new_location: str) -> 'GameState':
        """Explicit state update - no magic"""
        self.current_location = new_location
        if new_location not in self.known_locations:
            self.known_locations.append(new_location)
        return self
    
    def add_quest(self, quest_id: str) -> 'GameState':
        """Explicit quest addition"""
        if quest_id not in self.quests_active and quest_id not in self.quests_completed:
            self.quests_active.append(quest_id)
        return self
    
    def complete_quest(self, quest_id: str) -> 'GameState':
        """Explicit quest completion"""
        if quest_id in self.quests_active:
            self.quests_active.remove(quest_id)
            self.quests_completed.append(quest_id)
        return self
```

---

## Explicit System Functions

### 1. Character System (Deterministic)
```python
# core/systems/character.py
from typing import List, Dict, Optional
from core.models import Character, CharacterClass, CharacterStats
from core.validation import validate_character_name, validate_stats

def create_character(name: str, class_type: CharacterClass) -> Character:
    """
    Create a new character with default stats for class.
    
    Args:
        name: Character name (1-50 chars)
        class_type: Character class
        
    Returns:
        Created character
        
    Raises:
        ValueError: If name is invalid
    """
    validate_character_name(name)
    
    # Explicit default stats for each class
    default_stats = get_default_stats_for_class(class_type)
    
    # Calculate HP based on class and constitution
    max_hp = calculate_max_hp(class_type, default_stats.constitution)
    
    # Get default abilities for class
    abilities = get_default_abilities_for_class(class_type)
    
    return Character(
        name=name,
        class_type=class_type,
        level=1,
        stats=default_stats,
        hp=max_hp,
        max_hp=max_hp,
        gold=100,  # Default starting gold
        abilities=abilities,
        inventory=[]
    )

def get_default_stats_for_class(class_type: CharacterClass) -> CharacterStats:
    """
    Get default stats for character class.
    Deterministic - always returns same values.
    """
    stats_map = {
        CharacterClass.WARRIOR: CharacterStats(
            strength=15, dexterity=10, intelligence=8,
            wisdom=10, charisma=8, constitution=14
        ),
        CharacterClass.MAGE: CharacterStats(
            strength=8, dexterity=12, intelligence=16,
            wisdom=14, charisma=10, constitution=8
        ),
        CharacterClass.ROGUE: CharacterStats(
            strength=10, dexterity=16, intelligence=12,
            wisdom=10, charisma=12, constitution=8
        ),
        # ... 20 more classes
    }
    
    return stats_map.get(class_type, CharacterStats(
        strength=10, dexterity=10, intelligence=10,
        wisdom=10, charisma=10, constitution=10
    ))

def calculate_max_hp(class_type: CharacterClass, constitution: int) -> int:
    """
    Calculate max HP based on class and constitution.
    Deterministic formula.
    """
    base_hp_map = {
        CharacterClass.WARRIOR: 12,
        CharacterClass.MAGE: 6,
        CharacterClass.ROGUE: 8,
        # ... 20 more classes
    }
    
    base_hp = base_hp_map.get(class_type, 10)
    constitution_bonus = (constitution - 10) // 2  # 1 bonus per 2 points
    
    return max(1, base_hp + constitution_bonus)

def get_default_abilities_for_class(class_type: CharacterClass) -> List[str]:
    """
    Get default abilities for character class.
    Deterministic - always returns same list.
    """
    abilities_map = {
        CharacterClass.WARRIOR: ["Attack", "Defend", "Power Strike", "Shield Bash"],
        CharacterClass.MAGE: ["Attack", "Defend", "Fireball", "Magic Missile", "Teleport"],
        CharacterClass.ROGUE: ["Attack", "Defend", "Backstab", "Pick Lock", "Stealth"],
        # ... 20 more classes
    }
    
    return abilities_map.get(class_type, ["Attack", "Defend"])

def level_up_character(character: Character) -> Character:
    """
    Level up character by 1.
    Explicit stat increases - no randomness.
    """
    character.level += 1
    
    # Explicit stat increases per class
    stat_increases = get_stat_increases_for_class(character.class_type)
    character.stats.strength += stat_increases.strength
    character.stats.dexterity += stat_increases.dexterity
    character.stats.intelligence += stat_increases.intelligence
    character.stats.wisdom += stat_increases.wisdom
    character.stats.charisma += stat_increases.charisma
    character.stats.constitution += stat_increases.constitution
    
    # Recalculate HP with new constitution
    new_max_hp = calculate_max_hp(character.class_type, character.stats.constitution)
    hp_increase = new_max_hp - character.max_hp
    character.max_hp = new_max_hp
    character.hp = character.hp + hp_increase
    
    # Learn new abilities
    new_abilities = get_abilities_for_level(character.class_type, character.level)
    for ability in new_abilities:
        if ability not in character.abilities:
            character.abilities.append(ability)
    
    return character

def get_stat_increases_for_class(class_type: CharacterClass) -> CharacterStats:
    """
    Get stat increases per level for class.
    Deterministic - always same increases.
    """
    increase_map = {
        CharacterClass.WARRIOR: CharacterStats(
            strength=2, dexterity=1, intelligence=0,
            wisdom=0, charisma=0, constitution=2
        ),
        CharacterClass.MAGE: CharacterStats(
            strength=0, dexterity=1, intelligence=2,
            wisdom=2, charisma=1, constitution=0
        ),
        CharacterClass.ROGUE: CharacterStats(
            strength=1, dexterity=2, intelligence=1,
            wisdom=0, charisma=1, constitution=0
        ),
        # ... 20 more classes
    }
    
    return increase_map.get(class_type, CharacterStats(
        strength=1, dexterity=1, intelligence=1,
        wisdom=1, charisma=1, constitution=1
    ))
```

### 2. Combat System (Deterministic)
```python
# core/systems/combat.py
from typing import Tuple, Optional, List
from core.models import Character, GameState
from core.validation import validate_combat_participants

def calculate_attack_damage(attacker: Character, defender: Character) -> int:
    """
    Calculate attack damage.
    Deterministic formula - no randomness.
    
    Args:
        attacker: Attacking character
        defender: Defending character
        
    Returns:
        Damage amount (always >= 0)
    """
    validate_combat_participants(attacker, defender)
    
    # Base damage from strength
    base_damage = attacker.stats.strength
    
    # Class-specific damage multipliers
    damage_multiplier = get_damage_multiplier(attacker.class_type)
    
    # Apply multiplier
    multiplied_damage = int(base_damage * damage_multiplier)
    
    # Defense reduction based on defender's dexterity
    defense_reduction = defender.stats.dexterity // 3
    
    # Final damage (minimum 1)
    final_damage = max(1, multiplied_damage - defense_reduction)
    
    return final_damage

def get_damage_multiplier(class_type: CharacterClass) -> float:
    """
    Get damage multiplier for character class.
    Deterministic - always same multiplier.
    """
    multiplier_map = {
        CharacterClass.WARRIOR: 1.5,
        CharacterClass.MAGE: 1.0,
        CharacterClass.ROGUE: 1.3,
        # ... 20 more classes
    }
    
    return multiplier_map.get(class_type, 1.0)

def apply_damage(character: Character, damage: int) -> Character:
    """
    Apply damage to character.
    Explicit state change - no hidden effects.
    
    Args:
        character: Character to damage
        damage: Damage amount (>= 0)
        
    Returns:
        Updated character
    """
    if damage < 0:
        raise ValueError("Damage cannot be negative")
    
    character.hp = max(0, character.hp - damage)
    return character

def is_character_defeated(character: Character) -> bool:
    """
    Check if character is defeated.
    Deterministic check.
    """
    return character.hp <= 0

def execute_combat_round(attacker: Character, defender: Character) -> Tuple[Character, Character, str]:
    """
    Execute one combat round.
    Explicit combat mechanics - no hidden effects.
    
    Args:
        attacker: Attacking character
        defender: Defending character
        
    Returns:
        Tuple of (updated_attacker, updated_defender, combat_log)
    """
    validate_combat_participants(attacker, defender)
    
    # Calculate and apply damage
    damage = calculate_attack_damage(attacker, defender)
    apply_damage(defender, damage)
    
    # Create combat log entry
    log_entry = f"{attacker.name} deals {damage} damage to {defender.name}"
    
    # Check if defender is defeated
    if is_character_defeated(defender):
        log_entry += f". {defender.name} is defeated!"
    
    return attacker, defender, log_entry

def resolve_combat(player: Character, enemy: Character) -> Tuple[Character, List[str], bool]:
    """
    Resolve complete combat encounter.
    Deterministic combat resolution.
    
    Args:
        player: Player character
        enemy: Enemy character
        
    Returns:
        Tuple of (updated_player, combat_log, player_victory)
    """
    validate_combat_participants(player, enemy)
    
    combat_log = []
    combat_log.append(f"Combat started: {player.name} vs {enemy.name}")
    
    # Simple turn-based combat
    round_number = 1
    while not is_character_defeated(player) and not is_character_defeated(enemy):
        combat_log.append(f"--- Round {round_number} ---")
        
        # Player attacks
        player, enemy, player_log = execute_combat_round(player, enemy)
        combat_log.append(player_log)
        
        # Check if enemy is defeated
        if is_character_defeated(enemy):
            combat_log.append(f"{player.name} wins!")
            break
        
        # Enemy attacks
        enemy, player, enemy_log = execute_combat_round(enemy, player)
        combat_log.append(enemy_log)
        
        # Check if player is defeated
        if is_character_defeated(player):
            combat_log.append(f"{enemy.name} wins!")
            break
        
        round_number += 1
    
    player_victory = not is_character_defeated(player)
    return player, combat_log, player_victory
```

---

## Simple UI System (Curses-based)

### 1. Explicit UI Renderer
```python
# ui/renderer.py
import curses
from typing import Optional, Tuple
from core.models import Character, GameState

class UIRenderer:
    """
    Explicit UI renderer using curses.
    No reactive magic - explicit rendering only.
    """
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)  # Hide cursor
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Title
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Success
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)    # Error
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
        
    def clear(self) -> None:
        """Explicit screen clearing."""
        self.stdscr.clear()
    
    def refresh(self) -> None:
        """Explicit screen refresh."""
        self.stdscr.refresh()
    
    def render_title(self, title: str, y: int = 0, x: int = 0) -> None:
        """
        Render title at position.
        Explicit rendering - no auto-positioning.
        """
        title_text = f" {title} "
        self.stdscr.addstr(y, x, title_text, curses.color_pair(1))
    
    def render_character_info(self, character: Character, y: int = 2, x: int = 2) -> None:
        """
        Render character information.
        Explicit positioning and formatting.
        """
        self.stdscr.addstr(y, x, f"Name: {character.name}")
        self.stdscr.addstr(y+1, x, f"Class: {character.class_type.value}")
        self.stdscr.addstr(y+2, x, f"Level: {character.level}")
        self.stdscr.addstr(y+3, x, f"HP: {character.hp}/{character.max_hp}")
        self.stdscr.addstr(y+4, x, f"Gold: {character.gold}")
        
        # Stats
        self.stdscr.addstr(y+6, x, "Stats:")
        self.stdscr.addstr(y+7, x, f"  STR: {character.stats.strength}")
        self.stdscr.addstr(y+8, x, f"  DEX: {character.stats.dexterity}")
        self.stdscr.addstr(y+9, x, f"  INT: {character.stats.intelligence}")
        self.stdscr.addstr(y+10, x, f"  WIS: {character.stats.wisdom}")
        self.stdscr.addstr(y+11, x, f"  CHA: {character.stats.charisma}")
        self.stdscr.addstr(y+12, x, f"  CON: {character.stats.constitution}")
    
    def render_inventory(self, inventory: List[str], y: int = 2, x: int = 40) -> None:
        """
        Render inventory list.
        Explicit item rendering - no auto-formatting.
        """
        self.stdscr.addstr(y, x, "Inventory:")
        for i, item in enumerate(inventory[:10]):  # Max 10 items visible
            item_text = f"{i+1}. {item}"
            self.stdscr.addstr(y+1+i, x, item_text)
    
    def render_game_state(self, game_state: GameState) -> None:
        """
        Render complete game state.
        Explicit rendering of all components.
        """
        self.clear()
        
        # Title
        self.render_title("RPGSim - Agent Optimized", 0, 0)
        
        # Character info
        self.render_character_info(game_state.player, 2, 2)
        
        # Inventory
        self.render_inventory(game_state.player.inventory, 2, 40)
        
        # Location info
        self.stdscr.addstr(20, 2, f"Location: {game_state.current_location}")
        self.stdscr.addstr(21, 2, f"Time: {game_state.world_time}")
        self.stdscr.addstr(22, 2, f"Active Quests: {len(game_state.quests_active)}")
        
        self.refresh()
    
    def render_menu(self, title: str, options: List[str], selected: int = 0) -> int:
        """
        Render menu and return selection.
        Explicit menu handling - no auto-navigation.
        """
        while True:
            self.clear()
            self.render_title(title, 0, 0)
            
            # Render options
            for i, option in enumerate(options):
                marker = ">> " if i == selected else "   "
                option_text = f"{marker}{option}"
                self.stdscr.addstr(2 + i, 10, option_text)
            
            # Instructions
            self.stdscr.addstr(15, 5, "UP/DOWN: Navigate  ENTER: Select  ESC: Exit")
            
            self.refresh()
            
            # Get input
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(options)
            elif key == ord('\n') or key == ord('\r'):
                return selected
            elif key == 27:  # ESC
                return -1
```

### 2. Explicit Input Handler
```python
# ui/input.py
import curses
from typing import Optional, Callable

class InputHandler:
    """
    Explicit input handler.
    No complex event system - simple key handling.
    """
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.key_handlers = {}  # Explicit key -> handler mapping
    
    def register_key_handler(self, key: int, handler: Callable) -> None:
        """
        Register handler for specific key.
        Explicit registration - no automatic binding.
        """
        self.key_handlers[key] = handler
    
    def get_key(self) -> Optional[int]:
        """
        Get single key press.
        Explicit key reading - no buffering magic.
        """
        return self.stdscr.getch()
    
    def handle_key(self, key: int) -> bool:
        """
        Handle key press.
        Explicit handling - no automatic dispatch.
        
        Returns:
            True if key was handled, False otherwise
        """
        if key in self.key_handlers:
            self.key_handlers[key]()
            return True
        return False
    
    def wait_for_key(self) -> int:
        """
        Wait for any key press.
        Explicit waiting - no timeout magic.
        """
        return self.stdscr.getch()
```

---

## Agent Development Tools

### 1. Code Generator Helper
```python
# tools/code_generator.py
from typing import List, Dict, Any
import os

class CodeGenerator:
    """Helper class for LLM agents to generate code."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
    
    def generate_system_file(self, system_name: str, functions: List[Dict[str, Any]]) -> str:
        """
        Generate system file with explicit functions.
        Template for agent code generation.
        """
        template = f'''# core/systems/{system_name.lower()}.py
"""
        
        # Add imports
        template += '''
from typing import List, Dict, Optional, Tuple, Any
from core.models import Character, GameState
from core.validation import validate_character
'''
        
        # Add functions
        for func in functions:
            template += f'''
def {func['name']}({func['params']}){func['return_type']}:
    """
    {func['description']}
    
    Args:
{func['args_doc']}
    Returns:
        {func['return_doc']}
    
    Raises:
        {func['raises_doc']}
    """
    # TODO: Implement {func['name']}
    pass
'''
        
        return template
    
    def save_system_file(self, system_name: str, content: str) -> None:
        """Save system file to disk."""
        file_path = os.path.join(self.base_path, "core", "systems", f"{system_name.lower()}.py")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    def generate_test_file(self, system_name: str, test_functions: List[Dict[str, Any]]) -> str:
        """Generate test file for system."""
        template = f'''# tests/unit/test_{system_name.lower()}.py
import pytest
from core.systems.{system_name.lower()} import *
from core.models import Character, CharacterClass, GameState
from tests.fixtures import *
'''
        
        # Add test functions
        for test in test_functions:
            template += f'''
@pytest.mark.unit
def test_{test['name']}():
    """
    Test {test['description']}.
    """
    # TODO: Implement test {test['name']}
    pass
'''
        
        return template

# Pre-defined templates for common patterns
CHARACTER_CLASS_TEMPLATE = {
    'name': 'class_name',
    'description': 'Get default stats for character class',
    'params': 'class_type: CharacterClass',
    'return_type': ' -> CharacterStats',
    'args_doc': '''        class_type: Character class
''',
    'return_doc': '''        CharacterStats: Default stats for class
''',
    'raises_doc': '''        ValueError: If class_type is invalid
''',
}

COMBAT_FUNCTION_TEMPLATE = {
    'name': 'calculate_damage',
    'description': 'Calculate combat damage',
    'params': 'attacker: Character, defender: Character',
    'return_type': ' -> int',
    'args_doc': '''        attacker: Attacking character
        defender: Defending character
''',
    'return_doc': '''        int: Damage amount
''',
    'raises_doc': '''        ValueError: If characters are invalid
''',
}
```

### 2. Code Validator
```python
# tools/validator.py
import ast
import os
from typing import List, Dict, Any

class CodeValidator:
    """Validate agent-generated code for compliance."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate Python file for agent compliance."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Reset errors
            self.errors = []
            self.warnings = []
            
            # Validate structure
            self._validate_structure(tree, file_path)
            self._validate_imports(tree, file_path)
            self._validate_functions(tree, file_path)
            self._validate_types(tree, file_path)
            
            return {
                'valid': len(self.errors) == 0,
                'errors': self.errors,
                'warnings': self.warnings,
                'file_path': file_path
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Failed to parse {file_path}: {str(e)}"],
                'warnings': [],
                'file_path': file_path
            }
    
    def _validate_structure(self, tree: ast.AST, file_path: str) -> None:
        """Validate code structure for agent compliance."""
        # Check for async functions (not allowed)
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                self.errors.append(f"Async functions not allowed: {node.name} at line {node.lineno}")
            
            # Check for complex comprehensions (discouraged)
            if isinstance(node, ast.comprehension):
                self.warnings.append(f"Complex comprehension at line {node.lineno}")
    
    def _validate_imports(self, tree: ast.AST, file_path: str) -> None:
        """Validate imports for minimal dependencies."""
        allowed_imports = {
            'typing', 'core', 'tests', 'os', 'json',
            'pydantic', 'datetime', 'enum'
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in allowed_imports:
                        self.errors.append(f"Disallowed import: {alias.name}")
            
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module not in allowed_imports:
                    self.errors.append(f"Disallowed import from: {node.module}")
    
    def _validate_functions(self, tree: ast.AST, file_path: str) -> None:
        """Validate functions for explicit behavior."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for *args (discouraged)
                for arg in node.args.args:
                    if arg.arg == 'args':
                        self.warnings.append(f"Function {node.name} uses *args")
                
                # Check for **kwargs (discouraged)
                for arg in node.args.kwonlyargs:
                    if arg.arg == 'kwargs':
                        self.warnings.append(f"Function {node.name} uses **kwargs")
                
                # Check for return type annotation
                if not node.returns:
                    self.errors.append(f"Function {node.name} missing return type annotation")
    
    def _validate_types(self, tree: ast.AST, file_path: str) -> None:
        """Validate type annotations."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check function parameter types
                for arg in node.args.args:
                    if arg.annotation is None:
                        self.errors.append(f"Parameter {arg.arg} in function {node.name} missing type annotation")
                
                # Check for docstring
                if not ast.get_docstring(node):
                    self.errors.append(f"Function {node.name} missing docstring")

# Validation rules for agents
AGENT_RULES = {
    'no_async': True,
    'no_magic': True,
    'explicit_types': True,
    'minimal_imports': True,
    'deterministic': True,
    'docstrings_required': True,
    'type_hints_required': True
}
```

---

## Updated Requirements.txt (Agent-Optimized)

```txt
# LLM Agent-Optimized RPGSim Requirements

# Core - Minimal, explicit dependencies
pydantic>=2.0.0              # Explicit data validation
typing-extensions>=4.0.0      # Enhanced typing support

# Testing - Simple, explicit testing
pytest>=7.0.0                 # Simple testing framework
pytest-cov>=4.0.0            # Coverage reporting

# Code quality - Explicit rules
black>=23.0.0                  # Simple formatting
isort>=5.12.0                  # Import sorting
mypy>=1.0.0                    # Type checking

# Documentation - Simple docs
sphinx>=5.0.0                   # Documentation
sphinx-rtd-theme>=1.2.0        # Documentation theme

# Development tools - Simple tools
pre-commit>=3.0.0               # Pre-commit hooks

# Note: curses is built-in to Python
# Note: No UI frameworks (Rich, Textual, etc.)
# Note: No complex libraries (requests, pandas, etc.)
# Note: No async frameworks (aiohttp, etc.)
```

---

## Agent Development Workflow

### 1. Generate Code
```python
# Use CodeGenerator to create new system
generator = CodeGenerator()

# Define new system
system_functions = [
    {
        'name': 'create_item',
        'description': 'Create new item',
        'params': 'name: str, item_type: str, value: int',
        'return_type': ' -> Item',
        'args_doc': 'name: Item name\nitem_type: Item type\nvalue: Item value\n',
        'return_doc': 'Item: Created item',
        'raises_doc': 'ValueError: If parameters invalid'
    }
]

# Generate code
code = generator.generate_system_file('items', system_functions)
generator.save_system_file('items', code)
```

### 2. Validate Code
```python
# Validate generated code
validator = CodeValidator()
result = validator.validate_file('core/systems/items.py')

if not result['valid']:
    print("Code validation failed:")
    for error in result['errors']:
        print(f"  - {error}")
    for warning in result['warnings']:
        print(f"  - {warning}")
else:
    print("Code validation passed!")
```

### 3. Generate Tests
```python
# Generate test code
test_functions = [
    {
        'name': 'create_item_valid',
        'description': 'Test valid item creation'
    }
]

test_code = generator.generate_test_file('items', test_functions)
with open('tests/unit/test_items.py', 'w') as f:
    f.write(test_code)
```

### 4. Run Tests
```bash
# Simple, explicit test command
python -m pytest tests/ -v --cov=core --cov-fail-under=90
```

---

## Agent Success Metrics

### 1. **Code Generation Success Rate**
- Target: 95% of generated code compiles without syntax errors
- Target: 90% of generated code passes validation
- Target: 85% of generated code passes tests

### 2. **Development Velocity**
- Target: 10 functions per hour generated
- Target: 5 test cases per hour generated
- Target: 1 new system per day implemented

### 3. **Code Quality**
- Target: 100% type annotation coverage
- Target: 100% docstring coverage
- Target: Zero Pylint errors
- Target: 90%+ test coverage

### 4. **Maintainability**
- Target: Functions < 20 lines
- Target: Cyclomatic complexity < 5
- Target: 0 "magic" functions
- Target: Explicit dependencies only

This architecture transforms RPGSim from a human-centric game to an **agent-optimized development platform**, where every design decision prioritizes LLM agent productivity over human user experience.