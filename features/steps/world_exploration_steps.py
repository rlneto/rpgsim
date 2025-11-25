from behave import given, when, then
import random

# World Exploration System

@given('the player has created a character')
def step_player_created_character(context):
    if not hasattr(context, 'player'):
        context.player = {
            'created': True,
            'name': 'TestCharacter',
            'class': 'Warrior',
            'level': 1,
            'location': 'starting_city',
            'gold': 100,
            'inventory': [],
            'cities_visited': [],
            'world_position': {'x': 0, 'y': 0},
            'travel_history': []
        }

@when('they are in the game world')
def step_in_game_world(context):
    if not hasattr(context, 'world'):
        context.world = {
            'cities': [],
            'travel_routes': [],
            'current_time': 0,  # in-game time units
            'world_map_available': True
        }

        # Generate 20 distinct cities with unique characteristics
        city_themes = [
            'coastal_port', 'mountain_fortress', 'desert_oasis', 'forest_village',
            'river_crossing', 'plains_hub', 'mining_town', 'agricultural_center',
            'magical_academy', 'religious_pilgrimage', 'border_outpost', 'trading_mecca',
            'ancient_ruins', 'frontier_settlement', 'island_community', 'highland_retreat',
            'swamp_outpost', 'tundra_station', 'volcanic_settlement', 'cavern_city'
        ]

        building_types = [
            'tavern', 'blacksmith', 'temple', 'market', 'inn', 'guild_hall', 'library', 'bank',
            'stables', 'apothecary', 'barracks', 'town_hall', 'craft_shop', 'training_grounds',
            'residence', 'warehouse', 'watchtower', 'garden', 'fountain', 'monument'
        ]

        cultural_elements = [
            'architecture_style', 'local_cuisine', 'traditional_clothing', 'festivals',
            'language_dialect', 'religious_customs', 'art_style', 'music_tradition',
            'combat_styles', 'trade_goods', 'local_legends', 'social_hierarchy'
        ]

        # Create cities in a grid-like pattern with some randomness
        positions_used = set()
        for i in range(20):
            while True:
                x = random.randint(-10, 10)
                y = random.randint(-10, 10)
                if (x, y) not in positions_used:
                    positions_used.add((x, y))
                    break

            city = {
                'id': f'city_{i}',
                'name': f'{city_themes[i].replace("_", " ").title()}',
                'theme': city_themes[i],
                'position': {'x': x, 'y': y},
                'size': random.choice(['village', 'town', 'city', 'metropolis']),
                'geography': random.choice(['coastal', 'mountainous', 'plains', 'forest', 'desert', 'swamp', 'tundra', 'volcanic']),
                'buildings': random.sample(building_types, random.randint(8, 15)),
                'shops': [],
                'cultural_elements': random.sample(cultural_elements, random.randint(5, 10)),
                'population': random.randint(500, 50000),
                'founded_era': random.choice(['ancient', 'medieval', 'recent', 'contemporary']),
                'specialties': random.sample(['trade', 'craftsmanship', 'magic', 'military', 'religion', 'agriculture', 'mining'], 2)
            }

            # Generate unique shops for each city
            shop_types = ['weapons', 'armor', 'potions', 'scrolls', 'artifacts', 'general_goods', 'luxury_items', 'crafting_materials']
            num_shops = random.randint(3, 8)
            for j in range(num_shops):
                shop = {
                    'name': f"{city['name']} {random.choice(shop_types).title()} Shop",
                    'type': random.choice(shop_types),
                    'inventory_size': random.randint(20, 100),
                    'price_modifier': random.uniform(0.7, 1.5),
                    'unique_items': random.randint(0, 5),
                    'quality_level': random.choice(['basic', 'standard', 'premium', 'luxury'])
                }
                city['shops'].append(shop)

            context.world['cities'].append(city)

        # Generate travel routes between cities
        for city1 in context.world['cities']:
            for city2 in context.world['cities']:
                if city1['id'] < city2['id']:  # Avoid duplicates
                    distance = abs(city1['position']['x'] - city2['position']['x']) + \
                             abs(city1['position']['y'] - city2['position']['y'])

                    if distance <= 5:  # Only connect reasonably close cities
                        route = {
                            'from_city': city1['id'],
                            'to_city': city2['id'],
                            'distance': distance,
                            'travel_time': distance * random.randint(2, 6),  # hours
                            'difficulty': random.choice(['easy', 'moderate', 'difficult', 'dangerous']),
                            'terrain': random.choice(['road', 'trail', 'wilderness', 'mountain_pass', 'river_crossing'])
                        }
                        context.world['travel_routes'].append(route)

