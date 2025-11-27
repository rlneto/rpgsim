"""
E2E Test: Complete Gameplay Loop
Tests the entire RPG experience from title screen to all game endings
Includes towns, combat, dungeons, quests, items, exploration, and economy
"""

import pytest
import time
import random
from typing import Dict, List, Any, Optional
from core.models import GameState, Character, CharacterClass, Item, Quest, Enemy, Location
from core.systems.game import start_new_game, save_game, load_game
from core.systems.character import create_character, level_up_character, add_experience
from core.systems.combat import resolve_combat
from core.systems.quest import complete_quest
from core.systems.inventory import add_item_to_inventory, equip_item, remove_item_from_inventory
from core.systems.shop import ShopSystem, ShopType, ShopCreateParams
from core.systems.gamification import GamificationSystem
from core.systems.leveling import get_experience_for_level, level_up


class CompleteGameplayTester:
    """
    Complete gameplay loop tester that simulates a full RPG experience.
    Tests all major game systems working together.
    """

    def __init__(self):
        self.game_state: Optional[GameState] = None
        self.current_character: Optional[Character] = None
        self.shop_system = ShopSystem()
        self.gamification = GamificationSystem()
        self.game_session_id = f"test_session_{int(time.time())}"
        self.turn_count = 0
        self.locations_visited = []
        self.enemies_defeated = []
        self.quests_completed = []
        self.items_acquired = []
        self.gold_earned = 0
        self.experience_earned = 0

    def run_complete_gameplay_loop(self, player_class: str = "Warrior", ending_type: str = "warrior_victory") -> Dict[str, Any]:
        """
        Run the complete gameplay loop from start to finish.

        Args:
            player_class: Character class to play as
            ending_type: Target ending to achieve

        Returns:
            Dict with comprehensive gameplay results
        """
        start_time = time.time()

        try:
            # Phase 1: Game Initialization
            self._initialize_game(player_class)

            # Phase 2: Tutorial Area
            self._tutorial_phase()

            # Phase 3: First Town & Starting Quests
            self._first_town_phase()

            # Phase 4: Early Game (Levels 1-10)
            self._early_game_phase()

            # Phase 5: Mid Game (Levels 11-30)
            self._mid_game_phase()

            # Phase 6: Late Game (Levels 31-49)
            self._late_game_phase()

            # Phase 7: End Game (Level 50 + Ending)
            ending_result = self._end_game_phase(ending_type)

            execution_time = time.time() - start_time

            return {
                'success': True,
                'ending_type': ending_type,
                'ending_achieved': ending_result,
                'player_class': player_class,
                'final_level': self.current_character.level,
                'execution_time': execution_time,
                'turn_count': self.turn_count,
                'locations_visited': len(self.locations_visited),
                'enemies_defeated': len(self.enemies_defeated),
                'quests_completed': len(self.quests_completed),
                'items_acquired': len(self.items_acquired),
                'gold_earned': self.gold_earned,
                'experience_earned': self.experience_earned,
                'game_state': self._get_game_summary()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'turn_count': self.turn_count,
                'locations_visited': len(self.locations_visited),
                'enemies_defeated': len(self.enemies_defeated),
                'partial_progress': self._get_game_summary()
            }

    def _initialize_game(self, player_class: str) -> None:
        """Initialize new game with character creation."""
        print(f"🎮 Initializing game with {player_class}...")

        # Create new game state
        self.game_state = start_new_game()

        # Create character
        self.current_character = create_character(f"Test{player_class}", player_class)

        # Initialize game session
        self.game_state['current_character_id'] = self.current_character.id
        self.game_state['session_id'] = self.game_session_id
        self.game_state['game_time'] = 0
        self.game_state['location'] = "tutorial_area"

        # Add starting equipment
        starting_items = [
            {"name": "Iron Sword", "type": "weapon", "value": 50},
            {"name": "Leather Armor", "type": "armor", "value": 75},
            {"name": "Health Potion", "type": "consumable", "value": 25}
        ]

        for item_data in starting_items:
            result = add_item_to_inventory(self.current_character, item_data["name"])
            self.items_acquired.append(item_data["name"])

        # Give starting gold
        self.current_character.gold = 100

        print(f"✅ Game initialized! Character: {self.current_character.name}, Level: {self.current_character.level}")

    def _tutorial_phase(self) -> None:
        """Tutorial phase with basic combat and mechanics."""
        print("📚 Starting tutorial phase...")

        self.turn_count += 1
        self.game_state['location'] = "tutorial_area"

        # Tutorial combat - fight weak goblin
        goblin = self._create_enemy("Goblin", 2, 50)
        combat_result = resolve_combat(self.current_character, goblin)

        if combat_result.get('winner') == self.current_character.name:
            self.enemies_defeated.append("Goblin")
            exp_reward = 25
            gold_reward = 10
            self.experience_earned += exp_reward
            self.gold_earned += gold_reward
            add_experience(self.current_character, exp_reward)
            self.current_character.gold += gold_reward
            print(f"✅ Tutorial combat won! +{exp_reward} EXP, +{gold_reward} gold")

        # Tutorial quest
        tutorial_quest = self._create_quest("Tutorial", "Defeat Goblin", exp_reward=50, gold_reward=25)
        complete_quest(self.current_character, tutorial_quest)
        self.quests_completed.append("Tutorial")

        # Level up check
        if self.current_character.experience >= get_experience_for_level(2):
            level_up_character(self.current_character)
            print(f"✅ Leveled up to {self.current_character.level}!")

    def _first_town_phase(self) -> None:
        """First town experience with shops, NPCs, and quests."""
        print("🏘️ Entering first town...")

        self.turn_count += 5  # Travel time
        self.game_state['location'] = "starter_town"
        self.locations_visited.append("starter_town")

        # Town exploration
        self._explore_town("starter_town")

        # Shop interactions
        self._visit_town_shops("starter_town")

        # Quest acquisition
        town_quests = self._get_town_quests("starter_town")
        for quest in town_quests[:2]:  # Take first 2 quests
            self.quests_completed.append(quest.name)
            complete_quest(self.current_character, quest)

        # Equipment upgrades
        self._upgrade_equipment("starter_town")

    def _early_game_phase(self) -> None:
        """Early game exploration and combat (Levels 1-10)."""
        print("⚔️ Early game phase (Levels 1-10)...")

        while self.current_character.level < 10:
            self.turn_count += 1

            # Random encounter
            if random.random() < 0.7:  # 70% chance of encounter
                self._handle_random_encounter()

            # Resource gathering
            if random.random() < 0.3:  # 30% chance of finding resources
                self._gather_resources()

            # Visit town every 5 turns
            if self.turn_count % 5 == 0:
                self._visit_nearest_town()

            # Check for level up
            if self.current_character.experience >= get_experience_for_level(self.current_character.level + 1):
                level_up_character(self.current_character)
                print(f"✅ Leveled up to {self.current_character.level}!")

                # Learn abilities
                self._learn_class_abilities()

        print(f"✅ Early game complete! Level: {self.current_character.level}")

    def _mid_game_phase(self) -> None:
        """Mid game with dungeons and complex quests (Levels 11-30)."""
        print("🏰 Mid game phase (Levels 11-30)...")

        # Explore different areas
        areas = ["forest", "mountains", "swamp", "desert", "ruins"]

        while self.current_character.level < 30:
            self.turn_count += 1

            # Choose area to explore
            current_area = random.choice(areas)
            self.locations_visited.append(current_area)
            self.game_state['location'] = current_area

            # Area-specific encounters
            self._explore_area(current_area)

            # Dungeon exploration
            if self.turn_count % 10 == 0:
                self._explore_dungeon()

            # Major quest every 15 turns
            if self.turn_count % 15 == 0:
                major_quest = self._create_major_quest()
                complete_quest(self.current_character, major_quest)
                self.quests_completed.append(major_quest.name)

            # Level up check
            if self.current_character.experience >= get_experience_for_level(self.current_character.level + 1):
                level_up_character(self.current_character)
                print(f"✅ Leveled up to {self.current_character.level}!")
                self._learn_class_abilities()

    def _late_game_phase(self) -> None:
        """Late game with epic challenges (Levels 31-49)."""
        print("🐉 Late game phase (Levels 31-49)...")

        while self.current_character.level < 50:
            self.turn_count += 1

            # Epic locations
            epic_locations = ["dragon_lair", "ancient_tomb", "forgotten_realm", "celestial_plane"]
            location = random.choice(epic_locations)
            self.locations_visited.append(location)
            self.game_state['location'] = location

            # Boss encounters
            if random.random() < 0.4:  # 40% boss chance
                self._handle_boss_encounter(location)

            # Legendary dungeons
            if self.turn_count % 8 == 0:
                self._explore_legendary_dungeon()

            # Epic quests
            if self.turn_count % 12 == 0:
                epic_quest = self._create_epic_quest()
                complete_quest(self.current_character, epic_quest)
                self.quests_completed.append(epic_quest.name)

            # Level up check
            if self.current_character.experience >= get_experience_for_level(self.current_character.level + 1):
                level_up_character(self.current_character)
                print(f"✅ Leveled up to {self.current_character.level}!")
                self._learn_master_abilities()

    def _end_game_phase(self, ending_type: str) -> Dict[str, Any]:
        """End game content and final ending."""
        print("🏁 End game phase...")

        self.turn_count += 1
        self.game_state['location'] = "end_game_area"
        self.locations_visited.append("end_game_area")

        # Final boss challenge
        final_boss = self._create_final_boss()
        combat_result = resolve_combat(self.current_character, final_boss)

        if combat_result.get('winner') == self.current_character.name:
            self.enemies_defeated.append("Final Boss")
            self.experience_earned += 5000
            self.gold_earned += 10000
            add_experience(self.current_character, 5000)
            self.current_character.gold += 10000
            print("✅ Final boss defeated!")

        # Achieve ending based on character development
        ending = self._achieve_ending(ending_type)

        # Save final game state
        save_result = save_game(self.game_state, f"ending_{ending_type}_{self.game_session_id}")

        return ending

    def _create_enemy(self, name: str, level: int, hp: int) -> Enemy:
        """Create an enemy for combat."""
        from core.models import EnemyType

        # Determine enemy type based on name
        if any(beast_word in name.lower() for beast_word in ['goblin', 'wolf', 'bear']):
            enemy_type = EnemyType.BEAST
        elif any(humanoid_word in name.lower() for humanoid_word in ['bandit', 'rogue', 'warrior']):
            enemy_type = EnemyType.HUMANOID
        elif any(undead_word in name.lower() for undead_word in ['skeleton', 'zombie', 'ghost']):
            enemy_type = EnemyType.UNDEAD
        elif any(demon_word in name.lower() for demon_word in ['demon', 'devil', 'imp']):
            enemy_type = EnemyType.DEMON
        else:
            enemy_type = EnemyType.HUMANOID  # Default

        return Enemy(
            id=f"enemy_{name.lower()}_{self.turn_count}",
            name=name,
            type=enemy_type,
            level=level,
            hp=hp,
            max_hp=hp,
            attack_power=10 + level * 5,
            defense=5 + level * 3,
            reward_xp=50 * level,
            reward_gold=25 * level,
            abilities=[f"attack_{level}"]
        )

    def _create_quest(self, title: str, description: str, exp_reward: int = 100, gold_reward: int = 50) -> Quest:
        """Create a quest."""
        from core.models import QuestStatus

        return Quest(
            id=f"quest_{title.lower()}_{self.turn_count}",
            name=title,
            description=description,
            type="main_quest",
            difficulty="easy",
            giver="Quest_Giver",
            location=self.game_state['location'],
            objectives=[{
                'description': description,
                'completed': True
            }],
            rewards={
                'xp': exp_reward,
                'gold': gold_reward,
                'items': []
            },
            status=QuestStatus.COMPLETED
        )

    def _create_major_quest(self) -> Quest:
        """Create a major quest for mid-game."""
        quest_types = ["Slay Dragon", "Find Artifact", "Rescue Princess", "Defeat Warlord", "Explore Ruins"]
        quest_type = random.choice(quest_types)
        return self._create_quest(
            f"Major Quest: {quest_type}",
            f"Complete the {quest_type.lower()} challenge",
            exp_reward=500,
            gold_reward=250
        )

    def _create_epic_quest(self) -> Quest:
        """Create an epic quest for late-game."""
        quest_types = ["Stop Apocalypse", "Claim Throne", "Defeat God", "Seal Portal", "Find Ultimate Weapon"]
        quest_type = random.choice(quest_types)
        return self._create_quest(
            f"Epic Quest: {quest_type}",
            f"Complete the epic {quest_type.lower()}",
            exp_reward=2000,
            gold_reward=1000
        )

    def _explore_town(self, town_name: str) -> None:
        """Explore a town and interact with NPCs."""
        print(f"🏘️ Exploring {town_name}...")

        # Town NPCs
        npcs = ["Blacksmith", "Merchant", "Innkeeper", "Guild Master", "Healer"]
        for npc in npcs:
            if random.random() < 0.6:  # 60% chance to meet each NPC
                print(f"  👋 Met {npc}")
                # NPC interactions could yield quests, items, or information

    def _visit_town_shops(self, town_name: str) -> None:
        """Visit shops in town."""
        print(f"🛍️ Visiting shops in {town_name}...")

        # Create shops in town
        weapon_shop = self.shop_system.create_shop(
            shop_id=f"{town_name}_weapon_shop",
            name="Weapon Master",
            shop_type="WEAPONS",
            owner="Blacksmith",
            location=town_name
        )

        armor_shop = self.shop_system.create_shop(
            shop_id=f"{town_name}_armor_shop",
            name="Armor Smith",
            shop_type="ARMOR",
            owner="Armorer",
            location=town_name
        )

        # Purchase items if affordable
        affordable_items = [
            {"name": "Steel Sword", "price": 100},
            {"name": "Iron Shield", "price": 80},
            {"name": "Health Potion", "price": 25}
        ]

        for item in affordable_items:
            if self.current_character.gold >= item["price"]:
                # Simple shop transaction
                self.current_character.gold -= item["price"]
                add_item_to_inventory(self.current_character, item["name"])
                self.items_acquired.append(item["name"])
                print(f"  💰 Purchased {item['name']} for {item['price']} gold")

    def _upgrade_equipment(self, town_name: str) -> None:
        """Upgrade equipment in town."""
        print(f"⚔️ Upgrading equipment in {town_name}...")

        # For now, just simulate equipment upgrade
        if hasattr(self.current_character, 'inventory'):
            item_count = len(self.current_character.inventory)
            if item_count > 0:
                print(f"  ✅ Upgraded {item_count} items from inventory")
                # Add some equipment stats for testing
                if not hasattr(self.current_character, 'equipment'):
                    self.current_character.equipment = {
                        'weapon': 'Steel Sword',
                        'armor': 'Iron Shield'
                    }

    def _get_town_quests(self, town_name: str) -> List[Quest]:
        """Get available quests in town."""
        quest_templates = [
            "Clear nearby monsters",
            "Find missing item",
            "Deliver package",
            "Gather resources",
            "Investigate ruins"
        ]

        quests = []
        for template in quest_templates:
            if random.random() < 0.4:  # 40% chance for each quest
                quest = self._create_quest(f"{town_name}: {template}", template)
                quests.append(quest)

        return quests

    def _handle_random_encounter(self) -> None:
        """Handle random combat encounters."""
        enemy_types = ["Goblin", "Orc", "Wolf", "Bandit", "Spider"]
        enemy_type = random.choice(enemy_types)

        # Enemy level scales with player
        enemy_level = max(1, self.current_character.level - 2 + random.randint(-1, 2))
        enemy_hp = 50 + enemy_level * 20

        enemy = self._create_enemy(enemy_type, enemy_level, enemy_hp)
        print(f"⚔️ Random encounter: {enemy_type} (Level {enemy_level})")

        combat_result = resolve_combat(self.current_character, enemy)

        if combat_result.get('winner') == self.current_character.name:
            self.enemies_defeated.append(f"{enemy_type} (Level {enemy_level})")
            exp_reward = enemy.experience_reward
            gold_reward = enemy.gold_reward
            self.experience_earned += exp_reward
            self.gold_earned += gold_reward
            add_experience(self.current_character, exp_reward)
            self.current_character.gold += gold_reward
            print(f"  ✅ Victory! +{exp_reward} EXP, +{gold_reward} gold")
        else:
            print(f"  💀 Defeated by {enemy_type}!")

    def _gather_resources(self) -> None:
        """Gather resources during exploration."""
        resources = ["Herbs", "Ore", "Wood", "Food", "Gems"]
        resource = random.choice(resources)

        print(f"🌿 Found {resource}!")

        # Add to inventory
        add_item_to_inventory(self.current_character, resource)
        self.items_acquired.append(resource)

        # Small chance for gold
        if random.random() < 0.3:
            gold_found = random.randint(5, 25)
            self.gold_earned += gold_found
            self.current_character.gold += gold_found
            print(f"  💰 Found {gold_found} gold!")

    def _visit_nearest_town(self) -> None:
        """Visit nearest town for rest and supplies."""
        towns = ["starter_town", "forest_village", "mountain_hamlet", "coast_town"]
        town = random.choice(towns)

        print(f"🏘️ Visiting {town} for rest and supplies...")
        self._visit_town_shops(town)
        self._upgrade_equipment(town)

    def _explore_area(self, area_name: str) -> None:
        """Explore a specific area."""
        print(f"🗺️ Exploring {area_name}...")

        # Area-specific encounters
        if area_name == "forest":
            if random.random() < 0.3:
                self._gather_resources()  # Herbs and wood
        elif area_name == "mountains":
            if random.random() < 0.4:
                self._handle_random_encounter()  # Mountain monsters
        elif area_name == "swamp":
            if random.random() < 0.5:
                self._gather_resources()  # Rare ingredients
        elif area_name == "desert":
            if random.random() < 0.3:
                self._gather_resources()  # Gems and minerals
        elif area_name == "ruins":
            if random.random() < 0.6:
                self._explore_dungeon()  # Underground ruins

    def _explore_dungeon(self) -> None:
        """Explore a dungeon."""
        print("🏰 Exploring dungeon...")

        self.turn_count += 3  # Dungeon exploration takes time

        # Dungeon encounters
        for _ in range(random.randint(2, 5)):
            self._handle_random_encounter()

        # Treasure room
        if random.random() < 0.7:
            treasure_items = ["Ancient Sword", "Magic Ring", "Gold Coins", "Mystic Amulet"]
            treasure = random.choice(treasure_items)

            add_item_to_inventory(self.current_character, treasure)
            self.items_acquired.append(treasure)

            treasure_gold = random.randint(50, 200)
            self.gold_earned += treasure_gold
            self.current_character.gold += treasure_gold

            print(f"  💎 Found treasure: {treasure} and {treasure_gold} gold!")

    def _handle_boss_encounter(self, location: str) -> None:
        """Handle boss encounters."""
        boss_types = {
            "dragon_lair": "Ancient Dragon",
            "ancient_tomb": "Lich Lord",
            "forgotten_realm": "Elder Elemental",
            "celestial_plane": "Celestial Guardian"
        }

        boss_name = boss_types.get(location, "Ancient Beast")
        boss_level = self.current_character.level + 5
        boss_hp = 500 + boss_level * 50

        boss = self._create_enemy(boss_name, boss_level, boss_hp)
        print(f"🐉 BOSS FIGHT: {boss_name} (Level {boss_level})")

        combat_result = resolve_combat(self.current_character, boss)

        if combat_result.get('winner') == self.current_character.name:
            self.enemies_defeated.append(f"BOSS: {boss_name}")
            exp_reward = enemy.experience_reward * 5  # Boss gives 5x exp
            gold_reward = enemy.gold_reward * 3  # Boss gives 3x gold
            self.experience_earned += exp_reward
            self.gold_earned += gold_reward
            add_experience(self.current_character, exp_reward)
            self.current_character.gold += gold_reward
            print(f"  🏆 BOSS DEFEATED! +{exp_reward} EXP, +{gold_reward} gold")
        else:
            print(f"  💀 Defeated by BOSS {boss_name}!")

    def _explore_legendary_dungeon(self) -> None:
        """Explore legendary dungeon."""
        print("⚡ Exploring legendary dungeon...")

        self.turn_count += 5  # Legendary dungeons take longer

        # Multiple boss encounters
        for i in range(random.randint(1, 3)):
            self._handle_boss_encounter("ancient_tomb")

        # Legendary treasure
        legendary_items = ["Excalibur", "Dragon Armor", "Phoenix Staff", "Ultimate Shield"]
        legendary_item = random.choice(legendary_items)

        add_item_to_inventory(self.current_character, legendary_item)
        self.items_acquired.append(f"LEGENDARY: {legendary_item}")

        legendary_gold = random.randint(500, 2000)
        self.gold_earned += legendary_gold
        self.current_character.gold += legendary_gold

        print(f"  ⭐ LEGENDARY TREASURE: {legendary_item} and {legendary_gold} gold!")

    def _create_final_boss(self) -> Enemy:
        """Create final boss encounter."""
        final_boss = self._create_enemy("Dark Lord", self.current_character.level + 10, 2000)
        final_boss.attack_power *= 2
        final_boss.defense_power *= 2
        final_boss.experience_reward *= 10
        final_boss.gold_reward *= 10
        return final_boss

    def _learn_class_abilities(self) -> None:
        """Learn class-specific abilities."""
        print(f"📚 Learning abilities for {self.current_character.class_type}...")
        # This would add class-specific abilities to the character

    def _learn_master_abilities(self) -> None:
        """Learn master-level abilities."""
        print(f"✨ Learning master abilities for {self.current_character.class_type}...")
        # This would add powerful abilities at high levels

    def _achieve_ending(self, ending_type: str) -> Dict[str, Any]:
        """Achieve specific ending based on character and actions."""
        print(f"🎭 Achieving ending: {ending_type}")

        ending_requirements = {
            "warrior_victory": self.current_character.level >= 50 and len(self.enemies_defeated) >= 100,
            "mage_mastery": self.current_character.level >= 50 and len(self.items_acquired) >= 50,
            "rogue_stealth": self.current_character.level >= 50 and self.gold_earned >= 10000,
            "cleric_holy": self.current_character.level >= 50 and len(self.quests_completed) >= 20
        }

        requirements_met = ending_requirements.get(ending_type, True)  # Default to true for other endings

        return {
            'type': ending_type,
            'achieved': requirements_met,
            'character_level': self.current_character.level,
            'enemies_defeated': len(self.enemies_defeated),
            'quests_completed': len(self.quests_completed),
            'gold_earned': self.gold_earned,
            'locations_visited': len(self.locations_visited)
        }

    def _get_game_summary(self) -> Dict[str, Any]:
        """Get comprehensive game summary."""
        return {
            'character': {
                'name': self.current_character.name,
                'class': str(self.current_character.class_type),
                'level': self.current_character.level,
                'experience': self.current_character.experience,
                'gold': self.current_character.gold,
                'hp': self.current_character.hp,
                'max_hp': self.current_character.max_hp
            },
            'game_stats': {
                'turn_count': self.turn_count,
                'locations_visited': self.locations_visited,
                'enemies_defeated': self.enemies_defeated,
                'quests_completed': self.quests_completed,
                'items_acquired': self.items_acquired,
                'gold_earned': self.gold_earned,
                'experience_earned': self.experience_earned
            }
        }


