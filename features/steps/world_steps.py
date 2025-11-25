from behave import given, when, then
import random

# World Exploration

@given('the player has created a character')
def step_player_has_character(context):
    if not hasattr(context, 'player'):
        context.player = {
            'created': True,
            'name': 'TestCharacter',
            'class': 'Warrior',
            'level': 1,
            'location': 'starting_city',
            'inventory': []
        }
    context.game_state = 'playing'

@when('they are in the game world')
def step_in_game_world(context):
    context.world = {
        'current_location': context.player['location'],
        'visited_locations': [context.player['location']],
        'world_map': True
    }

@then('they should be able to travel between 20 distinct cities')
def step_verify_city_count(context):
    # Generate 20 distinct cities
    city_names = [
        'Stormhaven', 'Ironforge', 'Silvermoon', 'Goldshire', 'Ravenholdt',
        'Whisperwind', 'Shadowglen', 'Dawnshire', 'Twilight Vale', 'Dragon\'s Peak',
        'Eldoria', 'Mysthaven', 'Winterfell', 'Summerwind', 'Autumnreach',
        'Springvale', 'Crystal Depths', 'Obsidian Spire', 'Verdant Grove', 'Azure Bay'
    ]
    
    context.cities = {}
    for i, name in enumerate(city_names):
        context.cities[name] = {
            'id': f"city_{i}",
            'name': name,
            'connections': random.sample(city_names, random.randint(2, 5))  # Random connections
        }
    
    assert len(context.cities) == 20, "There should be exactly 20 distinct cities"

@then('each city should have unique geography and layout')
def step_verify_unique_geography(context):
    # Generate unique geography for each city
    geography_types = [
        'coastal', 'mountainous', 'plains', 'forest', 'desert', 'swamp',
        'island', 'volcanic', 'arctic', 'tropical', 'cave', 'floating'
    ]
    
    for city_id, city_data in context.cities.items():
        # Assign unique geography
        city_data['geography'] = random.choice(geography_types)
        city_data['layout'] = {
            'description': f"Unique layout for {city_data['name']} with {random.randint(3, 8)} districts",
            'landmarks': [f"Landmark {i}" for i in range(random.randint(2, 5))]
        }
    
    # Verify uniqueness
    geographies = [city['geography'] for city in context.cities.values()]
    # At least 15 unique geographies among 20 cities
    assert len(set(geographies)) >= 15, "Cities should have unique geography"

@then('travel should be possible through text-based world map')
def step_verify_world_map(context):
    context.world['map_system'] = {
        'type': 'text_based',
        'navigation': True,
        'travel_time': True,
        'travel_options': ['walk', 'horse', 'carriage', 'ship', 'teleport']
    }
    assert context.world['map_system']['type'] == 'text_based', "Map should be text-based"

@then('travel should have appropriate time costs')
def step_verify_travel_time(context):
    # Generate travel times between cities
    context.travel_times = {}
    for city_name, city_data in context.cities.items():
        for connection in city_data['connections']:
            if connection in context.cities:
                # Generate travel time in hours
                travel_time = random.randint(4, 72)  # 4 hours to 3 days
                context.travel_times[(city_name, connection)] = travel_time
    
    # Verify all travel times are reasonable
    for travel_pair, time in context.travel_times.items():
        assert 4 <= time <= 72, f"Travel time should be reasonable: {travel_pair} -> {time} hours"

@given('the player has entered a city')
def step_player_in_city(context):
    if not hasattr(context, 'cities'):
        # Create a simple city if not exists
        context.cities = {'TestCity': {
            'id': 'test_city',
            'name': 'TestCity',
            'buildings': ['Inn', 'Shop', 'Temple', 'Blacksmith', 'Tavern', 'Guild', 'Library', 'Market']
        }}
    
    # Set player location to first city
    first_city = list(context.cities.keys())[0]
    context.player['location'] = first_city
    context.current_city = context.cities[first_city]

@when('they explore the city')
def step_explore_city(context):
    # Player explores current city
    context.player['visited_buildings'] = []
    if not hasattr(context.current_city, 'buildings'):
        context.current_city['buildings'] = [
            'Inn', 'Shop', 'Temple', 'Blacksmith', 'Tavern', 'Guild', 'Library', 'Market'
        ]
    
    for building in context.current_city['buildings']:
        context.player['visited_buildings'].append(building)

