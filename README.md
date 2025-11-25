# RPGSim: Baldur's Gate Style Console RPG

A text-based RPG game inspired by Baldur's Gate but with console-based gameplay similar to Pool of Radiance.

## Project Overview

This project aims to create a comprehensive console RPG with the following features:
- 23 unique and balanced character classes
- 100 diverse quests with engaging storylines
- 50 explorable dungeons with unique themes
- 200 different enemy types plus 50 unique bosses
- 100 NPCs with distinct personalities and quests
- 200 magic items with randomized loot system
- 20 fully developed cities with shops and services
- Turn-based combat system
- Character progression with meaningful choices
- Economy system with strategic decision-making
- Save/load system with auto-save and quick-save features

## Technical Architecture

The game is being developed using Python with Behavior-Driven Development (BDD) methodology. The project structure includes:

```
rpgsim/
├── venv/                      # Python virtual environment
├── features/                  # BDD feature files
│   ├── character_creation.feature
│   ├── world_exploration.feature
│   ├── quest_system.feature
│   ├── combat_system.feature
│   ├── equipment_system.feature
│   ├── dungeon_exploration.feature
│   ├── character_progression.feature
│   ├── gamification_system.feature
│   ├── save_load_system.feature
│   └── steps/                 # BDD step implementations
│       ├── character_steps.py
│       ├── world_steps.py
│       ├── quest_steps.py
│       ├── combat_steps.py
│       ├── item_steps.py
│       └── environment.py
├── tests/                     # pytest unit tests
│   ├── test_character_system.py
│   ├── test_combat_system.py
│   ├── test_quest_system.py
│   └── __init__.py
├── game/                      # Game implementation
│   ├── character.py           # Character classes
│   ├── combat.py             # Combat system
│   ├── quest.py              # Quest system
│   └── main.py              # Main game entry
├── requirements.md             # Full BDD requirements
├── README.md                  # This file
├── behave.ini                # Behave configuration
├── pytest.ini               # pytest configuration
├── requirements.txt          # Python dependencies
├── conftest.py              # pytest fixtures
├── AGENTS.md                # Agent collaboration guide
└── TODO.md                  # Development TODO list
```

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment support

### Setup Instructions

1. Clone or download the project
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:
   ```bash
   python -m pytest --version
   python -m behave --version
   ```

## Running Tests

### BDD Testing
```bash
# Run all BDD features
behave

# Run specific feature
behave features/character_creation.feature

# Run with dry run to check syntax
behave --dry-run

# Run with specific tags
behave --tags=character
```

### Unit Testing
```bash
# Run all unit tests with coverage
pytest

# Run with coverage report
pytest --cov=game --cov-report=html

# Run specific test file
pytest tests/test_character_system.py

# Run with hypothesis statistics
pytest --hypothesis-show-statistics
```

## Development Status

The project is currently in the requirements and test design phase with the following progress:

- ✅ All 8 BDD feature files created
- ✅ 5 step implementation files created
- ✅ Comprehensive unit tests for character, combat, and quest systems
- ✅ pytest and hypothesis configuration set up
- ✅ Virtual environment structure established
- 🔄 Game engine implementation in progress
- ⏳ World exploration system pending
- ⏳ Equipment system pending
- ⏳ Save/load system pending

## Key Design Principles

### Game Balance
- No class should be more than 15% more powerful than any other
- Content difficulty should scale appropriately with player progression
- Economy should provide meaningful strategic choices
- Statistical models ensure fairness

### Content Variety
- Each of the 23 character classes has unique mechanics and abilities
- Cities, dungeons, and NPCs all have distinct characteristics
- Quests vary in type, difficulty, and rewards
- 200 different enemies and 50 unique bosses provide combat variety

### Player Experience
- Turn-based combat with tactical depth
- Rich character progression with meaningful choices
- Immersive world with deep lore and interesting interactions
- Save/load system prevents frustration with regular auto-saves

### Console Interface
- Clear text-based interface with intuitive commands
- Information display optimized for terminal environments
- Accessibility features for different terminal configurations
- Efficient text rendering for smooth gameplay

## Testing Coverage

The project uses a comprehensive testing approach:

### BDD Testing (Behave)
- All features tested from user perspective
- Scenario-based testing for all game systems
- Given/When/Then structure ensures clear test definitions
- Integration testing between game components

### Unit Testing (pytest)
- Component-level testing with >90% coverage target
- Hypothesis for property-based testing and edge cases
- Mock objects for isolated testing
- Statistical testing for game balance

### Test Coverage Goals
- Line coverage: >90%
- Branch coverage: >85%
- Function coverage: >95%
- BDD scenario coverage: 100%

## Contributing

When contributing to this project:

1. **Environment Setup**: Always work in the virtual environment
2. **Test First**: Write BDD scenarios and unit tests before implementation
3. **Coverage**: Ensure all new code has corresponding tests
4. **Balance**: Use mathematical models for game balance decisions
5. **Documentation**: Update documentation with new features
6. **Console Design**: Remember interface is text-based, not graphical

## Code Style

### BDD Patterns
- Features are defined in Gherkin format (Given/When/Then)
- Step definitions use descriptive function names
- Context objects share state between steps
- Use consistent naming for test data

### Python Conventions
- Follow PEP 8 style guide
- Use type hints where appropriate
- Keep functions focused and small
- Use descriptive variable names
- Add docstrings for complex functions
- Use venv for dependency management

## Game Features

### Character System
- 23 unique classes with distinct gameplay mechanics
- Each class has at least 10 unique abilities
- Characters have clear strengths and weaknesses
- Customizable appearance (text-based)
- Balanced using mathematical models (≤15% power difference)

### World
- 20 distinct cities with unique cultures and economies
- 50 themed dungeons with environmental challenges
- Text-based world map for navigation
- Travel system with time costs

### Quest System
- 100 diverse quests ranging from trivial to epic difficulty
- Quest acquisition through NPC interaction
- Quest rewards scale with difficulty
- Quest progress affects world state
- Reputation system influences quest availability

### Combat
- Turn-based combat with tactical depth
- Initiative based on character statistics
- Action time costs for strategic depth
- 200 unique enemy types with different behaviors
- 50 boss encounters with special mechanics

### Equipment
- 200 unique magic items with randomized loot
- Equipment modifies character statistics
- Item comparison for informed decisions
- Economy with shops in each city
- Limited vendor gold reserves

### NPCs
- 100 unique NPCs with distinct personalities
- NPCs offer different quests and services
- NPCs respond based on player actions and reputation
- Dynamic dialogue system with multiple factors

### Save/Load System
- Auto-save every 3 minutes
- Manual save at designated locations
- Quick-save and quick-load functionality
- Multiple save slots
- Preserves all game state

## Performance Targets

- Load times: <2 seconds
- Memory usage: <200MB
- Auto-save: <1 second
- Response time: <0.5 seconds for all actions
- Supported terminals: Most modern terminal emulators

This project represents an ambitious goal to create a deep, engaging console RPG that captures the spirit of classic games while providing a fresh experience with modern design principles and comprehensive testing.