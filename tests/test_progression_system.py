"""
Unit tests for Progression System implementation
Comprehensive test coverage for character progression mechanics
"""

import pytest
from unittest.mock import Mock, patch
from core.systems.progression import (
    SkillType, AbilityRarity, Ability, SkillProgress, LevelCalculator,
    SkillTree, ProgressionManager, ProgressionSystem
)
from core.models import Character, CharacterClass, CharacterStats


class TestSkillType:
    """Test SkillType constants"""

    def test_skill_type_constants(self):
        """Test SkillType class constants"""
        assert SkillType.COMBAT == "combat"
        assert SkillType.MAGIC == "magic"
        assert SkillType.STEALTH == "stealth"
        assert SkillType.SOCIAL == "social"
        assert SkillType.CRAFTING == "crafting"
        assert SkillType.SURVIVAL == "survival"
        assert SkillType.KNOWLEDGE == "knowledge"

    def test_skill_type_variety(self):
        """Test we have multiple skill types"""
        skill_types = [
            SkillType.COMBAT, SkillType.MAGIC, SkillType.STEALTH,
            SkillType.SOCIAL, SkillType.CRAFTING, SkillType.SURVIVAL, SkillType.KNOWLEDGE
        ]
        assert len(skill_types) == 7


class TestAbilityRarity:
    """Test AbilityRarity constants"""

    def test_ability_rarity_constants(self):
        """Test AbilityRarity class constants"""
        assert AbilityRarity.COMMON == "common"
        assert AbilityRarity.UNCOMMON == "uncommon"
        assert AbilityRarity.RARE == "rare"
        assert AbilityRarity.EPIC == "epic"
        assert AbilityRarity.LEGENDARY == "legendary"

    def test_ability_rarity_variety(self):
        """Test we have multiple rarity levels"""
        rarities = [
            AbilityRarity.COMMON, AbilityRarity.UNCOMMON, AbilityRarity.RARE,
            AbilityRarity.EPIC, AbilityRarity.LEGENDARY
        ]
        assert len(rarities) == 5


class TestAbility:
    """Test Ability dataclass"""

    def test_ability_creation(self):
        """Test Ability dataclass creation"""
        ability = Ability(
            id="test_ability",
            name="Test Ability",
            description="A test ability",
            skill_type=SkillType.COMBAT,
            rarity=AbilityRarity.COMMON,
            required_level=1
        )

        assert ability.id == "test_ability"
        assert ability.name == "Test Ability"
        assert ability.skill_type == SkillType.COMBAT
        assert ability.rarity == AbilityRarity.COMMON
        assert ability.required_level == 1
        assert ability.current_level == 0
        assert ability.max_level == 5

    def test_ability_can_upgrade(self):
        """Test ability upgrade conditions"""
        ability = Ability(
            id="test_ability",
            name="Test Ability",
            description="A test ability",
            skill_type=SkillType.COMBAT,
            rarity=AbilityRarity.COMMON,
            required_level=5
        )

        # Test with insufficient level
        low_level_char = Mock(level=3, abilities=[])
        assert not ability.can_upgrade(low_level_char)

        # Test with sufficient level
        high_level_char = Mock(level=5, abilities=[])
        assert ability.can_upgrade(high_level_char)

        # Test with prerequisites
        ability.prerequisites = ["prereq_ability"]
        high_level_char.abilities = ["other_ability"]
        assert not ability.can_upgrade(high_level_char)

        # Test with prerequisites met
        high_level_char.abilities = ["prereq_ability"]
        assert ability.can_upgrade(high_level_char)

    def test_ability_upgrade_cost(self):
        """Test ability upgrade cost calculation"""
        ability = Ability(
            id="test_ability",
            name="Test Ability",
            description="A test ability",
            skill_type=SkillType.COMBAT,
            rarity=AbilityRarity.COMMON,
            required_level=1
        )

        # Test level 1 to 2 cost
        ability.current_level = 1
        cost = ability.get_upgrade_cost()
        assert cost["skill_points"] == 200  # 100 * (1 + 1) * 1.0
        assert cost["gold"] == 2000  # skill_points * 10

        # Test rarity multiplier
        ability.rarity = AbilityRarity.RARE
        cost = ability.get_upgrade_cost()
        assert cost["skill_points"] == 400  # 200 * 2.0

    def test_ability_max_level(self):
        """Test ability max level constraint"""
        ability = Ability(
            id="test_ability",
            name="Test Ability",
            description="A test ability",
            skill_type=SkillType.COMBAT,
            rarity=AbilityRarity.COMMON,
            required_level=1,
            max_level=3
        )

        ability.current_level = 3
        character = Mock(level=10, abilities=[])
        assert not ability.can_upgrade(character)


