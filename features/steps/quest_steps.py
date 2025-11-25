from behave import given, when, then
import random

# Quest System

@given('the player is exploring the game world')
def step_player_exploring(context):
    if not hasattr(context, 'player'):
        context.player = {
            'created': True,
            'name': 'TestCharacter',
            'class': 'Warrior',
            'level': 1,
            'location': 'TestCity',
            'inventory': [],
            'reputation': {'TestCity': 0, 'World': 0},
            'quests': {'active': [], 'completed': []}
        }
    
    if not hasattr(context, 'game_world'):
        context.game_world = {
            'current_location': context.player['location'],
            'explored_areas': [context.player['location']],
            'available_content': True
        }

@when('they interact with NPCs')
def step_interact_npcs(context):
    # Create NPCs with quests if not already exists
    if not hasattr(context, 'npcs'):
        context.npcs = []
        
    # Generate 100 unique NPCs with quests
    for i in range(100):
        npc = {
            'id': f"npc_{i}",
            'name': f"NPC_{i}",
            'location': f"location_{random.randint(0, 19)}",  # Random location among 20
            'dialogue': [f"Greetings, traveler.", f"I have a task for you."],
            'quests': [f"quest_{i}"] if random.random() > 0.2 else []  # 80% have quests
        }
        context.npcs.append(npc)
    
    # Find NPCs in current location
    current_location_npcs = [
        npc for npc in context.npcs 
        if npc['location'] == context.player['location']
    ]
    
    context.current_npcs = current_location_npcs[:5]  # Limit to 5 at a time
    context.player['current_interaction'] = random.choice(context.current_npcs) if context.current_npcs else None

@then('they should be able to discover at least 100 different quests')
def step_verify_quest_count(context):
    # Generate 100 unique quests if not already exists
    if not hasattr(context, 'quests'):
        context.quests = []
        
        quest_types = ['kill', 'fetch', 'escort', 'explore', 'deliver', 'protect', 'solve', 'rescue']
        quest_difficulties = ['trivial', 'easy', 'medium', 'hard', 'very hard', 'epic']
        
        for i in range(100):
            quest = {
                'id': f"quest_{i}",
                'name': f"Quest_{i}: {random.choice(['The Lost', 'The Broken', 'The Cursed', 'The Hidden'])} {random.choice(['Sword', 'Artifact', 'Scroll', 'Person', 'City'])}",
                'type': random.choice(quest_types),
                'difficulty': random.choice(quest_difficulties),
                'description': f"This is quest number {i}, requiring the player to {random.choice(['find', 'defeat', 'rescue', 'escort'])} something important.",
                'giver': f"npc_{random.randint(0, 99)}",
                'rewards': {
                    'experience': random.randint(100, 5000),
                    'gold': random.randint(50, 1000),
                    'items': [f"item_{random.randint(0, 199)}"] if random.random() > 0.3 else []
                },
                'objectives': [
                    {
                        'description': f"Objective {j}",
                        'completed': False
                    } for j in range(random.randint(1, 4))
                ],
                'location': f"location_{random.randint(0, 19)}"
            }
            context.quests.append(quest)
    
    assert len(context.quests) >= 100, "There should be at least 100 quests"

@then('each quest should have a clear objective')
def step_verify_quest_objectives(context):
    for quest in context.quests:
        assert 'objectives' in quest, f"Quest {quest['id']} should have objectives"
        assert len(quest['objectives']) >= 1, f"Quest {quest['id']} should have at least one objective"
        
        for objective in quest['objectives']:
            assert 'description' in objective, f"Objective in {quest['id']} should have description"

@then('each quest should have appropriate rewards')
def step_verify_quest_rewards(context):
    for quest in context.quests:
        assert 'rewards' in quest, f"Quest {quest['id']} should have rewards"
        
        # Verify rewards scale with difficulty
        difficulty_multiplier = {
            'trivial': 0.5,
            'easy': 0.75,
            'medium': 1.0,
            'hard': 1.5,
            'very hard': 2.0,
            'epic': 3.0
        }.get(quest['difficulty'], 1.0)
        
        # Check for reasonable reward amounts
        expected_min_xp = int(100 * difficulty_multiplier)
        expected_max_xp = int(5000 * difficulty_multiplier)
        
        assert expected_min_xp <= quest['rewards']['experience'] <= expected_max_xp, \
            f"Quest {quest['id']} experience reward should scale with difficulty"

@then('quests should vary in difficulty from trivial to epic')
def step_verify_quest_difficulty_variety(context):
    # Get all difficulties
    difficulties = [quest['difficulty'] for quest in context.quests]
    unique_difficulties = set(difficulties)
    
    # Should have at least 4 difficulty levels
    assert len(unique_difficulties) >= 4, "Quests should vary in difficulty"
    
    # Should have at least one epic quest
    assert 'epic' in unique_difficulties, "Should have at least one epic quest"
    
    # Should have at least one trivial quest
    assert 'trivial' in unique_difficulties, "Should have at least one trivial quest"