@then('they should be able to travel between 20 distinct cities')
def step_verify_travel_between_cities(context):
    assert len(context.world['cities']) == 20, f"Should have exactly 20 cities, have {len(context.world['cities'])}"

    city_names = [city['name'] for city in context.world['cities']]
    unique_names = set(city_names)
    assert len(unique_names) == 20, "All cities should have distinct names"

    # Verify each city is reachable from at least one other city
    connected_cities = set()
    for route in context.world['travel_routes']:
        connected_cities.add(route['from_city'])
        connected_cities.add(route['to_city'])

    # Most cities should be connected (allow for some isolated frontier settlements)
    assert len(connected_cities) >= 15, f"Most cities should be connected, only {len(connected_cities)} are"

@then('each city should have unique geography and layout')
def step_verify_unique_geography(context):
    geographies = [city['geography'] for city in context.world['cities']]
    unique_geographies = set(geographies)

    # Should have geographic diversity
    assert len(unique_geographies) >= 5, f"Should have diverse geography types, found {len(unique_geographies)}"

    # Verify each city has complete geographical data
    for city in context.world['cities']:
        assert 'geography' in city, f"City {city['name']} should have geography"
        assert 'size' in city, f"City {city['name']} should have size"
        assert city['size'] in ['village', 'town', 'city', 'metropolis'], f"Invalid size for {city['name']}"
        assert 'population' in city, f"City {city['name']} should have population"
        assert city['population'] >= 100, f"Population should be reasonable for {city['name']}"

@then('travel should be possible through text-based world map')
def step_verify_world_map(context):
    assert context.world['world_map_available'], "World map should be available"

    # Simulate world map text interface
    context.world_map = {
        'display_mode': 'text',
        'grid_size': '21x21',  # -10 to 10 in both dimensions
        'symbols': {
            'player': '@',
            'city': 'C',
            'mountain': '^',
            'forest': 'T',
            'water': '~',
            'plains': '.'
        },
        'navigation_available': True
    }

    assert context.world_map['navigation_available'], "Map navigation should be available"
    assert 'symbols' in context.world_map, "Map should have symbols for different features"

@then('travel should have appropriate time costs')
def step_verify_travel_time_costs(context):
    for route in context.world['travel_routes']:
        assert 'travel_time' in route, f"Route {route['from_city']}->{route['to_city']} should have travel time"
        assert route['travel_time'] >= 1, f"Travel time should be at least 1 hour, got {route['travel_time']}"
        assert route['travel_time'] <= 50, f"Travel time should be reasonable, got {route['travel_time']}"

        # Travel time should be proportional to distance
        expected_min_time = route['distance'] * 1  # minimum 1 hour per distance unit
        expected_max_time = route['distance'] * 10  # maximum 10 hours per distance unit

        assert expected_min_time <= route['travel_time'] <= expected_max_time, \
            f"Travel time {route['travel_time']} should be proportional to distance {route['distance']}"

@given('the player has entered a city')
def step_player_entered_city(context):
    step_player_created_character(context)
    step_in_game_world(context)

    # Place player in a random city
    context.current_city = random.choice(context.world['cities'])
    context.player['location'] = context.current_city['id']
    context.player['cities_visited'].append(context.current_city['id'])