class TestSkillProgress:
    """Test SkillProgress dataclass"""

    def test_skill_progress_creation(self):
        """Test SkillProgress dataclass creation"""
        progress = SkillProgress(
            skill_name="test_skill",
            current_level=5,
            max_level=100
        )

        assert progress.skill_name == "test_skill"
        assert progress.current_level == 5
        assert progress.max_level == 100
        assert progress.experience == 0
        assert progress.total_experience == 0

    def test_add_experience_no_level_up(self):
        """Test adding experience without leveling up"""
        progress = SkillProgress(skill_name="test_skill")
        leveled_up = progress.add_experience(50)  # Less than exp_to_next (100)

        assert not leveled_up
        assert progress.current_level == 0
        assert progress.experience == 50
        assert progress.total_experience == 50

    def test_add_experience_with_level_up(self):
        """Test adding experience with level up"""
        progress = SkillProgress(skill_name="test_skill")
        leveled_up = progress.add_experience(150)  # More than exp_to_next (100)

        assert leveled_up
        assert progress.current_level == 1
        assert progress.experience == 50  # 150 - 100
        assert progress.total_experience == 150

    def test_calculate_experience_to_next(self):
        """Test experience calculation for next level"""
        progress = SkillProgress(skill_name="test_skill")

        # Level 0 to 1
        exp_needed = progress.calculate_experience_to_next()
        assert exp_needed == 100  # 100 * 1.15^0

        # Level 1 to 2
        progress.current_level = 1
        exp_needed = progress.calculate_experience_to_next()
        assert exp_needed == 115  # 100 * 1.15^1

    def test_get_effectiveness(self):
        """Test skill effectiveness calculation"""
        progress = SkillProgress(skill_name="test_skill")

        # Level 0 effectiveness
        effectiveness = progress.get_effectiveness()
        assert effectiveness == 1.0  # 1.0 + 0 * 0.05

        # Level 5 effectiveness
        progress.current_level = 5
        effectiveness = progress.get_effectiveness()
        assert effectiveness == 1.25  # 1.0 + 5 * 0.05

    def test_max_level_constraint(self):
        """Test max level constraint"""
        progress = SkillProgress(skill_name="test_skill", max_level=2)
        progress.current_level = 2
        progress.experience = 0

        # Add experience but shouldn't level up
        leveled_up = progress.add_experience(1000)
        assert not leveled_up
        assert progress.current_level == 2


class TestLevelCalculator:
    """Test LevelCalculator class"""

    def test_generate_experience_table(self):
        """Test experience table generation"""
        table = LevelCalculator.generate_experience_table()

        assert len(table) == 101  # Levels 0-100
        assert table[0] == 0  # Level 0 requires 0 exp
        assert table[1] == 0  # Level 1 requires 0 exp
        assert table[2] > table[1]  # Level 2 requires more than Level 1

    def test_get_experience_for_level(self):
        """Test getting experience for specific level"""
        assert LevelCalculator.get_experience_for_level(1) == 0
        assert LevelCalculator.get_experience_for_level(2) > 0
        assert LevelCalculator.get_experience_for_level(100) > LevelCalculator.get_experience_for_level(50)

    def test_get_level_from_experience(self):
        """Test level calculation from experience"""
        assert LevelCalculator.get_level_from_experience(0) == 1
        assert LevelCalculator.get_level_from_experience(500) == 2  # Level 2 requires some exp
        assert LevelCalculator.get_level_from_experience(100000) > 10  # High exp gives higher level

    def test_get_experience_progress(self):
        """Test getting current level progress"""
        character = Mock(level=5, experience=2500)

        # Mock the experience table
        with patch.object(LevelCalculator, 'get_experience_for_level') as mock_get_exp:
            mock_get_exp.side_effect = [1000, 2000, 3000]  # Level 4, 5, 6 exp
            current_exp, exp_needed = LevelCalculator.get_experience_progress(character)

            assert current_exp == 500  # 2500 - 2000 (exp for current level)
            assert exp_needed == 1000  # 3000 - 2000 (next level - current level)

    def test_can_level_up(self):
        """Test level up condition checking"""
        # Mock character at max level
        max_level_char = Mock(level=100, experience=999999)
        assert not LevelCalculator.can_level_up(max_level_char)

        # Mock character with insufficient exp
        low_exp_char = Mock(level=5, experience=1500)
        with patch.object(LevelCalculator, 'get_experience_for_level') as mock_get_exp:
            mock_get_exp.return_value = 2000  # Level 6 requires 2000
            assert not LevelCalculator.can_level_up(low_exp_char)

        # Mock character with sufficient exp
        high_exp_char = Mock(level=5, experience=2500)
        mock_get_exp.return_value = 2000
        assert LevelCalculator.can_level_up(high_exp_char)

    def test_calculate_level_up_rewards(self):
        """Test level up rewards calculation"""
        rewards = LevelCalculator.calculate_level_up_rewards(5, "warrior")

        assert "skill_points" in rewards
        assert "ability_points" in rewards
        assert "stat_increases" in rewards
        assert "hp_increase" in rewards
        assert rewards["skill_points"] == 3
        # Level 5 is an ability unlock level, so it gets extra ability points
        assert rewards["ability_points"] >= 1
        assert rewards["hp_increase"] == 10

    def test_class_specific_bonuses(self):
        """Test class-specific stat bonuses"""
        warrior_rewards = LevelCalculator.calculate_level_up_rewards(10, "warrior")
        mage_rewards = LevelCalculator.calculate_level_up_rewards(10, "mage")

        # Warrior should get more strength
        assert warrior_rewards["stat_increases"]["strength"] > mage_rewards["stat_increases"]["strength"]

        # Mage should get more intelligence
        assert mage_rewards["stat_increases"]["intelligence"] > warrior_rewards["stat_increases"]["intelligence"]

    def test_milestone_rewards(self):
        """Test milestone rewards at specific levels"""
        # Test regular level
        regular_rewards = LevelCalculator.calculate_level_up_rewards(15, "warrior")
        assert regular_rewards["milestone_reward"] is None

        # Test milestone level
        milestone_rewards = LevelCalculator.calculate_level_up_rewards(20, "warrior")
        assert milestone_rewards["milestone_reward"] is not None
        assert milestone_rewards["milestone_reward"]["level"] == 20
        assert milestone_rewards["milestone_reward"]["bonus_skill_points"] == 5


