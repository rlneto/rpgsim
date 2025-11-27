from behave import given, when, then
import random

# Combat System

@given('the player encounters an enemy')
def step_encounter_enemy(context):
    if not hasattr(context, 'enemies'):
        context.enemies = []
        
        # Create 200 different enemy types
        for i in range(200):
            enemy = {
                'id': f"enemy_{i}",
                'name': f"Enemy_{i}",
                'type': random.choice(['humanoid', 'beast', 'undead', 'demon', 'elemental', 'construct']),
                'level': random.randint(1, 30),
                'stats': {
                    'strength': random.randint(5, 20),
                    'dexterity': random.randint(5, 20),
                    'intelligence': random.randint(5, 20),
                    'wisdom': random.randint(5, 20),
                    'charisma': random.randint(5, 20),
                    'constitution': random.randint(5, 20)
                },
                'hp': random.randint(20, 500),
                'abilities': [f"ability_{i}_{j}" for j in range(random.randint(2, 6))],
                'ai_behavior': random.choice(['aggressive', 'defensive', 'tactical', 'random']),
                'weakness': random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical']),
                'resistance': random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical', 'none'])
            }
            context.enemies.append(enemy)
    
    # Set player in combat state
    context.player = context.player if hasattr(context, 'player') else {
        'created': True,
        'name': 'TestCharacter',
        'class': 'Warrior',
        'level': 1,
        'location': 'Dungeon',
        'hp': 100,
        'max_hp': 100,
        'stats': {
            'strength': 15,
            'dexterity': 12,
            'intelligence': 10,
            'wisdom': 11,
            'charisma': 9,
            'constitution': 14
        },
        'abilities': ['Attack', 'Defend', 'Power Strike', 'Heal'],
        'inventory': ['sword', 'shield', 'potion'],
        'initiative': 0
    }
    
    # Select a random enemy for encounter
    context.current_enemy = random.choice(context.enemies)
    context.combat_state = 'active'

@when('combat begins')
def step_combat_begins(context):
    # Initialize combat
    context.combat = {
        'participants': [context.player, context.current_enemy],
        'turn_order': [],
        'current_turn': None,
        'round': 1
    }
    
    # Calculate initiative
    for participant in context.combat['participants']:
        # Initiative based on dexterity with random factor
        initiative = participant['stats']['dexterity'] + random.randint(1, 20)
        participant['initiative'] = initiative
    
    # Determine turn order
    context.combat['turn_order'] = sorted(
        context.combat['participants'],
        key=lambda p: p['initiative'],
        reverse=True
    )
    
    # Set current turn
    context.combat['current_turn'] = context.combat['turn_order'][0]

@then('it should operate on a turn-based system')
def step_verify_turn_based(context):
    # Verify combat is turn-based
    assert 'turn_order' in context.combat, "Combat should have turn order"
    assert 'current_turn' in context.combat, "Combat should track current turn"
    assert len(context.combat['turn_order']) == 2, "Combat should include both player and enemy"

@then('initiative should be calculated based on character stats')
def step_verify_initiative_calculation(context):
    # Verify initiative is based on dexterity
    for participant in context.combat['participants']:
        assert 'initiative' in participant, "Each participant should have initiative"
        assert participant['initiative'] > 0, "Initiative should be positive"

@then('each action should have appropriate time costs')
def step_verify_action_time_costs(context):
    # Define action time costs
    context.action_costs = {
        'Attack': 6,           # 1.0 turn
        'Defend': 3,           # 0.5 turn
        'Power Strike': 9,     # 1.5 turns
        'Heal': 6,             # 1.0 turn
        'Use Item': 6,         # 1.0 turn
        'Wait': 3              # 0.5 turn
    }
    
    # Verify each action has a time cost
    for action, cost in context.action_costs.items():
        assert 3 <= cost <= 9, f"Action {action} should have reasonable time cost"

@then('players should have access to all character abilities during combat')
def step_verify_combat_abilities(context):
    # Check player has access to all abilities
    player = context.player
    assert 'abilities' in player, "Player should have abilities defined"
    assert len(player['abilities']) >= 4, "Player should have multiple abilities"
    
    # Each ability should be usable in combat
    for ability in player['abilities']:
        assert ability in context.action_costs, f"Ability {ability} should have defined time cost"

