"""
E2E Tests: Character Journey
Optimized for LLM agents with complete journey testing
"""

import pytest
import time
from core.models import (
    Character, CharacterClass, CharacterStats,
    Item, ItemRarity, ItemType,
    Enemy, EnemyType,
    Quest, QuestStatus, QuestObjective,
    GameState
)
from core.systems.character import (
    create_character,
    level_up_character,
    add_experience,
    heal_character,
    damage_character,
    learn_ability,
    equip_item,
    use_item,
    get_character_summary
)
from core.systems.game import (
    start_new_game,
    save_game,
    load_game
)


class TestCompleteCharacterLifecycle:
    """Test complete character lifecycle from creation to advanced play."""
    
    def test_warrior_complete_lifecycle(self):
        """Test complete warrior lifecycle from level 1 to 50."""
        start_time = time.time()
        
        # Phase 1: Character Creation
        character = create_character("WarriorHero", CharacterClass.WARRIOR)
        
        # Validate initial state
        assert character.name == "WarriorHero"
        assert character.class_type == CharacterClass.WARRIOR
        assert character.level == 1
        assert character.experience == 0
        assert character.gold == 100
        assert character.is_alive()
        assert len(character.abilities) >= 5
        assert character.stats.strength >= 12
        
        # Phase 2: Early Game Progression (Level 1-10)
        early_game_start = time.time()
        
        for level in range(2, 11):
            # Add sufficient experience
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            
            # Level up
            character = level_up_character(character)
            
            # Validate level up
            assert character.level == level
            assert character.hp == character.max_hp  # Full heal
            assert character.stats.strength >= 12 + (level - 1) * 2  # Stat growth
            
            # Add basic equipment at key levels
            if level % 3 == 0:
                weapon = self._create_weapon(f"Level {level} Sword", level)
                character.add_item_to_inventory(weapon)
        
        early_game_time = time.time() - early_game_start
        
        # Validate early game state
        assert character.level == 10
        assert character.stats.strength >= 30
        assert character.max_hp >= 120
        assert len(character.inventory) >= 3
        assert character.is_alive()
        
        # Phase 3: Mid Game Progression (Level 11-25)
        mid_game_start = time.time()
        
        for level in range(11, 26):
            # Add sufficient experience
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            
            # Level up
            character = level_up_character(character)
            
            # Validate progression
            assert character.level == level
            
            # Learn advanced abilities
            if level % 2 == 0:
                ability = f"Advanced Warrior Ability {level}"
                character.add_ability(ability)
            
            # Add better equipment
            if level % 4 == 0:
                weapon = self._create_weapon(f"Mid Game Sword {level}", level)
                armor = self._create_armor(f"Mid Game Armor {level}", level)
                character.add_item_to_inventory(weapon)
                character.add_item_to_inventory(armor)
        
        mid_game_time = time.time() - mid_game_start
        
        # Validate mid game state
        assert character.level == 25
        assert character.stats.strength >= 50  # Near max
        assert character.max_hp >= 200
        assert len(character.inventory) >= 8
        assert len(character.abilities) >= 10
        
        # Phase 4: Late Game Progression (Level 26-50)
        late_game_start = time.time()
        
        for level in range(26, 51):
            # Add sufficient experience
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            
            # Level up
            character = level_up_character(character)
            
            # Validate max level stats
            assert character.level == level
            assert character.stats.strength <= 20  # Capped at max
            
            # Add legendary equipment
            if level % 5 == 0:
                weapon = self._create_legendary_weapon(f"Legendary Sword {level}")
                armor = self._create_legendary_armor(f"Legendary Armor {level}")
                character.add_item_to_inventory(weapon)
                character.add_item_to_inventory(armor)
        
        late_game_time = time.time() - late_game_start
        
        # Phase 5: Final State Validation
        total_time = time.time() - start_time
        
        # Validate final character state
        assert character.level == 50
        assert character.stats.strength == 20  # Maxed
        assert character.stats.constitution == 20  # Maxed
        assert character.max_hp >= 400
        assert character.hp == character.max_hp  # Should be full from last level up
        assert len(character.inventory) >= 12
        assert len(character.abilities) >= 20
        assert character.gold >= 100
        assert character.is_alive()
        
        # Validate performance requirements
        assert total_time < 5.0, f"Warrior lifecycle took too long: {total_time}s"
        assert early_game_time < 1.0, f"Early game took too long: {early_game_time}s"
        assert mid_game_time < 2.0, f"Mid game took too long: {mid_game_time}s"
        assert late_game_time < 3.0, f"Late game took too long: {late_game_time}s"
        
        # Get final summary
        summary = get_character_summary(character)
        assert summary['level'] == 50
        assert summary['class'] == 'warrior'
        assert summary['is_alive'] == True
        assert summary['hp_percentage'] == 100.0
        assert summary['total_stats'] >= 100
    
    def test_mage_complete_lifecycle(self):
        """Test complete mage lifecycle from level 1 to 50."""
        start_time = time.time()
        
        # Create mage character
        character = create_character("MageHero", CharacterClass.MAGE)
        
        # Validate initial mage state
        assert character.stats.intelligence >= 12
        assert character.stats.intelligence > character.stats.strength
        assert character.max_hp < 50  # Lower HP than warrior
        assert "Fireball" in character.abilities
        
        # Progress through levels
        for level in range(2, 51):
            # Add experience and level up
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Validate mage-specific progression
            if level >= 10:
                assert character.stats.intelligence >= 20  # Maxed early
            
            # Add magical abilities
            if level % 2 == 0:
                magic_ability = f"Spell Level {level}"
                character.add_ability(magic_ability)
            
            # Add magical equipment
            if level % 3 == 0:
                staff = self._create_staff(f"Magic Staff {level}", level)
                character.add_item_to_inventory(staff)
        
        # Validate final mage state
        total_time = time.time() - start_time
        assert total_time < 5.0, f"Mage lifecycle took too long: {total_time}s"
        assert character.level == 50
        assert character.stats.intelligence == 20
        assert len(character.abilities) >= 25
        assert any("Spell" in ability for ability in character.abilities)
    
    def test_rogue_complete_lifecycle(self):
        """Test complete rogue lifecycle from level 1 to 50."""
        start_time = time.time()
        
        # Create rogue character
        character = create_character("RogueHero", CharacterClass.ROGUE)
        
        # Validate initial rogue state
        assert character.stats.dexterity >= 12
        assert character.stats.dexterity > character.stats.intelligence
        assert "Stealth" in character.abilities
        
        # Progress through levels
        for level in range(2, 51):
            # Add experience and level up
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Validate rogue-specific progression
            if level >= 15:
                assert character.stats.dexterity >= 20  # Maxed
            
            # Add stealth abilities
            if level % 2 == 0:
                stealth_ability = f"Stealth Move {level}"
                character.add_ability(stealth_ability)
            
            # Add rogue equipment
            if level % 3 == 0:
                daggers = self._create_daggers(f"Rogue Daggers {level}", level)
                character.add_item_to_inventory(daggers)
        
        # Validate final rogue state
        total_time = time.time() - start_time
        assert total_time < 5.0, f"Rogue lifecycle took too long: {total_time}s"
        assert character.level == 50
        assert character.stats.dexterity == 20
        assert len(character.abilities) >= 25
        assert any("Stealth" in ability for ability in character.abilities)
    
    def test_character_death_and_revival_cycle(self):
        """Test character death and revival cycle."""
        character = create_character("DeathTest", CharacterClass.WARRIOR)
        original_gold = character.gold
        
        # Kill character
        character.hp = 0
        assert character.is_defeated()
        assert not character.is_alive()
        
        # Apply death penalty
        death_penalty = original_gold // 2
        character.gold -= death_penalty
        assert character.gold == original_gold - death_penalty
        
        # Revive at temple
        character.hp = character.max_hp
        assert character.is_alive()
        assert not character.is_defeated()
        
        # Continue gameplay after revival
        character = add_experience(character, 100)
        character = level_up_character(character)
        assert character.level == 2
        assert character.is_alive()
    
    def test_character_save_load_throughout_journey(self):
        """Test character save/load throughout journey."""
        # Create character
        character = create_character("SaveTest", CharacterClass.PALADIN)
        
        # Create game state
        game_state = GameState(
            current_location="town",
            player=character,
            world_time=100,
            day=1
        )
        
        # Save at multiple points
        save_points = []
        for level in [5, 10, 15, 20]:
            # Progress to save point
            while character.level < level:
                exp_needed = self._get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            # Save game
            save_data = save_game(game_state)
            save_points.append({
                'level': level,
                'save_data': save_data,
                'character': character
            })
        
        # Validate each save point can be loaded
        for save_point in save_points:
            loaded_game_state = load_game(save_point['save_data'])
            assert loaded_game_state.player.level == save_point['level']
            assert loaded_game_state.player.name == character.name
            assert loaded_game_state.player.class_type == character.class_type
            assert loaded_game_state.player.is_alive()
        
        # Validate final state
        character = save_points[-1]['character']
        assert character.level == 20
        assert character.is_alive()