class TestSkillTree:
    """Test SkillTree class"""

    def test_skill_tree_initialization(self):
        """Test SkillTree initializes with default abilities"""
        skill_tree = SkillTree()

        assert len(skill_tree.abilities) > 0
        assert SkillType.COMBAT in skill_tree.skill_trees
        assert SkillType.MAGIC in skill_tree.skill_trees

    def test_get_ability_by_id(self):
        """Test getting ability by ID"""
        skill_tree = SkillTree()

        # Test existing ability
        ability = skill_tree.get_ability_by_id("power_strike")
        assert ability is not None
        assert ability.id == "power_strike"

        # Test non-existing ability
        ability = skill_tree.get_ability_by_id("non_existent")
        assert ability is None

    def test_get_available_abilities(self):
        """Test getting available abilities for character"""
        skill_tree = SkillTree()

        # Test low level character
        low_level_char = Mock(level=1, abilities=[])
        available = skill_tree.get_available_abilities(low_level_char)
        assert len(available) > 0  # Should have some level 1 abilities

        # Test high level character with some abilities
        high_level_char = Mock(level=10, abilities=["power_strike"])
        available = skill_tree.get_available_abilities(high_level_char)
        # Should include abilities that can be learned now

    def test_get_ability_tree(self):
        """Test getting abilities in skill tree"""
        skill_tree = SkillTree()

        combat_tree = skill_tree.get_ability_tree(SkillType.COMBAT)
        assert len(combat_tree) > 0

        for ability in combat_tree:
            assert ability.skill_type == SkillType.COMBAT

    def test_check_synergy(self):
        """Test ability synergy calculation"""
        skill_tree = SkillTree()

        # Create test ability with synergy
        ability = skill_tree.get_ability_by_id("dual_wield")
        if ability:
            ability.synergy_abilities = ["power_strike"]

            # Character without synergy ability
            no_synergy_char = Mock(abilities=[])
            synergy = skill_tree.check_synergy(no_synergy_char, ability.id)
            assert synergy == 1.0

            # Character with synergy ability
            synergy_char = Mock(abilities=["power_strike"])
            synergy = skill_tree.check_synergy(synergy_char, ability.id)
            assert synergy > 1.0

    def test_skill_types_organization(self):
        """Test abilities are properly organized by skill type"""
        skill_tree = SkillTree()

        for skill_type, ability_ids in skill_tree.skill_trees.items():
            assert len(ability_ids) > 0

            for ability_id in ability_ids:
                ability = skill_tree.get_ability_by_id(ability_id)
                assert ability is not None
                assert ability.skill_type == skill_type


