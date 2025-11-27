# RPGSim Agent Guide

This guide helps AI agents work effectively in the RPGSim codebase - a text-based RPG simulation inspired by Baldur's Gate.

## Project Overview

RPGSim is a comprehensive console RPG with:
- 23 unique character classes with distinct gameplay mechanics
- Turn-based combat system with tactical depth
- Modular architecture using Domain-Driven Design (DDD)
- Test-Driven Development with comprehensive test coverage
- Agent-optimized code structure with explicit validation

## Essential Commands

### Running Tests
```bash
# Run all unit tests with coverage
pytest

# Run with verbose output and coverage report
pytest --cov=game --cov-report=html --cov-report=term-missing -v

# Run specific test file
pytest tests/test_character_system.py

# Run with hypothesis statistics
pytest --hypothesis-show-statistics

# Run BDD tests
behave

# Run specific feature
behave features/character_creation.feature

# Run with specific tags
behave --tags=character
```

### Running the Game
```bash
# Start a new game
python main.py start

# Start with character details
python main.py start --name Aragorn --class Warrior

# Run quality checks
python main.py test

# Development mode with character testing
python main.py dev --character
```

### E2E Testing
```bash
# Run complete E2E test suite
./scripts/e2e_test_runner.sh
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy core/

# Linting
pylint core/
```

## Architecture & Code Organization

### Core Structure
```
rpgsim/
├── core/                   # Domain models and business logic
│   ├── models.py          # Pydantic models for all game entities
│   ├── systems/           # Game system implementations
│   │   ├── character/     # Character system with DDD layers
│   │   ├── world/         # World system
│   │   └── ...
│   └── constants.py       # Game constants
├── features/              # BDD feature files
├── tests/                 # pytest tests
├── game/                  # UI and game loop
└── scripts/              # Utility scripts
```

### Domain-Driven Design Patterns

#### Character System (Example)
- `core/systems/character/domain/character.py` - Domain entities and business rules
- `core/systems/character/services/` - Application services
- `core/systems/character/repositories/` - Data access layer
- `core/systems/character/facade.py` - Facade pattern for clean interfaces

#### Key Design Patterns
- **Facade Pattern**: Clean interfaces for complex subsystems
- **Dependency Injection**: Testable and maintainable code
- **Pydantic Models**: Explicit data validation with error messages
- **Type Hints**: Full type annotation for better agent understanding

## Code Style & Conventions

### Python Guidelines
- Use PEP 8 style guide (enforced by black)
- Always use type hints (validated by mypy)
- Use descriptive variable and function names
- Follow Domain-Driven Design patterns for complex systems
- Use pydantic models for all data structures

### Naming Conventions
- Classes: PascalCase (e.g., `CharacterSystem`)
- Functions/variables: snake_case (e.g., `create_character`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_LEVEL`)
- Private methods: prefixed with underscore (e.g., `_validate_stats`)

### File Organization
- Keep related functionality in the same module
- Use explicit imports (no `import *`)
- Group imports: standard library, third-party, local
- Use `__all__` for public API specification

## Testing Patterns

### Unit Testing
- All unit tests in `tests/` directory
- Use fixtures from `tests/conftest.py` for common test objects
- Hypothesis for property-based testing of edge cases
- 90%+ coverage requirement

### BDD Testing
- Feature files in `features/` directory
- Step implementations in `features/steps/`
- Use Given/When/Then pattern for clear test definitions
- Test all user journeys from end-to-end

### Test Fixtures
```python
# Use standard fixtures from conftest.py
@pytest.fixture
def mock_player():
    # Returns standardized mock player

@pytest.fixture
def mock_enemy():
    # Returns standardized mock enemy

@pytest.fixture
def mock_item():
    # Returns standardized mock item
```

## Key Gotchas

### Character System
- 23 character classes must be balanced (≤15% power difference)
- Each class needs unique mechanics and minimum 10 abilities
- Use `CharacterSystem` facade for operations
- Never create characters directly - use services

### Data Validation
- All models use Pydantic for validation
- Validation errors provide clear messages for debugging
- Models have `validate_assignment=True` for runtime validation
- Use `extra='forbid'` to prevent unintended fields

### Testing Gotchas
- BDD tests import from project root - ensure PYTHONPATH is set
- Some tests require hypothesis for property-based testing
- E2E tests need clean state - use fresh characters each test
- Performance requirements: startup < 1s, operations < 0.5s

### Import Patterns
- Add project root to path in main modules: `sys.path.insert(0, str(project_root))`
- Use relative imports within modules: `from .domain.character import Character`
- Use absolute imports for cross-module dependencies: `from core.systems.character import CharacterSystem`

## Important Context

### Game Balance Requirements
- No class more than 15% more powerful than others
- Content difficulty scales with player progression
- Economy provides meaningful strategic choices
- Statistical models ensure fairness

### Performance Targets
- Load times: <2 seconds
- Memory usage: <200MB
- Response time: <0.5 seconds for all actions
- Auto-save: <1 second

### Development Workflow
1. Write BDD scenarios first (features/)
2. Implement unit tests (tests/)
3. Implement domain logic (core/systems/)
4. Update facade if needed
5. Run full test suite before committing

### Agent-Specific Optimizations
- Explicit error messages for debugging
- Deterministic behavior - no randomness in core logic
- Clear separation of concerns for focused modifications
- Comprehensive test coverage for confident changes

## Useful Helper Functions

### Character Creation
```python
from core.systems.character import CharacterSystem

# Use facade for operations
character_system = CharacterSystem()
character = character_system.create_character("Name", "Class")
```

### Balance Validation
```python
# Validate class balance
from core.systems.character_utils import (
    validate_class_balance,
    verify_unique_mechanics,
    verify_minimum_abilities
)

is_balanced = validate_class_balance()
has_unique_mechanics = verify_unique_mechanics()
has_min_abilities = verify_minimum_abilities()
```

### Testing Helpers
```python
from tests.conftest import create_test_player, create_test_enemy

# Create standardized test objects
player = create_test_player(class_type="Warrior", level=5)
enemy = create_test_enemy(enemy_type="humanoid", level=5)
```

## Memory File Commands

This project uses memory files to store important commands and preferences. Update these files when you discover:
- Build/test/lint commands
- Code style preferences  
- Important codebase patterns
- Useful project information

## Quality Gates

Before considering any changes complete:
1. All tests pass: `pytest && behave`
2. Code formatted: `black . && isort .`
3. Type checking passes: `mypy core/`
4. Coverage >90%: `pytest --cov=game --cov-fail-under=90`
5. E2E tests pass: `./scripts/e2e_test_runner.sh`