class TestCharacterClassComparisons:
    """Test all character classes through journey comparison."""
    
    def test_all_classes_journey_comparison(self):
        """Test journey comparison across all character classes."""
        start_time = time.time()
        
        # Test all classes
        classes_to_test = list(CharacterClass)
        class_results = {}
        
        for character_class in classes_to_test:
            class_start_time = time.time()
            
            # Create character
            character = create_character(f"Test{character_class.value.title()}", character_class)
            initial_stats = character.stats
            
            # Progress to level 10
            for level in range(2, 11):
                exp_needed = self._get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            # Get final stats
            final_stats = character.stats
            
            # Calculate class-specific metrics
            class_metrics = {
                'level': character.level,
                'hp': character.max_hp,
                'abilities': len(character.abilities),
                'primary_stat_growth': self._get_primary_stat_growth(initial_stats, final_stats, character_class),
                'time_taken': time.time() - class_start_time
            }
            
            class_results[character_class] = class_metrics
        
        total_time = time.time() - start_time
        
        # Validate all classes completed journey
        assert len(class_results) == len(CharacterClass)
        assert all(result['level'] == 10 for result in class_results.values())
        assert total_time < 30.0, f"All classes comparison took too long: {total_time}s"
        
        # Validate class-specific characteristics
        warrior_result = class_results[CharacterClass.WARRIOR]
        mage_result = class_results[CharacterClass.MAGE]
        rogue_result = class_results[CharacterClass.ROGUE]
        
        # Warrior should have highest HP
        assert warrior_result['hp'] > mage_result['hp']
        assert warrior_result['hp'] > rogue_result['hp']
        
        # Mage should have lower HP but more abilities
        assert mage_result['hp'] < warrior_result['hp']
        assert mage_result['abilities'] >= warrior_result['abilities']
        
        # Rogue should be balanced
        assert rogue_result['hp'] < warrior_result['hp']
        assert rogue_result['hp'] > mage_result['hp']
        
        # Validate performance requirements
        for character_class, result in class_results.items():
            assert result['time_taken'] < 3.0, f"{character_class.value} took too long: {result['time_taken']}s"
    
    def _get_primary_stat_growth(self, initial_stats, final_stats, character_class):
        """Get primary stat growth for character class."""
        primary_stats = {
            CharacterClass.WARRIOR: 'strength',
            CharacterClass.MAGE: 'intelligence',
            CharacterClass.ROGUE: 'dexterity',
            CharacterClass.CLERIC: 'wisdom',
            CharacterClass.BARD: 'charisma'
        }
        
        primary_stat = primary_stats.get(character_class, 'strength')
        initial_value = getattr(initial_stats, primary_stat)
        final_value = getattr(final_stats, primary_stat)
        
        return final_value - initial_value


