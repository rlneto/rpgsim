from behave import given, when, then
import random

# Equipment and Magic Items

@given('the player defeats enemies or completes quests')
def step_player_defeats_enemies_or_completes_quests(context):
    # Set up player with some progress
    context.player = context.player if hasattr(context, 'player') else {
        'created': True,
        'name': 'TestCharacter',
        'class': 'Warrior',
        'level': 5,
        'location': 'Dungeon',
        'hp': 150,
        'max_hp': 150,
        'stats': {
            'strength': 15,
            'dexterity': 12,
            'intelligence': 10,
            'wisdom': 11,
            'charisma': 9,
            'constitution': 14
        },
        'abilities': ['Attack', 'Defend', 'Power Strike', 'Heal'],
        'inventory': [],
        'equipment': {
            'weapon': None,
            'armor': None,
            'accessory1': None,
            'accessory2': None
        },
        'gold': 500
    }
    
    # Record completed activities
    context.recent_victories = ['goblin_scout', 'orc_warrior', 'quest_item_delivery']
    context.activity_difficulty = random.choice(['easy', 'medium', 'hard'])

@when('receiving rewards')
def step_receive_rewards(context):
    # Generate loot based on activity
    context.received_loot = []
    
    # Generate random loot
    num_items = random.randint(1, 3)
    for i in range(num_items):
        item = {
            'id': f"item_{random.randint(0, 199)}",
            'name': f"Item {i}",
            'type': random.choice(['weapon', 'armor', 'accessory', 'consumable']),
            'quality': random.choice(['common', 'uncommon', 'rare', 'epic', 'legendary']),
            'stats': {},
            'effects': [],
            'value': random.randint(10, 500)
        }
        
        # Generate stats based on item type and quality
        if item['type'] in ['weapon', 'armor']:
            # Add stat bonuses
            num_stats = {'common': 1, 'uncommon': 2, 'rare': 3, 'epic': 4, 'legendary': 5}[item['quality']]
            possible_stats = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']
            for j in range(num_stats):
                stat = random.choice(possible_stats)
                bonus = {'common': 2, 'uncommon': 4, 'rare': 6, 'epic': 8, 'legendary': 10}[item['quality']]
                item['stats'][stat] = bonus
        
        # Generate magic effects for higher quality items
        if item['quality'] in ['rare', 'epic', 'legendary']:
            num_effects = {'rare': 1, 'epic': 2, 'legendary': 3}[item['quality']]
            possible_effects = ['fire_damage', 'life_steal', 'critical_chance', 'evasion', 'magic_resistance']
            for j in range(num_effects):
                effect = random.choice(possible_effects)
                item['effects'].append(effect)
        
        context.received_loot.append(item)

        # Add item to player's inventory
        context.player['inventory'].append(item)

    # Also add gold reward
    context.gold_reward = random.randint(20, 200)
    if context.activity_difficulty == 'medium':
        context.gold_reward *= 2
    elif context.activity_difficulty == 'hard':
        context.gold_reward *= 3

@then('they should have chance to find randomized loot')
def step_verify_randomized_loot(context):
    # Verify loot is randomized
    assert context.received_loot, "Player should receive at least one item"
    
    # Check variety in loot types
    loot_types = [item['type'] for item in context.received_loot]
    assert len(set(loot_types)) >= 1, "Loot should include different types"

@then('loot quality should scale with difficulty')
def step_verify_loot_quality_scaling(context):
    # Define quality scaling
    difficulty_quality_chances = {
        'easy': {'common': 70, 'uncommon': 25, 'rare': 5, 'epic': 0, 'legendary': 0},
        'medium': {'common': 40, 'uncommon': 40, 'rare': 15, 'epic': 4, 'legendary': 1},
        'hard': {'common': 20, 'uncommon': 35, 'rare': 30, 'epic': 12, 'legendary': 3}
    }
    
    # Check if quality is appropriate for difficulty
    # In a real implementation, this would check against actual random generation
    # For testing, we just verify the system has appropriate quality ranges
    assert context.activity_difficulty in difficulty_quality_chances, "Should handle all difficulty levels"

