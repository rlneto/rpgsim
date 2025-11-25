"""
RPGSim City Management BDD Step Definitions
LLM Agent-Optimized city management scenarios
"""

from behave import given, when, then
from typing import Dict, Any, List
import random
import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import base context manager
try:
    from bdd_base_steps import get_bdd_context
except ImportError:
    def get_bdd_context(context):
        return context

# -- CITY STRUCTURE STEPS --

@given('player enters any city')
def step_player_enters_city(context):
    """Set up city context for player entering"""
    bdd_ctx = get_bdd_context(context)

    # Initialize player if doesn't exist
    if not hasattr(bdd_ctx, 'player'):
        bdd_ctx.player = {
            'location': 'city_center',
            'visited_cities': []
        }

    # Create city data
    bdd_ctx.current_city = {
        'id': 'city_1',
        'name': 'Silverhaven',
        'size': 'medium',
        'population': random.randint(5000, 20000),
        'architectural_style': random.choice(['medieval', 'gothic', 'renaissance', 'oriental']),
        'buildings': [],
        'economy_type': random.choice(['trade', 'agricultural', 'industrial', 'magical']),
        'wealth_level': random.randint(1, 10)
    }

@when('they explore city layout')
def step_explore_city_layout(context):
    """Simulate city exploration and discover buildings"""
    bdd_ctx = get_bdd_context(context)

    building_types = [
        'tavern', 'weapon_shop', 'armor_shop', 'magic_shop', 'general_store',
        'temple', 'guild_hall', 'market', 'inn', 'bank', 'library',
        'blacksmith', 'alchemist', 'tailor', 'jeweler', 'barracks'
    ]

    # Create buildings with specific functions
    buildings = []
    for building_type in building_types[:8]:  # At least 8 building types
        building = {
            'id': f"building_{building_type}",
            'type': building_type,
            'name': building_type.replace('_', ' ').title(),
            'function': get_building_function(building_type),
            'position': random_position(),
            'visitable': True,
            'services': get_building_services(building_type)
        }
        buildings.append(building)

    bdd_ctx.current_city['buildings'] = buildings

def get_building_function(building_type):
    """Get specific function for building type"""
    functions = {
        'tavern': 'Social gathering place with food and drinks',
        'weapon_shop': 'Sells weapons and combat equipment',
        'armor_shop': 'Sells armor and protective gear',
        'magic_shop': 'Sells magical items and spell components',
        'general_store': 'Sells basic supplies and everyday items',
        'temple': 'Religious services and healing',
        'guild_hall': 'Professional organization and training',
        'market': 'Trading hub for various goods',
        'inn': 'Lodging and rest for travelers',
        'bank': 'Financial services and currency exchange',
        'library': 'Knowledge repository and research',
        'blacksmith': 'Metalworking and equipment repair',
        'alchemist': 'Potions and chemical compounds',
        'tailor': 'Clothing and textile goods',
        'jeweler': 'Precious items and accessories',
        'barracks': 'Military training and recruitment'
    }
    return functions.get(building_type, 'General purpose building')

def get_building_services(building_type):
    """Get available services for building type"""
    services_map = {
        'tavern': ['food', 'drinks', 'lodging', 'rumors'],
        'weapon_shop': ['weapon_sales', 'weapon_repair', 'weapon_upgrades'],
        'armor_shop': ['armor_sales', 'armor_repair', 'custom_fitting'],
        'magic_shop': ['magic_items', 'spell_components', 'enchanting'],
        'general_store': ['supplies', 'tools', 'food_items'],
        'temple': ['healing', 'blessings', 'confession', 'religious_guidance'],
        'guild_hall': ['training', 'quests', 'professional_services'],
        'market': ['trading', 'bargaining', 'specialty_goods'],
        'inn': ['rooms', 'food', 'stables', 'local_information'],
        'bank': ['deposits', 'loans', 'currency_exchange', 'safe_storage'],
        'library': ['research', 'knowledge_sharing', 'scrolls', 'maps'],
        'blacksmith': ['metal_work', 'repairs', 'custom_items'],
        'alchemist': ['potions', 'ingredients', 'transmutations'],
        'tailor': ['clothing', 'repairs', 'custom_outfits'],
        'jeweler': ['jewelry', 'gems', 'enchanted_items'],
        'barracks': ['training', 'recruitment', 'military_services']
    }
    return services_map.get(building_type, ['basic_service'])

