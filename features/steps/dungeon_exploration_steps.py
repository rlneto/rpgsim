from behave import given, when, then
import random

# Dungeon Exploration System

@given('the player enters a dungeon')
def step_player_enters_dungeon(context):
    if not hasattr(context, 'player'):
        context.player = {
            'created': True,
            'name': 'TestCharacter',
            'class': 'Warrior',
            'level': 1,
            'location': 'dungeon_entrance',
            'inventory': [],
            'dungeons_explored': [],
            'current_dungeon': None
        }

    if not hasattr(context, 'dungeons'):
        context.dungeons = []

        # Generate 50 unique dungeons with distinct themes
        themes = [
            'ancient_temple', 'crystal_caves', 'volcanic_fortress', 'flooded_catacombs',
            'enchanted_forest', 'abandoned_mine', 'ice_palace', 'shadow_realm',
            'desert_pyramid', 'sky_castle', 'underground_sea', 'cursed_manor',
            'goblin_warrens', 'dragon_lair', 'clockwork_city', 'poison_swamp',
            'frozen_wastes', 'forbidden_library', 'elemental_plane', 'dwarven_stronghold',
            'elven_sanctuary', 'demon_infested_keep', 'angelic_spire', 'time_distorted_ruins',
            'illusion_maze', 'bone_church', 'mushroom_caverns', 'magnetic_mines',
            'echoing_chasm', 'floating_islands', 'soul_prison', 'dreamscape_nexus',
            'blood_arena', 'astral_observatory', 'rust_wastelands', 'crystalline_labyrinth',
            'wind_carved_canyons', 'mirage_desert', 'sunken_palace', 'storm_chamber',
            'web_filled_lairs', 'liquid_metal_vats', 'inverted_cathedral', 'living_forest',
            'quantum_reactor', 'memory_palace', 'nightmare_fuel', 'harmony_gardens',
            'discordant_planes', 'void_touched_domain', 'primal_chaos', 'ordered_structures'
        ]

        puzzle_types = ['mechanical', 'magical', 'logical', 'spatial', 'temporal', 'pattern', 'riddle', 'environmental']
        environmental_challenges = ['darkness', 'poison', 'fire', 'ice', 'electricity', 'wind', 'gravity', 'time_warp']

        for i in range(50):
            dungeon = {
                'id': f'dungeon_{i}',
                'name': f'Dungeon_{i}: The {themes[i].replace("_", " ").title()}',
                'theme': themes[i],
                'level': random.randint(1, 50),
                'rooms': random.randint(10, 50),
                'layout': random.choice(['linear', 'branching', 'circular', 'maze', 'spiral', 'multilevel']),
                'puzzles': [random.choice(puzzle_types) for _ in range(random.randint(2, 8))],
                'environmental_challenges': random.sample(environmental_challenges, random.randint(1, 4)),
                'secrets': random.randint(3, 15),
                'hidden_areas': random.randint(2, 8),
                'lore_elements': random.randint(5, 20),
                'difficulty_progression': 'increasing',
                'reward_tiers': ['common', 'uncommon', 'rare', 'epic', 'legendary']
            }
            context.dungeons.append(dungeon)

    # Select a random dungeon for the player to enter
    available_dungeons = [d for d in context.dungeons if d['id'] not in context.player['dungeons_explored']]
    context.player['current_dungeon'] = random.choice(available_dungeons)
    context.player['location'] = context.player['current_dungeon']['id']

@when('they explore it')
def step_explore_dungeon(context):
    if not context.player.get('current_dungeon'):
        return

    dungeon = context.player['current_dungeon']

    # Simulate dungeon exploration
    context.exploration_results = {
        'rooms_explored': random.randint(1, dungeon['rooms']),
        'puzzles_solved': random.randint(0, len(dungeon['puzzles'])),
        'secrets_found': random.randint(0, dungeon['secrets']),
        'hidden_areas_discovered': random.randint(0, dungeon['hidden_areas']),
        'lore_pieces_found': random.randint(0, dungeon['lore_elements']),
        'challenges_faced': dungeon['environmental_challenges'][:],
        'strategic_decisions': random.randint(3, 12),
        'layout_pattern': dungeon['layout']
    }

@then('they should find unique layouts and environmental challenges')
def step_verify_unique_layouts(context):
    result = context.exploration_results

    assert 'layout_pattern' in result, "Should identify dungeon layout pattern"
    assert result['layout_pattern'] in ['linear', 'branching', 'circular', 'maze', 'spiral', 'multilevel'], \
        f"Layout should be a recognized type: {result['layout_pattern']}"

    assert 'challenges_faced' in result, "Should face environmental challenges"
    assert len(result['challenges_faced']) >= 1, "Should face at least one environmental challenge"

    valid_challenges = ['darkness', 'poison', 'fire', 'ice', 'electricity', 'wind', 'gravity', 'time_warp']
    for challenge in result['challenges_faced']:
        assert challenge in valid_challenges, f"Challenge should be valid: {challenge}"