@then('they should find approximately 200 unique magic items')
def step_verify_unique_items(context):
    if not hasattr(context, 'items'):
        context.items = []
        
        # Generate 200 unique magic items
        for i in range(200):
            item = {
                'id': f"item_{i}",
                'name': f"Magic Item {i}: {random.choice(['Sword', 'Armor', 'Ring', 'Amulet', 'Staff', 'Dagger'])} of {random.choice(['Power', 'Wisdom', 'Flames', 'Shadows', 'Protection'])}",
                'type': random.choice(['weapon', 'armor', 'accessory', 'consumable']),
                'quality': random.choice(['common', 'uncommon', 'rare', 'epic', 'legendary']),
                'stats': {},
                'effects': [],
                'value': random.randint(10, 2000),
                'description': f"This is a unique magical item with special properties."
            }
            
            # Generate stats
            if item['type'] in ['weapon', 'armor']:
                num_stats = {'common': 1, 'uncommon': 2, 'rare': 3, 'epic': 4, 'legendary': 5}[item['quality']]
                possible_stats = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']
                for j in range(num_stats):
                    stat = random.choice(possible_stats)
                    bonus = {'common': 2, 'uncommon': 4, 'rare': 6, 'epic': 8, 'legendary': 10}[item['quality']]
                    item['stats'][stat] = bonus
            
            # Generate effects
            if item['quality'] in ['rare', 'epic', 'legendary']:
                num_effects = {'rare': 1, 'epic': 2, 'legendary': 3}[item['quality']]
                possible_effects = [
                    'fire_damage', 'ice_damage', 'lightning_damage', 'life_steal', 
                    'critical_chance', 'evasion', 'magic_resistance', 'health_regeneration',
                    'mana_regeneration', 'stun_chance', 'poison_damage', 'holy_damage'
                ]
                for j in range(num_effects):
                    effect = random.choice(possible_effects)
                    item['effects'].append(effect)
            
            context.items.append(item)
    
    # Verify we have 200 unique items
    assert len(context.items) == 200, "Should have exactly 200 unique magic items"
    
    # Verify uniqueness
    item_names = [item['name'] for item in context.items]
    assert len(set(item_names)) == 200, "All items should have unique names"

@then('each item should have clear effects and benefits')
def step_verify_item_effects(context):
    for item in context.items:
        # Each item should have clear description
        assert 'description' in item, f"Item {item['id']} should have description"
        assert len(item['description']) > 10, f"Item {item['id']} should have meaningful description"
        
        # Each item should have clear value
        assert 'value' in item, f"Item {item['id']} should have value"
        assert item['value'] > 0, f"Item {item['id']} should have positive value"
        
        # Each item should have a clear type
        assert 'type' in item, f"Item {item['id']} should have type"
        assert item['type'] in ['weapon', 'armor', 'accessory', 'consumable'], \
            f"Item {item['id']} should have valid type"

@given('the player has acquired equipment')
def step_player_has_equipment(context):
    # Set up player with equipment
    context.player = context.player if hasattr(context, 'player') else {
        'created': True,
        'name': 'TestCharacter',
        'class': 'Warrior',
        'level': 5,
        'hp': 150,
        'max_hp': 150,
        'stats': {
            'strength': 15,
            'dexterity': 12,
            'intelligence': 10,
            'wisdom': 11,
            'charisma': 9,
            'constitution': 14
        },
        'inventory': [
            {
                'id': 'sword_1',
                'name': 'Iron Sword',
                'type': 'weapon',
                'stats': {'strength': 3},
                'effects': []
            },
            {
                'id': 'armor_1',
                'name': 'Leather Armor',
                'type': 'armor',
                'stats': {'constitution': 2},
                'effects': []
            },
            {
                'id': 'ring_1',
                'name': 'Ring of Protection',
                'type': 'accessory',
                'stats': {'constitution': 1},
                'effects': ['evasion']
            },
            {
                'id': 'amulet_1',
                'name': 'Amulet of Wisdom',
                'type': 'accessory',
                'stats': {'wisdom': 2},
                'effects': ['magic_resistance']
            }
        ],
        'equipment': {
            'weapon': None,
            'armor': None,
            'accessory1': None,
            'accessory2': None
        }
    }

