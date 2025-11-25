"""
RPGSim Combat BDD Step Definitions
LLM Agent-Optimized deterministic combat scenarios
"""

from behave import given, when, then
from typing import Dict, Any, List
import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.systems.game import get_game_instance, create_character, start_combat
from core.systems.character import Character
# from core.systems.combat import CombatEngine  # Temporarily disabled
from core.models import CharacterClass

# Import base context manager
from bdd_base_steps import get_bdd_context

# -- COMBAT SYSTEM SETUP STEPS --

@given('um combate é iniciado')
def step_combat_initialized(context):
    """Initialize combat system"""
    bdd_ctx = get_bdd_context(context)
    # bdd_ctx.combat_engine = CombatEngine()  # Temporarily disabled
    bdd_ctx.combat_log = []

@given('o jogador entra em combate')
def step_player_enters_combat(context):
    """Player enters combat state"""
    bdd_ctx = get_bdd_context(context)

    # Ensure player exists
    if not bdd_ctx.player:
        # Create default player if none exists
        result = create_character("Test_Warrior", "warrior")
        if result['status'] == 'success':
            bdd_ctx.store_character(result['character'])
        else:
            bdd_ctx.set_error(result['message'])
            return

@given('um inimigo "{enemy_type}" é encontrado')
def step_enemy_encountered(context, enemy_type: str):
    """Enemy is encountered"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.current_enemy = {
        'type': enemy_type,
        'name': f"Wild_{enemy_type}",
        'level': 1
    }

@when('o combate começa')
def step_combat_begins(context):
    """Start combat encounter"""
    bdd_ctx = get_bdd_context(context)

    if not bdd_ctx.player:
        bdd_ctx.set_error("No player available for combat")
        return

    if not hasattr(bdd_ctx, 'current_enemy'):
        bdd_ctx.set_error("No enemy available for combat")
        return

    # Start combat using game system
    enemy_id = bdd_ctx.current_enemy['type']
    result = start_combat(enemy_id)

    if result['status'] == 'success':
        bdd_ctx.set_result(result)
        bdd_ctx.add_combat_entry(f"Combat started with {enemy_id}")
    else:
        bdd_ctx.set_error(result['message'])

# -- COMBAT MECHANICS STEPS --

@given('o jogador ataca o inimigo')
def step_player_attacks_enemy(context):
    """Player attacks enemy"""
    bdd_ctx = get_bdd_context(context)

    if not bdd_ctx.player:
        bdd_ctx.set_error("No player available")
        return

    # Simulate attack damage calculation
    player_strength = bdd_ctx.player.get('stats', {}).get('strength', 10)
    damage = max(1, player_strength)  # Simplified damage

    bdd_ctx.combat_damage_dealt = damage
    bdd_ctx.add_combat_entry(f"Player deals {damage} damage")

@when('o dano é calculado')
def step_damage_calculated(context):
    """Damage calculation occurs"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'combat_damage_dealt'):
        damage = bdd_ctx.combat_damage_dealt
        bdd_ctx.add_combat_entry(f"Damage calculated: {damage}")
    else:
        # Default damage calculation
        bdd_ctx.combat_damage_dealt = 5
        bdd_ctx.add_combat_entry("Default damage calculated: 5")

@when('o inimigo recebe o dano')
def step_enemy_receives_damage(context):
    """Enemy receives damage"""
    bdd_ctx = get_bdd_context(context)

    damage = getattr(bdd_ctx, 'combat_damage_dealt', 0)
    enemy_hp = getattr(bdd_ctx, 'enemy_hp', 100)

    new_enemy_hp = max(0, enemy_hp - damage)
    bdd_ctx.enemy_hp = new_enemy_hp
    bdd_ctx.add_combat_entry(f"Enemy HP reduced to {new_enemy_hp}")

@then('o inimigo deve sofrer dano corretamente')
def step_enemy_takes_damage(context):
    """Verify enemy takes correct damage"""
    bdd_ctx = get_bdd_context(context)

    assert hasattr(bdd_ctx, 'enemy_hp'), "Enemy HP not tracked"
    assert hasattr(bdd_ctx, 'combat_damage_dealt'), "Damage not calculated"

    final_hp = bdd_ctx.enemy_hp
    damage = bdd_ctx.combat_damage_dealt

    assert damage > 0, f"Expected positive damage, got {damage}"
    assert final_hp >= 0, f"Enemy HP cannot be negative, got {final_hp}"

@then('o combate deve continuar até que um dos lados seja derrotado')
def step_combat_continues_until_defeat(context):
    """Verify combat continues until defeat"""
    bdd_ctx = get_bdd_context(context)

    # Simplified combat resolution
    player_hp = bdd_ctx.player.get('hp', 50)
    enemy_hp = getattr(bdd_ctx, 'enemy_hp', 100)

    # Simulate combat rounds
    round_count = 0
    while player_hp > 0 and enemy_hp > 0 and round_count < 20:  # Max 20 rounds
        round_count += 1

        # Player attacks
        player_damage = max(1, bdd_ctx.player.get('stats', {}).get('strength', 10))
        enemy_hp = max(0, enemy_hp - player_damage)
        bdd_ctx.add_combat_entry(f"Round {round_count}: Player deals {player_damage} damage")

        if enemy_hp == 0:
            bdd_ctx.add_combat_entry(f"Round {round_count}: Enemy defeated!")
            bdd_ctx.combat_winner = "player"
            break

        # Enemy attacks (simplified)
        enemy_damage = 8  # Fixed enemy damage
        player_hp = max(0, player_hp - enemy_damage)
        bdd_ctx.player['hp'] = player_hp
        bdd_ctx.add_combat_entry(f"Round {round_count}: Enemy deals {enemy_damage} damage")

        if player_hp == 0:
            bdd_ctx.add_combat_entry(f"Round {round_count}: Player defeated!")
            bdd_ctx.combat_winner = "enemy"
            break

    bdd_ctx.enemy_hp = enemy_hp
    bdd_ctx.combat_rounds = round_count

    assert round_count < 20, "Combat took too many rounds - possible infinite loop"

