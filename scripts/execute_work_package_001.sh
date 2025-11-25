#!/bin/bash
# Execute Work Package 001: Foundations
# Automated implementation script for LLM agents

echo "🚀 Executing Work Package 001: Foundations"
echo "=========================================="

# Set up environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Create directories if they don't exist
mkdir -p core/systems
mkdir -p tests
mkdir -p tests/integration
mkdir -p tests/e2e
mkdir -p logs
mkdir -p reports

# Function to check if file exists and has content
check_file() {
    local file_path=$1
    local description=$2
    
    if [ -f "$file_path" ] && [ -s "$file_path" ]; then
        echo "✅ $description - EXISTS"
        return 0
    else
        echo "❌ $description - MISSING OR EMPTY"
        return 1
    fi
}

# Function to validate Python syntax
validate_python() {
    local file_path=$1
    local description=$2
    
    if python -m py_compile "$file_path" 2>/dev/null; then
        echo "✅ $description - VALID SYNTAX"
        return 0
    else
        echo "❌ $description - SYNTAX ERROR"
        python -m py_compile "$file_path"
        return 1
    fi
}

# Function to run Pylint
run_pylint() {
    local file_path=$1
    local description=$2
    
    if pylint --score=yes --fail-under=10.0 "$file_path" >/dev/null 2>&1; then
        echo "✅ $description - PYLINT 10.0/10"
        return 0
    else
        echo "❌ $description - PYLINT FAILED"
        pylint --score=yes "$file_path"
        return 1
    fi
}

# Function to run pytest
run_pytest() {
    local test_file=$1
    local description=$2
    
    if python -m pytest "$test_file" -v --tb=short >/dev/null 2>&1; then
        echo "✅ $description - TESTS PASSED"
        return 0
    else
        echo "❌ $description - TESTS FAILED"
        python -m pytest "$test_file" -v --tb=short
        return 1
    fi
}

# Counters for tracking
total_checks=0
passed_checks=0

echo ""
echo "📋 STEP 1: Validating Core Models"
echo "-----------------------------------"

# Check core/models.py
if check_file "core/models.py" "Core Models"; then
    if validate_python "core/models.py" "Core Models Python"; then
        if run_pylint "core/models.py" "Core Models Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 2: Validating Validation System"
echo "----------------------------------------"

# Check core/validation.py
if check_file "core/validation.py" "Validation System"; then
    if validate_python "core/validation.py" "Validation System Python"; then
        if run_pylint "core/validation.py" "Validation System Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 3: Validating Game Constants"
echo "-------------------------------------"

# Check core/constants.py
if check_file "core/constants.py" "Game Constants"; then
    if validate_python "core/constants.py" "Game Constants Python"; then
        if run_pylint "core/constants.py" "Game Constants Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 4: Validating Core Systems"
echo "-----------------------------------"

# Check core/systems/character.py
if check_file "core/systems/character.py" "Character System"; then
    if validate_python "core/systems/character.py" "Character System Python"; then
        if run_pylint "core/systems/character.py" "Character System Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

# Check core/systems/stats.py
if check_file "core/systems/stats.py" "Stats System"; then
    if validate_python "core/systems/stats.py" "Stats System Python"; then
        if run_pylint "core/systems/stats.py" "Stats System Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

# Check core/systems/leveling.py
if check_file "core/systems/leveling.py" "Leveling System"; then
    if validate_python "core/systems/leveling.py" "Leveling System Python"; then
        if run_pylint "core/systems/leveling.py" "Leveling System Pylint"; then
            ((passed_checks++))
        fi
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 5: Validating Test Suite"
echo "---------------------------------"

# Check tests/test_models.py
if check_file "tests/test_models.py" "Model Tests"; then
    if run_pytest "tests/test_models.py" "Model Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

# Check tests/test_validation.py
if check_file "tests/test_validation.py" "Validation Tests"; then
    if run_pytest "tests/test_validation.py" "Validation Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

# Check tests/test_constants.py
if check_file "tests/test_constants.py" "Constants Tests"; then
    if run_pytest "tests/test_constants.py" "Constants Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

# Check tests/test_character_system.py
if check_file "tests/test_character_system.py" "Character System Tests"; then
    if run_pytest "tests/test_character_system.py" "Character System Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 6: Validating Integration Tests"
echo "--------------------------------------"

# Check tests/integration/test_character_workflow.py
if check_file "tests/integration/test_character_workflow.py" "Integration Tests"; then
    if run_pytest "tests/integration/test_character_workflow.py" "Integration Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 7: Validating E2E Tests"
echo "--------------------------------"

# Check tests/e2e/test_character_journey.py
if check_file "tests/e2e/test_character_journey.py" "E2E Tests"; then
    if run_pytest "tests/e2e/test_character_journey.py" "E2E Tests Execution"; then
        ((passed_checks++))
    fi
fi
((total_checks++))

echo ""
echo "📋 STEP 8: Validating Test Coverage"
echo "------------------------------------"

