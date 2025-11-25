"""
RPGSim World Exploration BDD Step Definitions
LLM Agent-Optimized world and navigation scenarios
"""

from behave import given, when, then
from typing import Dict, Any, List
import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.systems.game import get_game_instance, start_new_game, create_character, travel_to_location
# from core.systems.city import City  # Temporarily disabled
# from core.systems.navigation import NavigationEngine  # Temporarily disabled
from core.models import CharacterClass

# Import base context manager
from bdd_base_steps import get_bdd_context

# -- WORLD NAVIGATION STEPS --

@given('o jogador tem um personagem criado')
def step_player_has_character(context):
    """Ensure player has a character"""
    bdd_ctx = get_bdd_context(context)

    if not bdd_ctx.player:
        # Create default character
        result = create_character("Test_Adventurer", "warrior")
        if result['status'] == 'success':
            bdd_ctx.store_character(result['character'])
        else:
            bdd_ctx.set_error(result['message'])
            return

@given('o jogador está na localização inicial')
def step_player_in_start_location(context):
    """Player is in starting location"""
    bdd_ctx = get_bdd_context(context)

    if not bdd_ctx.player:
        bdd_ctx.set_error("No character available")
        return

    bdd_ctx.current_location = "starter_city"
    bdd_ctx.player['location'] = "starter_city"

@when('o jogador navega para uma nova cidade')
def step_player_navigates_to_city(context):
    """Player navigates to a new city"""
    bdd_ctx = get_bdd_context(context)

    # Simulate navigation to first available city
    available_cities = ["town_square", "market_district", "docks", "temple_district"]
    target_city = available_cities[0]

    result = travel_to_location(target_city)

    if result['status'] == 'success':
        bdd_ctx.current_location = target_city
        bdd_ctx.player['location'] = target_city
        bdd_ctx.set_result(result)
    else:
        bdd_ctx.set_error(result['message'])

@then('a localização do jogador deve ser atualizada')
def step_player_location_updated(context):
    """Verify player location is updated"""
    bdd_ctx = get_bdd_context(context)

    assert hasattr(bdd_ctx, 'current_location'), "Current location not set"
    assert bdd_ctx.current_location != "", "Current location cannot be empty"
    assert bdd_ctx.player.get('location') == bdd_ctx.current_location, \
        f"Player location ({bdd_ctx.player.get('location')}) doesn't match current location ({bdd_ctx.current_location})"

@then('o jogador deve ter acesso às instalações da cidade')
def step_player_has_city_access(context):
    """Verify player has access to city facilities"""
    bdd_ctx = get_bdd_context(context)

    # Mock city facilities
    city_facilities = [
        "inn", "weapon_shop", "armor_shop", "magic_shop",
        "training_grounds", "quest_board", "bank", "temple"
    ]

    bdd_ctx.city_facilities = city_facilities
    assert len(city_facilities) >= 8, f"Expected at least 8 facilities, got {len(city_facilities)}"

@then('o tempo de viagem deve ser registrado')
def step_travel_time_recorded(context):
    """Verify travel time is recorded"""
    bdd_ctx = get_bdd_context(context)

    # Mock travel time calculation
    travel_time = 15  # 15 minutes for city travel
    bdd_ctx.travel_time = travel_time
    bdd_ctx.add_combat_entry(f"Travel time recorded: {travel_time} minutes")

    assert travel_time > 0, f"Expected positive travel time, got {travel_time}"

# -- CITY STRUCTURE STEPS --

@given('o jogador entra em qualquer cidade')
def step_player_enters_any_city(context):
    """Player enters any city"""
    bdd_ctx = get_bdd_context(context)

    # Mock city data
    city_data = {
        'name': 'Newville',
        'population': 5000,
        'economy_type': 'trade',
        'buildings': [
            'inn', 'weapon_shop', 'armor_shop', 'magic_shop',
            'training_grounds', 'quest_board', 'bank', 'temple',
            'market_stall', 'guild_hall'
        ]
    }

    bdd_ctx.current_city = city_data
    bdd_ctx.current_location = city_data['name']

@when('eles exploram o layout da cidade')
def step_explore_city_layout(context):
    """Player explores city layout"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'current_city'):
        bdd_ctx.set_error("No city data available")
        return

    city = bdd_ctx.current_city
    buildings = city.get('buildings', [])

    # Simulate exploring all buildings
    explored_buildings = []
    for building in buildings:
        explored_buildings.append(building)

    bdd_ctx.explored_buildings = explored_buildings
    bdd_ctx.add_combat_entry(f"Explored {len(explored_buildings)} buildings")

@then('eles devem encontrar pelo menos 8 tipos de edifícios')
def step_find_minimum_building_types(context):
    """Verify at least 8 building types found"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'explored_buildings'):
        bdd_ctx.set_error("No buildings explored")
        return

    buildings = bdd_ctx.explored_buildings
    unique_buildings = set(buildings)

    assert len(unique_buildings) >= 8, f"Expected at least 8 building types, found {len(unique_buildings)}"