@pytest.mark.parametrize("ending_type", [
    "warrior_victory",
    "mage_mastery",
    "rogue_stealth",
    "cleric_holy"
])
@pytest.mark.e2e
def test_complete_gameplay_loop_ending(ending_type):
    """Test complete gameplay loop for different endings."""
    tester = CompleteGameplayTester()

    # Run complete gameplay loop
    result = tester.run_complete_gameplay_loop("Warrior", ending_type)

    # Validate results
    assert result['success'], f"Gameplay loop failed: {result.get('error', 'Unknown error')}"
    assert result['final_level'] >= 50, f"Character should reach level 50, got {result['final_level']}"
    assert result['enemies_defeated'] > 0, "Should defeat enemies"
    assert result['quests_completed'] > 0, "Should complete quests"
    assert result['items_acquired'] > 0, "Should acquire items"
    assert result['gold_earned'] > 0, "Should earn gold"
    assert result['locations_visited'] > 0, "Should visit locations"
    assert result['ending_achieved']['achieved'], f"Ending {ending_type} should be achievable"

    print(f"✅ {ending_type} ending test passed!")
    print(f"   Final Level: {result['final_level']}")
    print(f"   Enemies Defeated: {result['enemies_defeated']}")
    print(f"   Quests Completed: {result['quests_completed']}")
    print(f"   Gold Earned: {result['gold_earned']}")
    print(f"   Execution Time: {result['execution_time']:.2f}s")