# Run coverage if pytest-cov is available
if python -c "import pytest_cov" 2>/dev/null; then
    echo "Running test coverage analysis..."
    if python -m pytest tests/ --cov=core --cov-fail-under=95 --cov-report=term-missing >/dev/null 2>&1; then
        echo "✅ Test Coverage: 95%+"
        ((passed_checks++))
    else
        echo "❌ Test Coverage: Below 95%"
        python -m pytest tests/ --cov=core --cov-report=term-missing
    fi
else
    echo "⚠️  pytest-cov not available, skipping coverage test"
fi
((total_checks++))

echo ""
echo "📋 STEP 9: Validating Performance"
echo "----------------------------------"

# Test basic performance
echo "Testing basic performance..."
if python -c "
import time
from core.models import Character, CharacterClass
from core.systems.character import create_character

start_time = time.time()
character = create_character('PerfTest', CharacterClass.WARRIOR)
end_time = time.time()

execution_time = end_time - start_time
assert execution_time < 0.01, f'Creation too slow: {execution_time}s'
print(f'✅ Character creation time: {execution_time:.4f}s (< 0.01s)')
" 2>/dev/null; then
    echo "✅ Performance Requirements Met"
    ((passed_checks++))
else
    echo "❌ Performance Requirements Failed"
    python -c "
import time
from core.models import Character, CharacterClass
from core.systems.character import create_character

start_time = time.time()
character = create_character('PerfTest', CharacterClass.WARRIOR)
end_time = time.time()

execution_time = end_time - start_time
print(f'❌ Character creation time: {execution_time:.4f}s (>= 0.01s)')
"
fi
((total_checks++))

echo ""
echo "📋 STEP 10: Validating Agent Requirements"
echo "----------------------------------------"

# Test that agent can understand and use the system
echo "Testing agent requirements..."
if python -c "
from core.models import Character, CharacterClass
from core.systems.character import create_character, level_up_character
from core.validation import validate_character_name
import inspect

# Test 1: Clear function contracts
create_character_sig = inspect.signature(create_character)
assert 'name' in create_character_sig.parameters
assert 'class_type' in create_character_sig.parameters
assert 'return' in str(create_character_sig)

# Test 2: Deterministic behavior
char1 = create_character('Test', CharacterClass.WARRIOR)
char2 = create_character('Test', CharacterClass.WARRIOR)
assert char1.name == char2.name
assert char1.class_type == char2.class_type

# Test 3: Clear error messages
try:
    validate_character_name('')
except ValueError as e:
    assert len(str(e)) > 0
    assert 'empty' in str(e).lower()

print('✅ Agent Requirements Validated')
" 2>/dev/null; then
    echo "✅ Agent Requirements Met"
    ((passed_checks++))
else
    echo "❌ Agent Requirements Failed"
    python -c "
from core.models import Character, CharacterClass
from core.systems.character import create_character, level_up_character
from core.validation import validate_character_name
import inspect

try:
    # Test 1: Clear function contracts
    create_character_sig = inspect.signature(create_character)
    assert 'name' in create_character_sig.parameters
    assert 'class_type' in create_character_sig.parameters
    assert 'return' in str(create_character_sig)

    # Test 2: Deterministic behavior
    char1 = create_character('Test', CharacterClass.WARRIOR)
    char2 = create_character('Test', CharacterClass.WARRIOR)
    assert char1.name == char2.name
    assert char1.class_type == char2.class_type

    # Test 3: Clear error messages
    try:
        validate_character_name('')
    except ValueError as e:
        assert len(str(e)) > 0
        assert 'empty' in str(e).lower()

    print('✅ Agent Requirements Validated')
except Exception as e:
    print(f'❌ Agent Requirements Failed: {e}')
"
fi
((total_checks++))

echo ""
echo "📊 WORK PACKAGE 001 VALIDATION RESULTS"
echo "===================================="

success_rate=0
if [ $total_checks -gt 0 ]; then
    success_rate=$(echo "scale=2; $passed_checks * 100 / $total_checks" | bc)
fi

echo "Total Checks: $total_checks"
echo "Passed Checks: $passed_checks"
echo "Success Rate: ${success_rate}%"
echo ""

if [ $passed_checks -eq $total_checks ]; then
    echo "🎉 WORK PACKAGE 001 FOUNDATIONS: COMPLETE SUCCESS!"
    echo ""
    echo "✅ All core components implemented"
    echo "✅ All validation systems working"
    echo "✅ All tests passing"
    echo "✅ Performance requirements met"
    echo "✅ Agent requirements met"
    echo "✅ Quality requirements met"
    echo ""
    echo "🚀 Ready for Work Package 002: Combat System"
    exit 0
else
    echo "❌ WORK PACKAGE 001 FOUNDATIONS: INCOMPLETE"
    echo ""
    echo "⚠️  Some components need attention:"
    echo "   - Check failed components above"
    echo "   - Fix syntax errors"
    echo "   - Improve test coverage"
    echo "   - Optimize performance"
    echo "   - Ensure agent requirements"
    echo ""
    echo "🔧 Fix issues and re-run script"
    exit 1
fi