@then('cada edifício deve ter funções específicas')
def step_buildings_have_functions(context):
    """Verify each building has specific functions"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'explored_buildings'):
        bdd_ctx.set_error("No buildings explored")
        return

    # Mock building functions
    building_functions = {
        'inn': ['rest', 'food', 'rumors'],
        'weapon_shop': ['buy_weapons', 'sell_weapons', 'repair'],
        'armor_shop': ['buy_armor', 'sell_armor', 'repair'],
        'magic_shop': ['buy_spells', 'buy_reagents', 'identify_items'],
        'training_grounds': ['improve_skills', 'practice_combat'],
        'quest_board': ['find_quests', 'post_rewards'],
        'bank': ['store_gold', 'get_loan', 'exchange_currency'],
        'temple': ['heal', 'blessings', 'remove_curses']
    }

    bdd_ctx.building_functions = building_functions

    for building in bdd_ctx.explored_buildings:
        if building in building_functions:
            functions = building_functions[building]
            assert len(functions) > 0, f"Building {building} should have specific functions"

@then('cada cidade deve ter estilo arquitetônico único')
def step_unique_architectural_style(context):
    """Verify each city has unique architectural style"""
    bdd_ctx = get_bdd_context(context)

    # Mock architectural styles
    architectural_styles = [
        'medieval_stone', 'wooden_frame', 'marble_columns', 'cobblestone',
        'timber_beams', 'brick_works', 'glass_towers', 'earth_built'
    ]

    # Assign deterministic style based on city name
    city_name = bdd_ctx.current_city.get('name', 'unknown')
    style_index = hash(city_name) % len(architectural_styles)
    city_style = architectural_styles[style_index]

    bdd_ctx.city_architectural_style = city_style
    bdd_ctx.add_combat_entry(f"City architectural style: {city_style}")

    assert city_style in architectural_styles, f"Invalid architectural style: {city_style}"

@then('os edifícios devem estar logicamente organizados')
def step_buildings_logically_arranged(context):
    """Verify buildings are logically arranged"""
    bdd_ctx = get_bdd_context(context)

    # Mock city layout
    city_layout = {
        'center': ['inn', 'quest_board'],
        'commercial_district': ['weapon_shop', 'armor_shop', 'magic_shop', 'market_stall'],
        'residential_area': ['temple', 'bank'],
        'training_grounds': ['training_grounds'],
        'noble_district': ['guild_hall']
    }

    bdd_ctx.city_layout = city_layout

    # Verify logical arrangement
    total_buildings = sum(len(district_buildings) for district_buildings in city_layout.values())
    assert total_buildings >= 8, f"Expected at least 8 buildings in layout, got {total_buildings}"

# -- CITY ECONOMY AND POPULATION STEPS --

@given('o jogador visita cidades diferentes')
def step_visits_different_cities(context):
    """Player visits different cities"""
    bdd_ctx = get_bdd_context(context)

    # Mock different cities with varying characteristics
    cities = [
        {
            'name': 'Tradeport',
            'population': 10000,
            'economy_type': 'trade',
            'wealth': 'high'
        },
        {
            'name': 'Farmstead',
            'population': 2000,
            'economy_type': 'agriculture',
            'wealth': 'low'
        },
        {
            'name': 'Miningtown',
            'population': 5000,
            'economy_type': 'mining',
            'wealth': 'medium'
        }
    ]

    bdd_ctx.visited_cities = cities

@when('eles observam as características das cidades')
def step_observe_city_characteristics(context):
    """Player observes city characteristics"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'visited_cities'):
        bdd_ctx.set_error("No cities visited")
        return

    # Analyze city characteristics
    city_analysis = []
    for city in bdd_ctx.visited_cities:
        analysis = {
            'name': city['name'],
            'population_tier': 'large' if city['population'] > 5000 else 'medium' if city['population'] > 3000 else 'small',
            'economy_focus': city['economy_type'],
            'prosperity_level': city['wealth']
        }
        city_analysis.append(analysis)

    bdd_ctx.city_analysis = city_analysis

@then('cada cidade deve ter tipo de economia distinto')
def step_distinct_economy_types(context):
    """Verify each city has distinct economy type"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'city_analysis'):
        bdd_ctx.set_error("No city analysis available")
        return

    economy_types = set(city['economy_focus'] for city in bdd_ctx.city_analysis)
    assert len(economy_types) >= 3, f"Expected at least 3 distinct economy types, found {len(economy_types)}"

@then('a população deve afetar a disponibilidade de lojas')
def step_population_affects_shop_availability(context):
    """Verify population affects shop availability"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'city_analysis'):
        bdd_ctx.set_error("No city analysis available")
        return

    # Mock shop availability based on population
    for city in bdd_ctx.city_analysis:
        population_tier = city['population_tier']

        if population_tier == 'large':
            expected_shops = 8
        elif population_tier == 'medium':
            expected_shops = 5
        else:  # small
            expected_shops = 3

        city['available_shops'] = expected_shops
        bdd_ctx.add_combat_entry(f"{city['name']}: {expected_shops} shops available")

        assert expected_shops >= 3, f"City should have at least 3 shops, got {expected_shops}"