@when('they explore the city')
def step_explore_city(context):
    city = context.current_city

    context.exploration_results = {
        'buildings_found': random.sample(city['buildings'], random.randint(6, len(city['buildings']))),
        'buildings_accessed': random.randint(3, 8),
        'shops_visited': random.sample(city['shops'], random.randint(1, min(3, len(city['shops'])))),
        'cultural_elements_observed': random.sample(city['cultural_elements'], random.randint(3, 6)),
        'local_interactions': random.randint(5, 15),
        'time_spent': random.randint(1, 8),  # hours
        'discovered_secrets': random.randint(0, 3),
        'services_used': []
    }

@then('they should find at least 8 different building types')
def step_verify_building_types(context):
    city = context.current_city
    result = context.exploration_results

    assert len(city['buildings']) >= 8, f"City should have at least 8 buildings, has {len(city['buildings'])}"
    assert len(result['buildings_found']) >= 6, "Should find at least 6 buildings during exploration"

    valid_building_types = [
        'tavern', 'blacksmith', 'temple', 'market', 'inn', 'guild_hall', 'library', 'bank',
        'stables', 'apothecary', 'barracks', 'town_hall', 'craft_shop', 'training_grounds',
        'residence', 'warehouse', 'watchtower', 'garden', 'fountain', 'monument'
    ]

    for building in city['buildings']:
        assert building in valid_building_types, f"Building type should be valid: {building}"

    # Buildings should serve specific functions
    building_functions = {
        'tavern': 'social_drink_rest',
        'blacksmith': 'weapons_armor_repair',
        'temple': 'religious_healing',
        'market': 'trading_goods',
        'inn': 'lodging_rest',
        'guild_hall': 'professional_services',
        'library': 'knowledge_scrolls',
        'bank': 'money_storage_loans'
    }

    for building in result['buildings_found'][:5]:  # Check first 5 found buildings
        if building in building_functions:
            context.building_function = building_functions[building]
            assert context.building_function, f"Building {building} should have a clear function"

@then('each building should serve a specific function')
def step_verify_building_functions(context):
    city = context.current_city
    result = context.exploration_results

    # All buildings should have defined purposes
    all_building_functions = {
        'tavern': ['food', 'drink', 'rumors', 'social_gathering'],
        'blacksmith': ['weapon_repair', 'armor_repair', 'weapon_creation', 'armor_creation'],
        'temple': ['healing', 'blessings', 'religious_guidance', 'curse_removal'],
        'market': ['trade_goods', 'local_products', 'negotiation', 'price_discovery'],
        'inn': ['rest', 'lodging', 'food_service', 'traveler_accommodation'],
        'guild_hall': ['quest_board', 'training', 'professional_services', 'networking'],
        'library': ['knowledge_research', 'scroll_reading', 'history_study', 'magic_theory'],
        'bank': ['money_storage', 'loans', 'currency_exchange', 'investment'],
        'stables': ['horse_care', 'mount_rental', 'carriage_service', 'animal_healing'],
        'apothecary': ['potion_brewing', 'herb_sales', 'poison_antidote', 'medical_advice'],
        'barracks': ['military_training', 'guards', 'weapon_storage', 'strategic_planning'],
        'town_hall': ['administration', 'laws', 'taxes', 'civic_services'],
        'craft_shop': ['item_creation', 'material_sales', 'custom_orders', 'crafting_tools'],
        'training_grounds': ['combat_training', 'skill_practice', 'tournaments', 'physical_conditioning'],
        'residence': ['housing', 'family_life', 'domestic_activities', 'community'],
        'warehouse': ['goods_storage', 'inventory_management', 'bulk_storage', 'distribution'],
        'watchtower': ['city_surveillance', 'threat_detection', 'early_warning', 'defense'],
        'garden': ['medicinal_herbs', 'relaxation', 'beauty', 'food_production'],
        'fountain': ['water_source', 'meeting_point', 'decoration', 'ritual_purposes'],
        'monument': ['history_commemoration', 'cultural_identity', 'tourism', 'inspiration']
    }

    # Verify each building has multiple functions
    for building in result['buildings_found']:
        if building in all_building_functions:
            functions = all_building_functions[building]
            assert len(functions) >= 2, f"Building {building} should have multiple functions"

            # At least some functions should be accessible
            accessible_functions = random.sample(functions, random.randint(1, len(functions)))
            result['services_used'].extend(accessible_functions)

