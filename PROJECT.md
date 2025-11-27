# RPGSim - AI Agent Development Guide

## 🤖 AI AGENT: START HERE

**You are an AI agent working on the RPGSim project. This guide tells you exactly:**
1. **WHAT** we're building
2. **WHERE** we are now
3. **HOW** to continue
4. **WHEN** things should be done

## 📋 PROJECT STATUS TRACKING

### **📦 WORKING PACKAGES STATUS**

**🎯 WP-001: Foundation Core** (CURRENT)
- ✅ Character System: `core/systems/character.py` (COMPLETE) ← Move to World System
- ☐ World System: `core/systems/world.py` ← **ACTIVE**
- ☐ Integration Testing
- ☐ Documentation

**📦 WP-002: Economic Infrastructure** (PENDING)
- ☐ City Management System
- ☐ Travel System
- ☐ Shop System
- ☐ Integration Testing

**📦 WP-003: Gameplay Mechanics** (PENDING)
- ☐ Combat System
- ☐ Equipment System
- ☐ Quest System
- ☐ Progression System
- ☐ Integration Testing

**📦 WP-004: Advanced Features** (PENDING)
- ☐ Dungeon Exploration System
- ☐ Gamification System
- ☐ Music System ✅
- ☐ Integration Testing

### **🏁 MILESTONES STATUS**

**🎯 M1: Basic Player Experience** (TARGET: End of WP-001)
- ☐ Character creation with 23 classes
- ☐ Basic world navigation
- ☐ Location discovery system
- ☐ Player inventory and stats
- ☐ BDD Character tests passing
- ☐ BDD World tests passing

**📋 M2: Economic Foundation** (TARGET: End of WP-002)
- ☐ City management with services
- ☐ Travel system with resource costs
- ☐ Dynamic shop economy
- ☐ Trade routes and pricing
- ☐ All M2 BDD tests passing

**⚔️ M3: Core Gameplay Loop** (TARGET: End of WP-003)
- ☐ Turn-based combat system
- ☐ Equipment management
- ☐ Quest system with rewards
- ☐ Character progression
- ☐ All M3 BDD tests passing

**🏰 M4: Complete RPG Simulation** (TARGET: End of WP-004)
- ☐ Dungeon exploration
- ☐ Advanced gamification
- ☐ Modern engagement mechanics
- ☐ All BDD tests passing
- ☐ Performance benchmarks met

### **🎯 CURRENT ACTIVE TASK**

**📅 DATE**: Today
**📍 WORKING PACKAGE**: WP-001
**🎯 CURRENT MILESTONE**: M1
**🔧 ACTIVE TASK**: Character System Implementation
**📁 FILE**: `core/systems/character.py`
**⏱️ ETA**: 2-3 days
**🔥 STATUS**: IN PROGRESS

**📋 SUBTASKS:**
- ☐ Read BDD requirements
- ☐ Define Character class interface
- ☐ Implement 23 character classes
- ☐ Add inventory system
- ☐ Add stat calculations
- ☐ Run BDD tests
- ☐ Fix failures
- ☐ Complete Character System
- ☐ Mark WP-001 Character task as ✅

### **📋 NEXT STEPS AFTER COMPLETION**

**✅ WHEN CHARACTER SYSTEM COMPLETE:**
1. Check ☐ Character System in WP-001
2. Move to World System (`core/systems/world.py`)
3. Run integration tests
4. Complete WP-001
5. Check ☐ WP-001
6. Move to WP-002

**🎯 SUCCESS CRITERIA FOR CURRENT TASK:**
- All `features/character_creation.feature` scenarios pass
- Character class handles 23 different classes
- Inventory system functional
- Stat calculations working
- Integration with other systems (where applicable)

---

## 🏗️ PROJECT OVERVIEW

**RPGSim** = Text-based RPG simulation with modern game design principles, BDD/TDD methodology, optimized for LLM development.

**Key Features**: 23 character classes, 20 cities, dynamic economy, turn-based combat, quest system, dungeon exploration, gamification mechanics.

**Technology Stack**:
- **Language**: Python 3.8+
- **Testing Framework**: Behave (BDD) + Pytest
- **ORM**: SQLAlchemy with SQLite
- **Database**: SQLite for persistent game state and data integrity
- **Data Validation**: Pydantic models
- **Code Quality**: Pylint (10/10 target), >90% test coverage
- **Development**: Property-based testing with Hypothesis

## 🗺️ IMPLEMENTATION ROADMAP

### **🚀 PHASE 1: FOUNDATION (CURRENT PHASE)**
**Status**: BDD Complete, Code: 0% | **Target**: 2-5 days

#### **📍 TASK 1: Character System (START HERE)**
**🎯 NEXT ACTION**: Implement `core/systems/character.py`

**WHAT TO BUILD**:
- 23 character classes (Warrior, Mage, Rogue, etc.)
- Character stats (STR, DEX, INT, etc.)
- Inventory system with slots
- Level progression framework

**WHERE TO LOOK**:
- BDD Spec: `features/character_creation.feature`
- Steps: `features/steps/character_steps.py`
- Template: `core/systems/character.py` (CREATE THIS FILE)

