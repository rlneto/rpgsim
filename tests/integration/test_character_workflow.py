"""
Integration Tests: Character Workflow
Optimized for LLM agents with complete workflow testing
"""

import pytest
from core.models import (
    Character, CharacterClass, CharacterStats,
    Item, ItemRarity, ItemType,
    Enemy, EnemyType
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
from core.systems.stats import (
    calculate_base_hp,
    calculate_damage_multiplier
)
from core.systems.leveling import (
    get_experience_for_level,
    get_level_progress_percentage
)
from core.validation import ValidationError


class TestCompleteCharacterWorkflow:
    """Test complete character workflow from creation to advanced gameplay."""
    
    def test_warrior_complete_workflow(self):
        """Test complete workflow for warrior character."""
        # Step 1: Create character
        character = create_character("Aragorn", CharacterClass.WARRIOR)
        
        # Validate initial state
        assert character.name == "Aragorn"
        assert character.class_type == CharacterClass.WARRIOR
        assert character.level == 1
        assert character.experience == 0
        assert character.gold == 100
        assert character.is_alive()
        assert len(character.abilities) >= 5
        assert character.stats.strength >= 12
        assert character.max_hp >= 50
        
        # Step 2: Level progression to level 10
        target_level = 10
        total_exp_needed = get_experience_for_level(target_level)
        
        # Add experience in chunks
        character = add_experience(character, total_exp_needed)
        
        # Level up to target
        while character.level < target_level:
            old_level = character.level
            character = level_up_character(character)
            
            # Validate level up
            assert character.level == old_level + 1
            assert character.hp == character.max_hp  # Full heal
            assert character.stats.strength > 15  # Stats increased
        
        # Validate final state
        assert character.level == target_level
        assert character.stats.strength >= 20  # Maxed strength
        assert character.max_hp >= 100
        assert len(character.abilities) >= 8  # More abilities learned
        
        # Step 3: Equipment workflow
        sword = Item(
            id="warrior_sword",
            name="Warrior's Sword",
            type=ItemType.WEAPON,
            rarity=ItemRarity.RARE,
            value=500,
            stats_mod={"strength": 3, "damage": 10},
            equippable=True
        )
        
        armor = Item(
            id="warrior_armor",
            name="Warrior's Armor",
            type=ItemType.ARMOR,
            rarity=ItemRarity.RARE,
            value=800,
            stats_mod={"constitution": 2, "defense": 15},
            equippable=True
        )
        
        # Equip items
        sword_equipped = equip_item(character, sword)
        armor_equipped = equip_item(character, armor)
        
        assert sword_equipped
        assert armor_equipped
        assert len(character.inventory) >= 2
        
        # Step 4: Combat workflow
        goblin = Enemy(
            id="goblin",
            name="Goblin",
            type=EnemyType.BEAST,
            level=5,
            hp=50,
            max_hp=50,
            attack_power=8,
            defense=5,
            abilities=["Attack", "Bite"],
            reward_xp=100,
            reward_gold=50,
            boss=False
        )
        
        # Simulate combat
        from core.systems.combat import calculate_damage
        
        # Player attacks goblin
        player_damage = calculate_damage(character, goblin)
        assert player_damage >= 10  # Should do decent damage
        
        goblin.hp -= player_damage
        assert goblin.hp < goblin.max_hp
        
        # Goblin attacks player
        goblin_damage = calculate_damage(goblin, character)
        character.hp -= goblin_damage
        
        # Player defeats goblin
        player_damage = calculate_damage(character, goblin)
        goblin.hp -= player_damage
        assert goblin.hp <= 0
        
        # Gain rewards
        character = add_experience(character, goblin.reward_xp)
        character.add_gold(goblin.reward_gold)
        
        assert character.experience > 0
        assert character.gold > 100
        
        # Step 5: Recovery workflow
        # Use healing potion
        potion = Item(
            id="healing_potion",
            name="Healing Potion",
            type=ItemType.CONSUMABLE,
            rarity=ItemRarity.COMMON,
            value=50,
            consumable=True
        )
        
        old_hp = character.hp
        character.add_item_to_inventory(potion)
        potion_used = use_item(character, potion)
        
        assert potion_used
        assert character.hp > old_hp
        assert potion.id not in [item.id for item in character.inventory]
        
        # Step 6: Final validation
        summary = get_character_summary(character)
        
        assert summary['level'] == target_level
        assert summary['class'] == 'warrior'
        assert summary['is_alive'] == True
        assert summary['total_stats'] >= 100
        assert summary['equipment_value'] > 1000
        
        # Check damage multiplier
        damage_mult = calculate_damage_multiplier(CharacterClass.WARRIOR)
        assert damage_mult >= 1.5
        
        # Check HP calculation
        expected_hp = calculate_base_hp(CharacterClass.WARRIOR, character.stats.constitution, character.level)
        assert character.max_hp == expected_hp
    
    def test_mage_complete_workflow(self):
        """Test complete workflow for mage character."""
        # Step 1: Create character
        character = create_character("Gandalf", CharacterClass.MAGE)
        
        # Validate mage-specific attributes
        assert character.stats.intelligence >= 12
        assert character.stats.intelligence > character.stats.strength
        assert "Fireball" in character.abilities
        assert "Magic Missile" in character.abilities
        assert character.max_hp < 50  # Lower HP than warrior
        
        # Step 2: Level progression with magic focus
        for level in range(2, 8):
            exp_needed = get_experience_for_level(level) - character.experience
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Mages gain more intelligence
            assert character.stats.intelligence >= 14 + (level - 2)
            
            # Learn magical abilities
            if level >= 3:
                assert any("Magic" in ability for ability in character.abilities)
        
        # Step 3: Magic equipment workflow
        staff = Item(
            id="mage_staff",
            name="Archmage's Staff",
            type=ItemType.WEAPON,
            rarity=ItemRarity.EPIC,
            value=1000,
            stats_mod={"intelligence": 4, "spell_power": 20},
            equippable=True
        )
        
        robes = Item(
            id="mage_robes",
            name="Enchanted Robes",
            type=ItemType.ARMOR,
            rarity=ItemRarity.RARE,
            value=600,
            stats_mod={"intelligence": 2, "magic_resistance": 10},
            equippable=True
        )
        
        # Equip magic items
        assert equip_item(character, staff)
        assert equip_item(character, robes)
        
        # Step 4: Magic combat workflow
        dark_mage = Enemy(
            id="dark_mage",
            name="Dark Mage",
            type=EnemyType.HUMANOID,
            level=7,
            hp=40,
            max_hp=40,
            attack_power=12,
            defense=3,
            abilities=["Fireball", "Lightning Bolt"],
            reward_xp=150,
            reward_gold=75,
            boss=False
        )
        
        # Simulate magic combat
        from core.systems.combat import calculate_spell_damage
        
        # Player casts fireball
        spell_damage = calculate_spell_damage(character, "Fireball")
        assert spell_damage >= 15  # Should do good spell damage
        
        dark_mage.hp -= spell_damage
        assert dark_mage.hp < dark_mage.max_hp
        
        # Enemy casts back
        enemy_spell_damage = calculate_spell_damage(dark_mage, "Lightning Bolt")
        character.hp -= enemy_spell_damage
        
        # Player defeats enemy with spell
        final_spell_damage = calculate_spell_damage(character, "Magic Missile")
        dark_mage.hp -= final_spell_damage
        assert dark_mage.hp <= 0
        
        # Gain magical rewards
        character = add_experience(character, dark_mage.reward_xp)
        character.add_gold(dark_mage.reward_gold)
        
        # Step 5: Mana and magic recovery
        mana_potion = Item(
            id="mana_potion",
            name="Mana Potion",
            type=ItemType.CONSUMABLE,
            rarity=ItemRarity.COMMON,
            value=60,
            consumable=True
        )
        
        character.add_item_to_inventory(mana_potion)
        assert use_item(character, mana_potion)
        
        # Step 6: Magic character validation
        summary = get_character_summary(character)
        
        assert summary['class'] == 'mage'
        assert summary['primary_stat'] == 'intelligence'
        assert summary['is_alive'] == True
        assert character.stats.intelligence >= 20  # High intelligence
        
        # Check mage-specific damage
        damage_mult = calculate_damage_multiplier(CharacterClass.MAGE)
        assert damage_mult == 1.0  # Standard damage multiplier for mages
    
    def test_rogue_complete_workflow(self):
        """Test complete workflow for rogue character."""
        # Step 1: Create character
        character = create_character("Legolas", CharacterClass.ROGUE)
        
        # Validate rogue-specific attributes
        assert character.stats.dexterity >= 12
        assert character.stats.dexterity > character.stats.strength
        assert "Stealth" in character.abilities
        assert "Backstab" in character.abilities
        assert character.max_hp >= 40  # Moderate HP
        
        # Step 2: Rogue progression with stealth focus
        for level in range(2, 6):
            exp_needed = get_experience_for_level(level) - character.experience
            character = add_experience(character, exp_needed)
            character = level_up_character(character)
            
            # Rogues gain more dexterity
            assert character.stats.dexterity >= 14 + (level - 2)
        
        # Step 3: Rogue equipment workflow
        daggers = Item(
            id="rogue_daggers",
            name="Dual Daggers",
            type=ItemType.WEAPON,
            rarity=ItemRarity.RARE,
            value=400,
            stats_mod={"dexterity": 3, "critical_chance": 15},
            equippable=True
        )
        
        leather_armor = Item(
            id="leather_armor",
            name="Shadow Leather Armor",
            type=ItemType.ARMOR,
            rarity=ItemRarity.UNCOMMON,
            value=300,
            stats_mod={"dexterity": 2, "stealth": 10},
            equippable=True
        )
        
        # Equip rogue items
        assert equip_item(character, daggers)
        assert equip_item(character, leather_armor)
        
        # Step 4: Stealth combat workflow
        guard = Enemy(
            id="guard",
            name="Castle Guard",
            type=EnemyType.HUMANOID,
            level=5,
            hp=60,
            max_hp=60,
            attack_power=10,
            defense=8,
            abilities=["Attack", "Block"],
            reward_xp=120,
            reward_gold=60,
            boss=False
        )
        
        # Simulate stealth combat
        from core.systems.combat import calculate_stealth_attack, calculate_backstab_damage
        
        # Stealth attack
        stealth_damage = calculate_stealth_attack(character, guard)
        assert stealth_damage >= 12  # Bonus damage from stealth
        
        guard.hp -= stealth_damage
        
        # Backstab
        backstab_damage = calculate_backstab_damage(character, guard)
        guard.hp -= backstab_damage
        assert guard.hp <= 0
        
        # Gain rogue rewards
        character = add_experience(character, guard.reward_xp)
        character.add_gold(guard.reward_gold)
        
        # Step 5: Poison and consumables
        poison = Item(
            id="poison",
            name="Poison Vial",
            type=ItemType.CONSUMABLE,
            rarity=ItemRarity.UNCOMMON,
            value=75,
            consumable=True
        )
        
        character.add_item_to_inventory(poison)
        assert use_item(character, poison)
        
        # Step 6: Rogue character validation
        summary = get_character_summary(character)
        
        assert summary['class'] == 'rogue'
        assert summary['primary_stat'] == 'dexterity'
        assert summary['is_alive'] == True
        assert character.stats.dexterity >= 18  # High dexterity
        
        # Check rogue-specific damage
        damage_mult = calculate_damage_multiplier(CharacterClass.ROGUE)
        assert damage_mult >= 1.3  # Higher damage multiplier for rogues
    
    def test_character_death_and_revival_workflow(self):
        """Test character death and revival workflow."""
        # Create character
        character = create_character("Test", CharacterClass.WARRIOR)
        old_gold = character.gold
        
        # Simulate death
        character.hp = 0
        assert character.is_defeated()
        assert not character.is_alive()
        
        # Death penalty: lose gold
        death_penalty = old_gold // 2
        character.gold -= death_penalty
        assert character.gold < old_gold
        
        # Revival at temple
        temple_heal_amount = character.max_hp
        character.hp = temple_heal_amount
        
        # Validate revival
        assert character.is_alive()
        assert not character.is_defeated()
        assert character.hp == character.max_hp
        assert character.gold == old_gold - death_penalty
        
        # Apply revival blessing
        from core.systems.character import heal_character
        blessing_heal = heal_character(character, 5)  # Small bonus heal
        assert blessing_heal == 0  # Already at full HP
    
    def test_character_save_load_workflow(self):
        """Test character save/load workflow."""
        # Create and advance character
        character = create_character("SaveTest", CharacterClass.PALADIN)
        
        # Add experience and level up
        character = add_experience(character, 200)
        character = level_up_character(character)
        
        # Add items and gold
        sword = Item(
            id="save_sword",
            name="Save Test Sword",
            type=ItemType.WEAPON,
            rarity=ItemRarity.COMMON,
            value=100,
            equippable=True
        )
        
        character.add_item_to_inventory(sword)
        character.add_gold(150)
        
        # Learn ability
        character.add_ability("Holy Strike")
        
        # Damage and heal
        character.hp = character.max_hp - 20
        character.heal(10)
        
        # Create game state
        from core.models import GameState
        game_state = GameState(
            current_location="test_location",
            player=character,
            world_time=100,
            day=1,
            flags={"save_test": True}
        )
        
        # Save game state
        from core.systems.game import save_game
        save_data = save_game(game_state)
        
        # Validate save data
        assert save_data is not None
        assert len(save_data) > 0
        
        # Load game state
        from core.systems.game import load_game
        loaded_game_state = load_game(save_data)
        
        # Validate loaded state
        assert loaded_game_state.player.name == character.name
        assert loaded_game_state.player.level == character.level
        assert loaded_game_state.player.experience == character.experience
        assert loaded_game_state.player.gold == character.gold
        assert len(loaded_game_state.player.inventory) == 1
        assert loaded_game_state.player.has_ability("Holy Strike")
        assert loaded_game_state.player.hp == character.hp
        assert loaded_game_state.player.max_hp == character.max_hp
        assert loaded_game_state.world_time == 100
        assert loaded_game_state.day == 1
        assert loaded_game_state.flags["save_test"] == True
        
        # Validate character still alive
        assert loaded_game_state.player.is_alive()
        assert not loaded_game_state.player.is_defeated()
    
    def test_character_multi_class_comparison_workflow(self):
        """Test workflow comparing multiple character classes."""
        # Create characters of different classes
        classes_to_test = [
            CharacterClass.WARRIOR,
            CharacterClass.MAGE,
            CharacterClass.ROGUE,
            CharacterClass.CLERIC,
            CharacterClass.RANGER
        ]
        
        characters = {}
        
        for class_type in classes_to_test:
            character = create_character(f"Test{class_type.value.title()}", class_type)
            characters[class_type] = character
        
        # Level all characters to level 5
        for class_type, character in characters.items():
            exp_needed = get_experience_for_level(5)
            character = add_experience(character, exp_needed)
            
            while character.level < 5:
                character = level_up_character(character)
        
        # Compare class characteristics
        # Warrior: High HP, High Strength
        warrior = characters[CharacterClass.WARRIOR]
        assert warrior.max_hp >= 80
        assert warrior.stats.strength >= 18
        
        # Mage: Low HP, High Intelligence
        mage = characters[CharacterClass.MAGE]
        assert mage.max_hp < 60
        assert mage.stats.intelligence >= 18
        
        # Rogue: Moderate HP, High Dexterity
        rogue = characters[CharacterClass.ROGUE]
        assert rogue.max_hp >= 60
        assert rogue.stats.dexterity >= 18
        
        # Cleric: Moderate HP, High Wisdom
        cleric = characters[CharacterClass.CLERIC]
        assert cleric.max_hp >= 60
        assert cleric.stats.wisdom >= 18
        
        # Ranger: Moderate HP, Balanced Stats
        ranger = characters[CharacterClass.RANGER]
        assert ranger.max_hp >= 60
        assert ranger.stats.dexterity >= 16
        assert ranger.stats.wisdom >= 14
        
        # Test class-specific abilities
        assert warrior.has_ability("Power Strike")
        assert mage.has_ability("Fireball")
        assert rogue.has_ability("Stealth")
        assert cleric.has_ability("Heal")
        assert ranger.has_ability("Precise Shot")
        
        # Test combat effectiveness against same enemy
        goblin = Enemy(
            id="test_goblin",
            name="Test Goblin",
            type=EnemyType.BEAST,
            level=3,
            hp=30,
            max_hp=30,
            attack_power=5,
            defense=3,
            abilities=["Attack"],
            reward_xp=50,
            reward_gold=25,
            boss=False
        )
        
        # Test damage output
        from core.systems.combat import calculate_damage
        
        damages = {}
        for class_type, character in characters.items():
            damage = calculate_damage(character, goblin)
            damages[class_type] = damage
        
        # Warrior should do most physical damage
        assert damages[CharacterClass.WARRIOR] >= damages[CharacterClass.MAGE]
        assert damages[CharacterClass.WARRIOR] >= damages[CharacterClass.ROGUE]
        
        # All characters should be able to defeat goblin
        for class_type, damage in damages.items():
            assert damage >= 10  # Should do reasonable damage
        
        # Test progression
        for class_type, character in characters.items():
            summary = get_character_summary(character)
            assert summary['level'] == 5
            assert summary['is_alive'] == True
            assert summary['primary_stat'] in ['strength', 'intelligence', 'dexterity', 'wisdom']


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])