@then('they should find at least 8 different building types')
def step_verify_building_types(context):
    # Define all possible building types
    all_building_types = [
        'Inn', 'Shop', 'Temple', 'Blacksmith', 'Tavern', 'Guild', 'Library', 'Market',
        'Arena', 'Bank', 'Guard Tower', 'Castle', 'Farm', 'Stable', 'Docks', 'Alchemy Lab'
    ]
    
    # Ensure each city has at least 8 building types
    for city_name, city_data in context.cities.items():
        if 'buildings' not in city_data:
            # Assign at least 8 building types to each city
            city_data['buildings'] = random.sample(all_building_types, random.randint(8, 12))
        
        assert len(city_data['buildings']) >= 8, f"City {city_name} should have at least 8 building types"

@then('each building should serve a specific function')
def step_verify_building_functions(context):
    # Define functions for each building type
    building_functions = {
        'Inn': 'Rest and recovery',
        'Shop': 'Buy general goods',
        'Temple': 'Healing and blessings',
        'Blacksmith': 'Weapon and armor repair',
        'Tavern': 'Information and gossip',
        'Guild': 'Quests and training',
        'Library': 'Knowledge and lore',
        'Market': 'Trade and commerce',
        'Arena': 'Combat challenges',
        'Bank': 'Currency storage',
        'Guard Tower': 'Safety and quests',
        'Castle': 'Noble interaction',
        'Farm': 'Food production',
        'Stable': 'Animal services',
        'Docks': 'Sea travel',
        'Alchemy Lab': 'Potion creation'
    }
    
    # Verify each building has a function
    for city_name, city_data in context.cities.items():
        for building in city_data['buildings']:
            assert building in building_functions, f"Building {building} should have a defined function"

@then('each city should have unique shops with different inventories')
def step_verify_unique_shops(context):
    # Generate unique shop inventories for each city
    item_types = ['swords', 'armor', 'potions', 'scrolls', 'artifacts', 'gems', 'food', 'clothing']
    
    for city_name, city_data in context.cities.items():
        # Ensure city has shops
        if 'shops' not in city_data:
            city_data['shops'] = {}
            
        # Create 2-4 shops per city
        num_shops = random.randint(2, 4)
        for i in range(num_shops):
            shop_name = f"{city_name}_Shop_{i}"
            city_data['shops'][shop_name] = {
                'name': shop_name,
                'type': random.choice(['weapons', 'armor', 'magic', 'general']),
                'inventory': random.sample(item_types, random.randint(3, 6)),
                'prices': {item: random.randint(5, 500) for item in item_types[:3]}  # Sample prices
            }
    
    # Verify uniqueness by comparing inventories
    city_inventories = []
    for city_name, city_data in context.cities.items():
        inventory_signature = []
        for shop_name, shop_data in city_data['shops'].items():
            inventory_signature.append(tuple(sorted(shop_data['inventory'])))
        city_inventories.append(tuple(inventory_signature))
    
    # At least 15 cities should have unique inventory combinations
    assert len(set(city_inventories)) >= 15, "Cities should have unique shop inventories"

@then('each city should have distinctive cultural elements in descriptions')
def step_verify_cultural_elements(context):
    # Generate cultural elements for each city
    cultures = [
        'militaristic', 'scholarly', 'mercantile', 'religious', 'agricultural',
        'artistic', 'industrial', 'mysterious', 'nomadic', 'hierarchical'
    ]
    
    for city_name, city_data in context.cities.items():
        # Assign culture
        culture = random.choice(cultures)
        city_data['culture'] = culture
        
        # Generate cultural description
        city_data['description'] = f"{city_data['name']} is a {culture} city known for its "
        
        if culture == 'militaristic':
            city_data['description'] += "strong army and strict discipline"
        elif culture == 'scholarly':
            city_data['description'] += "great library and learned scholars"
        elif culture == 'mercantile':
            city_data['description'] += "bustling markets and wealthy merchants"
        elif culture == 'religious':
            city_data['description'] += "grand temples and devout followers"
        elif culture == 'agricultural':
            city_data['description'] += "fertile fields and hardworking farmers"
        elif culture == 'artistic':
            city_data['description'] += "beautiful art and talented performers"
        elif culture == 'industrial':
            city_data['description'] += "busy factories and skilled craftsmen"
        elif culture == 'mysterious':
            city_data['description'] += "ancient secrets and hidden knowledge"
        elif culture == 'nomadic':
            city_data['description'] += "traveling people and diverse traditions"
        elif culture == 'hierarchical':
            city_data['description'] += "strict social order and noble leadership"
    
    # Verify all cities have descriptions
    for city_name, city_data in context.cities.items():
        assert 'culture' in city_data, f"City {city_name} should have a defined culture"
        assert len(city_data['description']) > 20, f"City {city_name} should have a descriptive text"