def random_position():
    """Generate random position for city layout"""
    return {
        'x': random.randint(1, 10),
        'y': random.randint(1, 10),
        'district': random.choice(['market_district', 'residential', 'commercial', 'industrial', 'temple_district'])
    }

@then('they should find at least 8 building types')
def step_verify_building_types(context):
    """Verify minimum building variety"""
    bdd_ctx = get_bdd_context(context)

    buildings = bdd_ctx.current_city.get('buildings', [])
    building_types = [b['type'] for b in buildings]

    assert len(set(building_types)) >= 8, f"Should have at least 8 building types, got {len(set(building_types))}"
    assert len(buildings) >= 8, f"Should have at least 8 buildings, got {len(buildings)}"

@then('each building should have specific functions')
def step_verify_building_functions(context):
    """Verify buildings have defined functions"""
    bdd_ctx = get_bdd_context(context)

    buildings = bdd_ctx.current_city.get('buildings', [])

    for building in buildings:
        assert 'function' in building, f"Building {building['id']} should have a function"
        assert building['function'], f"Building {building['id']} should have a non-empty function"
        assert len(building['function']) > 10, f"Building {building['id']} function should be descriptive"

@then('city should have unique architectural style')
def step_verify_architectural_style(context):
    """Verify city has defined architectural style"""
    bdd_ctx = get_bdd_context(context)

    city = bdd_ctx.current_city
    assert 'architectural_style' in city, "City should have architectural style"
    assert city['architectural_style'] in ['medieval', 'gothic', 'renaissance', 'oriental'], \
        f"Invalid architectural style: {city['architectural_style']}"

@then('buildings should be logically arranged')
def step_verify_logical_arrangement(context):
    """Verify buildings are arranged logically"""
    bdd_ctx = get_bdd_context(context)

    buildings = bdd_ctx.current_city.get('buildings', [])

    # Check that buildings have positions
    for building in buildings:
        assert 'position' in building, f"Building {building['id']} should have a position"
        assert 'district' in building['position'], f"Building {building['id']} should be in a district"

    # Check that related buildings are in logical districts
    districts = [b['position']['district'] for b in buildings]
    assert len(set(districts)) >= 3, "City should have multiple districts"

# -- CITY ECONOMY STEPS --

@given('player visits different cities')
def step_player_visits_cities(context):
    """Set up multiple cities for comparison"""
    bdd_ctx = get_bdd_context(context)

    # Create multiple cities with different characteristics
    cities = []
    economy_types = ['trade', 'agricultural', 'industrial', 'magical']

    for i, economy_type in enumerate(economy_types):
        city = {
            'id': f'city_{i}',
            'name': f'City{chr(65+i)}',
            'economy_type': economy_type,
            'population': random.randint(3000, 50000),
            'wealth_level': random.randint(1, 10),
            'cultural_traits': get_cultural_traits(economy_type),
            'shop_availability': calculate_shop_availability(economy_type),
            'price_multiplier': calculate_price_multiplier(economy_type)
        }
        cities.append(city)

    bdd_ctx.cities = cities
    bdd_ctx.player['visited_cities'] = [city['id'] for city in cities]

def get_cultural_traits(economy_type):
    """Get cultural traits based on economy type"""
    cultural_map = {
        'trade': ['merchant_caravans', 'diverse_marketplace', 'foreign_goods', 'diplomatic_relations'],
        'agricultural': ['farming_communities', 'seasonal_festivals', 'food_production', 'rural_traditions'],
        'industrial': ['craftsmanship_guilds', 'innovation_centers', 'manufacturing_power', 'technical_expertise'],
        'magical': ['arcane_academy', 'mystical_research', 'spell_casting', 'magical_innovation']
    }
    return cultural_map.get(economy_type, ['general_culture'])

def calculate_shop_availability(economy_type):
    """Calculate shop availability based on economy"""
    base_availability = 100  # Base 100%
    availability_modifiers = {
        'trade': 1.3,      # More shops due to trade hub
        'agricultural': 0.8,  # Fewer shops, more farms
        'industrial': 1.2,    # More specialized shops
        'magical': 0.9       # Specialized magic shops
    }
    return int(base_availability * availability_modifiers.get(economy_type, 1.0))

def calculate_price_multiplier(economy_type):
    """Calculate price multiplier based on economy"""
    price_modifiers = {
        'trade': 0.9,        # Lower prices due to competition
        'agricultural': 1.1,  # Higher prices for scarcity
        'industrial': 1.0,    # Standard prices
        'magical': 1.3        # Higher prices for rarity
    }
    return price_modifiers.get(economy_type, 1.0)

