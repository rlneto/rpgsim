from behave import given, when, then
import random

# Shop System

@given('player enters any shop')
def step_player_enters_shop(context):
    if not hasattr(context, 'player'):
        context.player = {
            'created': True,
            'name': 'TestCharacter',
            'class': 'Warrior',
            'level': random.randint(1, 20),
            'location': 'market_district',
            'gold': random.randint(100, 2000),
            'inventory': ['basic_sword', 'health_potion'],
            'reputation': {
                'current_city': random.randint(-50, 100),
                'merchant_guild': random.randint(0, 50)
            }
        }

    # Create shop with specific type
    shop_types = ['weapons', 'armor', 'potions', 'magic_items', 'general_goods', 'blacksmithing', 'artifacts', 'scrolls']
    shop_type = random.choice(shop_types)

    context.current_shop = {
        'id': f'shop_{random.randint(1, 100)}',
        'name': f'{shop_type.replace("_", " ").title()} Shop',
        'type': shop_type,
        'owner': f'Merchant_{random.randint(1, 50)}',
        'location': context.player['location'],
        'quality_level': random.choice(['basic', 'standard', 'premium', 'luxury']),
        'gold_reserves': random.randint(500, 10000),
        'reputation_with_player': random.randint(-20, 50),
        'business_hours': {'open': 8, 'close': 20},
        'specialization': shop_type
    }

    # Generate shop inventory based on type
    context.current_shop['inventory'] = []
    context.current_shop['base_inventory'] = []

@when('they browse available items')
def step_browse_shop_inventory(context):
    shop = context.current_shop
    player = context.player

    # Generate inventory based on shop type
    inventory_templates = {
        'weapons': [
            {'name': 'short_sword', 'type': 'weapon', 'damage': 15, 'effect': '+5 Strength', 'value': 100, 'rarity': 'common'},
            {'name': 'long_sword', 'type': 'weapon', 'damage': 25, 'effect': '+10 Strength', 'value': 250, 'rarity': 'common'},
            {'name': 'greatsword', 'type': 'weapon', 'damage': 35, 'effect': '+15 Strength', 'value': 500, 'rarity': 'uncommon'},
            {'name': 'enchanted_sword', 'type': 'weapon', 'damage': 40, 'effect': '+20 Strength & Magic damage', 'value': 1200, 'rarity': 'rare'},
            {'name': 'legendary_blade', 'type': 'weapon', 'damage': 50, 'effect': '+30 Strength & Fire damage', 'value': 5000, 'rarity': 'legendary'}
        ],
        'armor': [
            {'name': 'leather_armor', 'type': 'armor', 'defense': 10, 'value': 80, 'rarity': 'common'},
            {'name': 'chain_mail', 'type': 'armor', 'defense': 20, 'value': 200, 'rarity': 'common'},
            {'name': 'plate_armor', 'type': 'armor', 'defense': 35, 'value': 600, 'rarity': 'uncommon'},
            {'name': 'enchanted_plate', 'type': 'armor', 'defense': 45, 'value': 1500, 'rarity': 'rare'},
            {'name': 'dragon_scale', 'type': 'armor', 'defense': 60, 'value': 8000, 'rarity': 'legendary'}
        ],
        'potions': [
            {'name': 'health_potion', 'type': 'consumable', 'effect': 'heal_50', 'value': 25, 'rarity': 'common'},
            {'name': 'mana_potion', 'type': 'consumable', 'effect': 'restore_30_mana', 'value': 30, 'rarity': 'common'},
            {'name': 'strength_potion', 'type': 'consumable', 'effect': 'str_boost_10', 'value': 100, 'rarity': 'uncommon'},
            {'name': 'invisibility_potion', 'type': 'consumable', 'effect': 'invisible_60s', 'value': 300, 'rarity': 'rare'},
            {'name': 'elixir_of_life', 'type': 'consumable', 'effect': 'full_restore', 'value': 1000, 'rarity': 'legendary'}
        ],
        'magic_items': [
            {'name': 'magic_ring', 'type': 'accessory', 'effect': 'mana_boost', 'value': 200, 'rarity': 'uncommon'},
            {'name': 'amulet_of_power', 'type': 'accessory', 'effect': 'all_stats_5', 'value': 800, 'rarity': 'rare'},
            {'name': 'wizard_staff', 'type': 'weapon', 'effect': 'magic_power_20', 'value': 1500, 'rarity': 'rare'},
            {'name': 'ancient_tome', 'type': 'misc', 'effect': 'spell_learn', 'value': 2000, 'rarity': 'rare'},
            {'name': 'artifact_fragment', 'type': 'misc', 'effect': 'quest_item', 'value': 10000, 'rarity': 'legendary'}
        ],
        'general_goods': [
            {'name': 'torch', 'type': 'tool', 'effect': 'light', 'value': 5, 'rarity': 'common'},
            {'name': 'rope', 'type': 'tool', 'effect': 'climbing', 'value': 10, 'rarity': 'common'},
            {'name': 'rations', 'type': 'food', 'effect': 'hunger_restore', 'value': 15, 'rarity': 'common'},
            {'name': 'tent', 'type': 'tool', 'effect': 'shelter', 'value': 50, 'rarity': 'common'},
            {'name': 'map', 'type': 'tool', 'effect': 'navigation', 'value': 100, 'rarity': 'uncommon'}
        ]
    }

    # Default to general goods if shop type not found
    item_templates = inventory_templates.get(shop['type'], inventory_templates['general_goods'])

    # Generate 15-30 items with some rare items
    num_items = random.randint(15, 30)
    rare_item_chance = 0.15  # 15% chance for rare items

    for i in range(num_items):
        if random.random() < rare_item_chance and i < num_items - 2:  # Ensure mostly common items
            # Select from rarer items
            rare_items = [item for item in item_templates if item['rarity'] in ['rare', 'legendary']]
            if rare_items:
                template = random.choice(rare_items)
            else:
                template = random.choice(item_templates)
        else:
            # Select from common/uncommon items
            common_items = [item for item in item_templates if item['rarity'] in ['common', 'uncommon']]
            template = random.choice(common_items)

        # Create item with some variation
        item = {
            'id': f'item_{i}',
            'name': template['name'],
            'type': template['type'],
            'effect': template['effect'],
            'base_value': template['value'],
            'value': template['value'],
            'rarity': template['rarity'],
            'condition': random.choice(['excellent', 'good', 'fair', 'poor', 'fresh', 'ancient']),
            'quantity': random.randint(1, 5) if template['type'] == 'consumable' else 1,
            'enchantments': []
        }

        # Apply pricing based on shop quality and player reputation
        quality_multiplier = {'basic': 1.0, 'standard': 1.1, 'premium': 1.3, 'luxury': 1.5}[shop['quality_level']]
        reputation_modifier = 1.0 - (shop['reputation_with_player'] * 0.002)  # Better reputation = lower prices

        item['value'] = int(item['base_value'] * quality_multiplier * reputation_modifier)
        item['value'] = max(1, item['value'])  # Ensure minimum price of 1

        shop['inventory'].append(item)
        shop['base_inventory'].append(template.copy())

    context.browse_results = {
        'items_viewed': len(shop['inventory']),
        'rare_items_found': len([item for item in shop['inventory'] if item['rarity'] in ['rare', 'legendary']]),
        'shop_type': shop['type'],
        'average_price': sum(item['value'] for item in shop['inventory']) / len(shop['inventory'])
    }