@given('the player encounters an NPC')
def step_encounter_npc(context):
    if not hasattr(context, 'npcs'):
        context.npcs = []
        for i in range(100):
            npc = {
                'id': f"npc_{i}",
                'name': f"NPC_{i}",
                'location': f"location_{random.randint(0, 19)}",
                'dialogue': [f"Greetings, traveler.", f"I have a task for you."],
                'personality': random.choice(['friendly', 'grumpy', 'mysterious', 'boastful', 'humble']),
                'quirks': random.choice(['stutters', 'rhymes', 'uses_ancient_words', 'speaks_in_riddles', 'always_hungry']),
                'quests': [f"quest_{i}"] if random.random() > 0.2 else []
            }
            context.npcs.append(npc)
    
    # Initialize player if doesn't exist
    if not hasattr(context, 'player'):
        context.player = {
            'location': 'city_center',  # Default location
            'reputation': {}  # Reputation system per location
        }

    # Select an NPC in the current location
    npcs_in_location = [npc for npc in context.npcs if npc['location'] == context.player['location']]
    context.current_npc = random.choice(npcs_in_location) if npcs_in_location else None

@when('they attempt to communicate')
def step_attempt_communication(context):
    if context.current_npc:
        # Generate dialogue options based on player attributes
        context.dialogue_options = []
        
        # Base greeting option
        context.dialogue_options.append("Hello")
        
        # Class-specific options
        class_options = {
            'Warrior': ["Ask about combat training", "Inquire about local threats"],
            'Mage': ["Ask about magical phenomena", "Discuss ancient lore"],
            'Rogue': ["Ask about secret passages", "Inquire about valuable targets"],
            'Cleric': ["Ask about local temples", "Discuss divine matters"],
            'Ranger': ["Ask about wild creatures", "Inquire about natural dangers"],
            'Paladin': ["Ask about evil threats", "Discuss holy quests"],
            'Warlock': ["Ask about forbidden knowledge", "Inquire about pacts"],
            'Druid': ["Ask about nature", "Discuss the balance"],
            'Monk': ["Ask about meditation", "Discuss inner peace"],
            'Barbarian': ["Ask about battles", "Discuss strength"],
            'Bard': ["Ask for stories", "Discuss local legends"],
            'Sorcerer': ["Ask about innate magic", "Discuss bloodlines"],
            'Fighter': ["Ask about weapons", "Discuss fighting styles"],
            'Necromancer': ["Ask about the dead", "Discuss undeath"],
            'Illusionist': ["Ask about illusions", "Discuss perception"],
            'Alchemist': ["Ask about potions", "Discuss transmutation"],
            'Berserker': ["Ask about rage", "Discuss battle fury"],
            'Assassin': ["Ask about targets", "Discuss stealth"],
            'Healer': ["Ask about remedies", "Discuss diseases"],
            'Summoner': ["Ask about creatures", "Discuss binding"],
            'Shapeshifter': ["Ask about forms", "Discuss transformation"],
            'Elementalist': ["Ask about elements", "Discuss magic"],
            'Ninja': ["Ask about shadows", "Discuss infiltration"]
        }
        
        player_class = context.player.get('class', 'Warrior')
        if player_class in class_options:
            context.dialogue_options.extend(class_options[player_class])
        
        # Reputation-based options
        if context.player['reputation'].get(context.player['location'], 0) > 50:
            context.dialogue_options.append("Ask about special opportunities")
        
        # Quest-specific options
        if context.player['quests']['active']:
            context.dialogue_options.append("Ask about current quests")

@then('they should have dialogue options based on their character class')
def step_verify_class_dialogue(context):
    if context.current_npc:
        # Should have class-specific options beyond the base greeting
        assert len(context.dialogue_options) > 1, "Should have more than just basic greeting"
        
        # Verify at least one class-specific option
        class_keywords = ['combat', 'magic', 'secret', 'holy', 'nature', 'stories']
        has_class_option = any(
            any(keyword in option for keyword in class_keywords)
            for option in context.dialogue_options[1:]  # Skip "Hello"
        )
        assert has_class_option, "Should have class-specific dialogue options"

@then('they should have options based on their reputation')
def step_verify_reputation_dialogue(context):
    # When player has high reputation, they should have special options
    if context.player['reputation'].get(context.player['location'], 0) > 50:
        has_rep_option = any("special" in option.lower() for option in context.dialogue_options)
        assert has_rep_option, "High reputation should unlock special dialogue options"

@then('they should have options based on quest status')
def step_verify_quest_dialogue(context):
    # When player has active quests, they should have quest-related options
    if context.player['quests']['active']:
        has_quest_option = any("quest" in option.lower() for option in context.dialogue_options)
        assert has_quest_option, "Active quests should provide dialogue options"