@when('they observe city characteristics')
def step_observe_city_characteristics(context):
    """Simulate observation of city features"""
    bdd_ctx = get_bdd_context(context)

    # Store observations for verification
    bdd_ctx.city_observations = {
        'distinct_economies': set(),
        'population_effects': {},
        'wealth_effects': {},
        'cultural_differences': set()
    }

    for city in bdd_ctx.cities:
        bdd_ctx.city_observations['distinct_economies'].add(city['economy_type'])
        bdd_ctx.city_observations['population_effects'][city['id']] = city['shop_availability']
        bdd_ctx.city_observations['wealth_effects'][city['id']] = city['price_multiplier']
        bdd_ctx.city_observations['cultural_differences'].update(city['cultural_traits'])

@then('each city should have distinct economy type')
def step_verify_distinct_economies(context):
    """Verify cities have different economy types"""
    bdd_ctx = get_bdd_context(context)

    economies = bdd_ctx.city_observations['distinct_economies']
    assert len(economies) >= 3, f"Should have at least 3 distinct economy types, got {len(economies)}"

@then('population should affect shop availability')
def step_verify_population_shop_correlation(context):
    """Verify population correlates with shop availability"""
    bdd_ctx = get_bdd_context(context)

    effects = bdd_ctx.city_observations['population_effects']

    for city_id, availability in effects.items():
        assert availability > 50, f"City {city_id} should have reasonable shop availability"
        assert availability <= 150, f"City {city_id} shop availability should be realistic"

@then('city wealth should influence item prices')
def step_verify_wealth_price_correlation(context):
    """Verify wealth level affects pricing"""
    bdd_ctx = get_bdd_context(context)

    effects = bdd_ctx.city_observations['wealth_effects']

    for city_id, price_mult in effects.items():
        assert 0.7 <= price_mult <= 1.5, f"City {city_id} price multiplier should be reasonable: {price_mult}"

@then('cities should have cultural uniqueness')
def step_verify_cultural_uniqueness(context):
    """Verify cities have unique cultural traits"""
    bdd_ctx = get_bdd_context(context)

    cultural_traits = bdd_ctx.city_observations['cultural_differences']
    assert len(cultural_traits) >= 10, f"Cities should have at least 10 cultural traits, got {len(cultural_traits)}"

# -- CITY SERVICES STEPS --

@given('player interacts with city services')
def step_player_interacts_services(context):
    """Set up city services interaction"""
    bdd_ctx = get_bdd_context(context)

    # Create city services
    bdd_ctx.city_services = {
        'guards': {
            'strength': random.randint(5, 20),
            'response_time': random.randint(1, 5),
            'patrol_coverage': random.randint(50, 100),
            'crime_rate': random.randint(1, 10)
        },
        'healthcare': {
            'hospitals': random.randint(1, 5),
            'healers': random.randint(2, 10),
            'potion_shops': random.randint(3, 8),
            'service_quality': random.randint(60, 100)
        },
        'education': {
            'schools': random.randint(2, 6),
            'libraries': random.randint(1, 4),
            'academies': random.randint(0, 2),
            'literacy_rate': random.randint(70, 100)
        },
        'infrastructure': {
            'roads_quality': random.randint(3, 10),
            'water_system': random.randint(5, 10),
            'lighting': random.randint(3, 10),
            'sanitation': random.randint(4, 10)
        }
    }

@when('they utilize public facilities')
def step_utilize_facilities(context):
    """Simulate usage of city facilities"""
    bdd_ctx = get_bdd_context(context)

    # Track facility usage
    bdd_ctx.facility_usage = {
        'guards_called': random.randint(0, 3),
        'healing_received': random.randint(0, 2),
        'books_read': random.randint(1, 10),
        'infrastructure_used': random.randint(2, 8)
    }

@then('guard services should respond appropriately')
def step_verify_guard_services(context):
    """Verify guard system effectiveness"""
    bdd_ctx = get_bdd_context(context)

    guards = bdd_ctx.city_services['guards']

    # Verify guard strength and response
    assert guards['strength'] >= 5, "Guards should have minimum strength"
    assert guards['response_time'] <= 5, "Guards should respond within reasonable time"
    assert guards['patrol_coverage'] >= 50, "Guards should provide adequate patrol coverage"

    # Verify crime correlation
    if guards['strength'] > 15:
        assert guards['crime_rate'] <= 5, "Strong guards should reduce crime rate"