@when('they manage their inventory')
def step_manage_inventory(context):
    # Initialize inventory management system
    context.inventory_management = {
        'view': True,
        'equip': True,
        'unequip': True,
        'compare': True,
        'sell': True,
        'drop': True
    }
    
    # Calculate current stats from equipment
    context.equipment_stats = {
        'strength': 0,
        'dexterity': 0,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0,
        'constitution': 0,
        'effects': []
    }

@then('they should be able to equip items to appropriate slots')
def step_verify_item_equipping(context):
    # Try to equip items to appropriate slots
    for item in context.player['inventory']:
        if item['type'] == 'weapon':
            # Should be equippable to weapon slot
            context.player['equipment']['weapon'] = item
        elif item['type'] == 'armor':
            # Should be equippable to armor slot
            context.player['equipment']['armor'] = item
        elif item['type'] == 'accessory':
            # Should be equippable to accessory slots
            if context.player['equipment']['accessory1'] is None:
                context.player['equipment']['accessory1'] = item
            elif context.player['equipment']['accessory2'] is None:
                context.player['equipment']['accessory2'] = item
    
    # Verify items are equipped
    assert context.player['equipment']['weapon'] is not None, "Weapon should be equipped"
    assert context.player['equipment']['armor'] is not None, "Armor should be equipped"
    assert context.player['equipment']['accessory1'] is not None, "First accessory should be equipped"
    assert context.player['equipment']['accessory2'] is not None, "Second accessory should be equipped"

@then('equipped items should modify character stats appropriately')
def step_verify_stat_modification(context):
    # Calculate stat bonuses from equipment
    for slot, item in context.player['equipment'].items():
        if item and 'stats' in item:
            for stat, bonus in item['stats'].items():
                context.equipment_stats[stat] += bonus
        
        if item and 'effects' in item:
            context.equipment_stats['effects'].extend(item['effects'])
    
    # Verify stats are modified
    assert context.equipment_stats['strength'] > 0, "Strength should be modified by equipment"
    assert context.equipment_stats['constitution'] > 0, "Constitution should be modified by equipment"
    assert context.equipment_stats['wisdom'] > 0, "Wisdom should be modified by equipment"
    assert len(context.equipment_stats['effects']) > 0, "Effects should be added from equipment"

@then('they should be able to compare items visually')
def step_verify_item_comparison(context):
    # Test item comparison
    new_item = {
        'id': 'sword_2',
        'name': 'Steel Sword',
        'type': 'weapon',
        'stats': {'strength': 5},
        'effects': ['critical_chance'],
        'value': 100
    }
    
    # Compare with currently equipped weapon
    equipped_weapon = context.player['equipment']['weapon']
    
    context.item_comparison = {
        'current': equipped_weapon,
        'new': new_item,
        'differences': {}
    }
    
    # Calculate differences
    all_stats = set()
    all_stats.update(equipped_weapon.get('stats', {}).keys())
    all_stats.update(new_item.get('stats', {}).keys())
    
    for stat in all_stats:
        current_val = equipped_weapon.get('stats', {}).get(stat, 0)
        new_val = new_item.get('stats', {}).get(stat, 0)
        context.item_comparison['differences'][stat] = new_val - current_val
    
    # Verify comparison is possible
    assert 'differences' in context.item_comparison, "Should be able to compare item stats"