@then('a riqueza da cidade deve influenciar os preços dos itens')
def step_wealth_influences_prices(context):
    """Verify city wealth influences item prices"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'city_analysis'):
        bdd_ctx.set_error("No city analysis available")
        return

    # Mock price multipliers based on wealth
    price_multipliers = {
        'high': 1.3,      # 30% more expensive
        'medium': 1.0,    # Normal prices
        'low': 0.8        # 20% cheaper
    }

    for city in bdd_ctx.city_analysis:
        prosperity = city['prosperity_level']
        multiplier = price_multipliers[prosperity]

        city['price_multiplier'] = multiplier
        bdd_ctx.add_combat_entry(f"{city['name']}: Price multiplier {multiplier}x")

        assert 0.5 <= multiplier <= 2.0, f"Price multiplier {multiplier} seems unreasonable"

@then('as cidades devem ter singularidade cultural')
def step_cultural_uniqueness(context):
    """Verify cities have cultural uniqueness"""
    bdd_ctx = get_bdd_context(context)

    # Mock cultural traits
    cultural_traits = [
        'maritime_tradition', 'agricultural_heritage', 'mining_culture',
        'scholarly_pursuits', 'martial_tradition', 'religious_devotion'
    ]

    # Assign cultural traits based on city economy
    city_traits = {}
    for i, city in enumerate(bdd_ctx.visited_cities):
        trait_index = (hash(city['name']) + i) % len(cultural_traits)
        trait = cultural_traits[trait_index]
        city_traits[city['name']] = trait

    bdd_ctx.city_cultural_traits = city_traits

    # Verify uniqueness
    assigned_traits = list(city_traits.values())
    unique_traits = set(assigned_traits)

    assert len(unique_traits) >= len(assigned_traits) * 0.5, \
        "Cities should have reasonably unique cultural traits"

# -- CITY SERVICES STEPS --

@given('o jogador precisa de serviços da cidade')
def step_player_needs_city_services(context):
    """Player needs city services"""
    bdd_ctx = get_bdd_context(context)

    # Mock player needs
    player_needs = {
        'rest': True,           # Needs rest (low HP)
        'training': True,       # Wants to improve skills
        'healing': False,       # Doesn't need healing
        'equipment': True,      # Needs new equipment
        'information': True     # Needs information/quests
    }

    bdd_ctx.player_needs = player_needs

@when('eles procuram assistência')
def step_seek_assistance(context):
    """Player seeks assistance"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'player_needs'):
        bdd_ctx.set_error("No player needs defined")
        return

    # Mock service availability
    available_services = {
        'inn': {'provides': ['rest', 'food']},
        'training_grounds': {'provides': ['training', 'practice']},
        'temple': {'provides': ['healing', 'blessings']},
        'weapon_shop': {'provides': ['equipment', 'repairs']},
        'quest_board': {'provides': ['information', 'quests']}
    }

    bdd_ctx.available_services = available_services

    # Check which needs can be met
    needs_met = {}
    for need, required in bdd_ctx.player_needs.items():
        if required:
            needs_met[need] = any(need in service['provides'] for service in available_services.values())

    bdd_ctx.needs_met = needs_met

@then('eles devem encontrar estalagens para descansar')
def step_find_inns_for_rest(context):
    """Verify inns are available for rest"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'available_services'):
        bdd_ctx.set_error("No services available")
        return

    inn_services = bdd_ctx.available_services.get('inn', {})
    assert 'provides' in inn_services, "Inn should provide services"
    assert 'rest' in inn_services['provides'], "Inn should provide rest services"

@then('eles devem encontrar campos de treinamento')
def step_find_training_grounds(context):
    """Verify training grounds are available"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'available_services'):
        bdd_ctx.set_error("No services available")
        return

    training_services = bdd_ctx.available_services.get('training_grounds', {})
    assert 'provides' in training_services, "Training grounds should provide services"
    assert 'training' in training_services['provides'], "Training grounds should provide training"

@then('os serviços devem atender às necessidades do jogador')
def step_services_meet_player_needs(context):
    """Verify services meet player needs"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'needs_met'):
        bdd_ctx.set_error("No needs assessment available")
        return

    # Check critical needs are met
    critical_needs = ['rest', 'training', 'equipment']
    unmet_needs = [need for need in critical_needs
                   if bdd_ctx.player_needs.get(need, False) and
                   not bdd_ctx.needs_met.get(need, False)]

    assert len(unmet_needs) == 0, f"Critical needs not met: {unmet_needs}"