@then('healthcare services should be available')
def step_verify_healthcare_services(context):
    """Verify healthcare availability"""
    bdd_ctx = get_bdd_context(context)

    healthcare = bdd_ctx.city_services['healthcare']

    # Verify healthcare facilities
    total_healers = healthcare['healers'] + healthcare['potion_shops']
    assert total_healers >= 5, "City should have adequate healthcare providers"
    assert healthcare['service_quality'] >= 60, "Healthcare service quality should be acceptable"

@then('educational institutions should provide learning')
def step_verify_educational_services(context):
    """Verify educational services"""
    bdd_ctx = get_bdd_context(context)

    education = bdd_ctx.city_services['education']

    # Verify educational facilities
    total_educational = education['schools'] + education['libraries'] + education['academies']
    assert total_educational >= 3, "City should have multiple educational facilities"
    assert education['literacy_rate'] >= 70, "City should have reasonable literacy rate"

@then('infrastructure should support daily life')
def step_verify_infrastructure_services(context):
    """Verify infrastructure quality"""
    bdd_ctx = get_bdd_context(context)

    infrastructure = bdd_ctx.city_services['infrastructure']

    # Verify infrastructure quality
    assert infrastructure['roads_quality'] >= 3, "Roads should be usable"
    assert infrastructure['water_system'] >= 5, "Water system should be functional"
    assert infrastructure['sanitation'] >= 4, "Sanitation should be adequate"

# -- CITY DYNAMICS STEPS --

@given('city evolves over time')
def step_city_evolves(context):
    """Set up city evolution simulation"""
    bdd_ctx = get_bdd_context(context)

    # Create city evolution data
    bdd_ctx.city_evolution = {
        'starting_population': 5000,
        'growth_rate': random.uniform(0.01, 0.05),
        'development_level': random.randint(1, 5),
        'prosperity': random.randint(20, 80),
        'event_history': []
    }

@when('time passes and events occur')
def step_time_passes_events(context):
    """Simulate passage of time and events"""
    bdd_ctx = get_bdd_context(context)

    # Simulate events
    events = ['festival', 'merchant_arrival', 'monster_attack', 'discovery', 'building_completion']

    for _ in range(random.randint(3, 7)):
        event = random.choice(events)
        bdd_ctx.city_evolution['event_history'].append({
            'event': event,
            'impact': random.uniform(-10, 20),
            'date': f"Day {random.randint(1, 365)}"
        })

@then('city should grow and develop')
def step_verify_city_growth(context):
    """Verify city growth patterns"""
    bdd_ctx = get_bdd_context(context)

    evolution = bdd_ctx.city_evolution

    # Calculate growth
    growth = evolution['starting_population'] * evolution['growth_rate']
    assert growth > 0, "City should show positive growth"
    assert evolution['development_level'] >= 1, "City should have development level"

    # Verify event impact
    total_impact = sum(e['impact'] for e in evolution['event_history'])
    assert len(evolution['event_history']) >= 3, "City should have experienced multiple events"

@then('prosperity should reflect city management')
def step_verify_prosperity_management(context):
    """Verify prosperity management effectiveness"""
    bdd_ctx = get_bdd_context(context)

    evolution = bdd_ctx.city_evolution

    assert 20 <= evolution['prosperity'] <= 80, "Prosperity should be within reasonable range"
    assert evolution['development_level'] > 0, "Development level should be positive"

# -- CITY INTERACTION STEPS --

@given('player has reputation in cities')
def step_player_has_reputation(context):
    """Set up player reputation system"""
    bdd_ctx = get_bdd_context(context)

    if not hasattr(bdd_ctx, 'player'):
        bdd_ctx.player = {}

    # Create reputation data per city
    bdd_ctx.player['reputation'] = {}
    city_names = ['silverhaven', 'goldshire', 'crystalpeak', 'shadowmere', 'windridge']

    for city in city_names:
        reputation = random.randint(-50, 100)  # Can be negative or positive
        bdd_ctx.player['reputation'][city] = reputation

@when('they interact with city residents')
def step_interact_residents(context):
    """Simulate interactions with city residents"""
    bdd_ctx = get_bdd_context(context)

    # Create resident interaction results
    bdd_ctx.resident_interactions = []

    for city, reputation in bdd_ctx.player['reputation'].items():
        interaction = {
            'city': city,
            'resident_attitude': calculate_attitude(reputation),
            'service_pricing': calculate_pricing_modifier(reputation),
            'quest_availability': calculate_quest_availability(reputation)
        }
        bdd_ctx.resident_interactions.append(interaction)

