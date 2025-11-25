# pytest configuration and shared fixtures
import pytest
import random
from unittest.mock import MagicMock

# Try to import hypothesis, but don't fail if not available
try:
    from hypothesis import given, strategies as st
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False
    # Create dummy functions if hypothesis not available
    def given(func):
        return func
    class strategies:
        @staticmethod
        def text(*args, **kwargs):
            return "test"
        @staticmethod
        def integers(*args, **kwargs):
            return 1
        @staticmethod
        def lists(*args, **kwargs):
            return []
        @staticmethod
        def fixed_dictionaries(*args, **kwargs):
            return {}
        @staticmethod
        def sampled_from(*args, **kwargs):
            return args[0][0] if args else "test"
    st = strategies

@pytest.fixture
def mock_player():
    """Returns a mock player object with default attributes"""
    player = MagicMock()
    player.created = True
    player.name = "TestCharacter"
    player.class_type = "Warrior"
    player.level = 5
    player.hp = 150
    player.max_hp = 150
    player.stats = {
        'strength': 15,
        'dexterity': 12,
        'intelligence': 10,
        'wisdom': 11,
        'charisma': 9,
        'constitution': 14
    }
    player.abilities = ['Attack', 'Defend', 'Power Strike', 'Heal']
    player.inventory = []
    player.equipment = {
        'weapon': None,
        'armor': None,
        'accessory1': None,
        'accessory2': None
    }
    player.gold = 500
    player.reputation = {'TestCity': 0, 'World': 0}
    player.quests = {'active': [], 'completed': []}
    return player

@pytest.fixture
def mock_enemy():
    """Returns a mock enemy object with default attributes"""
    enemy = MagicMock()
    enemy.id = "enemy_test"
    enemy.name = "TestEnemy"
    enemy.type = "humanoid"
    enemy.level = 5
    enemy.stats = {
        'strength': 12,
        'dexterity': 10,
        'intelligence': 8,
        'wisdom': 8,
        'charisma': 7,
        'constitution': 13
    }
    enemy.hp = 100
    enemy.max_hp = 100
    enemy.abilities = ["Slash", "Block", "Power Attack"]
    enemy.ai_behavior = "aggressive"
    enemy.weakness = "ice"
    enemy.resistance = "fire"
    return enemy

@pytest.fixture
def mock_item():
    """Returns a mock item object with default attributes"""
    item = MagicMock()
    item.id = "item_test"
    item.name = "Test Sword"
    item.type = "weapon"
    item.quality = "rare"
    item.stats = {"strength": 5, "damage": 10}
    item.effects = ["critical_chance"]
    item.value = 250
    item.description = "A finely crafted sword with magical properties"
    return item

@pytest.fixture
def mock_quest():
    """Returns a mock quest object with default attributes"""
    quest = MagicMock()
    quest.id = "quest_test"
    quest.name = "Test Quest: The Missing Artifact"
    quest.type = "fetch"
    quest.difficulty = "medium"
    quest.description = "Find the missing artifact and return it safely"
    quest.giver = "npc_test"
    quest.rewards = {
        'experience': 500,
        'gold': 200,
        'items': ["item_test"]
    }
    quest.objectives = [
        {"description": "Find the artifact", "completed": False},
        {"description": "Return to quest giver", "completed": False}
    ]
    quest.location = "city_1"
    return quest

@pytest.fixture
def mock_npc():
    """Returns a mock NPC object with default attributes"""
    npc = MagicMock()
    npc.id = "npc_test"
    npc.name = "Test NPC"
    npc.location = "city_1"
    npc.personality = "friendly"
    npc.quirks = "speaks_in_riddles"
    npc.dialogue = ["Greetings, traveler.", "I have a task for you."]
    npc.quests = ["quest_test"]
    npc.backstory = "Once a great warrior, now a wise mentor to young adventurers"
    return npc

@pytest.fixture
def mock_dungeon():
    """Returns a mock dungeon object with default attributes"""
    dungeon = MagicMock()
    dungeon.id = "dungeon_test"
    dungeon.name = "Test Dungeon: The Dark Caverns"
    dungeon.level = 5
    dungeon.theme = "dark"
    dungeon.layout = {
        'rooms': 15,
        'floors': 2,
        'secrets': 4
    }
    dungeon.enemies = ["enemy_1", "enemy_2", "enemy_3"]
    dungeon.boss = "boss_test"
    dungeon.puzzles = ["puzzle_1", "puzzle_2"]
    return dungeon

@pytest.fixture
def mock_shop():
    """Returns a mock shop object with default attributes"""
    shop = MagicMock()
    shop.id = "shop_test"
    shop.name = "Test Shop"
    shop.type = "weapons"
    shop.location = "city_1"
    shop.gold = 2000
    shop.inventory = [
        {
            'id': 'shop_item_1',
            'name': 'Iron Sword',
            'type': 'weapon',
            'value': 100,
            'stock': 5
        },
        {
            'id': 'shop_item_2',
            'name': 'Steel Sword',
            'type': 'weapon',
            'value': 250,
            'stock': 2
        }
    ]
    return shop

@pytest.fixture
def game_state():
    """Returns a minimal game state for testing"""
    state = {
        'player': {
            'created': False,
            'name': None,
            'class': None,
            'level': 1,
            'hp': 100,
            'max_hp': 100,
            'stats': {}
        },
        'world': {
            'current_location': 'starting_city',
            'visited_locations': [],
            'available_content': True
        },
        'combat': {
            'active': False,
            'participants': [],
            'turn_order': [],
            'current_turn': None,
            'round': 1
        }
    }
    return state