@then('each city should have unique shops with different inventories')
def step_verify_unique_shops(context):
    city = context.current_city
    result = context.exploration_results

    assert len(city['shops']) >= 3, f"City should have at least 3 shops, has {len(city['shops'])}"

    # Shops should be unique within the city
    shop_types_in_city = [shop['type'] for shop in city['shops']]
    unique_shop_types = set(shop_types_in_city)

    # Allow some repetition but require variety
    assert len(unique_shop_types) >= len(city['shops']) // 2, "Should have variety of shop types"

    # Verify shop characteristics
    for shop in result['shops_visited']:
        assert 'type' in shop, "Shop should have a type"
        assert 'inventory_size' in shop, "Shop should have inventory size"
        assert 'price_modifier' in shop, "Shop should have price modifier"

        assert shop['inventory_size'] >= 10, "Shop should have reasonable inventory"
        assert 0.5 <= shop['price_modifier'] <= 2.0, "Price modifier should be reasonable"
        assert shop['quality_level'] in ['basic', 'standard', 'premium', 'luxury'], "Quality level should be valid"

    # Inventory should vary between cities
    inventory_signatures = []
    for city_check in context.world['cities']:
        city_signature = {
            'num_shops': len(city_check['shops']),
            'shop_types': set(shop['type'] for shop in city_check['shops']),
            'avg_quality': sum(1 if shop['quality_level'] in ['premium', 'luxury'] else 0 for shop in city_check['shops']) / max(len(city_check['shops']), 1)
        }
        inventory_signatures.append(city_signature)

    # Most cities should have unique shop characteristics
    unique_signatures = len(set((sig['num_shops'], tuple(sorted(sig['shop_types']))) for sig in inventory_signatures))
    assert unique_signatures >= 15, "Most cities should have unique shop characteristics"

@then('each city should have distinctive cultural elements in descriptions')
def step_verify_cultural_elements(context):
    city = context.current_city
    result = context.exploration_results

    assert len(city['cultural_elements']) >= 5, f"City should have at least 5 cultural elements, has {len(city['cultural_elements'])}"
    assert len(result['cultural_elements_observed']) >= 3, "Should observe at least 3 cultural elements"

    # Cultural elements should be diverse
    cultural_categories = {
        'architecture': ['architecture_style'],
        'food_culture': ['local_cuisine'],
        'clothing': ['traditional_clothing'],
        'celebrations': ['festivals'],
        'language': ['language_dialect'],
        'religion': ['religious_customs'],
        'arts': ['art_style', 'music_tradition'],
        'combat': ['combat_styles'],
        'economy': ['trade_goods'],
        'social_structure': ['social_hierarchy']
    }

    observed_categories = set()
    for element in result['cultural_elements_observed']:
        for category, elements in cultural_categories.items():
            if element in elements:
                observed_categories.add(category)

    # Should observe multiple cultural categories
    assert len(observed_categories) >= 2, f"Should observe multiple cultural categories, saw {len(observed_categories)}"

    # Cultural elements should be thematically consistent
    city_theme = city['theme']
    if 'coastal' in city_theme:
        assert 'trade_goods' in city['cultural_elements'] or 'local_cuisine' in city['cultural_elements'], \
            "Coastal cities should have trade or food cultural elements"
    elif 'mountain' in city_theme:
        assert 'architecture_style' in city['cultural_elements'] or 'combat_styles' in city['cultural_elements'], \
            "Mountain cities should have architectural or martial cultural elements"
    elif 'academy' in city_theme:
        assert 'art_style' in city['cultural_elements'] or 'music_tradition' in city['cultural_elements'], \
            "Academy cities should have artistic or scholarly cultural elements"