def calculate_attitude(reputation):
    """Calculate resident attitude based on reputation"""
    if reputation > 50:
        return 'friendly'
    elif reputation > 0:
        return 'neutral'
    elif reputation > -30:
        return 'suspicious'
    else:
        return 'hostile'

def calculate_pricing_modifier(reputation):
    """Calculate pricing modifier based on reputation"""
    # Better reputation = better prices
    base_modifier = 1.0
    if reputation > 50:
        return base_modifier - (reputation / 200)  # Discount
    elif reputation < -30:
        return base_modifier + abs(reputation / 100)  # Surcharge
    else:
        return base_modifier

def calculate_quest_availability(reputation):
    """Calculate quest availability based on reputation"""
    if reputation > 30:
        return 'abundant'
    elif reputation > -20:
        return 'moderate'
    else:
        return 'scarce'

@then('reputation should affect treatment')
def step_verify_reputation_treatment(context):
    """Verify reputation affects city treatment"""
    bdd_ctx = get_bdd_context(context)

    for interaction in bdd_ctx.resident_interactions:
        reputation = bdd_ctx.player['reputation'][interaction['city']]

        # Verify attitude matches reputation
        if reputation > 50:
            assert interaction['resident_attitude'] == 'friendly', f"Good reputation should result in friendly attitude"
        elif reputation < -30:
            assert interaction['resident_attitude'] in ['suspicious', 'hostile'], f"Bad reputation should result in negative attitude"

@then('prices should vary by reputation')
def step_verify_reputation_pricing(context):
    """Verify pricing varies with reputation"""
    bdd_ctx = get_bdd_context(context)

    for interaction in bdd_ctx.resident_interactions:
        reputation = bdd_ctx.player['reputation'][interaction['city']]
        pricing = interaction['service_pricing']

        # Verify pricing logic
        if reputation > 50:
            assert pricing < 1.0, f"Good reputation should provide discount"
        elif reputation < -30:
            assert pricing > 1.0, f"Bad reputation should result in surcharge"

@then('quest opportunities should change with reputation')
def step_verify_reputation_quests(context):
    """Verify quest availability changes with reputation"""
    bdd_ctx = get_bdd_context(context)

    for interaction in bdd_ctx.resident_interactions:
        reputation = bdd_ctx.player['reputation'][interaction['city']]
        quest_availability = interaction['quest_availability']

        # Verify quest availability
        assert quest_availability in ['abundant', 'moderate', 'scarce'], f"Quest availability should be valid"

# -- CITY SERVICES AND FACILITIES STEPS --

@given('player needs city services')
def step_player_needs_services(context):
    """Set up player seeking city services"""
    bdd_ctx = get_bdd_context(context)

    # Initialize player if needed
    if not hasattr(bdd_ctx, 'player'):
        bdd_ctx.player = {}

    # Ensure player has required attributes
    if 'health' not in bdd_ctx.player:
        bdd_ctx.player['health'] = 50
    if 'level' not in bdd_ctx.player:
        bdd_ctx.player['level'] = 5
    if 'experience' not in bdd_ctx.player:
        bdd_ctx.player['experience'] = 0

    # Create available city services
    bdd_ctx.city_services_available = {
        'inns': [
            {'name': 'The Prancing Pony', 'quality': 'good', 'price': 10},
            {'name': 'Sleeping Dragon Inn', 'quality': 'basic', 'price': 5},
            {'name': 'Royal Suites', 'quality': 'luxury', 'price': 25}
        ],
        'training_grounds': [
            {'type': 'combat', 'skills': ['sword', 'archery', 'magic'], 'trainer': 'Master Giles'},
            {'type': 'magic', 'skills': ['elemental', 'healing', 'necromancy'], 'trainer': 'Archmage Elara'},
            {'type': 'stealth', 'skills': ['lockpicking', 'sneaking', 'disguise'], 'trainer': 'Shadow Hand'}
        ],
        'quest_boards': [
            {'location': 'Town Square', 'quests_available': random.randint(5, 15)},
            {'location': 'Guild Hall', 'quests_available': random.randint(3, 8)},
            {'location': 'Inn Notice Board', 'quests_available': random.randint(2, 6)}
        ],
        'crafting_stations': [
            {'type': 'blacksmith', 'materials': ['iron', 'steel', 'mythril'], 'items': ['weapons', 'armor']},
            {'type': 'alchemy', 'materials': ['herbs', 'minerals', 'essences'], 'items': ['potions', 'elixirs']},
            {'type': 'enchanting', 'materials': ['gems', 'rune_stones', 'soul_crystals'], 'items': ['enchanted_items']}
        ]
    }