class TestCharacterPerformanceJourney:
    """Test character performance throughout journey."""
    
    def test_character_performance_scaling(self):
        """Test character performance scaling throughout journey."""
        character = create_character("PerfTest", CharacterClass.WARRIOR)
        
        # Create test enemies at various levels
        enemies = [
            self._create_enemy("Goblin", 2),
            self._create_enemy("Orc", 5),
            self._create_enemy("Troll", 10),
            self._create_enemy("Dragon", 20),
            self._create_enemy("Demon Lord", 40)
        ]
        
        performance_metrics = []
        
        # Test combat at various character levels
        for level in [1, 5, 10, 20, 40]:
            # Progress to level
            while character.level < level:
                exp_needed = self._get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            # Test combat against appropriate enemy
            enemy_index = min(level // 10, len(enemies) - 1)
            enemy = enemies[enemy_index]
            
            # Simulate combat
            combat_start_time = time.time()
            player_damage = self._simulate_combat(character, enemy)
            combat_time = time.time() - combat_start_time
            
            # Calculate combat effectiveness
            combat_effectiveness = player_damage / enemy.max_hp
            
            performance_metrics.append({
                'character_level': character.level,
                'enemy_level': enemy.level,
                'damage_dealt': player_damage,
                'combat_time': combat_time,
                'combat_effectiveness': combat_effectiveness
            })
        
        # Validate performance scaling
        for i, metric in enumerate(performance_metrics):
            assert metric['combat_time'] < 0.1, f"Combat took too long at level {metric['character_level']}: {metric['combat_time']}s"
            assert metric['combat_effectiveness'] >= 0.1, f"Low combat effectiveness at level {metric['character_level']}: {metric['combat_effectiveness']}"
        
        # Validate scaling (higher levels should be more effective)
        assert performance_metrics[-1]['combat_effectiveness'] > performance_metrics[0]['combat_effectiveness']
    
    def test_character_memory_usage_journey(self):
        """Test character memory usage throughout journey."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create and progress character
        character = create_character("MemoryTest", CharacterClass.MAGE)
        
        # Progress through levels
        for level in range(2, 51):
            # Add experience
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Add items and abilities
            if level % 2 == 0:
                item = self._create_staff(f"Staff {level}", level)
                character.add_item_to_inventory(item)
            
            if level % 3 == 0:
                ability = f"Ability {level}"
                character.add_ability(ability)
            
            # Check memory usage every 10 levels
            if level % 10 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                memory_increase = current_memory - initial_memory
                
                # Memory usage should not increase dramatically
                assert memory_increase < 50, f"Memory usage too high at level {level}: {memory_increase} MB"
        
        # Final memory check
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        total_memory_increase = final_memory - initial_memory
        
        assert total_memory_increase < 100, f"Total memory increase too high: {total_memory_increase} MB"


class TestCharacterEdgeCasesJourney:
    """Test character edge cases throughout journey."""
    
    def test_character_stat_edge_cases_journey(self):
        """Test character stat edge cases throughout journey."""
        # Create character with minimum stats
        min_stats = CharacterStats(
            strength=1,
            dexterity=1,
            intelligence=1,
            wisdom=1,
            charisma=1,
            constitution=1
        )
        
        character = create_character("MinStats", CharacterClass.WARRIOR, min_stats)
        
        # Progress through levels
        for level in range(2, 51):
            exp_needed = self._get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Validate stats never go below minimum
            assert character.stats.strength >= 1
            assert character.stats.dexterity >= 1
            assert character.stats.intelligence >= 1
            assert character.stats.wisdom >= 1
            assert character.stats.charisma >= 1
            assert character.stats.constitution >= 1
            
            # Validate stats never exceed maximum
            assert character.stats.strength <= 20
            assert character.stats.dexterity <= 20
            assert character.stats.intelligence <= 20
            assert character.stats.wisdom <= 20
            assert character.stats.charisma <= 20
            assert character.stats.constitution <= 20
    
    def test_character_ability_edge_cases_journey(self):
        """Test character ability edge cases throughout journey."""
        character = create_character("AbilityTest", CharacterClass.BARD)
        
        # Track unique abilities
        unique_abilities = set()
        
        # Progress through levels
        for level in range(1, 51):
            # Add test abilities
            for i in range(3):  # Add 3 abilities per level
                ability = f"Test Ability {level}-{i}"
                character.add_ability(ability)
                unique_abilities.add(ability)
            
            # Level up every 5 levels
            if level > 1 and level % 5 == 0:
                exp_needed = self._get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            # Validate ability list integrity
            assert len(character.abilities) == len(set(character.abilities))  # No duplicates
            assert len(character.abilities) <= level * 3 + 10  # Reasonable upper bound
        
        # Validate final state
        assert len(character.abilities) >= 50  # Should have many abilities
        assert len(character.abilities) == len(unique_abilities)  # All unique
    
    def test_character_item_edge_cases_journey(self):
        """Test character item edge cases throughout journey."""
        character = create_character("ItemTest", CharacterClass.ROGUE)
        
        # Add various types of items
        for level in range(1, 51):
            # Add weapons
            weapon = self._create_weapon(f"Weapon {level}", level)
            character.add_item_to_inventory(weapon)
            
            # Add armor
            armor = self._create_armor(f"Armor {level}", level)
            character.add_item_to_inventory(armor)
            
            # Add consumables
            consumable = self._create_consumable(f"Potion {level}", level)
            character.add_item_to_inventory(consumable)
            
            # Validate inventory size
            assert len(character.inventory) <= 200  # Reasonable upper bound
        
        # Validate inventory integrity
        for item in character.inventory:
            assert item.id is not None
            assert item.name is not None
            assert item.value >= 0
        
        # Validate final inventory size
        assert len(character.inventory) >= 150  # Should have many items


# Helper methods for E2E testing
def _get_experience_for_level(self, level):
    """Get experience needed for level."""
    import math
    if level == 1:
        return 0
    if level <= 20:
        return 100 * (level - 1) ** 2
    else:
        return int(100 * math.pow(level - 1, 1.8))

def _create_weapon(self, name, level):
    """Create weapon for testing."""
    return Item(
        id=f"weapon_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.WEAPON,
        rarity=ItemRarity.RARE,
        value=100 * level,
        stats_mod={"damage": 5 * level, "strength": level},
        equippable=True
    )

def _create_armor(self, name, level):
    """Create armor for testing."""
    return Item(
        id=f"armor_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.ARMOR,
        rarity=ItemRarity.RARE,
        value=80 * level,
        stats_mod={"defense": 3 * level, "constitution": level},
        equippable=True
    )

def _create_legendary_weapon(self, name):
    """Create legendary weapon for testing."""
    return Item(
        id=f"legendary_weapon_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.WEAPON,
        rarity=ItemRarity.LEGENDARY,
        value=5000,
        stats_mod={"damage": 50, "strength": 5, "critical_chance": 20},
        equippable=True
    )

def _create_legendary_armor(self, name):
    """Create legendary armor for testing."""
    return Item(
        id=f"legendary_armor_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.ARMOR,
        rarity=ItemRarity.LEGENDARY,
        value=3000,
        stats_mod={"defense": 30, "constitution": 5, "magic_resistance": 25},
        equippable=True
    )

def _create_staff(self, name, level):
    """Create magical staff for testing."""
    return Item(
        id=f"staff_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.WEAPON,
        rarity=ItemRarity.RARE,
        value=120 * level,
        stats_mod={"spell_power": 6 * level, "intelligence": level},
        equippable=True
    )

def _create_daggers(self, name, level):
    """Create daggers for testing."""
    return Item(
        id=f"daggers_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        value=90 * level,
        stats_mod={"damage": 4 * level, "dexterity": level, "critical_chance": level},
        equippable=True
    )

def _create_consumable(self, name, level):
    """Create consumable item for testing."""
    return Item(
        id=f"consumable_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.CONSUMABLE,
        rarity=ItemRarity.COMMON,
        value=20 * level,
        consumable=True
    )

def _create_enemy(self, name, level):
    """Create enemy for testing."""
    return Enemy(
        id=f"enemy_{name.lower().replace(' ', '_')}",
        name=name,
        type=EnemyType.BEAST,
        level=level,
        hp=20 * level,
        max_hp=20 * level,
        attack_power=2 * level,
        defense=1 * level,
        abilities=["Attack"],
        reward_xp=10 * level,
        reward_gold=5 * level,
        boss=False
    )

def _simulate_combat(self, character, enemy):
    """Simulate combat between character and enemy."""
    # Simple damage calculation
    base_damage = character.stats.strength * 2
    enemy_damage = enemy.attack_power
    
    # Player attacks
    player_damage = base_damage + character.level * 5
    
    return player_damage


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])