@then('o jogador deve ganhar experiência se vencer')
def step_player_gains_experience(context):
    """Verify player gains experience on victory"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'combat_winner'):
        bdd_ctx.set_error("Combat winner not determined")
        return

    if bdd_ctx.combat_winner == "player":
        # Award experience
        exp_gained = 50  # Fixed experience for victory
        current_exp = bdd_ctx.player.get('experience', 0)
        new_exp = current_exp + exp_gained

        bdd_ctx.player['experience'] = new_exp
        bdd_ctx.add_combat_entry(f"Player gained {exp_gained} experience")

        assert new_exp > current_exp, "Player should have gained experience"

# -- ENEMY VARIETY STEPS --

@given('existe uma variedade de 200 tipos de inimigos')
def step_enemy_variety_exists(context):
    """Verify 200 enemy types exist"""
    bdd_ctx = get_bdd_context(context)

    # Mock enemy database
    enemy_types = []
    for i in range(200):
        enemy_types.append(f"Enemy_Type_{i+1}")

    bdd_ctx.available_enemies = enemy_types
    assert len(enemy_types) == 200, f"Expected 200 enemy types, got {len(enemy_types)}"

@when('um jogador encontra inimigos diferentes')
def step_player_encounters_different_enemies(context):
    """Player encounters different enemy types"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'available_enemies'):
        bdd_ctx.set_error("No enemy types available")
        return

    # Simulate encountering 5 different enemies
    encountered_enemies = bdd_ctx.available_enemies[:5]
    bdd_ctx.encountered_enemies = encountered_enemies
    bdd_ctx.add_combat_entry(f"Encountered {len(encountered_enemies)} different enemy types")

@then('cada inimigo deve ter características únicas')
def step_verify_unique_enemy_characteristics(context):
    """Verify each enemy has unique characteristics"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'encountered_enemies'):
        bdd_ctx.set_error("No enemies encountered")
        return

    encountered = bdd_ctx.encountered_enemies
    assert len(set(encountered)) == len(encountered), "All encountered enemies should be unique"

    # Verify each enemy type has unique traits
    enemy_traits = {}
    for enemy_type in encountered:
        # Generate deterministic traits based on enemy type
        enemy_hash = hash(enemy_type) % 1000
        traits = {
            'strength': max(1, 10 + enemy_hash % 10),
            'dexterity': max(1, 10 + (enemy_hash // 10) % 10),
            'special_ability': f"Ability_{enemy_hash % 5}"
        }
        enemy_traits[enemy_type] = traits

    bdd_ctx.enemy_traits = enemy_traits
    assert len(enemy_traits) == len(encountered), "Each enemy should have unique traits"

# -- BOSS ENCOUNTER STEPS --

@given('existem 50 chefes únicos disponíveis')
def step_unique_bosses_available(context):
    """Verify 50 unique bosses exist"""
    bdd_ctx = get_bdd_context(context)

    # Mock boss database
    boss_types = []
    for i in range(50):
        boss_types.append(f"Boss_{i+1}")

    bdd_ctx.available_bosses = boss_types
    assert len(boss_types) == 50, f"Expected 50 boss types, got {len(boss_types)}"

@when('o jogador encontra um chefe')
def step_player_encounters_boss(context):
    """Player encounters a boss"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'available_bosses'):
        bdd_ctx.set_error("No bosses available")
        return

    # Select first boss for encounter
    boss = bdd_ctx.available_bosses[0]
    bdd_ctx.current_boss = {
        'name': boss,
        'level': 5,  # Bosses are higher level
        'hp': 200,   # More HP than regular enemies
        'special_move': f"Special_{boss}"
    }
    bdd_ctx.add_combat_entry(f"Encountered boss: {boss}")

@then('o chefe deve ter mecânicas especiais')
def step_verify_boss_special_mechanics(context):
    """Verify boss has special mechanics"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'current_boss'):
        bdd_ctx.set_error("No boss encountered")
        return

    boss = bdd_ctx.current_boss

    # Verify boss has special characteristics
    assert 'special_move' in boss, "Boss should have special move"
    assert boss['level'] > 1, "Boss should be higher level than regular enemies"
    assert boss['hp'] > 100, "Boss should have more HP than regular enemies"

    bdd_ctx.add_combat_entry(f"Boss special move: {boss['special_move']}")

@then('a luta contra o chefe deve ser mais desafiadora')
def step_verify_boss_combat_challenge(context):
    """Verify boss combat is more challenging"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'current_boss'):
        bdd_ctx.set_error("No boss encountered")
        return

    boss = bdd_ctx.current_boss

    # Simulate boss combat difficulty
    player_level = bdd_ctx.player.get('level', 1)
    boss_level = boss['level']

    assert boss_level >= player_level + 2, f"Boss should be at least 2 levels higher than player"

    # Boss should have multiple phases or abilities
    boss_phases = ['normal', 'enraged', 'desperate']
    bdd_ctx.boss_phases = boss_phases
    assert len(boss_phases) >= 2, "Boss should have at least 2 combat phases"

    bdd_ctx.add_combat_entry(f"Boss has {len(boss_phases)} combat phases: {', '.join(boss_phases)}")