@when('they seek assistance')
def step_seek_city_assistance(context):
    """Simulate player seeking city services"""
    bdd_ctx = get_bdd_context(context)

    # Record which services the player seeks
    bdd_ctx.services_sought = []

    if bdd_ctx.player['health'] < 80:
        bdd_ctx.services_sought.append('inns')

    if bdd_ctx.player['level'] < 10:
        bdd_ctx.services_sought.append('training_grounds')

    if bdd_ctx.player['experience'] < 1000:
        bdd_ctx.services_sought.append('quest_boards')

    # Always seek crafting occasionally
    if random.random() > 0.5:
        bdd_ctx.services_sought.append('crafting_stations')

@then('they should find inns for rest')
def step_verify_inns_available(context):
    """Verify inns are available for rest"""
    bdd_ctx = get_bdd_context(context)

    inns = bdd_ctx.city_services_available['inns']

    assert len(inns) >= 2, "City should have at least 2 inns"

    for inn in inns:
        assert 'name' in inn, f"Inn should have a name"
        assert 'quality' in inn, f"Inn should have quality rating"
        assert 'price' in inn, f"Inn should have pricing"
        assert inn['price'] > 0, f"Inn price should be positive"

@then('they should find training grounds')
def step_verify_training_grounds(context):
    """Verify training grounds are available"""
    bdd_ctx = get_bdd_context(context)

    training_grounds = bdd_ctx.city_services_available['training_grounds']

    assert len(training_grounds) >= 2, "City should have multiple training grounds"

    for training in training_grounds:
        assert 'type' in training, f"Training ground should have type"
        assert 'skills' in training, f"Training ground should offer skills"
        assert len(training['skills']) >= 2, f"Training ground should offer multiple skills"
        assert 'trainer' in training, f"Training ground should have trainer"

@then('they should find quest boards')
def step_verify_quest_boards(context):
    """Verify quest boards are available"""
    bdd_ctx = get_bdd_context(context)

    quest_boards = bdd_ctx.city_services_available['quest_boards']

    assert len(quest_boards) >= 2, "City should have multiple quest boards"

    total_quests = sum(board['quests_available'] for board in quest_boards)
    assert total_quests >= 10, f"City should have at least 10 available quests, got {total_quests}"

@then('they should find crafting stations')
def step_verify_crafting_stations(context):
    """Verify crafting stations are available"""
    bdd_ctx = get_bdd_context(context)

    crafting_stations = bdd_ctx.city_services_available['crafting_stations']

    assert len(crafting_stations) >= 2, "City should have multiple crafting stations"

    for station in crafting_stations:
        assert 'type' in station, f"Crafting station should have type"
        assert 'materials' in station, f"Crafting station should list materials"
        assert 'items' in station, f"Crafting station should list craftable items"

# -- CITY DISCOVERY STEPS --

@given('player discovers new city')
def step_player_discovers_city(context):
    """Set up new city discovery scenario"""
    bdd_ctx = get_bdd_context(context)

    # Create new undiscovered city
    bdd_ctx.new_city = {
        'name': f"City{random.choice(['ville', 'shire', 'port', 'ton', 'burg'])}",
        'population': random.randint(1000, 50000),
        'economic_focus': random.choice(['trade', 'agriculture', 'mining', 'fishing', 'magic']),
        'services': {
            'market': random.choice(['grand', 'local', 'specialty']),
            'guards': random.randint(5, 50),
            'inns': random.randint(1, 10),
            'shops': random.randint(5, 30)
        },
        'discovered': False
    }

    # Set up player discovery
    if not hasattr(bdd_ctx, 'player'):
        bdd_ctx.player = {}

    if 'visited_cities' not in bdd_ctx.player:
        bdd_ctx.player['visited_cities'] = []

@when('they enter city for first time')
def step_first_city_entry(context):
    """Simulate player entering city for first time"""
    bdd_ctx = get_bdd_context(context)

    # Mark city as discovered
    bdd_ctx.new_city['discovered'] = True
    bdd_ctx.player['visited_cities'].append(bdd_ctx.new_city['name'])

    # Create city information for player
    bdd_ctx.city_information = {
        'description': generate_city_description(bdd_ctx.new_city),
        'services_summary': generate_services_summary(bdd_ctx.new_city),
        'economic_analysis': generate_economic_analysis(bdd_ctx.new_city)
    }