**HOW TO BUILD**:
1. Read `features/character_creation.feature` → Understand requirements
2. Look at step definitions → See expected methods
3. Create `Character` class with required methods
4. Run BDD tests → Fix failures
5. Move to next system

**EXPECTED INTERFACES**:
```python
class Character:
    def create_character(name: str, class_type: str) -> bool
    def calculate_stats() -> Dict[str, int]
    def add_to_inventory(item: Item) -> bool
    def level_up() -> bool
```

#### **📍 TASK 2: World System (PENDING)**
**File**: `core/systems/world.py` (CREATE AFTER CHARACTER)
**Dependencies**: Character System
**ETA**: 1-2 days

---

### **📦 WORKING PACKAGES**

#### **🎯 WP-001: Foundation Core**
**Files to Create**:
- `core/systems/character.py`
- `core/systems/world.py`

**Success Criteria**:
- ✅ All BDD scenarios pass
- ✅ Character can be created with 23 classes
- ✅ Player can navigate between locations
- ✅ Basic inventory management

**HOW TO KNOW IT'S DONE**:
```bash
behave features/character_creation.feature  # All pass
behave features/world_exploration.feature    # All pass
```

---

### **🎯 NEXT PHASES (FUTURE)**

#### **📋 PHASE 2: Economy (8-11 days)**
- City Management → Travel System → Shop System

#### **⚔️ PHASE 3: Gameplay (9-12 days)**
- Combat → Equipment → Quest → Progression

#### **🏰 PHASE 4: Advanced (11-13 days)**
- Dungeons → Gamification → Music

---

## 🤖 AI AGENT INSTRUCTIONS

### **🔄 COMPLETE BDD/TDD DEVELOPMENT CYCLE**

**🎯 CORE PRINCIPLE**: Features → Steps → Tests → Code → All Tests Pass

**📋 DEVELOPMENT PHASES**:

**Phase 1: FEATURE DEFINITION** ✅ (ALREADY COMPLETE)
- ✅ All `.feature` files written and validated
- ✅ Business requirements defined in Gherkin
- ✅ Acceptance criteria specified

**Phase 2: STEP DEFINITIONS** ✅ (ALREADY COMPLETE)
- ✅ All step definitions implemented
- ✅ 330+ BDD steps created
- ✅ All features have step definitions

**Phase 3: TEST VALIDATION** ⚠️ (CURRENT STATE)
- ⚠️ BDD tests exist but most are failing (code not implemented)
- ⚠️ Need to run tests to see specific failures
- ⚠️ This is where you start coding

**Phase 4: CODE IMPLEMENTATION** 🎯 (YOUR WORK)
- 🎯 Write Python code to make ALL BDD tests pass
- 🎯 Implement complete systems, not individual steps
- 🎯 Focus on making entire feature test suites green

**Morning (When you start)**:
1. **READ STATUS**: Look at "PROJECT STATUS TRACKING" above
2. **FIND CURRENT TASK**: Look at "CURRENT ACTIVE TASK" section
3. **SELECT SYSTEM**: Choose from Character System → World System → etc

**🚨 CRITICAL: VIRTUAL ENVIRONMENT USAGE**
- **NEVER** use system pip (`pip install`) - this is managed by the OS
- **ALWAYS** use virtual environment: `source venv/bin/activate`
- **ALWAYS** install with: `pip install -r requirements.txt`
- **NEVER** use `--break-system-packages` - this breaks system dependencies
- **ALWAYS** check you're in venv: `which python` should show `./venv/bin/python`
- **IF IN DOUBT**: `deactivate` then `source venv/bin/activate`

**SYSTEM IMPLEMENTATION CYCLE**:
1. **📁 READ FEATURE**: `features/[system_name].feature` → Understand requirements
2. **📝 STUDY STEPS**: `features/steps/[system_name]_steps.py` → See expected interfaces
3. **🧪 RUN TESTS**: `behave features/[system_name].feature` → See what's failing
4. **💻 IMPLEMENT CODE**: Create `core/systems/[system_name].py` to pass ALL tests
5. **🧪 ADD UNIT TESTS**: Write comprehensive unit tests with >90% coverage
6. **🔍 ADD HYPOTHESIS**: Add property-based tests for complex logic (if applicable)
7. **🎭 ADD E2E TESTS**: Write end-to-end tests (where makes sense for system)
8. **📏 RUN PYLINT**: Achieve 10/10 score on implementation
9. **🔄 ITERATE**: Fix all failures, rerun all tests, until EVERYTHING passes
10. **🧹 CLEANUP**: Remove any obsolete/unnecessary files
11. **✅ VERIFY COMPLETE**: BDD + Unit + E2E + Coverage + Pylint all pass
12. **🔄 COMMIT**: `git commit` and `push` completed system
13. **⏸️ UPDATE**: Check off system when ALL quality gates pass

**SUCCESS CRITERIA**:
```bash
# BDD Tests
behave features/[system_name].feature
# Expected: 1 feature passed, X steps passed, 0 steps failed, 0 steps undefined

# Unit Tests + Coverage
pytest --cov=core/systems/[system_name] --cov-report=term-missing
# Expected: >90% coverage, 0 failures

# Code Quality
pylint core/systems/[system_name].py
# Expected: 10.0/10 score

# Property Tests (if applicable)
hypothesis tests/test_[system_name]_property.py
# Expected: All property tests pass

# E2E Tests (if applicable)
pytest tests/e2e/test_[system_name]_e2e.py
# Expected: End-to-end scenarios pass
```

