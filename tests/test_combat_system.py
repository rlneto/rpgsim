"""
Unit tests for combat system implementation
Uses pytest with hypothesis for edge and boundary testing
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import MagicMock, patch
from game.combat import Combat, Enemy, Boss
from tests.conftest import (
    create_test_player, create_test_enemy, mock_player, 
    mock_enemy, st_ai_behavior, st_element_type
)


class TestCombat:
    """Test combat system mechanics"""
    
    @pytest.mark.unit
    def test_combat_initialization(self, mock_player, mock_enemy):
        """Test that combat initializes correctly"""
        combat = Combat(mock_player, mock_enemy)
        
        assert combat.player == mock_player
        assert combat.enemies == [mock_enemy]
        assert combat.is_active is True
        assert combat.round == 1
        assert len(combat.turn_order) == 2  # Player and enemy
    
    @pytest.mark.unit
    def test_combat_turn_order_calculation(self, mock_player, mock_enemy):
        """Test that turn order is calculated correctly based on initiative"""
        combat = Combat(mock_player, mock_enemy)
        
        # All participants should have initiative
        for participant in combat.turn_order:
            assert hasattr(participant, 'initiative')
            assert participant.initiative > 0
        
        # Turn order should be sorted by initiative
        initiatives = [p.initiative for p in combat.turn_order]
        assert initiatives == sorted(initiatives, reverse=True)
    
    @pytest.mark.unit
    def test_combat_next_turn(self, mock_player, mock_enemy):
        """Test that combat correctly advances to next turn"""
        combat = Combat(mock_player, mock_enemy)
        initial_round = combat.round
        initial_turn = combat.current_turn
        
        combat.next_turn()
        
        # Should advance to next participant
        assert combat.current_turn != initial_turn
        
        # Should advance round when cycle completes
        if combat.turn_order.index(combat.current_turn) == 0:
            assert combat.round == initial_round + 1
    
    @pytest.mark.unit
    def test_combat_attack_execution(self, mock_player, mock_enemy):
        """Test that combat attack executes correctly"""
        combat = Combat(mock_player, mock_enemy)
        
        # Record initial HP
        initial_player_hp = mock_player.hp
        initial_enemy_hp = mock_enemy.hp
        
        # Execute player attack
        combat.execute_attack(mock_player, mock_enemy)
        
        # Enemy should take damage
        assert mock_enemy.hp < initial_enemy_hp
        
        # Player should not take damage from own attack
        assert mock_player.hp == initial_player_hp
    
    @pytest.mark.unit
    def test_combat_defense_action(self, mock_player, mock_enemy):
        """Test that defense action works correctly"""
        combat = Combat(mock_player, mock_enemy)
        
        # Record initial HP
        initial_player_hp = mock_player.hp
        
        # Execute defense
        combat.execute_defense(mock_player)
        
        # Defense should reduce damage for this turn
        assert hasattr(mock_player, 'defense_bonus')
        assert mock_player.defense_bonus > 0
    
    @pytest.mark.unit
    @given(st.integers(min_value=0, max_value=100))
    def test_combat_damage_calculation(self, damage_value):
        """Test damage calculation with various values"""
        attacker = create_test_player("Warrior", 5)
        defender = create_test_enemy("humanoid", 5)
        
        # Mock attacker damage
        with patch.object(attacker, 'calculate_attack_damage', return_value=damage_value):
            combat = Combat(attacker, defender)
            initial_hp = defender.hp
            
            combat.execute_attack(attacker, defender)
            
            # Verify damage was applied correctly
            expected_hp = max(0, initial_hp - damage_value)
            assert defender.hp == expected_hp
    
    @pytest.mark.unit
    def test_combat_end_when_all_enemies_defeated(self, mock_player, mock_enemy):
        """Test that combat ends when all enemies are defeated"""
        combat = Combat(mock_player, mock_enemy)
        
        # Defeat enemy
        mock_enemy.hp = 0
        
        combat.check_combat_end()
        
        assert combat.is_active is False
    
    @pytest.mark.unit
    def test_combat_end_when_player_defeated(self, mock_player, mock_enemy):
        """Test that combat ends when player is defeated"""
        combat = Combat(mock_player, mock_enemy)
        
        # Defeat player
        mock_player.hp = 0
        
        combat.check_combat_end()
        
        assert combat.is_active is False
    
    @pytest.mark.unit
    def test_combat_continues_with_both_alive(self, mock_player, mock_enemy):
        """Test that combat continues when both are alive"""
        combat = Combat(mock_player, mock_enemy)
        
        # Ensure both have HP
        mock_player.hp = 50
        mock_enemy.hp = 50
        
        combat.check_combat_end()
        
        assert combat.is_active is True
    
    @pytest.mark.unit
    @given(st.lists(st.integers(min_value=1, max_value=6), min_size=1, max_size=3))
    def test_multi_enemy_combat(self, enemy_levels):
        """Test combat with multiple enemies"""
        player = create_test_player("Warrior", 5)
        enemies = [create_test_enemy("humanoid", level) for level in enemy_levels]
        
        combat = Combat(player, enemies)
        
        # All enemies should be added
        assert len(combat.enemies) == len(enemy_levels)
        
        # Turn order should include all enemies
        assert len(combat.turn_order) == 1 + len(enemy_levels)  # Player + enemies
    
    @pytest.mark.unit
    def test_action_time_costs(self):
        """Test that actions have appropriate time costs"""
        from game.combat import ACTION_COSTS
        
        # Verify action costs exist
        assert 'attack' in ACTION_COSTS
        assert 'defend' in ACTION_COSTS
        assert 'use_item' in ACTION_COSTS
        assert 'flee' in ACTION_COSTS
        
        # Verify reasonable time costs
        assert 3 <= ACTION_COSTS['attack'] <= 9
        assert 3 <= ACTION_COSTS['defend'] <= 9
        assert 3 <= ACTION_COSTS['use_item'] <= 9
        assert 3 <= ACTION_COSTS['flee'] <= 9


class TestEnemy:
    """Test enemy behaviors and attributes"""
    
    @pytest.mark.unit
    def test_enemy_creation(self):
        """Test that enemies are created correctly"""
        enemy = Enemy("goblin", 3, "aggressive")
        
        assert enemy.name == "goblin"
        assert enemy.level == 3
        assert enemy.ai_behavior == "aggressive"
        assert enemy.hp > 0
        assert enemy.max_hp > 0
        assert len(enemy.abilities) >= 2
    
    @pytest.mark.unit
    @given(st.text(min_size=1), st.integers(min_value=1, max_value=30), st_ai_behavior)
    def test_enemy_creation_with_various_inputs(self, name, level, ai_behavior):
        """Test enemy creation with various inputs"""
        enemy = Enemy(name, level, ai_behavior)
        
        assert enemy.name == name
        assert enemy.level == level
        assert enemy.ai_behavior == ai_behavior
    
    @pytest.mark.unit
    def test_enemy_has_weakness(self):
        """Test that enemies have weaknesses"""
        enemy = Enemy("goblin", 3, "aggressive")
        
        assert hasattr(enemy, 'weakness')
        assert enemy.weakness in ['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical']
    
    @pytest.mark.unit
    def test_enemy_has_resistance(self):
        """Test that enemies have resistances"""
        enemy = Enemy("goblin", 3, "aggressive")
        
        assert hasattr(enemy, 'resistance')
        assert enemy.resistance in ['fire', 'ice', 'lightning', 'holy', 'poison', 'magic', 'physical', 'none']
    
    @pytest.mark.unit
    @given(st_element_type)
    def test_enemy_weakness_effectiveness(self, element_type):
        """Test that enemy weaknesses are correctly applied"""
        enemy = Enemy("goblin", 3, "aggressive")
        enemy.weakness = element_type
        
        # Normal damage
        normal_damage = 10
        # Same element as weakness
        weakness_damage = enemy.calculate_damage_received(normal_damage, element_type)
        
        # Weakness should increase damage
        assert weakness_damage > normal_damage
    
    @pytest.mark.unit
    @given(st_element_type)
    def test_enemy_resistance_effectiveness(self, element_type):
        """Test that enemy resistances are correctly applied"""
        enemy = Enemy("goblin", 3, "aggressive")
        enemy.resistance = element_type
        
        # Normal damage
        normal_damage = 10
        # Same element as resistance
        resistance_damage = enemy.calculate_damage_received(normal_damage, element_type)
        
        # Resistance should decrease damage
        assert resistance_damage < normal_damage
    
    @pytest.mark.unit
    def test_enemy_ai_aggressive_behavior(self):
        """Test that aggressive AI behaves correctly"""
        enemy = Enemy("goblin", 3, "aggressive")
        player = create_test_player("Warrior", 5)
        
        action = enemy.choose_action(player)
        
        # Aggressive AI should prefer attack
        assert action in ['attack', 'special_attack']
    
    @pytest.mark.unit
    def test_enemy_ai_defensive_behavior(self):
        """Test that defensive AI behaves correctly"""
        enemy = Enemy("goblin", 3, "defensive")
        player = create_test_player("Warrior", 5)
        
        # Set enemy HP low to trigger defensive behavior
        enemy.hp = int(enemy.max_hp * 0.3)
        
        action = enemy.choose_action(player)
        
        # Defensive AI should prefer defend or heal
        assert action in ['defend', 'heal', 'flee']
    
    @pytest.mark.unit
    def test_enemy_ai_tactical_behavior(self):
        """Test that tactical AI behaves correctly"""
        enemy = Enemy("goblin", 3, "tactical")
        player = create_test_player("Warrior", 5)
        
        action = enemy.choose_action(player)
        
        # Tactical AI should make strategic decisions
        assert action in ['attack', 'special_attack', 'defend', 'use_item']
    
    @pytest.mark.unit
    def test_enemy_ai_random_behavior(self):
        """Test that random AI behaves correctly"""
        enemy = Enemy("goblin", 3, "random")
        player = create_test_player("Warrior", 5)
        
        action = enemy.choose_action(player)
        
        # Random AI should pick any valid action
        assert action in ['attack', 'defend', 'special_attack', 'flee']
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=30))
    def test_enemy_hp_scales_with_level(self, level):
        """Test that enemy HP scales with level"""
        enemy = Enemy("goblin", level, "aggressive")
        
        # HP should increase with level
        assert enemy.max_hp >= 20 + (level * 10)
        assert enemy.max_hp <= 20 + (level * 30)  # Reasonable upper bound
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=30))
    def test_enemy_damage_scales_with_level(self, level):
        """Test that enemy damage scales with level"""
        enemy = Enemy("goblin", level, "aggressive")
        player = create_test_player("Warrior", 5)
        
        damage = enemy.calculate_attack_damage(player)
        
        # Damage should scale with level
        min_damage = 5 + (level * 2)
        max_damage = 15 + (level * 5)
        
        assert min_damage <= damage <= max_damage


class TestBoss:
    """Test boss enemies and special mechanics"""
    
    @pytest.mark.unit
    def test_boss_creation(self):
        """Test that bosses are created correctly"""
        boss = Boss("Dragon", 15, "tactical", "volcano")
        
        assert boss.name == "Dragon"
        assert boss.level == 15
        assert boss.ai_behavior == "tactical"
        assert boss.theme == "volcano"
        assert boss.hp > 0
        assert boss.max_hp > 0
    
    @pytest.mark.unit
    def test_boss_has_special_mechanics(self):
        """Test that bosses have special mechanics"""
        boss = Boss("Dragon", 15, "tactical", "volcano")
        
        assert hasattr(boss, 'mechanics')
        assert len(boss.mechanics) >= 2
    
    @pytest.mark.unit
    @given(st.text(min_size=1), st.integers(min_value=15, max_value=40), 
           st_ai_behavior, st.text(min_size=1))
    def test_boss_creation_with_various_inputs(self, name, level, ai_behavior, theme):
        """Test boss creation with various inputs"""
        boss = Boss(name, level, ai_behavior, theme)
        
        assert boss.name == name
        assert boss.level == level
        assert boss.ai_behavior == ai_behavior
        assert boss.theme == theme
    
    @pytest.mark.unit
    def test_boss_hp_is_higher_than_regular_enemies(self):
        """Test that bosses have higher HP than regular enemies"""
        level = 15
        enemy = Enemy("goblin", level, "aggressive")
        boss = Boss("Dragon", level, "tactical", "volcano")
        
        assert boss.max_hp > enemy.max_hp
    
    @pytest.mark.unit
    def test_boss_has_more_abilities_than_regular_enemies(self):
        """Test that bosses have more abilities than regular enemies"""
        level = 15
        enemy = Enemy("goblin", level, "aggressive")
        boss = Boss("Dragon", level, "tactical", "volcano")
        
        assert len(boss.abilities) > len(enemy.abilities)
    
    @pytest.mark.unit
    def test_boss_thematic_abilities(self):
        """Test that boss abilities match their theme"""
        boss = Boss("Fire Dragon", 15, "tactical", "fire")
        
        # Should have fire-themed abilities
        has_fire_ability = any("fire" in ability.lower() for ability in boss.abilities)
        assert has_fire_ability
    
    @pytest.mark.unit
    def test_boss_phase_transitions(self):
        """Test that bosses can transition phases"""
        boss = Boss("Dragon", 15, "tactical", "volcano")
        
        # Should start in phase 1
        assert boss.current_phase == 1
        
        # Transition to phase 2 at 50% HP
        boss.hp = int(boss.max_hp * 0.5)
        boss.check_phase_transition()
        
        assert boss.current_phase == 2
    
    @pytest.mark.unit
    def test_boss_rewards_are_better(self):
        """Test that bosses provide better rewards than regular enemies"""
        level = 15
        enemy = Enemy("goblin", level, "aggressive")
        boss = Boss("Dragon", level, "tactical", "volcano")
        
        # Boss rewards
        assert boss.rewards['experience'] > enemy.calculate_xp_reward()
        assert boss.rewards['gold'] > enemy.calculate_gold_reward()
        assert len(boss.rewards['items']) >= 2
        assert 'special_reward' in boss.rewards
    
    @pytest.mark.unit
    @given(st.integers(min_value=15, max_value=40))
    def test_boss_difficulty_scales_with_level(self, level):
        """Test that boss difficulty scales with level"""
        boss = Boss("Dragon", level, "tactical", "volcano")
        player = create_test_player("Warrior", level)
        
        # Boss should be challenging but not impossible
        damage = boss.calculate_attack_damage(player)
        
        # Reasonable damage range
        assert 10 + (level * 3) <= damage <= 30 + (level * 5)
    
    @pytest.mark.unit
    def test_boss_unique_mechanics_not_shared_with_regular_enemies(self):
        """Test that bosses have unique mechanics"""
        from game.combat import ENEMY_TYPES, BOSS_TYPES
        
        # Get all regular enemy mechanics
        regular_mechanics = set()
        for enemy_type in ENEMY_TYPES.values():
            regular_mechanics.update(enemy_type.mechanics)
        
        # Boss mechanics should have unique elements
        for boss_type in BOSS_TYPES.values():
            boss_mechanics = set(boss_type.mechanics)
            
            # At least one unique mechanic per boss
            assert len(boss_mechanics - regular_mechanics) >= 1, \
                f"Boss {boss_type.name} should have unique mechanics"


class TestCombatFormulas:
    """Test combat calculations and formulas"""
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=20))
    def test_attack_formula_with_strength(self, strength):
        """Test attack formula with different strength values"""
        player = create_test_player("Warrior", 5)
        player.stats['strength'] = strength
        
        enemy = create_test_enemy("humanoid", 5)
        
        # More strength should increase damage
        damage = player.calculate_attack_damage(enemy)
        
        # Damage should be influenced by strength
        assert damage >= strength  # Minimum damage should be strength
        assert damage <= strength * 3  # Maximum reasonable damage
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=20))
    def test_defense_formula_with_dexterity(self, dexterity):
        """Test defense formula with different dexterity values"""
        player = create_test_player("Rogue", 5)
        player.stats['dexterity'] = dexterity
        
        # More dexterity should increase defense
        defense = player.calculate_defense()
        
        assert defense >= dexterity // 2  # Minimum defense
        assert defense <= dexterity * 2  # Maximum reasonable defense
    
    @pytest.mark.unit
    def test_critical_hit_formula(self):
        """Test critical hit calculations"""
        player = create_test_player("Rogue", 5)
        
        # Test with many iterations to check distribution
        crit_count = 0
        attacks = 1000
        
        for _ in range(attacks):
            if player.is_critical_hit():
                crit_count += 1
        
        # Should be approximately 5% by default
        assert 2 <= crit_count <= 80  # Allow reasonable variance
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=30))
    def test_xp_calculation_scales_with_enemy_level(self, enemy_level):
        """Test XP calculation scales with enemy level"""
        player = create_test_player("Warrior", 5)
        enemy = create_test_enemy("humanoid", enemy_level)
        
        xp = enemy.calculate_xp_reward()
        
        # XP should scale with level
        expected_min = 10 + (enemy_level * 5)
        expected_max = 50 + (enemy_level * 15)
        
        assert expected_min <= xp <= expected_max
    
    @pytest.mark.unit
    def test_level_difference_modifier(self):
        """Test level difference affects combat calculations"""
        player = create_test_player("Warrior", 10)
        enemy = create_test_enemy("humanoid", 5)
        
        # Player should have advantage against lower level enemy
        damage_modifier = player.calculate_level_advantage(enemy)
        
        assert damage_modifier > 1.0  # Damage bonus
        
        # Enemy should have disadvantage against higher level player
        enemy_modifier = enemy.calculate_level_disadvantage(player)
        
        assert enemy_modifier < 1.0  # Damage penalty