def generate_city_description(city):
    """Generate descriptive text for city"""
    descriptions = {
        'trade': "A bustling merchant hub with caravans and diverse marketplaces",
        'agriculture': "A peaceful farming community surrounded by fertile fields",
        'mining': "A rugged mountain settlement built around rich mineral deposits",
        'fishing': "A coastal town with thriving fishing industry and harbor",
        'magic': "An arcane center filled with mystical energy and magical academies"
    }
    return descriptions.get(city['economic_focus'], "A growing settlement with diverse opportunities")

def generate_services_summary(city):
    """Generate summary of available services"""
    services = city['services']
    summary = []

    summary.append(f"Market: {services['market'].title()} marketplace")
    summary.append(f"Security: {services['guards']} guards maintaining order")
    summary.append(f"Lodging: {services['inns']} inns available")
    summary.append(f"Commerce: {services['shops']} various shops")

    return summary

def generate_economic_analysis(city):
    """Generate economic focus analysis"""
    focus = city['economic_focus']

    analyses = {
        'trade': "Thriving trade economy with high merchant activity",
        'agriculture': "Stable agricultural economy with food production",
        'mining': "Resource-based economy with mineral extraction",
        'fishing': "Maritime economy with fishing and trade",
        'magic': "Magical economy with arcane services and goods"
    }

    return analyses.get(focus, "Developing economy with multiple sectors")

@then('they should receive city description')
def step_verify_city_description(context):
    """Verify player receives city description"""
    bdd_ctx = get_bdd_context(context)

    city_info = bdd_ctx.city_information

    assert 'description' in city_info, "City information should include description"
    assert len(city_info['description']) > 20, "Description should be descriptive"
    assert bdd_ctx.new_city['name'] in city_info['description'] or \
           bdd_ctx.new_city['economic_focus'] in city_info['description'], \
           "Description should mention city characteristics"

@then('they should learn about available services')
def step_verify_services_information(context):
    """Verify player learns about city services"""
    bdd_ctx = get_bdd_context(context)

    city_info = bdd_ctx.city_information

    assert 'services_summary' in city_info, "City information should include services summary"
    assert len(city_info['services_summary']) >= 3, "Services summary should be comprehensive"

    # Check specific services are mentioned
    summary_text = ' '.join(city_info['services_summary'])
    assert any(service in summary_text.lower() for service in ['market', 'guards', 'inns', 'shops']), \
           "Services summary should mention key services"

@then('they should see population size')
def step_verify_population_display(context):
    """Verify player sees population information"""
    bdd_ctx = get_bdd_context(context)

    population = bdd_ctx.new_city['population']

    assert population > 0, "Population should be positive"
    assert population >= 1000, "City should have reasonable minimum population"

@then('they should understand economic focus')
def step_verify_economic_understanding(context):
    """Verify player understands city's economic focus"""
    bdd_ctx = get_bdd_context(context)

    economic_focus = bdd_ctx.new_city['economic_focus']
    city_info = bdd_ctx.city_information

    assert economic_focus in ['trade', 'agriculture', 'mining', 'fishing', 'magic'], \
           "City should have valid economic focus"

    assert 'economic_analysis' in city_info, "Economic analysis should be provided"
    assert len(city_info['economic_analysis']) > 10, "Economic analysis should be informative"

# -- CITY REPUTATION SYSTEM STEPS --

@given('player interacts with city over time')
def step_player_city_interactions(context):
    """Set up long-term city interaction history"""
    bdd_ctx = get_bdd_context(context)

    # Initialize player if needed
    if not hasattr(bdd_ctx, 'player'):
        bdd_ctx.player = {}

    # Ensure player has required attributes
    if 'completed_quests' not in bdd_ctx.player:
        bdd_ctx.player['completed_quests'] = 0
    if 'trade_volume' not in bdd_ctx.player:
        bdd_ctx.player['trade_volume'] = 0

    # Create interaction history
    bdd_ctx.interaction_history = {
        'quests_completed': random.randint(0, 20),
        'trades_made': random.randint(0, 50),
        'reputation_changes': [],
        'time_in_city': random.randint(1, 100),  # days
        'major_events': []
    }

    # Generate major events
    for _ in range(random.randint(1, 3)):
        event = random.choice(['saved_city', 'defeated_threat', 'helped_npcs', 'discovered_treasure'])
        impact = random.randint(10, 30)
        bdd_ctx.interaction_history['major_events'].append({'event': event, 'reputation_impact': impact})