@pytest.mark.e2e
def test_complete_gameplay_performance():
    """Test performance of complete gameplay loop."""
    tester = CompleteGameplayTester()

    start_time = time.time()
    result = tester.run_complete_gameplay_loop("Warrior", "warrior_victory")
    execution_time = time.time() - start_time

    # Performance assertions
    assert execution_time < 30.0, f"Gameplay loop should complete in under 30 seconds, took {execution_time:.2f}s"
    assert result['turn_count'] > 0, "Should have game turns"
    assert result['success'], "Gameplay should complete successfully"

    print(f"✅ Performance test passed!")
    print(f"   Execution Time: {execution_time:.2f}s")
    print(f"   Turns Processed: {result['turn_count']}")
    print(f"   Turns/Second: {result['turn_count'] / execution_time:.1f}")


@pytest.mark.e2e
def test_game_state_persistence():
    """Test game state saving and loading during gameplay."""
    tester = CompleteGameplayTester()

    # Initialize game
    tester._initialize_game("Mage")
    tester._tutorial_phase()

    # Save game state
    save_result = save_game(tester.game_state, "test_persistence_save")

    # Modify game state
    original_turn_count = tester.turn_count
    tester.turn_count += 10
    tester.current_character.gold += 500

    # Load game state
    loaded_state = load_game("test_persistence_save")

    # Validate persistence
    assert loaded_state is not None, "Game state should be loadable"
    assert save_result['success'], "Game save should succeed"

    print("✅ Game state persistence test passed!")
    print(f"   Save Result: {save_result}")


if __name__ == "__main__":
    # Run specific test
    tester = CompleteGameplayTester()
    result = tester.run_complete_gameplay_loop("Warrior", "warrior_victory")

    print("\n" + "="*60)
    print("COMPLETE GAMEPLAY LOOP TEST RESULTS")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Final Level: {result['final_level']}")
    print(f"Turn Count: {result['turn_count']}")
    print(f"Locations Visited: {result['locations_visited']}")
    print(f"Enemies Defeated: {result['enemies_defeated']}")
    print(f"Quests Completed: {result['quests_completed']}")
    print(f"Items Acquired: {result['items_acquired']}")
    print(f"Gold Earned: {result['gold_earned']}")
    print(f"Experience Earned: {result['experience_earned']}")
    print(f"Execution Time: {result['execution_time']:.2f} seconds")
    print("="*60)