**COMMIT TEMPLATE**:
```bash
git add .
git commit -m "feat: implement [system] system

- Complete BDD implementation with all scenarios passing
- Unit tests with >90% coverage
- Pylint 10/10 score achieved
- Hypothesis property tests added for critical logic
- Code cleaned and documented

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

**When SYSTEM COMPLETE**:
1. **ALL BDD PASS**: Every scenario in feature file passes
2. **INTEGRATION OK**: Works with previous systems
3. **CHECKOFF**: ☐ → ✅ in WORKING PACKAGES
4. **CHECKOFF**: Relevant ☐ → ✅ in MILESTONES
5. **MOVE**: To next system

### **🎯 QUALITY GATES**

**System MUST Pass**:
- ✅ 0 failing BDD scenarios
- ✅ 0 undefined steps
- ✅ 0 skipped scenarios
- ✅ Integration with previous systems (if applicable)
- ✅ Code follows project patterns
- ✅ Test coverage > 90%
- ✅ Pylint score 10/10
- ✅ Hypothesis property tests (where applicable)
- ✅ Clean codebase (no obsolete files)

**Implementation Requirements**:
- 🧪 **Test Coverage**: Maintain >90% coverage with `pytest --cov`
- 🔍 **Hypothesis**: Use property-based testing for complex logic
- 📏 **Pylint**: Achieve 10/10 score on every commit
- 🔄 **Git Workflow**: Commit and push after each system completion
- 🧹 **Code Cleanliness**: Remove obsolete/unnecessary files immediately

**Quality Commands**:
```bash
# Run quality checks before commit
pytest --cov=core --cov-report=term-missing
pylint core/systems/
hypothesis tests/test_[system]_property.py
git add .
git commit -m "feat: implement [system] with >90% coverage and pylint 10/10"
git push
```

**Example Success Output**:
```
$ behave features/character_creation.feature
Feature: Character Creation # features/character_creation.feature:2
  Scenario: Create character with valid class       # features/character_creation.feature:4
    Given the player wants to create a character   # features/steps/character_steps.py:5  0.000s
    And they select a valid class                 # features/steps/character_steps.py:10 0.001s
    When they create the character                 # features/steps/character_steps.py:15 0.000s
    Then the character should be created            # features/steps/character_steps.py:20 0.000s
    And the character should have appropriate stats  # features/steps/character_steps.py:25 0.001s