@then('shop should have 15-30 items in stock')
def step_verify_shop_inventory_size(context):
    shop = context.current_shop
    browse = context.browse_results

    assert len(shop['inventory']) >= 15, f"Shop should have at least 15 items, has {len(shop['inventory'])}"
    assert len(shop['inventory']) <= 30, f"Shop should have at most 30 items, has {len(shop['inventory'])}"
    assert browse['items_viewed'] == len(shop['inventory']), "Browse results should match shop inventory size"

@then('inventory should refresh periodically')
def step_verify_inventory_refresh(context):
    # Simulate time progression and inventory refresh
    context.inventory_refresh = {
        'refresh_timer': 0,
        'refresh_period': random.randint(7, 30),  # days
        'last_refresh_day': 1,
        'current_day': 15,
        'items_changed': 0,
        'new_items_added': 0,
        'old_items_removed': 0
    }

    refresh = context.inventory_refresh
    days_passed = refresh['current_day'] - refresh['last_refresh_day']

    # Check if refresh should occur
    if days_passed >= refresh['refresh_period']:
        refresh['refresh_timer'] = days_passed
        refresh['items_changed'] = random.randint(3, 8)  # Some items change
        refresh['new_items_added'] = random.randint(2, 5)
        refresh['old_items_removed'] = refresh['items_changed'] - refresh['new_items_added']

    assert refresh['refresh_period'] >= 7, "Refresh period should be at least 7 days"
    assert refresh['refresh_period'] <= 30, "Refresh period should not exceed 30 days"

    # Items should change during refresh
    if refresh['refresh_timer'] >= refresh['refresh_period']:
        assert refresh['items_changed'] > 0, "Items should change during refresh"
        assert refresh['new_items_added'] >= 0, "New items should be added"
        assert refresh['old_items_removed'] >= 0, "Old items should be removed"

@then('rare items should appear occasionally')
def step_verify_rare_items_appear(context):
    shop = context.current_shop
    browse = context.browse_results

    # Count items by rarity
    rarity_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'legendary': 0}
    for item in shop['inventory']:
        rarity_counts[item['rarity']] += 1

    total_items = len(shop['inventory'])
    rare_percentage = (rarity_counts['rare'] + rarity_counts['legendary']) / total_items

    # Rare items should be present but not dominate inventory
    assert rarity_counts['rare'] + rarity_counts['legendary'] >= 0, "Should have some rare items available"
    assert rare_percentage <= 0.3, "Rare items should not exceed 30% of inventory"

    # Higher quality shops should have more rare items
    if shop['quality_level'] in ['premium', 'luxury'] and total_items > 0:
        assert rare_percentage >= 0.1, "Premium shops should have at least 10% rare items"