@when('they complete quests or trade')
def step_complete_quests_or_trade(context):
    """Simulate quest completion and trading activities"""
    bdd_ctx = get_bdd_context(context)

    # Simulate specific activities that affect reputation
    recent_activities = []

    # Quest completions
    for _ in range(random.randint(1, 5)):
        quest_complete = {
            'type': 'quest_completed',
            'difficulty': random.choice(['easy', 'medium', 'hard']),
            'reputation_change': random.randint(1, 10),
            'reward': random.randint(50, 500)
        }
        recent_activities.append(quest_complete)
        bdd_ctx.interaction_history['reputation_changes'].append(quest_complete)

    # Trading activities
    for _ in range(random.randint(1, 8)):
        trade = {
            'type': 'trade',
            'volume': random.randint(10, 1000),
            'reputation_change': random.randint(-2, 5),
            'profit': random.randint(-100, 300)
        }
        recent_activities.append(trade)
        bdd_ctx.interaction_history['reputation_changes'].append(trade)

    bdd_ctx.recent_activities = recent_activities

@then('their reputation should change')
def step_verify_reputation_change(context):
    """Verify reputation changes appropriately"""
    bdd_ctx = get_bdd_context(context)

    changes = bdd_ctx.interaction_history['reputation_changes']

    assert len(changes) > 0, "There should be reputation changes recorded"

    # Calculate total reputation change
    total_change = sum(change['reputation_change'] for change in changes)
    assert total_change != 0, "Total reputation should have changed"

    # Verify some positive changes (quests should be positive)
    quest_changes = [c for c in changes if c['type'] == 'quest_completed']
    assert all(c['reputation_change'] > 0 for c in quest_changes), "Quest completions should increase reputation"

@then('reputation should affect prices')
def step_verify_reputation_pricing(context):
    """Verify reputation affects pricing"""
    bdd_ctx = get_bdd_context(context)

    # Calculate current reputation level
    total_reputation = sum(change['reputation_change'] for change in bdd_ctx.interaction_history['reputation_changes'])

    # Determine pricing modifier based on reputation
    if total_reputation > 50:
        pricing_modifier = 0.9  # 10% discount
    elif total_reputation < -20:
        pricing_modifier = 1.2  # 20% surcharge
    else:
        pricing_modifier = 1.0  # Standard pricing

    assert 0.8 <= pricing_modifier <= 1.3, "Pricing modifier should be reasonable"

@then('reputation should unlock new services')
def step_verify_service_unlocks(context):
    """Verify high reputation unlocks services"""
    bdd_ctx = get_bdd_context(context)

    # Calculate total reputation
    total_reputation = sum(change['reputation_change'] for change in bdd_ctx.interaction_history['reputation_changes'])

    # Define services unlocked by reputation level
    basic_services = ['general_store', 'tavern']
    advanced_services = ['specialty_shop', 'guild_membership', 'elite_training']
    premium_services = ['noble_favor', 'city_council', 'royal_commissions']

    unlocked_services = basic_services.copy()

    if total_reputation > 30:
        unlocked_services.extend(advanced_services)

    if total_reputation > 70:
        unlocked_services.extend(premium_services)

    assert len(unlocked_services) >= len(basic_services), "Basic services should always be available"

    # High reputation should unlock more services
    if total_reputation > 50:
        assert len(unlocked_services) > len(basic_services), "Good reputation should unlock additional services"

@then('high reputation should provide special benefits')
def step_verify_reputation_benefits(context):
    """Verify high reputation provides special benefits"""
    bdd_ctx = get_bdd_context(context)

    # Calculate total reputation
    total_reputation = sum(change['reputation_change'] for change in bdd_ctx.interaction_history['reputation_changes'])

    # Define benefits by reputation level
    benefits = []

    if total_reputation > 20:
        benefits.append('guard assistance')
    if total_reputation > 40:
        benefits.append('merchant discounts')
    if total_reputation > 60:
        benefits.append('quest priority')
    if total_reputation > 80:
        benefits.append('noble patronage')

    # Should have at least some benefits for positive reputation
    if total_reputation > 0:
        assert len(benefits) > 0, "Positive reputation should provide benefits"

    # Higher reputation should provide more benefits
    if total_reputation > 50:
        assert len(benefits) >= 2, "High reputation should provide multiple benefits"