1 feature passed, 5 steps passed, 0 steps failed, 0 steps skipped, 0 steps undefined
```

### **✅ COMPLETION PROCEDURE**

**When System Implementation Complete**:
- All BDD tests pass ✅
- Check off system in working package ✅
- Move to next system

**When System Complete**:
1. **CHECKOFF**: ☐ → ✅ in WORKING PACKAGES STATUS
2. **CHECKOFF**: Relevant ☐ → ✅ in MILESTONES STATUS
3. **VERIFY**: All BDD scenarios pass
4. **MOVE**: To next system in working package

**When Working Package Complete**:
1. **CHECKOFF**: Entire WP-001 ☐ → ✅
2. **UPDATE**: "CURRENT ACTIVE TASK" section
3. **MOVE**: To first system in WP-002

### **🔍 NAVIGATION GUIDE**

**Finding Your Work**:
- **Current Task**: Search for "NEXT ACTION" or "START HERE"
- **System Details**: Search for system name + "System"
- **BDD Requirements**: Search for feature name + ".feature"
- **Implementation**: Search for file path in this guide

**Quick Searches**:
- `"NEXT ACTION"` → What to do now
- `"WP-001"` → Current working package
- `"M1"` → Current milestone goal
- `"character.py"` → File to create/edit

### **⚠️ HANDLING ISSUES**

**If Tests Fail**:
1. Read error message carefully
2. Check BDD step expectations
3. Verify your implementation matches requirements
4. Ask for clarification if stuck

**If Dependencies Missing**:
1. Check "Dependencies" section in system description
2. Implement prerequisite systems first
3. Update status accordingly

**If Confused**:
1. Re-read "Quick Project Status"
2. Look at "WHAT TO BUILD" section
3. Study BDD feature file
4. Ask for clarification

---

## 🎯 CURRENT WORKING CONTEXT

**📅 DATE**: Today
**🎯 GOAL**: Complete Character System implementation
**📍 LOCATION**: WP-001 → Character System → `core/systems/character.py`
**📋 PREREQUISITES**: None (start fresh)
**⏱️ TIME ALLOCATION**: 2-3 days
**🏁 SUCCESS**: BDD tests pass, character creation working

**📝 NOTES**:
- BDD tests are already written and working
- Focus on implementing the actual Python classes
- Follow the interface patterns shown in BDD steps
- Keep code simple and LLM-friendly
- Test frequently with BDD runner

**🔄 NEXT AFTER CHARACTER**: World System (`core/systems/world.py`)

---

## 📋 COMPLETE SYSTEM ARCHITECTURE (REFERENCE)

### **🎯 ALL SYSTEMS (Full Project Scope)**

**📦 WP-001: Foundation Core** (2-5 days)
- **Character System**: `core/systems/character.py` ← **CURRENT TASK**
- **World System**: `core/systems/world.py`

**📦 WP-002: Economic Infrastructure** (8-11 days)
- **City Management**: `core/systems/city.py`
- **Travel System**: `core/systems/travel.py`
- **Shop System**: `core/systems/shop.py`

**📦 WP-003: Gameplay Mechanics** (9-12 days)
- **Combat System**: `core/systems/combat.py`
- **Equipment System**: `core/systems/equipment.py`
- **Quest System**: `core/systems/quest.py`
- **Progression System**: `core/systems/progression.py`

**📦 WP-004: Advanced Features** (11-13 days)
- **Dungeon System**: `core/systems/dungeon.py`
- **Gamification System**: `core/systems/gamification.py`
- **Music System**: `core/systems/music.py` ✅ (COMPLETE)

### **🎯 MILESTONES (Progress Tracking)**

- **M1**: Basic Player Experience (End of WP-001)
- **M2**: Economic Foundation (End of WP-002)
- **M3**: Core Gameplay Loop (End of WP-003)
- **M4**: Complete RPG Simulation (End of WP-004)

---

## 🔑 QUICK REFERENCE CHEAT SHEET

### **For AI Agent Starting Work**
1. **READ**: "Quick Project Status" → Know where we are
2. **FIND**: "NEXT ACTION" → Know what to do
3. **BUILD**: Follow "HOW TO BUILD" steps
4. **TEST**: Run BDD tests to verify
5. **UPDATE**: Mark progress in status section

### **Common Searches**
- `"START HERE"` → Where to begin
- `"NEXT ACTION"` → Current task
- `"WP-###"` → Working package details
- `"M#"` → Milestone requirements
- `"[system].py"` → File location

### **Success Indicators**
- ✅ All BDD scenarios pass
- ✅ System integrates with previous
- ✅ Code matches interface expectations
- ✅ No regression in existing tests

---

**🤖 AI AGENT: You now have everything needed to continue development independently!**
- **Output**: Resource management, route optimization, random events
- **ETA**: 3-4 days

#### 5. Shop System
- **File**: `core/systems/shop.py`
- **Dependencies**: Character, City, Travel Systems
- **Complexity**: High
- **BDD**: `shop_system.feature`
- **Output**: Economy mechanics, dynamic pricing, inventory management
- **ETA**: 3-4 days

### Phase 3: Core Gameplay Mechanics

#### 6. Combat System
- **File**: `core/systems/combat.py`
- **Dependencies**: Character System
- **Complexity**: High
- **BDD**: `combat_system.feature`
- **Output**: Turn-based combat, damage calculation, AI behavior
- **ETA**: 4-5 days

#### 7. Equipment System
- **File**: `core/systems/equipment.py`
- **Dependencies**: Character, Shop Systems
- **Complexity**: Medium-High
- **BDD**: `equipment_system.feature`
- **Output**: Item management, equipment effects, stat modifications
- **ETA**: 2-3 days

#### 8. Quest System
- **File**: `core/systems/quest.py`
- **Dependencies**: Character, World, City, Combat Systems
- **Complexity**: Medium-High
- **BDD**: `quest_system.feature`
- **Output**: Mission structure, reward distribution, progression tracking
- **ETA**: 3-4 days

#### 9. Character Progression System
- **File**: `core/systems/progression.py`
- **Dependencies**: Combat, Equipment, Quest Systems
- **Complexity**: Medium
- **Output**: Level advancement, skill development, XP calculation
- **ETA**: 2-3 days

### Phase 4: Advanced Systems

#### 10. Dungeon Exploration System
- **File**: `core/systems/dungeon.py`
- **Dependencies**: Combat, Equipment, Quest, Travel, World Systems
- **Complexity**: Very High
- **BDD**: `dungeon_exploration.feature`
- **Output**: Complex dungeons, tactical gameplay, procedural generation
- **ETA**: 5-6 days

#### 11. Gamification System
- **File**: `core/systems/gamification.py`
- **Dependencies**: Character, Combat, Equipment, Quest Systems
- **Complexity**: Very High
- **BDD**: `gamification_system.feature`
- **Output**: DDA, flow state optimization, engagement metrics
- **ETA**: 6-7 days

#### 12. Music System (Optional - can be parallel)
- **File**: `core/systems/music.py` (already implemented)
- **Dependencies**: Character, World Systems
- **Complexity**: Low
- **BDD**: `music_system.feature`
- **Output**: Dynamic music, atmosphere enhancement
- **ETA**: 1-2 days

## 📦 Working Packages

### WP-001: Foundation Core
**Duration**: 4-6 days
**Systems**: Character System, World Exploration
**Milestone**: Player can be created and navigate basic world
**BDD Coverage**: `character_creation.feature`, `world_exploration.feature`

### WP-002: Economic Infrastructure
**Duration**: 8-11 days
**Systems**: City Management, Travel System, Shop System
**Milestone**: Complete economic simulation with dynamic pricing
**BDD Coverage**: `city_management.feature`, `travel_system.feature`, `shop_system.feature`

### WP-003: Gameplay Mechanics
**Duration**: 9-12 days
**Systems**: Combat System, Equipment System, Quest System, Character Progression
**Milestone**: Full combat gameplay with progression mechanics
**BDD Coverage**: `combat_system.feature`, `equipment_system.feature`, `quest_system.feature`

### WP-004: Advanced Features
**Duration**: 11-13 days
**Systems**: Dungeon Exploration, Gamification System
**Milestone**: Complete RPG simulation with modern engagement mechanics
**BDD Coverage**: `dungeon_exploration.feature`, `gamification_system.feature`

## 🎯 Milestones

### M1: Basic Player Experience (End of WP-001)
- ✅ Character creation with 23 classes
- ✅ Basic world navigation
- ✅ Location discovery system
- ✅ Player inventory and stats

### M2: Economic Foundation (End of WP-002)
- ✅ City management with services
- ✅ Travel system with resource costs
- ✅ Dynamic shop economy
- ✅ Trade routes and pricing

### M3: Core Gameplay Loop (End of WP-003)
- ✅ Turn-based combat system
- ✅ Equipment management
- ✅ Quest system with rewards
- ✅ Character progression

### M4: Complete RPG Simulation (End of WP-004)
- ✅ Dungeon exploration
- ✅ Advanced gamification
- ✅ Modern engagement mechanics
- ✅ Complete BDD coverage

## 🤖 LLM Agent Optimized BDD/TDD Flow

### Phase-Based Development Strategy

#### **Phase Entry Requirements**
1. **BDD Analysis**: Review feature scenarios and step definitions
2. **Dependency Check**: Verify all prerequisites are implemented
3. **Interface Design**: Define class interfaces based on step definitions
4. **Test Data**: Create test fixtures and mock data

#### **Implementation Flow**

**Step 1: BDD-First Design**
```python
# Analyze Given/When/Then steps
@given('the player has created a character')
def step_player_created(context):
    # This tells us we need a Character class
    # with create_character() method