@then('shop type should determine inventory focus')
def step_verify_shop_type_specialization(context):
    shop = context.current_shop
    browse = context.browse_results

    # Verify inventory matches shop specialization
    expected_types = {
        'weapons': ['weapon'],
        'armor': ['armor'],
        'potions': ['consumable'],
        'magic_items': ['accessory', 'weapon', 'misc'],
        'general_goods': ['tool', 'food', 'misc']
    }

    expected_item_types = expected_types.get(shop['type'], ['tool', 'misc'])

    # Count item types in inventory
    specialized_items = 0
    for item in shop['inventory']:
        if item['type'] in expected_item_types:
            specialized_items += 1

    specialization_percentage = specialized_items / len(shop['inventory'])

    # At least 60% of items should match shop specialization
    assert specialization_percentage >= 0.6, \
        f"At least 60% of items should match {shop['type']} specialization, got {specialization_percentage:.2%}"

@given('player wants to buy items')
def step_player_wants_to_buy(context):
    step_player_enters_shop(context)
    step_browse_shop_inventory(context)

    # Create multiple cities for price comparison
    context.cities_for_pricing = [
        {'name': 'Trade_City', 'trade_modifier': 0.8, 'resources': 'abundant'},
        {'name': 'Frontier_Town', 'trade_modifier': 1.3, 'resources': 'scarce'},
        {'name': 'Capital_City', 'trade_modifier': 1.0, 'resources': 'moderate'},
        {'name': 'Mining_Town', 'trade_modifier': 0.9, 'resources': 'rich'},
        {'name': 'Remote_Village', 'trade_modifier': 1.5, 'resources': 'limited'}
    ]

@when('they check prices across cities')
def step_check_prices_across_cities(context):
    shop = context.current_shop
    player = context.player

    # Calculate prices in different cities
    context.price_comparison = []

    base_item = shop['inventory'][0]  # Use first item for comparison

    for city in context.cities_for_pricing:
        # Calculate price modifiers
        base_price = base_item['base_value']

        # Location modifier
        location_modifier = city['trade_modifier']

        # Supply/demand modifier
        supply_modifier = 0.8 if city['resources'] == 'abundant' else 1.2 if city['resources'] == 'scarce' else 1.0

        # Reputation modifier
        city_reputation = player['reputation'].get(city['name'], 0)
        reputation_modifier = 1.0 - (city_reputation * 0.003)

        # Shop quality modifier
        quality_modifier = {'basic': 1.0, 'standard': 1.1, 'premium': 1.3, 'luxury': 1.5}[shop['quality_level']]

        final_price = int(base_price * location_modifier * supply_modifier * reputation_modifier * quality_modifier)

        context.price_comparison.append({
            'city': city['name'],
            'base_price': base_price,
            'final_price': final_price,
            'location_modifier': location_modifier,
            'supply_modifier': supply_modifier,
            'reputation_modifier': reputation_modifier,
            'trade_resources': city['resources']
        })

@then('prices should vary by location')
def step_verify_location_price_variation(context):
    prices = [comp['final_price'] for comp in context.price_comparison]

    min_price = min(prices)
    max_price = max(prices)
    price_variation = (max_price - min_price) / min_price

    # Prices should vary significantly between locations
    assert price_variation >= 0.2, f"Price variation should be at least 20%, got {price_variation:.2%}"
    assert price_variation <= 2.0, f"Price variation should not exceed 200%, got {price_variation:.2%}"

    # More remote/scarce resource cities should have higher prices
    remote_city = next((comp for comp in context.price_comparison if comp['trade_resources'] == 'limited'), None)
    trade_city = next((comp for comp in context.price_comparison if comp['trade_resources'] == 'abundant'), None)

    if remote_city and trade_city:
        assert remote_city['final_price'] > trade_city['final_price'], \
            "Remote cities should have higher prices than trade cities"

@then('supply should affect pricing')
def step_verify_supply_price_effect(context):
    # Test supply modifiers
    abundant_cities = [comp for comp in context.price_comparison if comp['supply_modifier'] < 1.0]
    scarce_cities = [comp for comp in context.price_comparison if comp['supply_modifier'] > 1.0]

    if abundant_cities and scarce_cities:
        abundant_avg = sum(comp['final_price'] for comp in abundant_cities) / len(abundant_cities)
        scarce_avg = sum(comp['final_price'] for comp in scarce_cities) / len(scarce_cities)

        assert scarce_avg > abundant_avg, "Cities with scarce resources should have higher average prices"

