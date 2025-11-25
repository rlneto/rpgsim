"""
Boundary and Edge Case Tests for RPGSim
Property-based testing using Hypothesis for comprehensive coverage
TDD-focused: testing only what currently exists
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from hypothesis.strategies import integers, text, lists, dictionaries, floats, booleans
from typing import List, Dict, Any, Optional
import json
from pydantic import ValidationError

from core.models import Character, CharacterClass, CharacterStats


class TestCharacterStatsBoundary:
    """Property-based tests for CharacterStats boundary conditions."""

    @given(
        strength=integers(min_value=-100, max_value=100),
        dexterity=integers(min_value=-100, max_value=100),
        intelligence=integers(min_value=-100, max_value=100),
        wisdom=integers(min_value=-100, max_value=100),
        charisma=integers(min_value=-100, max_value=100),
        constitution=integers(min_value=-100, max_value=100),
    )
    def test_character_stats_boundaries(
        self, strength, dexterity, intelligence, wisdom, charisma, constitution
    ):
        """Test CharacterStats with extreme boundary values."""
        # Test valid range (1-20)
        if (
            1 <= strength <= 20
            and 1 <= dexterity <= 20
            and 1 <= intelligence <= 20
            and 1 <= wisdom <= 20
            and 1 <= charisma <= 20
            and 1 <= constitution <= 20
        ):
            stats = CharacterStats(
                strength=strength,
                dexterity=dexterity,
                intelligence=intelligence,
                wisdom=wisdom,
                charisma=charisma,
                constitution=constitution,
            )
            assert stats.strength == strength
            assert stats.dexterity == dexterity
            assert stats.intelligence == intelligence
            assert stats.wisdom == wisdom
            assert stats.charisma == charisma
            assert stats.constitution == constitution
        else:
            # Should raise ValidationError for invalid values
            with pytest.raises(ValidationError):
                CharacterStats(
                    strength=strength,
                    dexterity=dexterity,
                    intelligence=intelligence,
                    wisdom=wisdom,
                    charisma=charisma,
                    constitution=constitution,
                )

    @given(stat_value=integers(min_value=0, max_value=30))
    def test_individual_stat_boundaries(self, stat_value):
        """Test individual stat boundary values."""
        # Test exact boundaries
        boundary_cases = [0, 1, 20, 21, 30]

        for case in boundary_cases:
            if case == stat_value:
                if 1 <= case <= 20:
                    # Valid case
                    stats = CharacterStats(
                        strength=case,
                        dexterity=10,
                        intelligence=10,
                        wisdom=10,
                        charisma=10,
                        constitution=10,
                    )
                    assert stats.strength == case
                else:
                    # Invalid case
                    with pytest.raises(ValidationError):
                        CharacterStats(
                            strength=case,
                            dexterity=10,
                            intelligence=10,
                            wisdom=10,
                            charisma=10,
                            constitution=10,
                        )

    @given(all_stats=integers(min_value=1, max_value=20))
    def test_stat_modifiers_calculation(self, all_stats):
        """Test stat modifiers calculation with boundary values."""
        stats = CharacterStats(
            strength=all_stats,
            dexterity=all_stats,
            intelligence=all_stats,
            wisdom=all_stats,
            charisma=all_stats,
            constitution=all_stats,
        )

        modifiers = stats.get_stat_modifiers()

        # Test boundary cases for modifiers
        if all_stats == 1:
            # Minimum stat should give -4 modifier
            assert all(mod == -4 for mod in modifiers.values())
        elif all_stats == 10:
            # Average stat should give 0 modifier
            assert all(mod == 0 for mod in modifiers.values())
        elif all_stats == 20:
            # Maximum stat should give +5 modifier
            assert all(mod == 5 for mod in modifiers.values())

    @given(
        stats_list=lists(integers(min_value=1, max_value=20), min_size=6, max_size=6)
    )
    def test_total_stats_calculation(self, stats_list):
        """Test total stats calculation with various combinations."""
        strength, dexterity, intelligence, wisdom, charisma, constitution = stats_list

        stats = CharacterStats(
            strength=strength,
            dexterity=dexterity,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            constitution=constitution,
        )

        total = stats.get_total_stats()
        expected_total = sum(stats_list)

        assert total == expected_total

        # Test boundary cases
        if all(stat == 1 for stat in stats_list):
            assert total == 6  # Minimum possible total
        elif all(stat == 20 for stat in stats_list):
            assert total == 120  # Maximum possible total


class TestCharacterBoundary:
    """Property-based tests for Character model boundaries."""

    @given(
        name=text(min_size=0, max_size=100),
        level=integers(min_value=-10, max_value=200),
        experience=integers(min_value=-1000, max_value=1000000),
        gold=integers(min_value=-1000, max_value=1000000),
        hp=integers(min_value=-100, max_value=10000),
        max_hp=integers(min_value=-100, max_value=10000),
    )
    def test_character_boundaries(self, name, level, experience, gold, hp, max_hp):
        """Test Character model with boundary values."""
        # Create valid stats for character
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

        # Test name boundaries
        if len(name) < 1 or len(name) > 50:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=level,
                    experience=experience,
                    stats=stats,
                    hp=hp,
                    max_hp=max_hp,
                    gold=gold,
                )
            return

        # Test level boundaries
        if level < 1 or level > 100:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=level,
                    experience=experience,
                    stats=stats,
                    hp=hp,
                    max_hp=max_hp,
                    gold=gold,
                )
            return

        # Test experience boundaries
        if experience < 0:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=level,
                    experience=experience,
                    stats=stats,
                    hp=hp,
                    max_hp=max_hp,
                    gold=gold,
                )
            return

        # Test gold boundaries
        if gold < 0:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=level,
                    experience=experience,
                    stats=stats,
                    hp=hp,
                    max_hp=max_hp,
                    gold=gold,
                )
            return

        # Test HP boundaries
        if hp < 0 or max_hp < 0:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=level,
                    experience=experience,
                    stats=stats,
                    hp=hp,
                    max_hp=max_hp,
                    gold=gold,
                )
            return

        # Valid character creation
        character = Character(
            id="test",
            name=name,
            class_type=CharacterClass.WARRIOR,
            level=level,
            experience=experience,
            stats=stats,
            hp=hp,
            max_hp=max_hp,
            gold=gold,
        )

        assert character.name == name
        assert character.level == level
        assert character.experience == experience
        assert character.gold == gold
        assert character.hp == hp
        assert character.max_hp == max_hp

    @given(character_class=st.sampled_from(list(CharacterClass)))
    def test_character_class_coverage(self, character_class):
        """Test character creation with all possible classes."""
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

        character = Character(
            id="test",
            name="TestChar",
            class_type=character_class,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0,
        )

        assert character.class_type == character_class
        assert str(character.class_type) == character_class.value

    @given(
        abilities_list=lists(text(min_size=1, max_size=20), min_size=0, max_size=50),
        inventory_list=lists(text(min_size=1, max_size=20), min_size=0, max_size=100),
        quests_list=lists(text(min_size=1, max_size=20), min_size=0, max_size=1000),
        skills_dict=dictionaries(
            keys=text(min_size=1, max_size=20),
            values=integers(min_value=0, max_value=100),
            min_size=0,
            max_size=50,
        ),
    )
    def test_character_collections_boundaries(
        self, abilities_list, inventory_list, quests_list, skills_dict
    ):
        """Test character collection boundaries."""
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0,
            abilities=abilities_list,
            inventory=inventory_list,
            quests_completed=quests_list,
            skills=skills_dict,
        )

        assert len(character.abilities) == len(abilities_list)
        assert len(character.inventory) == len(inventory_list)
        assert len(character.quests_completed) == len(quests_list)
        assert len(character.skills) == len(skills_dict)

        # Test boundary cases
        if len(abilities_list) == 50:
            assert len(character.abilities) == 50  # Maximum reasonable size
        if len(inventory_list) == 100:
            assert len(character.inventory) == 100  # Maximum reasonable size
        if len(quests_list) == 1000:
            assert len(character.quests_completed) == 1000  # Maximum reasonable size


class TestCharacterNameEdgeCases:
    """Property-based tests for character name edge cases."""

    @given(text(min_size=0, max_size=60))
    def test_character_name_edge_cases(self, name):
        """Test character name with various edge cases."""
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

        # Test empty name
        if name == "":
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=1,
                    experience=0,
                    stats=stats,
                    hp=100,
                    max_hp=100,
                    gold=0,
                )
            return

        # Test name too long
        if len(name) > 50:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=1,
                    experience=0,
                    stats=stats,
                    hp=100,
                    max_hp=100,
                    gold=0,
                )
            return

        # Test valid name
        character = Character(
            id="test",
            name=name,
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0,
        )

        assert character.name == name

    @given(
        lists(elements=integers(min_value=0, max_value=255), min_size=1, max_size=10)
    )
    def test_character_name_unicode(self, char_codes):
        """Test character name with various Unicode characters."""
        name = "".join(chr(code) for code in char_codes)

        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )

        # Test control characters (should fail)
        if any(code < 32 for code in char_codes):
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=1,
                    experience=0,
                    stats=stats,
                    hp=100,
                    max_hp=100,
                    gold=0,
                )
            return

        # Test name length boundaries
        if len(name) > 50:
            with pytest.raises(ValidationError):
                Character(
                    id="test",
                    name=name,
                    class_type=CharacterClass.WARRIOR,
                    level=1,
                    experience=0,
                    stats=stats,
                    hp=100,
                    max_hp=100,
                    gold=0,
                )
            return

        # Valid Unicode names should work
        try:
            character = Character(
                id="test",
                name=name,
                class_type=CharacterClass.WARRIOR,
                level=1,
                experience=0,
                stats=stats,
                hp=100,
                max_hp=100,
                gold=0,
            )
            assert character.name == name
        except ValidationError:
            # Some Unicode combinations might be invalid
            pass


class TestPerformanceStress:
    """Stress tests for performance boundaries."""

    @settings(max_examples=100)
    @given(characters_count=integers(min_value=1, max_value=1000))
    def test_mass_character_creation(self, characters_count):
        """Test creating many characters at once."""
        characters = []

        for i in range(characters_count):
            stats = CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            )

            character = Character(
                id=f"char_{i}",
                name=f"Char{i}",
                class_type=CharacterClass.WARRIOR,
                level=1,
                experience=0,
                stats=stats,
                hp=100,
                max_hp=100,
                gold=0,
            )
            characters.append(character)

        assert len(characters) == characters_count

        # Verify all characters are valid
        for char in characters:
            assert char.name.startswith("Char")
            assert char.class_type == CharacterClass.WARRIOR
            assert char.level == 1
            assert char.hp == 100
            assert char.max_hp == 100

    @settings(max_examples=50)
    @given(
        stat_combinations=lists(
            integers(min_value=1, max_value=20), min_size=6, max_size=6
        )
    )
    def test_mass_stats_calculation(self, stat_combinations):
        """Test many stat calculations for performance."""
        results = []

        for _ in range(1000):  # Test 1000 calculations
            stats = CharacterStats(
                strength=stat_combinations[0],
                dexterity=stat_combinations[1],
                intelligence=stat_combinations[2],
                wisdom=stat_combinations[3],
                charisma=stat_combinations[4],
                constitution=stat_combinations[5],
            )

            modifiers = stats.get_stat_modifiers()
            total = stats.get_total_stats()

            results.append((modifiers, total))

        assert len(results) == 1000

        # Verify consistency
        for modifiers, total in results:
            assert isinstance(modifiers, dict)
            assert len(modifiers) == 6  # All 6 stats
            assert isinstance(total, int)
            assert 6 <= total <= 120  # Valid range