```

**Step 2: Interface Definition**
```python
# Define required interfaces based on BDD steps
class Character:
    def __init__(self):
        self.name: str = ""
        self.class_type: str = ""
        self.level: int = 1
        self.stats: Dict[str, int] = {}
        self.inventory: List[Item] = []

    def create_character(self, name: str, class_type: str) -> bool:
        pass
```

**Step 3: TDD Implementation**
```python
# Write failing tests first
def test_character_creation():
    char = Character()
    result = char.create_character("TestPlayer", "Warrior")
    assert result == True
    assert char.name == "TestPlayer"
    assert char.class_type == "Warrior"

# Then implement to pass tests
def create_character(self, name: str, class_type: str) -> bool:
    # Implementation
```

**Step 4: BDD Integration**
```python
# Update BDD steps to use real implementation
@given('the player has created a character')
def step_player_created(context):
    context.player = Character()
    context.player.create_character("TestCharacter", "Warrior")
```

#### **LLM Agent Development Guidelines**

**1. Atomic Development**
- Focus on one step definition at a time
- Implement minimal viable functionality
- Ensure each step passes independently

**2. Progressive Enhancement**
- Start with basic functionality
- Add complexity incrementally
- Maintain backward compatibility

**3. Test-Driven Validation**
- Write tests before implementation
- Validate against BDD scenarios
- Ensure statistical requirements are met

**4. Interface Consistency**
- Maintain consistent naming conventions
- Follow established patterns from previous systems
- Document interfaces clearly

#### **Error Handling Strategy**

**Expected vs Unexpected Errors**
```python
# Expected game events
def create_character(self, name: str, class_type: str) -> bool:
    if class_type not in VALID_CLASSES:
        return False  # Expected failure

    # Unexpected errors should raise exceptions
    if not isinstance(name, str):
        raise ValueError("Name must be a string")
```

**Graceful Degradation**
- Implement fallback behaviors
- Provide meaningful error messages
- Maintain game state consistency

#### **Performance Considerations**

**LLM-Friendly Patterns**
```python
# Avoid complex inheritance chains
class Character:  # Simple, flat structure
    pass

# Use composition over inheritance
class Equipment:
    def __init__(self):
        self.weapon = Weapon()
        self.armor = Armor()

# Clear, explicit interfaces
def calculate_damage(self, attacker: Character, defender: Character) -> int:
    # Straightforward calculation, no magic
    base_damage = attacker.stats.strength
    defense = defender.stats.defense
    return max(1, base_damage - defense)
```

#### **Validation Strategy**

**BDD Validation**
```python
# Statistical validation requirements
def test_dda_algorithm(self):
    # Test the specific formula from BDD
    new_difficulty = base_difficulty * (0.7 + 0.3 * (target_performance / measured_performance))
    assert abs(new_difficulty - current_difficulty) <= (base_difficulty * 0.15)
```

**Property-Based Testing**
```python
# Use hypothesis for edge cases
@given(st.integers(min_value=1, max_value=20), st.sampled_from(VALID_CLASSES))
def test_character_level_scaling(self, level, class_type):
    char = Character()
    char.create_character("Test", class_type)
    char.level = level

    # Validate level scaling properties
    assert char.stats.health > 0
    assert char.stats.strength >= 0