@pytest.fixture
def class_stats():
    """Returns a dictionary of default class stats"""
    return {
        'Warrior': {'strength': 15, 'dexterity': 10, 'intelligence': 8, 'wisdom': 9, 'charisma': 7, 'constitution': 14},
        'Mage': {'strength': 7, 'dexterity': 10, 'intelligence': 16, 'wisdom': 12, 'charisma': 8, 'constitution': 9},
        'Rogue': {'strength': 10, 'dexterity': 16, 'intelligence': 10, 'wisdom': 8, 'charisma': 12, 'constitution': 10},
        'Cleric': {'strength': 10, 'dexterity': 8, 'intelligence': 10, 'wisdom': 16, 'charisma': 12, 'constitution': 10},
        'Ranger': {'strength': 12, 'dexterity': 14, 'intelligence': 9, 'wisdom': 14, 'charisma': 8, 'constitution': 11},
        'Paladin': {'strength': 14, 'dexterity': 8, 'intelligence': 8, 'wisdom': 12, 'charisma': 14, 'constitution': 12},
        'Warlock': {'strength': 8, 'dexterity': 10, 'intelligence': 14, 'wisdom': 10, 'charisma': 16, 'constitution': 8},
        'Druid': {'strength': 10, 'dexterity': 12, 'intelligence': 12, 'wisdom': 14, 'charisma': 8, 'constitution': 12},
        'Monk': {'strength': 12, 'dexterity': 14, 'intelligence': 10, 'wisdom': 14, 'charisma': 8, 'constitution': 10},
        'Barbarian': {'strength': 16, 'dexterity': 10, 'intelligence': 7, 'wisdom': 8, 'charisma': 7, 'constitution': 15}
    }

# Hypothesis strategies
st_player_stats = st.fixed_dictionaries({
    'strength': st.integers(min_value=1, max_value=20),
    'dexterity': st.integers(min_value=1, max_value=20),
    'intelligence': st.integers(min_value=1, max_value=20),
    'wisdom': st.integers(min_value=1, max_value=20),
    'charisma': st.integers(min_value=1, max_value=20),
    'constitution': st.integers(min_value=1, max_value=20)
})

st_item_quality = st.sampled_from(['common', 'uncommon', 'rare', 'epic', 'legendary'])
st_item_type = st.sampled_from(['weapon', 'armor', 'accessory', 'consumable'])
st_difficulty = st.sampled_from(['trivial', 'easy', 'medium', 'hard', 'very hard', 'epic'])
st_ai_behavior = st.sampled_from(['aggressive', 'defensive', 'tactical', 'random'])
st_element_type = st.sampled_from(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical'])

# Helper functions
def create_test_player(class_type="Warrior", level=5):
    """Create a test player with the specified class and level"""
    player = MagicMock()
    player.created = True
    player.name = f"Test{class_type}"
    player.class_type = class_type
    player.level = level
    player.hp = 100 + (level * 10)
    player.max_hp = player.hp
    player.stats = {
        'strength': 10 + level,
        'dexterity': 10 + level // 2,
        'intelligence': 10 + level // 2,
        'wisdom': 10 + level // 2,
        'charisma': 10,
        'constitution': 10 + level
    }
    player.abilities = [f"Ability_{i}" for i in range(1, 5)]
    player.inventory = []
    player.equipment = {
        'weapon': None,
        'armor': None,
        'accessory1': None,
        'accessory2': None
    }
    player.gold = 100 * level
    player.reputation = {'TestCity': 0, 'World': 0}
    player.quests = {'active': [], 'completed': []}
    return player

def create_test_enemy(enemy_type="humanoid", level=5):
    """Create a test enemy with the specified type and level"""
    enemy = MagicMock()
    enemy.id = f"enemy_{enemy_type}_{level}"
    enemy.name = f"{enemy_type.title()} Level {level}"
    enemy.type = enemy_type
    enemy.level = level
    enemy.stats = {
        'strength': 5 + level,
        'dexterity': 5 + level,
        'intelligence': 5 + level,
        'wisdom': 5 + level,
        'charisma': 5 + level,
        'constitution': 5 + level
    }
    enemy.hp = 20 + (level * 20)
    enemy.max_hp = enemy.hp
    enemy.abilities = [f"Enemy_Ability_{i}" for i in range(1, 3)]
    enemy.ai_behavior = random.choice(['aggressive', 'defensive', 'tactical', 'random'])
    enemy.weakness = random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical'])
    enemy.resistance = random.choice(['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical', 'none'])
    return enemy

def calculate_class_balance(stats_dict):
    """Calculate balance metrics for class stats"""
    power_levels = {}
    
    for class_name, stats in stats_dict.items():
        # Calculate total power level
        power = sum(stats.values())
        power_levels[class_name] = power
    
    max_power = max(power_levels.values())
    min_power = min(power_levels.values())
    balance_ratio = (max_power - min_power) / min_power if min_power > 0 else float('inf')
    
    return {
        'power_levels': power_levels,
        'max_power': max_power,
        'min_power': min_power,
        'balance_ratio': balance_ratio,
        'is_balanced': balance_ratio <= 0.15
    }