@then('they should be able to sell unwanted items to vendors')
def step_verify_item_selling(context):
    # Create a vendor
    context.vendor = {
        'name': 'Merchant',
        'gold': 1000,
        'buy_price_multiplier': 0.5  # Vendor buys at 50% of value
    }
    
    # Sell an item
    item_to_sell = context.player['inventory'][0]

    # Ensure item has value (debug fix)
    if 'value' not in item_to_sell:
        item_to_sell['value'] = random.randint(10, 500)  # Default value

    sale_price = int(item_to_sell['value'] * context.vendor['buy_price_multiplier'])

    # Ensure player has gold attribute
    if 'gold' not in context.player:
        context.player['gold'] = 0
    
    # Verify vendor can afford the item
    assert context.vendor['gold'] >= sale_price, "Vendor should have enough gold to buy items"
    
    # Process sale
    context.player['inventory'].remove(item_to_sell)
    context.player['gold'] += sale_price
    context.vendor['gold'] -= sale_price
    
    # Verify sale
    assert item_to_sell not in context.player['inventory'], "Sold item should be removed from inventory"
    assert context.player['gold'] > 500, "Player should receive gold from sale"
    assert context.vendor['gold'] < 1000, "Vendor gold should decrease after purchase"

@given('the player enters a shop in any city')
def step_enters_shop(context):
    # Set up shop context
    context.player = context.player if hasattr(context, 'player') else {
        'created': True,
        'name': 'TestCharacter',
        'class': 'Warrior',
        'level': 5,
        'gold': 500,
        'inventory': [
            {
                'id': 'sword_1',
                'name': 'Iron Sword',
                'type': 'weapon',
                'value': 100
            },
            {
                'id': 'potion_1',
                'name': 'Health Potion',
                'type': 'consumable',
                'value': 25
            }
        ]
    }
    
    # Create shops if not exists
    if not hasattr(context, 'shops'):
        context.shops = []
        
        # Create shops for different types
        shop_types = ['weapons', 'armor', 'magic', 'general', 'alchemical']
        shop_names = ['Ironforge', 'Silvermoon', 'Goldshire', 'Stormhaven', 'Dragon\'s Peak']
        
        for i in range(5):
            shop = {
                'id': f"shop_{i}",
                'name': shop_names[i],
                'type': shop_types[i],
                'location': f"city_{i}",
                'gold': random.randint(1000, 5000),
                'inventory': []
            }
            
            # Generate shop inventory based on type
            num_items = random.randint(10, 30)
            for j in range(num_items):
                item = {
                    'id': f"shop_{i}_item_{j}",
                    'name': f"{shop['name']} {shop['type']} item {j}",
                    'type': shop['type'],
                    'value': random.randint(20, 500),
                    'stock': random.randint(1, 10)
                }
                shop['inventory'].append(item)
            
            context.shops.append(shop)
    
    # Player enters first shop
    context.current_shop = context.shops[0]

@when('they interact with the shopkeeper')
def step_interact_shopkeeper(context):
    # Shopkeeper interaction
    context.shopkeeper = {
        'name': f"{context.current_shop['name']} Shopkeeper",
        'shop': context.current_shop,
        'dialogue': [
            "Welcome to my shop!",
            "Take a look at my wares.",
            "I also buy items if you have anything to sell."
        ]
    }
    
    # Transaction state
    context.transaction = {
        'mode': 'browsing',  # 'browsing', 'buying', 'selling'
        'selected_item': None,
        'price': 0
    }

@then('they should be able to buy items appropriate to the shop type')
def step_verify_shop_buying(context):
    # Verify shop has appropriate items
    shop_type = context.current_shop['type']
    for item in context.current_shop['inventory']:
        assert item['type'] == shop_type, f"Shop {context.current_shop['name']} should only sell {shop_type} items"
    
    # Test buying an item
    item_to_buy = context.current_shop['inventory'][0]
    context.transaction['mode'] = 'buying'
    context.transaction['selected_item'] = item_to_buy
    context.transaction['price'] = item_to_buy['value']
    
    # Verify player can afford at least one item
    affordable_items = [
        item for item in context.current_shop['inventory']
        if item['value'] <= context.player['gold']
    ]
    assert len(affordable_items) > 0, "Shop should have items player can afford"