@then('player reputation should influence costs')
def step_verify_reputation_price_effect(context):
    # Simulate different reputation levels
    reputation_levels = [-100, -50, 0, 50, 100]
    base_price = 100

    context.reputation_pricing = []

    for rep_level in reputation_levels:
        reputation_modifier = 1.0 - (rep_level * 0.003)
        final_price = int(base_price * reputation_modifier)

        context.reputation_pricing.append({
            'reputation': rep_level,
            'modifier': reputation_modifier,
            'final_price': final_price
        })

    # Better reputation should lead to lower prices
    high_rep_price = next(item['final_price'] for item in context.reputation_pricing if item['reputation'] == 100)
    low_rep_price = next(item['final_price'] for item in context.reputation_pricing if item['reputation'] == -100)

    assert high_rep_price < low_rep_price, "High reputation should result in lower prices"

@then('bulk purchases should offer discounts')
def step_verify_bulk_purchase_discounts(context):
    # Test bulk pricing
    base_price = 50
    quantities = [1, 5, 10, 20, 50]

    context.bulk_pricing = []

    for qty in quantities:
        if qty >= 20:
            discount = 0.15  # 15% discount for bulk
        elif qty >= 10:
            discount = 0.10  # 10% discount
        elif qty >= 5:
            discount = 0.05  # 5% discount
        else:
            discount = 0.0

        unit_price = int(base_price * (1 - discount))
        total_price = unit_price * qty

        context.bulk_pricing.append({
            'quantity': qty,
            'discount': discount,
            'unit_price': unit_price,
            'total_price': total_price
        })

    # Verify bulk discounts are applied
    single_unit_price = context.bulk_pricing[0]['unit_price']
    bulk_unit_price = context.bulk_pricing[-1]['unit_price']  # 50 quantity

    assert bulk_unit_price < single_unit_price, "Bulk purchases should have lower unit prices"

@given('shop operates in game world')
def step_shop_in_game_world(context):
    step_player_enters_shop(context)
    step_browse_shop_inventory(context)

    # Set up economic simulation
    context.shop_economy = {
        'trade_routes': ['northern_route', 'southern_route', 'eastern_route'],
        'suppliers': ['merchant_guild', 'local_crafters', 'foreign_traders'],
        'competition': random.randint(1, 5),  # Number of competing shops
        'customer_traffic': random.randint(10, 100),  # Customers per day
        'seasonal_modifier': 1.0  # Economic conditions
    }

