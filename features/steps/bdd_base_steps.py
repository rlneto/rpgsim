"""
RPGSim Base BDD Step Definitions
LLM Agent-Optimized implementation for consistent step patterns
"""

from behave import given, when, then
from typing import Dict, Any, List
import json
import sys
import os

# Add core to path for deterministic imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.systems.game import get_game_instance, start_new_game, create_character
from core.systems.character import Character
# from core.systems.city import City  # Temporarily disabled
from core.models import CharacterClass, GameState

class BDDContext:
    """Explicit context manager for BDD scenarios"""

    def __init__(self):
        self.game_state: Dict[str, Any] = {}
        self.player: Dict[str, Any] = {}
        self.characters: List[Dict[str, Any]] = []
        self.combat_log: List[str] = []
        self.current_city: Dict[str, Any] = {}
        self.error_message: str = ""
        self.result: Dict[str, Any] = {}

    def reset(self) -> None:
        """Reset context for new scenario"""
        self.game_state = {}
        self.player = {}
        self.characters = []
        self.combat_log = []
        self.current_city = {}
        self.error_message = ""
        self.result = {}

    def store_game_state(self, state: Dict[str, Any]) -> None:
        """Store game state explicitly"""
        self.game_state = state.copy()

    def store_character(self, character_data: Dict[str, Any]) -> None:
        """Store character data explicitly"""
        self.player = character_data.copy()
        self.characters.append(character_data.copy())

    def add_combat_entry(self, entry: str) -> None:
        """Add combat log entry"""
        self.combat_log.append(entry)

    def set_error(self, error_message: str) -> None:
        """Set error state"""
        self.error_message = error_message

    def set_result(self, result: Dict[str, Any]) -> None:
        """Set operation result"""
        self.result = result.copy()

def get_bdd_context(context) -> BDDContext:
    """Get or create BDD context wrapper"""
    if not hasattr(context, 'bdd_context'):
        context.bdd_context = BDDContext()
    return context.bdd_context

# -- CHARACTER CREATION STEPS --

@given('eu inicio uma nova sessão de jogo')
def step_start_new_game_session(context):
    """Initialize new game session"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.reset()

    result = start_new_game()

    if result['status'] == 'success':
        bdd_ctx.store_game_state(result['game_state'])
    else:
        bdd_ctx.set_error(result['message'])

@given('eu informo o nome "{name}" para o personagem')
def step_inform_character_name(context, name: str):
    """Set character name"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player['name'] = name

@given('eu escolho a classe "{character_class}"')
def step_choose_character_class(context, character_class: str):
    """Set character class"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player['class_type'] = character_class

@when('eu crio o personagem com os dados informados')
def step_create_character_with_data(context):
    """Create character with provided data"""
    bdd_ctx = get_bdd_context(context)

    name = bdd_ctx.player.get('name', '')
    character_class = bdd_ctx.player.get('class_type', '')

    result = create_character(name, character_class)

    if result['status'] == 'success':
        bdd_ctx.store_character(result['character'])
    else:
        bdd_ctx.set_error(result['message'])

@then('o personagem deve ser criado com sucesso')
def step_character_created_successfully(context):
    """Verify character was created successfully"""
    bdd_ctx = get_bdd_context(context)

    assert bdd_ctx.error_message == "", f"Unexpected error: {bdd_ctx.error_message}"
    assert 'name' in bdd_ctx.player, "Character name not set"
    assert 'class_type' in bdd_ctx.player, "Character class not set"

@then('o nome do personagem deve ser "{expected_name}"')
def step_verify_character_name(context, expected_name: str):
    """Verify character name"""
    bdd_ctx = get_bdd_context(context)
    actual_name = bdd_ctx.player.get('name', '')

    assert actual_name == expected_name, f"Expected name '{expected_name}', got '{actual_name}'"

@then('a classe do personagem deve ser "{expected_class}"')
def step_verify_character_class(context, expected_class: str):
    """Verify character class"""
    bdd_ctx = get_bdd_context(context)
    actual_class = bdd_ctx.player.get('class_type', '')

    assert actual_class == expected_class, f"Expected class '{expected_class}', got '{actual_class}'"

@then('o personagem deve começar no nível 1')
def step_verify_character_level_one(context):
    """Verify character starts at level 1"""
    bdd_ctx = get_bdd_context(context)
    level = bdd_ctx.player.get('level', 0)

    assert level == 1, f"Expected level 1, got {level}"

@then('o personagem deve ter HP inicial positivo')
def step_verify_positive_hp(context):
    """Verify character has positive HP"""
    bdd_ctx = get_bdd_context(context)
    hp = bdd_ctx.player.get('hp', 0)
    max_hp = bdd_ctx.player.get('max_hp', 0)

    assert hp > 0, f"Expected positive HP, got {hp}"
    assert max_hp > 0, f"Expected positive max HP, got {max_hp}"
    assert hp <= max_hp, f"HP ({hp}) cannot exceed max HP ({max_hp})"

@then('o personagem deve ter alguma quantidade de ouro inicial')
def step_verify_initial_gold(context):
    """Verify character has initial gold"""
    bdd_ctx = get_bdd_context(context)
    gold = bdd_ctx.player.get('gold', 0)

    assert gold >= 0, f"Expected non-negative gold, got {gold}"

# -- ERROR HANDLING STEPS --

@then('a criação deve falhar com mensagem de erro')
def step_verify_creation_fails(context):
    """Verify creation fails with error"""
    bdd_ctx = get_bdd_context(context)

    assert bdd_ctx.error_message != "", "Expected error message but got none"

@then('a mensagem deve mencionar que o nome é inválido')
def step_verify_name_error_message(context):
    """Verify error message mentions invalid name"""
    bdd_ctx = get_bdd_context(context)

    error_lower = bdd_ctx.error_message.lower()
    assert any(keyword in error_lower for keyword in ['name', 'nome', 'character']), \
        f"Error message should mention name: {bdd_ctx.error_message}"

# -- VALIDATION STEPS --

@given('eu informo um nome com mais de 50 caracteres')
def step_inform_long_name(context):
    """Set name with more than 50 characters"""
    long_name = "A" * 51  # 51 characters
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player['name'] = long_name

@given('eu informo um nome vazio')
def step_inform_empty_name(context):
    """Set empty name"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player['name'] = ""

@given('eu escolho uma classe inexistente')
def step_choose_invalid_class(context):
    """Set invalid character class"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player['class_type'] = "invalid_class"

# -- MULTIPLE CHARACTER CREATION STEPS --

@given('eu crio personagens de todas as 23 classes disponíveis')
def step_create_all_character_classes(context):
    """Create one character for each available class"""
    bdd_ctx = get_bdd_context(context)
    game = get_game_instance()

    available_classes = game._get_available_classes()
    assert len(available_classes) == 23, f"Expected 23 classes, got {len(available_classes)}"

    created_characters = []
    for character_class in available_classes:
        test_name = f"Test_{character_class}"
        result = create_character(test_name, character_class)

        if result['status'] == 'success':
            created_characters.append(result['character'])
        else:
            bdd_ctx.set_error(f"Failed to create {character_class}: {result['message']}")
            return

    bdd_ctx.characters = created_characters

@then('todas as 23 classes devem ser criadas com sucesso')
def step_verify_all_classes_created(context):
    """Verify all 23 classes were created successfully"""
    bdd_ctx = get_bdd_context(context)

    assert bdd_ctx.error_message == "", f"Creation failed: {bdd_ctx.error_message}"
    assert len(bdd_ctx.characters) == 23, f"Expected 23 characters, got {len(bdd_ctx.characters)}"