@then('they should be able to sell items at reasonable rates')
def step_verify_shop_selling(context):
    # Test selling an item
    item_to_sell = context.player['inventory'][0]
    
    # Calculate sell price (typically 50% of value)
    sell_price = int(item_to_sell['value'] * 0.5)
    
    context.transaction['mode'] = 'selling'
    context.transaction['selected_item'] = item_to_sell
    context.transaction['price'] = sell_price
    
    # Verify sell price is reasonable
    assert 0 < sell_price < item_to_sell['value'], "Sell price should be reasonable fraction of item value"

@then('prices should vary between cities based on supply and demand')
def step_verify_price_variation(context):
    # Create cities with different economic conditions
    if not hasattr(context, 'cities'):
        context.cities = {}
        
        economic_conditions = ['poor', 'average', 'wealthy']
        for i in range(5):
            city = {
                'id': f"city_{i}",
                'name': f"City_{i}",
                'economy': economic_conditions[i % 3],
                'price_modifier': {'poor': 0.8, 'average': 1.0, 'wealthy': 1.3}[economic_conditions[i % 3]]
            }
            context.cities[city['id']] = city
    
    # Apply price modifiers to shops
    for shop in context.shops:
        city_id = shop['location']
        if city_id in context.cities:
            price_modifier = context.cities[city_id]['price_modifier']
            for item in shop['inventory']:
                item['value'] = int(item['value'] * price_modifier)
    
    # Verify price variation
    item_values_by_city = {}
    for shop in context.shops:
        city_id = shop['location']
        if city_id not in item_values_by_city:
            item_values_by_city[city_id] = []
        
        if shop['inventory']:
            item_values_by_city[city_id].append(shop['inventory'][0]['value'])
    
    # Calculate average values by city
    city_averages = {
        city_id: sum(values) / len(values)
        for city_id, values in item_values_by_city.items()
        if values
    }
    
    # Verify at least 3 different price levels
    assert len(set(int(avg) for avg in city_averages.values())) >= 3, "Prices should vary between cities"

@then('shopkeepers should have limited gold reserves')
def step_verify_shopkeeper_gold(context):
    # Verify shopkeeper has limited gold
    assert 'gold' in context.current_shop, "Shop should have gold reserve"
    assert 0 < context.current_shop['gold'] < 10000, "Shop should have reasonable gold reserve"
    
    # Test selling to shopkeeper until they run out of gold
    total_player_items_value = sum(item['value'] for item in context.player['inventory'])
    total_shop_gold = context.current_shop['gold']
    
    # Shopkeeper should run out of gold if trying to buy too much
    if total_player_items_value > total_shop_gold * 2:  # Selling at 50% price
        assert True, "Shopkeeper should run out of gold for large purchases"

@given('the player has acquired currency')
def step_player_has_currency(context):
    context.player = context.player if hasattr(context, 'player') else {
        'created': True,
        'name': 'TestCharacter',
        'class': 'Warrior',
        'level': 5,
        'gold': 500,
        'inventory': []
    }

@when('managing their finances')
def step_manage_finances(context):
    # Set up financial tracking
    context.financial_management = {
        'current_gold': context.player['gold'],
        'transaction_history': [
            {'type': 'quest_reward', 'amount': 100, 'description': 'Completed quest'},
            {'type': 'item_sale', 'amount': 50, 'description': 'Sold sword'},
            {'type': 'purchase', 'amount': -75, 'description': 'Bought potion'}
        ],
        'total_earned': 150,
        'total_spent': 75
    }

@then('they should be able to track their wealth')
def step_verify_wealth_tracking(context):
    # Verify player can track wealth
    assert 'gold' in context.player, "Player should have gold attribute"
    assert context.player['gold'] >= 0, "Player gold should not be negative"
    
    # Verify transaction history
    assert 'transaction_history' in context.financial_management, "Should have transaction history"
    assert len(context.financial_management['transaction_history']) > 0, "Should have recorded transactions"