```

## 🔄 Development Workflow

### Daily Development Cycle

1. **Morning (Planning)**: Review BDD scenarios for current system
2. **Mid-Morning**: Design interfaces based on step definitions
3. **Late Morning**: Write TDD tests
4. **Afternoon**: Implement functionality to pass tests
5. **Late Afternoon**: Integrate with BDD steps
6. **End of Day**: Run full BDD test suite

### Quality Gates

**System Complete Checklist**
- [ ] All BDD scenarios pass
- [ ] TDD tests have >90% coverage
- [ ] Integration tests with previous systems pass
- [ ] Performance benchmarks met
- [ ] Code reviewed for LLM-friendliness
- [ ] Documentation updated

### Integration Strategy

**Continuous Integration**
```yaml
# Pipeline for each working package
stages:
  - lint
  - unit_test
  - bdd_test
  - integration_test
  - performance_test
  - deploy
```

**Rollback Strategy**
- Maintain backward compatibility
- Feature flags for new systems
- Gradual rollout approach
- Monitor key metrics

## 📊 Success Metrics

### Development Metrics
- BDD step implementation rate: >95%
- Test coverage: >90%
- Integration success rate: 100%
- Performance targets met: >95%

### Quality Metrics
- Code complexity: Low-Medium
- Documentation coverage: >80%
- Bug density: <1 per 1000 lines
- Review coverage: 100%

### Project Metrics
- On-time delivery: >90%
- Budget adherence: >95%
- Stakeholder satisfaction: >4.5/5
- System reliability: >99%

---

## 🏆 PRODUCTION READINESS REQUIREMENTS

### **CODE QUALITY GATES**
**MANDATORY FOR COMPLETION:**

#### **Pylint Excellence**
- ✅ **ALL systems must achieve 10.0/10 Pylint score**
- ❌ **No disabled checks or workarounds permitted**
- ❌ **No suppressed warnings or errors**
- ✅ **All systems must pass with default Pylint configuration**

#### **Test Coverage Excellence**
- ✅ **100% unit test pass rate** - ALL tests must pass
- ✅ **>90% code coverage** for ALL systems
- ✅ **Comprehensive E2E gameplay testing**
- ❌ **No skipped or failing tests permitted**

#### **End-to-End Gameplay Verification**
- ✅ **Complete gameplay from title screen to all possible endings**
- ✅ **All player paths and decision branches tested**
- ✅ **Save/load functionality throughout gameplay**
- ✅ **Character progression tested from level 1 to max level**
- ✅ **All 23 character classes fully playable**

### **🎯 FINAL ACCEPTANCE CRITERIA**
**MANDATORY FOR PROJECT COMPLETION:**

#### **BDD/TDD Excellence**
- ✅ **ALL BDD steps implemented and passing**
- ✅ **ALL TDD and Hypothesis tests passing**
- ✅ **Complete scenario coverage for all game systems**

#### **Code Quality Excellence**
- ✅ **Pylint 10/10 on ALL code without skipping checks**
- ✅ **No disabled rules or suppressed warnings**
- ✅ **Clean, maintainable, production-ready code**

#### **Full E2E Playthrough Testing**
- ✅ **Complete playthroughs to all endings**
- ✅ **All possible class combinations tested**
- ✅ **All ending paths validated and working**
- ✅ **Full gameplay loop from character creation to completion**

#### **Integration Testing**
- ✅ **All system-to-system interfaces verified**
- ✅ **Data flow integrity across complete game loop**
- ✅ **Error handling and edge cases covered**
- ✅ **Performance requirements met in realistic scenarios**

### **PRODUCTION DEPLOYMENT STANDARDS**

#### **Code Quality Metrics**
- ✅ **No magic numbers or hardcoded values**
- ✅ **Comprehensive docstrings for ALL functions and classes**
- ✅ **Type hints implemented throughout codebase**
- ✅ **Consistent coding style and naming conventions**
- ✅ **No debugging code or TODO comments left in production**

#### **Game Performance Requirements**
- ✅ **Startup time < 2 seconds on standard hardware**
- ✅ **Memory usage < 500MB during gameplay**
- ✅ **UI responsiveness with <100ms interaction delay**
- ✅ **Save game operation <1 second**
- ✅ **Load game operation <3 seconds**

#### **User Experience Requirements**
- ✅ **Intuitive controls and interface**
- ✅ **Clear feedback for all user actions**
- ✅ **Progressive difficulty curve**
- ✅ **Engaging tutorial system**
- ✅ **Satisfying win conditions and endings**

#### **Technical Requirements**
- ✅ **Graceful error handling and recovery**
- ✅ **Data persistence and validation**
- ✅ **Cross-platform compatibility**
- ✅ **Security best practices implemented**
- ✅ **Scalable architecture for future features**

### **COMPLETION ACCEPTANCE CRITERIA**

**RPGSim is considered COMPLETE when ALL of the following are TRUE:**

1. **🔧 Code Quality**: All 20+ core systems achieve 10.0/10 Pylint score
2. **✅ Test Excellence**: 100% test pass rate with >90% coverage
3. **🎮 Gameplay Verified**: Complete E2E gameplay from start to all endings
4. **🏗️ Architecture**: All system interfaces and data flows verified
5. **🚀 Performance**: All performance benchmarks met
6. **📋 Documentation**: Complete API documentation and user guides

**🎯 SUCCESS METRICS:**
- **Code Quality**: 100% systems at 10.0/10 Pylint
- **Test Coverage**: >95% average across all systems
- **Gameplay**: Full playthrough with all content experienced
- **Integration**: Zero critical bugs in integration layer
- **Performance**: All benchmarks exceeded or met

**This ensures RPGSim is a production-ready, professional-quality text-based RPG simulation that meets industry standards for code quality, testing, and user experience.**

---

## **ACTIVE BACKLOG & TECHNICAL DEBT**

### **🚨 IMMEDIATE BLOCKERS (Must Complete for 100% Test Success)**

#### **Shop System Test Failures (17/35 passing - 46%)**
- **Priority 1**: 18 remaining test failures blocking production readiness
- **Missing Methods**: `process_transaction`, `calculate_buy_price`, trading mechanics
- **Data Model Issues**: ShopItem.stock property, ShopEconomy.gold_reserve alias
- **Economic Simulation**: Supply/demand pricing, reputation systems, bulk discounts
- **Integration Tests**: Character/Shop/Item/Economy system integration

#### **Comprehensive Test Refactoring for Modular Architecture (Priority 1)**
- Refactor ALL unit tests to match new modular architecture
- Update ALL BDD steps to use proper service facades
- Create integration tests for ALL modular components
- Add repository pattern testing for ALL systems
- Update test coverage targets for ALL modular packages
- Create service layer unit tests for ALL systems
- Add domain entity unit tests for ALL domains
- Test dependency injection patterns across ALL systems
- Create individual module test suites for ALL packages
- Test modular component isolation across ALL systems
- Validate separation of concerns across ALL systems
- Refactor property-based tests for ALL services
- Update end-to-end tests for modular architecture
- Create modular component integration tests
- Test cross-system interactions with new architecture

#### **Pydantic V2 Migration (Critical Technical Debt)**
- **Status**: In Progress - Character models partially migrated
- **Remaining Classes**: Item, Enemy, Quest, Location, GameState models
- **Pattern Migration**:
  - `class Config` → `model_config = ConfigDict()`
  - `@validator` → `@field_validator`
  - `values` parameter → `info.data` in validators
- **Impact**: All deprecation warnings eliminated, modern stack compliance

#### **User Experience Enhancements**
- Advanced tutorial system
- Accessibility features
- UI/UX improvements
- Save game management
- Achievement system

### **🔧 ENHANCEMENT BACKLOG (Post-Production)**

#### **SQLite Database Implementation**
- Database schema design with proper PK/FK relationships
- ORM integration with SQLAlchemy
- Migration system with Alembic
- Save/load game functionality
- Data persistence and integrity
- Performance optimization with indexing
- Hybrid approach with in-memory caching

#### **Shop System Advanced Features**
- Dynamic pricing algorithms
- Trade route simulation
- Shopkeeper AI behaviors
- Regional economy variations
- Supply chain mechanics

#### **SQLite Database Implementation**
- Database schema design with proper PK/FK relationships
- ORM integration with SQLAlchemy
- Migration system with Alembic
- Save/load game functionality
- Data persistence and integrity
- Performance optimization with indexing
- Hybrid approach with in-memory caching

#### **Performance Optimizations**
- Memory usage profiling
- Database query optimization
- Cache layer implementation
- Concurrent processing improvements

### **📋 TECHNICAL DEBT TRACKER**

#### **Code Quality**
- [x] Complete Pydantic V2 migration (Item, Enemy, Quest, Location, GameState) ✅
- [x] Eliminate all deprecation warnings ✅
- [ ] Implement missing shop system methods
- [ ] Add comprehensive error handling
- [ ] Design and implement SQLite database schema
- [ ] Add SQLAlchemy ORM integration
- [ ] Create database migration system (Alembic)
- [ ] Refactor character tests for modular architecture

#### **Testing Excellence**
- [ ] Achieve 35/35 shop tests passing (100%)
- [ ] Add performance benchmarks for shop system
- [ ] Implement property-based testing for economic systems
- [ ] Add integration test coverage for all system interactions
- [ ] Add database integration tests
- [ ] Test data integrity and constraints
- [ ] Performance test database operations

#### **Documentation**
- [ ] Update API docs for Pydantic V2 changes
- [ ] Document shop system architecture
- [ ] Add economic simulation documentation
- [ ] Create deployment guide
- [ ] Document database schema and relationships
- [ ] Add ORM usage guidelines
- [ ] Create database migration documentation

### **🔄 BACKLOG COMPLETO COM ORDENAÇÃO DE PRECEDÊNCIA**

**PRIORIDADE 1 - CRÍTICO (Bloqueia Progresso)**
- [P1.1] 🔥 Refatorar arquitetura modular para TODOS os sistemas (bloqueia tudo)
  - **Dependências**: Nenhuma
  - **Pré-requisito para**: TODAS as outras tarefas
  - **Estimativa**: 3-4 dias
- [P1.2] 🔥 Refatorar TODOS os testes para arquitetura modular
  - **Dependências**: P1.1
  - **Impacto**: Falha em todos os testes atuais
  - **Estimativa**: 2-3 dias

**PRIORIDADE 2 - URGENTE (Necessário para Funcionalidade)**
- [P2.1] ⚡ Implementar padrão de repositório em TODOS os sistemas
  - **Dependências**: P1.1
  - **Pré-requisito para**: Persistência de dados
  - **Estimativa**: 2 dias
- [P2.2] ⚡ Implementar injeção de dependências em TODOS os sistemas
  - **Dependências**: P1.1, P2.1
  - **Impacto**: Testabilidade e manutenção
  - **Estimativa**: 1-2 dias
- [P2.3] ⚡ Criar fachadas de serviço para TODOS os sistemas
  - **Dependências**: P1.1
  - **Pré-requisito para**: API limpa
  - **Estimativa**: 2 dias

**PRIORIDADE 3 - IMPORTANTE (Infraestrutura de Dados)**
- [P3.1] 🗄️ Desenhar schema de banco de dados SQLite
  - **Dependências**: P1.1, P2.1
  - **Pré-requisito para**: Persistência
  - **Estimativa**: 1 dia
- [P3.2] 🗄️ Implementar integração SQLAlchemy ORM
  - **Dependências**: P3.1, P2.2
  - **Impacto**: Camada de dados
  - **Estimativa**: 2 dias
- [P3.3] 🗄️ Criar sistema de migração Alembic
  - **Dependências**: P3.2
  - **Impacto**: Controle de versão de dados
  - **Estimativa**: 1 dia

**PRIORIDADE 4 - REQUERIDO (Qualidade e Produção)**
- [P4.1] ✅ Migrar TODOS os modelos para Pydantic V2
  - **Dependências**: P1.1
  - **Sistemas restantes**: Item, Enemy, Quest, Location, GameState
  - **Estimativa**: 2 dias
- [P4.2] 🧹 Eliminar TODOS os avisos de depreciação
  - **Dependências**: P4.1, P1.2
  - **Impacto**: Estabilidade do sistema
  - **Estimativa**: 1 dia

**PRIORIDADE 5 - FUNCIONALIDADE (Sistemas Específicos)**
- [P5.1] 🛒 Corrigir falhas nos testes do sistema de loja
  - **Dependências**: P1.2, P2.3 (sistema shop precisa ser refatorado)
  - **Métodos faltando**: process_transaction, calculate_buy_price
  - **Estimativa**: 2 dias
- [P5.2] ⚔️ Implementar sistema de combate modular
  - **Dependências**: P1.1, P2.1, P2.3
  - **Estimativa**: 3 dias
- [P5.3] 🌍 Implementar sistema mundial modular
  - **Dependências**: P1.1, P2.1, P3.2
  - **Estimativa**: 2-3 dias

**PRIORIDADE 6 - MELHORIAS (Pós-Produção)**
- [P6.1] 🎮 Implementar sistema de gamificação modular
  - **Dependências**: P1.1, P5.2
  - **Estimativa**: 2 dias
- [P6.2] 🏰 Implementar sistema de masmorra modular
  - **Dependências**: P1.1, P5.2, P5.3
  - **Estimativa**: 3 dias
- [P6.3] 🎵 Refatorar sistema de música para padrão modular
  - **Dependências**: P1.1
  - **Estimativa**: 1 dia

**PRIORIDADE 7 - OTIMIZAÇÃO (Performance)**
- [P7.1] ⚡ Implementar cache em memória com Redis
  - **Dependências**: P3.2, P2.2
  - **Impacto**: Performance de leitura
  - **Estimativa**: 2 dias
- [P7.2] 📊 Otimizar consultas de banco de dados
  - **Dependências**: P3.2
  - **Impacto**: Performance geral
  - **Estimativa**: 1-2 dias

**CADEIA DE DEPENDÊNCIAS CRÍTICA:**
P1.1 → P1.2 → P2.1 → P2.2 → P2.3 → P3.1 → P3.2 → P3.3 → P4.1 → P4.2

**BLOQUEIOS ATUAIS:**
- TODOS os sistemas estão bloqueados pela arquitetura monolítica (P1.1)
- TODOS os testes estão falhando devido à refatoração (P1.2)
- Persistência de dados impossível sem repositórios (P2.1)
- Manutenção de código impossível sem injeção de dependências (P2.2)

**PRÓXIMA AÇÃO IMEDIATA:**
🔥 **INICIAR P1.1 - Refatorar arquitetura modular para TODOS os sistemas**
- Esta é a única tarefa que desbloqueia todo o resto do projeto
- Sem isso, NENHUMA outra tarefa pode ser completada com sucesso
- Estimativa: 3-4 dias para TODOS os sistemas

### **🎯 CURRENT PRIORITIES**

1. **MAXIMUM PRIORITY**: Complete modular architecture refactoring
2. **CRITICAL**: Refactor ALL tests for modular architecture  
3. **URGENT**: Convert ALL monolithic systems to modular pattern
4. **HIGH**: Create proper separation of concerns across ALL systems
5. **HIGH**: Implement dependency injection across ALL systems
6. **HIGH**: Add comprehensive error handling to ALL modular systems
7. **MEDIUM**: Design and implement SQLite database architecture
8. **MEDIUM**: Complete Pydantic V2 migration for remaining systems
9. **LOW**: Fix remaining shop system tests (after modular refactoring)
10. **LOW**: Eliminate remaining deprecation warnings

---

**This architecture ensures systematic, test-driven development with clear milestones and LLM-optimized development practices.**