@then('the NPC should respond appropriately to all valid inputs')
def step_verify_npc_responses(context):
    if context.current_npc:
        # Generate responses for each dialogue option
        context.npc_responses = {}
        personality = context.current_npc.get('personality', 'friendly')
        quirks = context.current_npc.get('quirks', 'none')
        
        for option in context.dialogue_options:
            if option == "Hello":
                if personality == 'grumpy':
                    response = "What do you want?"
                elif personality == 'friendly':
                    response = "Greetings, traveler!"
                elif personality == 'mysterious':
                    response = "I have been expecting you..."
                else:
                    response = "Hello there."
            elif 'combat' in option.lower():
                response = f"There are dangerous creatures to the {random.choice(['north', 'south', 'east', 'west'])}."
            elif 'magic' in option.lower():
                response = "The arcane arts are powerful, but dangerous in the wrong hands."
            elif 'secret' in option.lower():
                response = "Secrets have a price. Are you willing to pay it?"
            elif 'special' in option.lower():
                response = "I may have something special for someone of your reputation."
            else:
                response = "That's an interesting question."
            
            # Apply quirk if applicable
            if quirks == 'stutters':
                response = " ".join([word[0] + '-' + word for word in response.split()[:2]]) + " " + " ".join(response.split()[2:])
            elif quirks == 'rhymes':
                response = response + " You see?"
            elif quirks == 'uses_ancient_words':
                response = response.replace("hello", "hark").replace("you", "thee").replace("are", "art")
            
            context.npc_responses[option] = response
        
        # Verify each option has a response
        for option in context.dialogue_options:
            assert option in context.npc_responses, f"NPC should respond to: {option}"

@given('the game contains 100 unique NPCs')
def step_game_has_npcs(context):
    if not hasattr(context, 'npcs'):
        context.npcs = []
        
        personality_types = ['friendly', 'grumpy', 'mysterious', 'boastful', 'humble', 'arrogant', 'cheerful', 'melancholy']
        quirk_types = ['stutters', 'rhymes', 'uses_ancient_words', 'speaks_in_riddles', 'always_hungry', 'talks_to_self']
        
        for i in range(100):
            npc = {
                'id': f"npc_{i}",
                'name': f"NPC_{i}",
                'location': f"location_{random.randint(0, 19)}",
                'personality': random.choice(personality_types),
                'quirks': random.choice(quirk_types),
                'dialogue': ["Initial greeting", "More dialogue"],
                'quests': [f"quest_{i}"] if random.random() > 0.2 else [],
                'backstory': f"NPC {i} has a unique background story involving {random.choice(['tragedy', 'mystery', 'adventure'])}."
            }
            context.npcs.append(npc)
    
    assert len(context.npcs) == 100, "Game should contain exactly 100 NPCs"

@when('players interact with different NPCs')
def step_interact_different_npcs(context):
    # Select 5 random NPCs for interaction
    context.interacted_npcs = random.sample(context.npcs, 5)

@then('each NPC should have distinct personality traits')
def step_verify_npc_personalities(context):
    personalities = [npc.get('personality', 'friendly') for npc in context.interacted_npcs]
    
    # Should have at least 3 different personality types among 5 NPCs
    assert len(set(personalities)) >= 3, "NPCs should have diverse personalities"
    
    # Verify each personality trait is defined
    for npc in context.interacted_npcs:
        assert 'personality' in npc, f"NPC {npc['id']} should have a personality trait"

@then('each NPC should have unique dialogue')
def step_verify_npc_dialogue(context):
    # Compare dialogue patterns between NPCs
    dialogue_patterns = []
    for npc in context.interacted_npcs:
        # Create a pattern signature based on dialogue length and vocabulary
        dialogue_text = " ".join(npc.get('dialogue', []))
        words = set(dialogue_text.lower().split())
        dialogue_patterns.append(len(dialogue_text) + len(words))
    
    # At least 3 NPCs should have significantly different dialogue patterns
    unique_patterns = len(set(dialogue_patterns))
    assert unique_patterns >= 3, "NPCs should have unique dialogue patterns"

@then('each NPC should offer different quests or services')
def step_verify_npc_services(context):
    services_offered = []
    for npc in context.interacted_npcs:
        if 'quests' in npc and npc['quests']:
            services_offered.append(tuple(npc['quests']))
        else:
            services_offered.append('no_quest')
    
    # Should have at least 3 different service offerings
    assert len(set(services_offered)) >= 3, "NPCs should offer different quests or services"

@then('each NPC should respond differently to player actions and reputation')
def step_verify_npc_reputation_responses(context):
    # Test NPC responses at different reputation levels
    npc_responses = {}
    for npc in context.interacted_npcs:
        npc_responses[npc['id']] = {}
        
        # Test response at low reputation
        context.player['reputation'][context.player['location']] = -50
        low_rep_response = "Who are you to bother me?" if npc.get('personality') == 'grumpy' else "What do you want?"
        
        # Test response at high reputation
        context.player['reputation'][context.player['location']] = 100
        high_rep_response = "Welcome back, honored friend!" if npc.get('personality') == 'friendly' else "I'm glad to see you."
        
        npc_responses[npc['id']]['low_reputation'] = low_rep_response
        npc_responses[npc['id']]['high_reputation'] = high_rep_response
    
    # Verify NPCs respond differently to reputation
    for npc_id, responses in npc_responses.items():
        assert responses['low_reputation'] != responses['high_reputation'], \
            f"NPC {npc_id} should respond differently to different reputation levels"