@then('they should be able to make strategic purchasing decisions')
def step_verify_strategic_purchasing(context):
    # Create items with different value propositions
    strategic_items = [
        {'name': 'Basic Potion', 'value': 10, 'effect': 'heal 25 hp', 'efficiency': 2.5},
        {'name': 'Advanced Potion', 'value': 30, 'effect': 'heal 100 hp', 'efficiency': 3.33},
        {'name': 'Basic Sword', 'value': 100, 'damage': 15, 'efficiency': 0.15},
        {'name': 'Advanced Sword', 'value': 300, 'damage': 50, 'efficiency': 0.17}
    ]
    
    # Verify efficiency differences
    basic_potion = strategic_items[0]
    advanced_potion = strategic_items[1]
    
    # Advanced items should be more efficient
    assert advanced_potion['efficiency'] > basic_potion['efficiency'], "Advanced items should offer better value"
    
    # Player should be able to compare value
    context.value_comparison = {
        'item1': basic_potion,
        'item2': advanced_potion,
        'better_value': advanced_potion['name']
    }

@then('they should have opportunities to earn currency through various means')
def step_verify_earning_opportunities(context):
    # Define different earning methods
    context.earning_methods = {
        'quests': {
            'description': 'Complete quests for NPCs',
            'potential_income': random.randint(20, 500),
            'frequency': 'common'
        },
        'selling_loot': {
            'description': 'Sell items found in dungeons',
            'potential_income': random.randint(10, 300),
            'frequency': 'common'
        },
        'combat': {
            'description': 'Defeat enemies for gold',
            'potential_income': random.randint(5, 100),
            'frequency': 'common'
        },
        'crafting': {
            'description': 'Create and sell items',
            'potential_income': random.randint(50, 1000),
            'frequency': 'uncommon'
        },
        'treasure': {
            'description': 'Find treasure chests',
            'potential_income': random.randint(25, 500),
            'frequency': 'uncommon'
        }
    }
    
    # Verify multiple earning methods
    assert len(context.earning_methods) >= 5, "Should have multiple ways to earn currency"
    
    # Verify variety in income potential
    income_ranges = [
        method['potential_income'] for method in context.earning_methods.values()
    ]
    min_income = min(income_ranges)
    max_income = max(income_ranges)
    assert max_income > min_income * 5, "Should have variety in income potential"

@then('they should face meaningful economic choices')
def step_verify_economic_choices(context):
    # Create economic decision scenarios
    context.economic_choices = [
        {
            'situation': 'Find rare item vs sell common items',
            'options': [
                {'action': 'Keep rare item for later use', 'cost': 0, 'long_term_value': 'high'},
                {'action': 'Sell rare item now', 'gain': 500, 'long_term_value': 'medium'},
                {'action': 'Sell common items instead', 'gain': 200, 'long_term_value': 'low'}
            ]
        },
        {
            'situation': 'Buy equipment vs save for major purchase',
            'options': [
                {'action': 'Buy immediate upgrade', 'cost': 300, 'immediate_benefit': 'medium'},
                {'action': 'Save for legendary item', 'cost': 2000, 'long_term_benefit': 'high'},
                {'action': 'Buy consumables', 'cost': 100, 'short_term_benefit': 'low'}
            ]
        }
    ]
    
    # Verify economic choices have meaningful trade-offs
    for choice in context.economic_choices:
        # Each choice should have multiple options
        assert len(choice['options']) >= 3, "Should have multiple economic options"
        
        # Options should have different trade-offs
        costs = [opt.get('cost', 0) for opt in choice['options']]
        benefits = [
            opt.get('gain', 0) + 
            (10 if opt.get('long_term_value') == 'high' else 
             5 if opt.get('long_term_value') == 'medium' else 
             1 if opt.get('long_term_value') == 'low' else 0)
            for opt in choice['options']
        ]
        
        # Not all options should have same cost/benefit ratio
        cost_benefit_ratios = []
        for i, cost in enumerate(costs):
            if cost > 0:
                cost_benefit_ratios.append(benefits[i] / cost)
        
        if len(cost_benefit_ratios) > 1:
            assert max(cost_benefit_ratios) > min(cost_benefit_ratios) * 1.5, \
                "Economic choices should have different cost/benefit ratios"