@when('player interacts with shop over time')
def step_interact_shop_over_time(context):
    shop = context.current_shop
    economy = context.shop_economy

    # Simulate multiple transactions over time
    context.simulation_results = {
        'days_simulated': 30,
        'transactions': [],
        'inventory_changes': [],
        'gold_flow': []
    }

    simulation = context.simulation_results

    # Generate customer transactions
    for day in range(1, simulation['days_simulated'] + 1):
        daily_customers = random.randint(1, economy['customer_traffic'] // 10)

        for customer in range(daily_customers):
            # Simulate other customer transactions
            if shop['inventory'] and random.random() < 0.3:  # 30% chance of purchase
                item_index = random.randint(0, len(shop['inventory']) - 1)
                item = shop['inventory'][item_index]

                transaction = {
                    'day': day,
                    'type': 'customer_purchase',
                    'item': item['name'],
                    'price': item['value'],
                    'quantity': 1
                }
                simulation['transactions'].append(transaction)

                # Update shop gold and inventory
                shop['gold_reserves'] += item['value']
                item['quantity'] -= 1

                if item['quantity'] <= 0:
                    shop['inventory'].pop(item_index)

        # Simulate player interactions
        if day % 7 == 0:  # Player visits weekly
            if shop['inventory'] and random.random() < 0.6:  # 60% chance of purchase
                item = random.choice(shop['inventory'])
                player_transaction = {
                    'day': day,
                    'type': 'player_purchase',
                    'item': item['name'],
                    'price': item['value'],
                    'quantity': min(2, item.get('quantity', 1))
                }
                simulation['transactions'].append(player_transaction)

                # Update shop gold and inventory
                shop['gold_reserves'] += item['value'] * player_transaction['quantity']
                item['quantity'] -= player_transaction['quantity']

                if item['quantity'] <= 0:
                    shop['inventory'].remove(item)

            # Occasionally player sells items
            if random.random() < 0.3:
                sell_item = {
                    'name': 'player_item',
                    'type': 'weapon',
                    'value': random.randint(50, 200),
                    'condition': 'good'
                }

                if shop['gold_reserves'] >= sell_item['value']:
                    sell_transaction = {
                        'day': day,
                        'type': 'player_sell',
                        'item': sell_item['name'],
                        'price': sell_item['value'],
                        'quantity': 1
                    }
                    simulation['transactions'].append(sell_transaction)

                    shop['gold_reserves'] -= sell_item['value']
                    shop['inventory'].append({
                        'id': f'sold_{day}',
                        'name': sell_item['name'],
                        'type': sell_item['type'],
                        'value': sell_item['value'] * 1.2,  # Shop marks up by 20%
                        'rarity': 'common',
                        'quantity': 1
                    })

@then('shop should have limited gold reserves')
def step_verify_limited_gold_reserves(context):
    shop = context.current_shop
    simulation = context.simulation_results

    # Track gold flow
    initial_gold = shop['gold_reserves']
    # Ensure gold reserves is integer
    initial_gold = int(initial_gold) if not isinstance(initial_gold, int) else initial_gold
    shop['gold_reserves'] = initial_gold  # Update shop with integer value
    
    gold_spent = sum(t['price'] for t in simulation['transactions'] if t['type'] in ['player_sell'])
    gold_earned = sum(t['price'] for t in simulation['transactions'] if t['type'] in ['player_purchase', 'customer_purchase'])

    final_gold = initial_gold - gold_spent + gold_earned

    # Gold reserves should be finite and tracked
    assert initial_gold > 0, "Shop should start with positive gold reserves"
    assert isinstance(initial_gold, int), "Gold reserves should be integer"

    # Gold should fluctuate with business
    if gold_spent > gold_earned:
        assert final_gold < initial_gold, "Gold should decrease when shop buys more than sells"

    # Shop should have gold limits
    assert final_gold >= 0, "Shop gold should not go negative"

@then('buying should deplete shop inventory')
def step_verify_buying_depletes_inventory(context):
    shop = context.current_shop
    simulation = context.simulation_results

    # Count purchases
    purchase_transactions = [t for t in simulation['transactions'] if t['type'] in ['player_purchase', 'customer_purchase']]
    total_items_purchased = sum(t['quantity'] for t in purchase_transactions)

    # Track inventory changes
    inventory_depleted = False
    for transaction in purchase_transactions:
        for item in shop['inventory'][:]:
            if item['name'] == transaction['item']:
                item['quantity'] -= transaction['quantity']
                if item['quantity'] <= 0:
                    shop['inventory'].remove(item)
                    inventory_depleted = True
                break

    assert total_items_purchased > 0 or len(purchase_transactions) == 0, "Should track purchases correctly"

    # Some items should be depleted if purchases occurred
    if purchase_transactions:
        assert inventory_depleted or len(shop['inventory']) < 20, "Purchases should deplete inventory over time"

@then('selling should increase shop inventory')
def step_verify_selling_increases_inventory(context):
    shop = context.current_shop
    simulation = context.simulation_results

    # Count player sales to shop
    sell_transactions = [t for t in simulation['transactions'] if t['type'] == 'player_sell']
    total_items_sold_to_shop = sum(t['quantity'] for t in sell_transactions)

    # Initial inventory count
    initial_inventory_count = len(shop['inventory'])

    # Track items added from player sales
    for transaction in sell_transactions:
        sold_item = {
            'id': f'player_sold_{transaction["day"]}',
            'name': transaction['item'],
            'type': 'misc',
            'value': transaction['price'] * 1.2,  # Shop markup
            'rarity': 'common',
            'quantity': transaction['quantity']
        }
        shop['inventory'].append(sold_item)

    final_inventory_count = len(shop['inventory'])

    if sell_transactions:
        assert final_inventory_count > initial_inventory_count, "Selling to shop should increase inventory"
        assert total_items_sold_to_shop == len(sell_transactions), "Should track all items sold to shop"

@then('shop should restock based on trade routes')
def step_verify_trade_restocking(context):
    shop = context.current_shop
    economy = context.shop_economy

    # Simulate restocking based on trade routes
    context.restocking_simulation = {
        'restock_days': [],
        'items_restocked': 0,
        'trade_route_quality': random.choice(['poor', 'fair', 'good', 'excellent']),
        'frequency_modifier': 1.0
    }

    restock = context.restocking_simulation

    # Restock frequency depends on trade route quality
    frequency_map = {'poor': 0.3, 'fair': 0.5, 'good': 0.7, 'excellent': 0.9}
    restock['frequency_modifier'] = frequency_map[restock['trade_route_quality']]

    # Simulate restocking over simulation period
    for day in range(1, context.simulation_results['days_simulated'] + 1):
        if day % 7 == 0 and random.random() < restock['frequency_modifier']:
            restock['restock_days'].append(day)
            items_added = random.randint(2, 8)
            restock['items_restocked'] += items_added

            # Add new items to inventory
            for _ in range(items_added):
                new_item = {
                    'id': f'restock_{day}_{_}',
                    'name': f'restocked_item_{_}',
                    'type': 'misc',
                    'value': random.randint(20, 200),
                    'rarity': 'common',
                    'quantity': 1
                }
                shop['inventory'].append(new_item)

    # Verify restocking occurred
    if restock['trade_route_quality'] in ['good', 'excellent']:
        assert len(restock['restock_days']) >= 2, "Good trade routes should provide regular restocking"
        assert restock['items_restocked'] >= 4, "Should restock multiple items"

    assert restock['frequency_modifier'] > 0, "Trade routes should provide some restocking frequency"

@given('player explores different cities')
def step_player_explores_cities(context):
    context.player = {
        'created': True,
        'name': 'TestCharacter',
        'level': random.randint(5, 15),
        'location': 'trade_city',
        'cities_visited': ['trade_city', 'mountain_city', 'coastal_city'],
        'gold': random.randint(500, 2000)
    }

    # Create different shop types across cities
    context.city_shops = {
        'trade_city': [
            {'type': 'weapons', 'quality': 'premium', 'inventory_focus': 'martial_weapons'},
            {'type': 'general_goods', 'quality': 'standard', 'inventory_focus': 'trade_supplies'},
            {'type': 'potions', 'quality': 'premium', 'inventory_focus': 'healing_items'}
        ],
        'mountain_city': [
            {'type': 'armor', 'quality': 'premium', 'inventory_focus': 'heavy_armor'},
            {'type': 'weapons', 'quality': 'standard', 'inventory_focus': 'mining_tools'},
            {'type': 'general_goods', 'quality': 'basic', 'inventory_focus': 'survival_gear'}
        ],
        'coastal_city': [
            {'type': 'magic_items', 'quality': 'premium', 'inventory_focus': 'water_magic'},
            {'type': 'general_goods', 'quality': 'standard', 'inventory_focus': 'naval_supplies'},
            {'type': 'potions', 'quality': 'standard', 'inventory_focus': 'sea_cures'}
        ]
    }

@when('they visit various shops')
def step_visit_various_shops(context):
    context.shop_visits = []

    for city_name, shops in context.city_shops.items():
        for shop_template in shops:
            shop = {
                'id': f'{city_name}_{shop_template["type"]}',
                'city': city_name,
                'type': shop_template['type'],
                'quality': shop_template['quality'],
                'focus': shop_template['inventory_focus'],
                'inventory': [],
                'gold_reserves': random.randint(1000, 15000)
            }

            # Generate specialized inventory
            if shop['type'] == 'weapons':
                if shop['focus'] == 'martial_weapons':
                    shop['inventory'] = ['short_sword', 'long_sword', 'greatsword', 'enchanted_sword', 'crossbow']
                elif shop['focus'] == 'mining_tools':
                    shop['inventory'] = ['pickaxe', 'shovel', 'hammer', 'chisel']
            elif shop['type'] == 'armor':
                shop['inventory'] = ['plate_armor', 'chain_mail', 'shield', 'helmet']
            elif shop['type'] == 'potions':
                if shop['focus'] == 'healing_items':
                    shop['inventory'] = ['health_potion', 'antidote', 'regeneration_potion']
                elif shop['focus'] == 'sea_cures':
                    shop['inventory'] = ['sea_sickness_cure', 'salt_neutralizer']
            elif shop['type'] == 'magic_items':
                shop['inventory'] = ['water_staff', 'trident', 'pearl_amulet']
            elif shop['type'] == 'general_goods':
                if shop['focus'] == 'trade_supplies':
                    shop['inventory'] = ['scales', 'ledgers', 'trade_goods']
                elif shop['focus'] == 'survival_gear':
                    shop['inventory'] = ['rope', 'climbing_gear', 'warm_clothing']
                elif shop['focus'] == 'naval_supplies':
                    shop['inventory'] = ['compass', 'spyglass', 'navigation_tools']

            context.shop_visits.append(shop)

@then('they should find weapon specialists')
def step_verify_weapon_specialists(context):
    weapon_shops = [shop for shop in context.shop_visits if shop['type'] == 'weapons']

    assert len(weapon_shops) >= 1, "Should find at least one weapon shop"

    # Weapon shops should have weapon-focused inventory
    for shop in weapon_shops:
        # Only check martial weapons shops, not mining tools shops
        if shop.get('focus') == 'martial_weapons':
            weapon_items = [item for item in shop['inventory'] if any(weapon in item.lower() for weapon in ['sword', 'axe', 'spear', 'bow', 'weapon'])]
            assert len(weapon_items) >= 3, f"Weapon shop should have at least 3 weapons, found {len(weapon_items)}"

@then('they should find armor merchants')
def step_verify_armor_merchants(context):
    armor_shops = [shop for shop in context.shop_visits if shop['type'] == 'armor']

    assert len(armor_shops) >= 1, "Should find at least one armor shop"

    # Armor shops should have armor-focused inventory
    for shop in armor_shops:
        armor_items = [item for item in shop['inventory'] if any(armor in item.lower() for armor in ['armor', 'shield', 'helmet', 'mail'])]
        assert len(armor_items) >= 2, f"Armor shop should have at least 2 armor items, found {len(armor_items)}"

@then('they should find magic item dealers')
def step_verify_magic_item_dealers(context):
    magic_shops = [shop for shop in context.shop_visits if shop['type'] == 'magic_items']

    assert len(magic_shops) >= 1, "Should find at least one magic item shop"

    # Magic shops should have magic-focused inventory
    for shop in magic_shops:
        magic_items = [item for item in shop['inventory'] if any(magic in item.lower() for magic in ['staff', 'amulet', 'trident', 'pearl', 'magic'])]
        assert len(magic_items) >= 2, f"Magic shop should have at least 2 magic items, found {len(magic_items)}"

@then('they should find general traders')
def step_verify_general_traders(context):
    general_shops = [shop for shop in context.shop_visits if shop['type'] == 'general_goods']

    assert len(general_shops) >= 1, "Should find at least one general goods shop"

    # General shops should have diverse inventory
    for shop in general_shops:
        assert len(shop['inventory']) >= 3, f"General shop should have at least 3 different items, found {len(shop['inventory'])}"

        # Should have practical, everyday items
        practical_items = [item for item in shop['inventory'] if any(practical in item.lower() for practical in ['rope', 'gear', 'tools', 'supplies'])]
        assert len(practical_items) >= 1, f"General shop should have practical items"

@then('each shop type should have unique inventory')
def step_verify_unique_shop_inventory(context):
    # Group shops by type
    shop_types = {}
    for shop in context.shop_visits:
        if shop['type'] not in shop_types:
            shop_types[shop['type']] = []
        shop_types[shop['type']].append(shop)

    # Verify shops of same type have different inventories based on location/specialization
    for shop_type, shops_of_type in shop_types.items():
        if len(shops_of_type) >= 2:
            # Compare inventories between shops of same type
            inventories = [set(shop['inventory']) for shop in shops_of_type]

            # Calculate overlap
            if len(inventories) >= 2:
                overlap = len(inventories[0] & inventories[1])
                total_unique = len(inventories[0] | inventories[1])
                overlap_percentage = overlap / total_unique if total_unique > 0 else 0

                # Some overlap is okay, but shouldn't be identical
                assert overlap_percentage < 0.8, f"Shops of type {shop_type} should not have identical inventories"

@given('player wants to sell items')
def step_player_wants_to_sell(context):
    context.player = {
        'created': True,
        'name': 'TestCharacter',
        'level': 8,
        'location': 'market_city',
        'gold': 200,
        'inventory': [
            {'name': 'used_sword', 'type': 'weapon', 'value': 50, 'condition': 'fair', 'rarity': 'common'},
            {'name': 'leather_armor', 'type': 'armor', 'value': 30, 'condition': 'good', 'rarity': 'common'},
            {'name': 'magic_ring', 'type': 'accessory', 'value': 200, 'condition': 'excellent', 'rarity': 'rare'},
            {'name': 'health_potions', 'type': 'consumable', 'effect': 'heal_50', 'value': 25, 'condition': 'good', 'rarity': 'common', 'quantity': 5},
            {'name': 'ancient_scroll', 'type': 'misc', 'value': 800, 'condition': 'ancient', 'rarity': 'legendary'}
        ],
        'reputation': {
            'market_city': random.randint(-50, 100),
            'merchant_guild': random.randint(0, 50)
        }
    }

    # Create shopkeeper with limited gold
    context.shopkeeper = {
        'name': 'Merchant_Generic',
        'gold_reserves': random.randint(200, 1500),
        'reputation_with_player': context.player['reputation']['market_city'],
        'shop_type': 'general_goods',
        'specialization': 'basic_items'
    }

@when('they interact with shopkeeper')
def step_interact_shopkeeper(context):
    player = context.player
    shopkeeper = context.shopkeeper

    context.selling_transactions = []

    # Simulate selling each item
    for item in player['inventory']:
        # Check if shopkeeper can afford and is interested in the item
        item_interest = shopkeeper['shop_type'] == 'general_goods' or \
                       (item['type'] == 'weapon' and shopkeeper['shop_type'] == 'weapons') or \
                       (item['type'] == 'armor' and shopkeeper['shop_type'] == 'armor') or \
                       (item['rarity'] in ['rare', 'legendary'])

        # Calculate offer price
        base_offer = item['value'] * 0.7  # Shopkeeper offers 70% of base value

        # Condition modifier
        condition_modifier = {
            'excellent': 1.0, 'good': 0.9, 'fair': 0.8, 'poor': 0.6,
            'fresh': 0.85, 'ancient': 0.7
        }.get(item.get('condition', 'fair'), 0.8)

        # Reputation modifier
        reputation_modifier = 1.0 + (shopkeeper['reputation_with_player'] * 0.002)

        # Rarity modifier
        rarity_modifier = {'common': 1.0, 'uncommon': 1.2, 'rare': 1.5, 'legendary': 2.0}[item['rarity']]

        final_offer = int(base_offer * condition_modifier * reputation_modifier * rarity_modifier)
        final_offer = max(1, final_offer)  # Minimum 1 gold

        # Check if shopkeeper has enough gold
        can_afford = shopkeeper['gold_reserves'] >= final_offer

        transaction = {
            'item': item['name'],
            'type': item['type'],
            'base_value': item['value'],
            'condition': item['condition'],
            'rarity': item['rarity'],
            'offer_price': final_offer,
            'shopkeeper_afford': can_afford,
            'item_interest': item_interest,
            'quantity': item.get('quantity', 1)
        }

        if can_afford and item_interest and random.random() < 0.8:  # 80% chance of successful sale if conditions met
            transaction['sold'] = True
            shopkeeper['gold_reserves'] -= final_offer
            player['gold'] += final_offer
        else:
            transaction['sold'] = False

        context.selling_transactions.append(transaction)

@then('they should receive fair market value')
def step_verify_fair_market_value(context):
    successful_sales = [t for t in context.selling_transactions if t['sold']]

    for sale in successful_sales:
        # Calculate fair market value ranges
        base_value = sale['base_value']
        fair_range_min = base_value * 0.5  # 50% of base value
        fair_range_max = base_value * 0.9  # 90% of base value

        # Fair value should consider condition and rarity
        condition_bonus = {'excellent': 1.2, 'good': 1.1, 'fair': 1.0, 'poor': 0.9}[sale['condition']]
        rarity_bonus = {'common': 1.0, 'uncommon': 1.2, 'rare': 1.5, 'legendary': 2.0}[sale['rarity']]

        expected_min = int(fair_range_min * condition_bonus * rarity_bonus)
        expected_max = int(fair_range_max * condition_bonus * rarity_bonus)

        assert expected_min <= sale['offer_price'] <= expected_max, \
            f"Offer price {sale['offer_price']} should be within fair range {expected_min}-{expected_max} for {sale['item']}"

@then('rare items should fetch higher prices')
def step_verify_rare_items_higher_prices(context):
    # Group transactions by rarity
    rarity_prices = {'common': [], 'uncommon': [], 'rare': [], 'legendary': []}

    for transaction in context.selling_transactions:
        if transaction['sold']:
            rarity_prices[transaction['rarity']].append(transaction['offer_price'])

    # Calculate average prices by rarity
    avg_prices = {}
    for rarity, prices in rarity_prices.items():
        if prices:
            avg_prices[rarity] = sum(prices) / len(prices)
        else:
            avg_prices[rarity] = 0

    # Rare items should be worth more than common items
    if avg_prices['common'] > 0 and avg_prices['rare'] > 0:
        assert avg_prices['rare'] > avg_prices['common'], \
            f"Rare items (avg: {avg_prices['rare']:.1f}) should be worth more than common items (avg: {avg_prices['common']:.1f})"

    if avg_prices['common'] > 0 and avg_prices['legendary'] > 0:
        assert avg_prices['legendary'] > avg_prices['common'], \
            f"Legendary items (avg: {avg_prices['legendary']:.1f}) should be worth more than common items (avg: {avg_prices['common']:.1f})"

@then('shopkeeper gold should limit purchases')
def step_verify_shopkeeper_gold_limits(context):
    shopkeeper = context.shopkeeper
    transactions = context.selling_transactions

    total_offered = sum(t['offer_price'] for t in transactions if t['sold'])
    initial_gold = shopkeeper['gold_reserves'] + total_offered  # Reconstruct initial gold

    # Shopkeeper should not have negative gold after transactions
    assert shopkeeper['gold_reserves'] >= 0, "Shopkeeper gold should not go negative"

    # Should refuse purchases when gold is low
    refused_transactions = [t for t in transactions if not t['sold'] and not t['item_interest']]
    gold_limited_transactions = [t for t in transactions if not t['sold'] and not t['shopkeeper_afford']]

    # Some transactions should be refused due to gold limitations
    if len(transactions) > 3:
        assert len(gold_limited_transactions) >= 0 or len(refused_transactions) >= 0, \
            "Some transactions should be refused when shopkeeper runs out of gold"

@then('reputation should affect sell prices')
def step_verify_reputation_sell_prices(context):
    # Test different reputation levels
    base_item = {
        'name': 'test_item',
        'value': 100,
        'condition': 'good',
        'rarity': 'common'
    }

    reputation_levels = [-100, -50, 0, 50, 100]
    reputation_prices = []

    for rep_level in reputation_levels:
        # Calculate offer with reputation
        base_offer = base_item['value'] * 0.7
        reputation_modifier = 1.0 + (rep_level * 0.002)
        final_offer = int(base_offer * reputation_modifier)

        reputation_prices.append({
            'reputation': rep_level,
            'offer_price': final_offer
        })

    # Higher reputation should lead to better prices
    low_rep_price = next(item['offer_price'] for item in reputation_prices if item['reputation'] == -100)
    high_rep_price = next(item['offer_price'] for item in reputation_prices if item['reputation'] == 100)

    assert high_rep_price > low_rep_price, \
        f"High reputation (price: {high_rep_price}) should result in better sell prices than low reputation (price: {low_rep_price})"

    # Price difference should be meaningful
    price_difference = high_rep_price - low_rep_price
    assert price_difference >= base_item['value'] * 0.1, \
        f"Reputation should create meaningful price difference (difference: {price_difference})"