class TestProgressionManager:
    """Test ProgressionManager class"""

    def test_progression_manager_initialization(self):
        """Test ProgressionManager initialization"""
        manager = ProgressionManager()

        assert hasattr(manager, 'level_calculator')
        assert hasattr(manager, 'skill_tree')
        assert hasattr(manager, 'character_skills')
        assert isinstance(manager.character_skills, dict)

    def test_add_experience_no_level_up(self):
        """Test adding experience without level up"""
        manager = ProgressionManager()
        character = Mock(level=1, experience=0, class_type="warrior", hp=50, max_hp=50)

        with patch.object(manager, 'level_calculator') as mock_calc:
            mock_calc.can_level_up.return_value = False

            result = manager.add_experience(character, 100, "test")

            assert result["experience_gained"] == 100
            assert result["source"] == "test"
            assert result["total_levels_gained"] == 0
            assert len(result["level_ups"]) == 0

    def test_add_experience_with_level_up(self):
        """Test adding experience with level up"""
        manager = ProgressionManager()
        character = Mock(level=1, experience=0, class_type="warrior", hp=50, max_hp=50)

        with patch.object(manager, 'level_calculator') as mock_calc:
            with patch.object(manager, '_level_up_character') as mock_level_up:
                mock_calc.can_level_up.return_value = True
                mock_calc.get_experience_for_level.return_value = 1000
                mock_level_up.return_value = {"hp_increase": 10}

                result = manager.add_experience(character, 2000, "test")

                assert result["total_levels_gained"] == 1
                assert len(result["level_ups"]) == 1

    def test_upgrade_skill(self):
        """Test skill upgrading"""
        manager = ProgressionManager()
        character = Mock(id="test_char", skills={})

        result = manager.upgrade_skill(character, "test_skill", 100)

        assert result["skill_name"] == "test_skill"
        assert result["experience_gained"] == 100
        assert "old_level" in result
        assert "new_level" in result
        assert "effectiveness" in result

    def test_learn_ability(self):
        """Test learning new ability"""
        manager = ProgressionManager()
        character = Mock(abilities=[])

        # Create mock ability
        ability = Mock(id="test_ability")
        ability.can_upgrade.return_value = True

        with patch.object(manager.skill_tree, 'get_ability_by_id', return_value=ability):
            result = manager.learn_ability(character, "test_ability")

            assert result["success"] is True
            assert "test_ability" in character.abilities

    def test_learn_ability_not_found(self):
        """Test learning non-existent ability"""
        manager = ProgressionManager()
        character = Mock(abilities=[])

        with patch.object(manager.skill_tree, 'get_ability_by_id', return_value=None):
            result = manager.learn_ability(character, "non_existent")

            assert result["success"] is False
            assert "error" in result

    def test_upgrade_ability(self):
        """Test upgrading existing ability"""
        manager = ProgressionManager()
        character = Mock(abilities=["test_ability"])

        # Create mock ability
        ability = Mock(id="test_ability", current_level=1, max_level=5)
        ability.current_level = 1
        ability.get_upgrade_cost.return_value = {"skill_points": 100}

        with patch.object(manager.skill_tree, 'get_ability_by_id', return_value=ability):
            result = manager.upgrade_ability(character, "test_ability")

            assert result["success"] is True
            assert result["new_level"] == 2

    def test_get_character_progression_summary(self):
        """Test getting character progression summary"""
        manager = ProgressionManager()
        character = Mock(
            id="test_char",
            name="TestHero",
            class_type="warrior",
            level=10,
            experience=5000,
            hp=150,
            max_hp=150,
            gold=1000,
            abilities=["test_ability"],
            skills={"test_skill": 5}
        )

        with patch.object(manager, 'character_skills', {"test_char": {"test_skill": Mock(
            current_level=5, max_level=100, experience=50, experience_to_next=100,
            get_effectiveness=Mock(return_value=1.25)
        )}}):
            with patch.object(manager, 'level_calculator') as mock_calc:
                mock_calc.get_experience_progress.return_value = (1000, 2000)

                summary = manager.get_character_progression_summary(character)

                assert summary["character_id"] == "test_char"
                assert summary["name"] == "TestHero"
                assert summary["level"] == 10
                assert "experience" in summary
                assert "skills" in summary
                assert "abilities" in summary