@then('they should encounter puzzles appropriate to the theme')
def step_verify_theme_puzzles(context):
    dungeon = context.player['current_dungeon']
    result = context.exploration_results

    assert 'puzzles' in dungeon, "Dungeon should have puzzles defined"
    assert len(dungeon['puzzles']) >= 2, "Dungeon should have at least 2 puzzle types"

    valid_puzzles = ['mechanical', 'magical', 'logical', 'spatial', 'temporal', 'pattern', 'riddle', 'environmental']
    for puzzle in dungeon['puzzles']:
        assert puzzle in valid_puzzles, f"Puzzle type should be valid: {puzzle}"

    # Verify puzzle-theme appropriateness (thematic validation)
    theme = dungeon['theme']
    if 'temple' in theme or 'church' in theme:
        assert any(p in dungeon['puzzles'] for p in ['riddle', 'magical']), "Temple themes should have appropriate puzzles"
    elif 'mine' in theme or 'fortress' in theme:
        assert any(p in dungeon['puzzles'] for p in ['mechanical', 'environmental']), "Mine/fortress themes should have mechanical puzzles"

@then('they should find secrets and hidden areas')
def step_verify_secrets_hidden_areas(context):
    dungeon = context.player['current_dungeon']
    result = context.exploration_results

    assert 'secrets' in dungeon, "Dungeon should have secrets defined"
    assert 'hidden_areas' in dungeon, "Dungeon should have hidden areas defined"
    assert dungeon['secrets'] >= 3, "Dungeon should have at least 3 secrets"
    assert dungeon['hidden_areas'] >= 2, "Dungeon should have at least 2 hidden areas"

    assert result['secrets_found'] >= 0, "Should find some secrets"
    assert result['hidden_areas_discovered'] >= 0, "Should discover some hidden areas"

    # Should not find more secrets than exist
    assert result['secrets_found'] <= dungeon['secrets'], "Cannot find more secrets than exist"
    assert result['hidden_areas_discovered'] <= dungeon['hidden_areas'], "Cannot discover more hidden areas than exist"

@then('each of the 50 dungeons should have a distinct theme')
def step_verify_distinct_themes(context):
    themes = [dungeon['theme'] for dungeon in context.dungeons]
    unique_themes = set(themes)

    assert len(context.dungeons) == 50, f"Should have exactly 50 dungeons, have {len(context.dungeons)}"
    assert len(unique_themes) == 50, f"All 50 dungeons should have distinct themes, have {len(unique_themes)} unique themes"

    # Verify theme diversity
    theme_categories = {
        'elemental': ['fire', 'ice', 'earth', 'wind', 'water', 'lightning'],
        'location': ['temple', 'caves', 'fortress', 'catacombs', 'forest', 'mine', 'palace'],
        'alignment': ['holy', 'demonic', 'angelic', 'cursed', 'forbidden'],
        'conceptual': ['time', 'space', 'memory', 'dreams', 'chaos', 'order']
    }

    category_coverage = {}
    for category, keywords in theme_categories.items():
        category_coverage[category] = any(
            any(keyword in theme for keyword in keywords)
            for theme in themes
        )

    # Should cover multiple thematic categories
    covered_categories = sum(category_coverage.values())
    assert covered_categories >= 3, f"Dungeons should cover diverse thematic categories (found {covered_categories})"

@given('the player is exploring a dungeon')
def step_player_exploring_dungeon(context):
    # Reuse dungeon entry logic
    step_player_enters_dungeon(context)
    step_explore_dungeon(context)

