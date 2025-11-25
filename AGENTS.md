# RPGSim Agent Guide

This document provides essential information for AI agents working on the RPGSim project - a console-based RPG in the style of Baldur's Gate with Pool of Radiance aesthetics.

## Project Overview

RPGSim is a text-based RPG game with the following key features:
- 23 unique and balanced character classes
- 100 diverse quests with engaging storylines
- 50 explorable dungeons with unique themes
- 200 different enemy types plus 50 unique bosses
- 100 NPCs with distinct personalities and quests
- 200 magic items with randomized loot system
- 20 fully developed cities with shops and services

## Technical Architecture

### Language & Framework
- **Language**: Python 3.8+
- **Testing Framework**: Behave (BDD framework)
- **UI**: Console-based text interface

### Project Structure
```
rpgsim/
├── features/                  # BDD feature files
│   ├── *.feature             # Feature definitions in Gherkin format
│   └── steps/                 # Step implementations for tests
│       └── *.py              # Python step definition files
├── requirements.md             # Full BDD requirements
├── README.md                  # Project overview
├── behave.ini                # Behave configuration
└── requirements.txt           # Python dependencies
```

## Key Commands

### Testing Commands
```bash
# Install dependencies (requires virtual environment)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run all BDD tests
behave

# Run specific feature file
behave features/character_creation.feature

# Run with dry run to check syntax
behave --dry-run

# Run with specific tags
behave --tags=@character
```

### Development Commands
```bash
# Run Python files directly
python game/main.py

# Validate BDD syntax without execution
python -m behave --dry-run
```

## Code Style & Conventions

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

## Important Implementation Details

### Character System
- 23 classes must be balanced within 15% power difference
- Each class needs unique mechanics not shared with others
- Classes must have at least 10 unique abilities
- Character creation includes name selection and text-based customization

### World Design
- 20 cities with unique geography and layouts
- Travel must be possible through text-based world map
- Cities must have at least 8 different building types
- Each city must have distinctive cultural elements in descriptions

### Quest System
- 100 quests must vary in difficulty from trivial to epic
- Each quest needs clear objectives and appropriate rewards
- 100 NPCs need distinct personalities and unique dialogue
- NPCs must respond differently based on player reputation

### Combat Mechanics
- Turn-based combat with initiative calculation
- Action costs must be balanced (6=standard, 3=quick, 9=slow)
- 200 enemy types with unique abilities and weaknesses
- 50 boss encounters with special mechanics

### Item System
- 200 unique magic items with clear effects
- Loot quality must scale with difficulty
- Equipment must modify character stats appropriately
- Economy must provide meaningful strategic choices

## Development Workflow

1. **Write BDD Scenarios First**: Always start with feature files before implementation
2. **Implement Step Definitions**: Create Python step implementations for features
3. **Run Tests Frequently**: Validate changes with `behave` commands
4. **Verify Game Balance**: Use mathematical models to ensure class/item balance
5. **Test Console Interface**: Ensure text display is clear in terminal environments

## Testing Strategy

### BDD Testing
- All features must have corresponding Behave tests
- Tests should cover all game mechanics and edge cases
- Use context objects to maintain state between steps
- Verify both positive and negative test cases

### Balance Testing
- Verify no class is >15% more powerful than others
- Test item progression curves
- Validate economy stability over long-term play
- Check difficulty scaling throughout the game

## Key Gotchas

1. **Console Limitations**: Remember the interface is text-based, not graphical
2. **Randomization**: Balance randomness with predictability for good player experience
3. **Balance is Mathematical**: Use actual formulas, not "feel", for balance decisions
4. **Content Scale**: With 200 items, 100 NPCs, etc., ensure content generation is systematic
5. **Performance**: Console games must remain responsive even with large data sets

## Resource References

- For BDD practices: Refer to existing feature files in `/features/`
- For game balance formulas: Check combat_steps.py and character_steps.py
- For content generation patterns: See quest_steps.py and item_steps.py
- For project setup: Review behave.ini and requirements.txt

## Implementation Priorities

1. **P0 (Critical)**: Character creation, basic combat, world navigation
2. **P1**: Quest system, NPCs, shops, basic items
3. **P2**: Dungeons, bosses, advanced combat, complex items
4. **P3**: City variety, NPC depth, quest variety, balance tweaks

When working on this project, always prioritize implementing BDD tests before game code, and maintain the balance requirements throughout development.