class TestProgressionSystem:
    """Test ProgressionSystem main interface"""

    def test_progression_system_initialization(self):
        """Test ProgressionSystem initialization"""
        system = ProgressionSystem()

        assert hasattr(system, 'progression_manager')
        assert hasattr(system, 'character_progress')
        assert isinstance(system.character_progress, dict)

    def test_add_experience_tracks_progress(self):
        """Test that adding experience tracks character progress"""
        system = ProgressionSystem()
        character = Mock(level=1, experience=0, id="test_char")

        with patch.object(system.progression_manager, 'add_experience', return_value={
            "experience_gained": 100,
            "total_levels_gained": 0,
            "old_level": 1,
            "new_level": 1
        }):
            result = system.add_experience(character, 100, "combat")

            assert result["experience_gained"] == 100
            assert character.id in system.character_progress
            assert system.character_progress[character.id]["total_experience_gained"] == 100

    def test_learn_ability_tracks_progress(self):
        """Test that learning abilities tracks character progress"""
        system = ProgressionSystem()
        character = Mock(id="test_char")

        with patch.object(system.progression_manager, 'learn_ability', return_value={
            "success": True,
            "ability": Mock(name="Test Ability")
        }):
            result = system.learn_ability(character, "test_ability")

            assert result["success"] is True
            assert system.character_progress[character.id]["abilities_learned"] == 1

    def test_get_character_summary(self):
        """Test getting complete character summary"""
        system = ProgressionSystem()
        character = Mock(id="test_char")

        with patch.object(system.progression_manager, 'get_character_progression_summary', return_value={
            "name": "TestHero",
            "level": 10,
            "experience": {"progress_percentage": 50.0}
        }):
            summary = system.get_character_summary(character)

            assert summary["name"] == "TestHero"
            assert "progression_stats" in summary

    def test_get_available_abilities(self):
        """Test getting available abilities"""
        system = ProgressionSystem()
        character = Mock()

        with patch.object(system.progression_manager.skill_tree, 'get_available_abilities', return_value=[]):
            abilities = system.get_available_abilities(character, SkillType.COMBAT)
            assert isinstance(abilities, list)

    def test_get_skill_trees(self):
        """Test getting all skill trees"""
        system = ProgressionSystem()

        with patch.object(system.progression_manager.skill_tree, 'get_ability_tree', return_value=[]):
            skill_trees = system.get_skill_trees()

            assert isinstance(skill_trees, dict)
            # Should return skill trees for each skill type
            # Implementation would check for specific skill types


class TestProgressionIntegration:
    """Integration tests for the complete progression system"""

    def test_full_progression_cycle(self):
        """Test complete progression cycle from level 1 to multiple levels"""
        # Create test character
        stats = CharacterStats(
            strength=10, intelligence=10, dexterity=10,
            constitution=10, wisdom=10, charisma=10
        )

        character = Character(
            id="integration_test_char",
            name="IntegrationHero",
            class_type="warrior",
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0
        )

        # Initialize progression system
        system = ProgressionSystem()

        # Test multiple experience additions
        total_levels = 0
        exp_amounts = [500, 1000, 2000, 5000]

        for exp in exp_amounts:
            result = system.add_experience(character, exp, "test_combat")
            total_levels += result["total_levels_gained"]
            assert character.level >= 1
            assert character.experience >= 0

        # Verify progression was tracked
        summary = system.get_character_summary(character)
        assert character.id in system.character_progress
        assert system.character_progress[character.id]["total_experience_gained"] > 0
        assert summary["level"] > 1

    def test_ability_learning_cycle(self):
        """Test ability learning and upgrading cycle"""
        # Create higher level character for ability testing
        stats = CharacterStats(
            strength=10, intelligence=10, dexterity=10,
            constitution=10, wisdom=10, charisma=10
        )

        character = Character(
            id="ability_test_char",
            name="AbilityHero",
            class_type="warrior",
            level=10,
            experience=10000,
            stats=stats,
            hp=200,
            max_hp=200,
            gold=1000
        )

        system = ProgressionSystem()

        # Get available abilities
        available_abilities = system.get_available_abilities(character)
        assert len(available_abilities) >= 1

        # Learn first available ability
        if available_abilities:
            first_ability = available_abilities[0]
            learn_result = system.learn_ability(character, first_ability.id)

            if learn_result["success"]:
                assert first_ability.id in character.abilities
                assert system.character_progress[character.id]["abilities_learned"] >= 1

    def test_skill_progression_cycle(self):
        """Test skill experience and leveling cycle"""
        system = ProgressionManager()

        character = Mock(id="skill_test_char", skills={})

        # Add skill experience multiple times
        skill_name = "combat"
        exp_amounts = [50, 100, 200, 300]

        for exp in exp_amounts:
            result = system.upgrade_skill(character, skill_name, exp)

            assert result["skill_name"] == skill_name
            assert result["experience_gained"] == exp
            assert result["new_level"] >= result["old_level"]
            assert result["effectiveness"] >= 1.0

        # Verify character skills were updated
        assert skill_name in character.skills
        assert character.skills[skill_name] >= 1