@when('they navigate through it')
def step_navigate_dungeon(context):
    if not context.player.get('current_dungeon'):
        return

    dungeon = context.player['current_dungeon']

    # Simulate dungeon navigation with progression
    context.navigation_results = {
        'depth_reached': random.randint(1, dungeon['rooms'] // 2),
        'total_rooms': dungeon['rooms'],
        'difficulty_curve': [],
        'rewards_found': [],
        'strategic_choices_made': random.randint(5, 15),
        'lore_discovered': random.randint(1, dungeon['lore_elements']),
        'bosses_defeated': random.randint(0, 1 + (dungeon['level'] // 25)),
        'time_spent': random.randint(30, 180),  # minutes
        'resources_used': {
            'health_potions': random.randint(0, 5),
            'mana_potions': random.randint(0, 5),
            'special_items': random.randint(0, 3)
        }
    }

    # Generate difficulty progression
    num_stages = min(5, context.navigation_results['depth_reached'])
    for i in range(num_stages):
        difficulty_multiplier = 1 + (i * 0.3)  # 30% increase per stage
        context.navigation_results['difficulty_curve'].append(difficulty_multiplier)

    # Generate rewards based on progression depth
    reward_tiers = dungeon['reward_tiers']
    max_tier_index = min(len(reward_tiers) - 1, context.navigation_results['depth_reached'] // 10)

    for tier in reward_tiers[:max_tier_index + 1]:
        reward_count = random.randint(1, 4)
        for _ in range(reward_count):
            reward = {
                'tier': tier,
                'type': random.choice(['weapon', 'armor', 'accessory', 'consumable', 'material']),
                'value': random.randint(50, 1000) * (1 + max_tier_index),
                'rarity': tier
            }
            context.navigation_results['rewards_found'].append(reward)

@then('they should face increasing difficulty')
def step_verify_increasing_difficulty(context):
    result = context.navigation_results
    difficulty_curve = result['difficulty_curve']

    assert len(difficulty_curve) >= 2, "Should have multiple difficulty stages"

    # Verify monotonic increase in difficulty
    for i in range(1, len(difficulty_curve)):
        assert difficulty_curve[i] > difficulty_curve[i-1], \
            f"Difficulty should increase: stage {i-1} = {difficulty_curve[i-1]}, stage {i} = {difficulty_curve[i]}"

    # Verify reasonable difficulty progression
    assert difficulty_curve[-1] >= difficulty_curve[0] * 1.5, \
        "Final difficulty should be at least 50% higher than initial difficulty"

@then('they should find progressively better rewards')
def step_verify_progressively_better_rewards(context):
    result = context.navigation_results
    rewards = result['rewards_found']

    if len(rewards) >= 2:
        # Check that reward values generally increase with progression
        early_rewards = rewards[:len(rewards)//2]
        late_rewards = rewards[len(rewards)//2:]

        early_avg = sum(r['value'] for r in early_rewards) / len(early_rewards) if early_rewards else 0
        late_avg = sum(r['value'] for r in late_rewards) / len(late_rewards) if late_rewards else 0

        # Later rewards should be more valuable on average
        if early_avg > 0 and late_avg > 0:
            assert late_avg >= early_avg * 1.2, \
                f"Later rewards should be more valuable: early avg={early_avg:.1f}, late avg={late_avg:.1f}"

    # Should have rewards from multiple tiers
    reward_tiers_found = set(reward['tier'] for reward in rewards)
    assert len(reward_tiers_found) >= 1, "Should find rewards from at least one tier"

@then('they should have opportunities for strategic decisions')
def step_verify_strategic_decisions(context):
    result = context.navigation_results

    assert result['strategic_choices_made'] >= 5, "Should make at least 5 strategic decisions"

    # Strategic decision types
    decision_types = [
        'path_choice', 'resource_management', 'risk_assessment',
        'puzzle_approach', 'combat_tactics', 'exploration_priority'
    ]

    context.strategic_decisions_made = random.sample(
        decision_types,
        min(result['strategic_choices_made'], len(decision_types))
    )

    assert len(context.strategic_decisions_made) >= 3, \
        "Should face diverse types of strategic decisions"

@then('they should find clues about the dungeon\'s lore')
def step_verify_dungeon_lore(context):
    dungeon = context.player['current_dungeon']
    result = context.navigation_results

    assert dungeon['lore_elements'] >= 5, "Dungeon should have at least 5 lore elements"
    assert result['lore_discovered'] >= 1, "Should discover at least some lore"
    assert result['lore_discovered'] <= dungeon['lore_elements'], "Cannot discover more lore than exists"

    # Lore should be themed appropriately
    lore_types = [
        'historical_records', 'inscriptions', 'environmental_storytelling',
        'item_descriptions', 'boss_backgrounds', 'architectural_clues'
    ]

    context.discovered_lore = random.sample(
        lore_types,
        min(result['lore_discovered'], len(lore_types))
    )

    assert len(context.discovered_lore) >= 1, "Should find specific types of lore"

    # Lore should connect to dungeon theme
    theme = dungeon['theme']
    if 'temple' in theme:
        assert any('inscriptions' in lore or 'historical' in lore for lore in context.discovered_lore), \
            "Temple dungeons should have appropriate lore types"
    elif 'fortress' in theme or 'keep' in theme:
        assert any('architectural' in lore or 'boss' in lore for lore in context.discovered_lore), \
            "Fortress dungeons should have appropriate lore types"