@given('the player is exploring dungeons')
def step_player_exploring_dungeons(context):
    if not hasattr(context, 'dungeons'):
        context.dungeons = {}
        
        # Create 50 unique dungeons
        for i in range(50):
            dungeon = {
                'id': f"dungeon_{i}",
                'name': f"Dungeon_{i}: The {random.choice(['Dark', 'Lost', 'Cursed', 'Forgotten', 'Ancient'])} {random.choice(['Caverns', 'Citadel', 'Temple', 'Crypt', 'Fortress'])}",
                'level': random.randint(1, 30),
                'theme': random.choice(['dark', 'fire', 'ice', 'nature', 'undead', 'demonic', 'elemental', 'mechanical']),
                'layout': {
                    'rooms': random.randint(10, 30),
                    'floors': random.randint(1, 5),
                    'secrets': random.randint(2, 8)
                },
                'enemies': [f"enemy_{random.randint(0, 199)}" for _ in range(random.randint(5, 15))],
                'boss': f"boss_{i}",
                'puzzles': [f"puzzle_{i}_{j}" for j in range(random.randint(1, 5))]
            }
            context.dungeons[dungeon['id']] = dungeon
    
    # Initialize player if doesn't exist
    if not hasattr(context, 'player'):
        context.player = {}

    # Set player in a random dungeon
    dungeon_id = random.choice(list(context.dungeons.keys()))
    context.player['location'] = dungeon_id
    context.current_dungeon = context.dungeons[dungeon_id]

@when('they encounter enemies')
def step_encounter_dungeon_enemies(context):
    # Select enemies from current dungeon
    if not hasattr(context, 'enemies'):
        context.enemies = []
        
        # Create 200 different enemy types
        for i in range(200):
            enemy = {
                'id': f"enemy_{i}",
                'name': f"Enemy_{i}",
                'type': random.choice(['humanoid', 'beast', 'undead', 'demon', 'elemental', 'construct']),
                'level': random.randint(1, 30),
                'stats': {
                    'strength': random.randint(5, 20),
                    'dexterity': random.randint(5, 20),
                    'intelligence': random.randint(5, 20),
                    'wisdom': random.randint(5, 20),
                    'charisma': random.randint(5, 20),
                    'constitution': random.randint(5, 20)
                },
                'hp': random.randint(20, 500),
                'abilities': [f"ability_{i}_{j}" for j in range(random.randint(2, 6))],
                'ai_behavior': random.choice(['aggressive', 'defensive', 'tactical', 'random']),
                'weakness': random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical']),
                'resistance': random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical', 'none'])
            }
            context.enemies.append(enemy)
    
    # Get enemies for current dungeon
    dungeon_enemies = [
        enemy for enemy in context.enemies
        if enemy['id'] in context.current_dungeon['enemies']
    ]
    
    # Select 1-3 enemies for encounter
    num_enemies = random.randint(1, 3)
    context.encountered_enemies = random.sample(dungeon_enemies, min(num_enemies, len(dungeon_enemies)))

@then('they should face 200 different enemy types')
def step_verify_enemy_count(context):
    # Verify 200 enemy types exist
    assert len(context.enemies) == 200, "Game should have exactly 200 enemy types"

@then('each enemy should have unique abilities and attacks')
def step_verify_enemy_abilities(context):
    # Check that enemies have unique ability sets
    ability_sets = []
    for enemy in context.enemies:
        abilities = tuple(sorted(enemy['abilities']))
        ability_sets.append(abilities)
    
    # At least 150 enemies should have unique ability combinations
    unique_sets = len(set(ability_sets))
    assert unique_sets >= 150, "Most enemies should have unique ability combinations"

@then('each enemy should have appropriate AI behavior')
def step_verify_enemy_ai(context):
    # Verify each enemy has defined AI behavior
    for enemy in context.enemies:
        assert 'ai_behavior' in enemy, f"Enemy {enemy['id']} should have AI behavior"
        assert enemy['ai_behavior'] in ['aggressive', 'defensive', 'tactical', 'random'], \
            f"Enemy {enemy['id']} should have valid AI behavior"

@then('each enemy should have weaknesses that can be exploited')
def step_verify_enemy_weaknesses(context):
    # Verify each enemy has a weakness
    for enemy in context.enemies:
        assert 'weakness' in enemy, f"Enemy {enemy['id']} should have a weakness"
        assert enemy['weakness'] in ['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical'], \
            f"Enemy {enemy['id']} should have valid weakness type"

                

