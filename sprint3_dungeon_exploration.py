#!/usr/bin/env python3
"""
Sprint 3: Dungeon Exploration - PLAYABLE CONTENT
FOCUS: Real gameplay experience, expanding Silverbrook world
STRATEGY: More playable content, respecting BDD foundation
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, Input, Select, ListView, ListItem, ProgressBar
from textual.screen import Screen
from textual.binding import Binding
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from typing import Dict, List, Optional, Tuple
import asyncio
import random

# Import existing systems
from core.systems.character import create_character, get_all_character_classes
from core.systems.dungeon import generate_dungeon, explore_dungeon_room
from core.systems.equipment import generate_equipment, get_all_equipment_types
from core.systems.quest import create_quest, complete_quest, update_quest_progress
from core.systems.combat import resolve_combat, calculate_damage
from core.systems.gamification import grant_experience, unlock_achievement, check_level_up
from core.systems.progression import level_up_character, improve_skill
from core.systems.game_clean import save_game, load_game

# Import existing world
from rpg_game_world import world, RPGWorld

# Enhanced world with dungeon
class EnhancedRPGWorld(RPGWorld):
    """Enhanced world with dungeon exploration"""
    
    def __init__(self):
        super().__init__()
        self.current_dungeon = None
        self.dungeon_progress = {"rooms_cleared": 0, "total_rooms": 0}
        self.combat_results = []
        self.loot_found = []
        self.dungeon_complete = False
        
        # Add Goblin Cave location
        self.locations["silverbrook_village"]["places"].append({
            "name": "Goblin Cave Entrance",
            "type": "dungeon",
            "description": "A dark cave entrance where goblins have been seen coming from.",
            "access_level": 1
        })
        
        # Enhanced NPCs with dungeon references
        self.npc_dialogues["Mayor Thompson"].update({
            "dungeon_quest": "The goblin cave is north of here. Be careful - their leader is tough!",
            "post_dungeon": "Thank you for clearing the goblin cave! Silverbrook is safe again!"
        })
        
        self.npc_dialogues["Blacksmith"].update({
            "dungeon_tips": "Take health potions into the cave. Goblins fight in groups.",
            "loot_processing": "I can forge better weapons from goblin weapons you find."
        })

# Enhanced world instance
enhanced_world = EnhancedRPGWorld()

class DungeonEntranceScreen(Screen):
    NAME = "dungeon_entrance"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🕳️ Goblin Cave Entrance", classes="location_title"),
            Static("📋 The source of Silverbrook's troubles", classes="location_subtitle"),
            
            # Warning/Preparation
            Container(
                Static("⚠️ Warning", classes="section_title"),
                Static(
                    "Mayor Thompson told you to be careful here. "
                    "Goblins fight in groups and their leader is tough. "
                    "Make sure you're prepared before entering.",
                    classes="warning_text"
                ),
                id="warning_section"
            ),
            
            # Character Status
            Container(
                Static("👤 Your Status", classes="section_title"),
                Static("", id="character_status", classes="status_display"),
                id="status_section"
            ),
            
            # Preparations
            Container(
                Static("🎒 Preparations", classes="section_title"),
                Button("🧪 Buy Health Potion (15 Gold)", id="buy_potion", variant="primary"),
                Button("🔨 Upgrade Weapon (30 Gold)", id="upgrade_weapon", variant="secondary"),
                Button("📜 Check Quest Journal", id="check_quest", variant="default"),
                id="prep_section"
            ),
            
            # Enter Dungeon
            Container(
                Button("🕳️ Enter Goblin Cave", id="enter_dungeon", variant="warning"),
                Button("🔙 Back to Village", id="back_village", variant="secondary"),
                id="action_section"
            ),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Update display when screen loads"""
        self.update_character_status()
    
    def update_character_status(self) -> None:
        """Update character status display"""
        status = self.query_one("#character_status", Static)
        
        if not enhanced_world.player_character:
            return
        
        character = enhanced_world.player_character
        
        status_text = (
            f"👤 {character.name} - {character.class_type}\n"
            f"❤️ HP: {character.hp}/{character.max_hp}\n"
            f"⚔️ Level: {character.level} | 💰 Gold: {character.gold}\n"
            f"⭐ Experience: {character.experience}"
        )
        
        status.update(status_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle dungeon entrance buttons"""
        if event.button.id == "buy_potion":
            await self.buy_health_potion()
        elif event.button.id == "upgrade_weapon":
            await self.upgrade_weapon()
        elif event.button.id == "check_quest":
            self.app.push_screen(QuestJournalScreen())
        elif event.button.id == "enter_dungeon":
            await self.enter_dungeon()
        elif event.button.id == "back_village":
            self.app.pop_screen()
    
    async def buy_health_potion(self) -> None:
        """Buy health potion"""
        character = enhanced_world.player_character
        
        if not character:
            self.app.notify("❌ No character found!", severity="error")
            return
        
        if character.gold >= 15:
            character.gold -= 15
            character.hp = min(character.max_hp, character.hp + 30)
            
            self.update_character_status()
            self.app.notify("✅ Purchased Health Potion! HP restored!", severity="success")
        else:
            self.app.notify("❌ Not enough gold for Health Potion!", severity="error")
    
    async def upgrade_weapon(self) -> None:
        """Upgrade weapon"""
        character = enhanced_world.player_character
        
        if not character:
            self.app.notify("❌ No character found!", severity="error")
            return
        
        if character.gold >= 30:
            character.gold -= 30
            # Add weapon upgrade (simplified)
            if not hasattr(character, 'weapon_damage'):
                character.weapon_damage = 8
            character.weapon_damage += 2
            
            self.update_character_status()
            self.app.notify("✅ Weapon upgraded! +2 damage!", severity="success")
        else:
            self.app.notify("❌ Not enough gold for weapon upgrade!", severity="error")
    
    async def enter_dungeon(self) -> None:
        """Enter the dungeon"""
        if not enhanced_world.player_character:
            self.app.notify("❌ Create a character first!", severity="error")
            return
        
        # Generate dungeon
        dungeon = generate_dungeon("normal")
        enhanced_world.current_dungeon = dungeon
        enhanced_world.dungeon_progress["total_rooms"] = dungeon.layout.floors * dungeon.layout.rooms_per_floor
        enhanced_world.dungeon_progress["rooms_cleared"] = 0
        
        # Update quest progress
        update_quest_progress("goblin_quest", 33)
        
        self.app.notify("🕳️ Entering Goblin Cave... Good luck!", severity="info")
        await asyncio.sleep(1)
        
        self.app.push_screen(DungeonExplorationScreen())

class DungeonExplorationScreen(Screen):
    NAME = "dungeon_exploration"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🕳️ Goblin Cave - Room 1", classes="location_title"),
            Static("📋 Dark, damp cave with goblin markings", classes="location_subtitle"),
            
            # Dungeon Layout Display
            Horizontal(
                # Room Description
                ScrollableContainer(
                    Static("📍 Current Room", classes="section_title"),
                    Static("", id="room_description", classes="room_desc"),
                    Static("", id="room_contents", classes="room_contents"),
                    id="room_panel"
                ),
                
                # Mini-map
                ScrollableContainer(
                    Static("🗺️ Cave Map", classes="section_title"),
                    Static("", id="dungeon_map", classes="dungeon_map"),
                    Static("", id="progress_display", classes="progress_info"),
                    id="map_panel"
                )
            ),
            
            # Combat Results
            Container(
                Static("⚔️ Combat Log", classes="section_title"),
                Static("", id="combat_log", classes="combat_log"),
                id="combat_panel"
            ),
            
            # Action Buttons
            Container(
                Button("🔍 Explore Current Room", id="explore_room", variant="primary"),
                Button("⚔️ Fight Enemy", id="fight_enemy", variant="warning"),
                Button("💎 Take Loot", id="take_loot", variant="success"),
                Button("🚪 Next Room", id="next_room", variant="secondary"),
                Button("🚪 Exit Dungeon", id="exit_dungeon", variant="error"),
                id="action_buttons"
            ),
            
            Footer()
        )
    
    current_room = 1
    current_room_explored = False
    current_enemy = None
    current_loot = None
    
    def on_mount(self) -> None:
        """Initialize dungeon when screen loads"""
        self.update_dungeon_display()
    
    def update_dungeon_display(self) -> None:
        """Update all dungeon display elements"""
        self.update_room_display()
        self.update_dungeon_map()
        self.update_progress()
    
    def update_room_display(self) -> None:
        """Update current room display"""
        room_desc = self.query_one("#room_description", Static)
        room_contents = self.query_one("#room_contents", Static)
        
        if self.current_room_explored:
            # Show room contents
            room_desc.update(f"📍 Room {self.current_room} - Explored")
            
            contents_text = "📋 Room contents:\n"
            if self.current_enemy:
                contents_text += f"  ⚔️ Enemy: {self.current_enemy.get('name', 'Unknown')}\n"
                contents_text += f"  💪 Strength: {self.current_enemy.get('strength', 10)}\n"
            if self.current_loot:
                contents_text += f"  💎 Loot: {self.current_loot.get('name', 'Unknown')}\n"
                contents_text += f"  💰 Value: {self.current_loot.get('gold_value', 0)} gold\n"
            
            room_contents.update(contents_text)
        else:
            room_desc.update(f"📍 Room {self.current_room} - Unexplored")
            room_contents.update("📋 Room not yet explored. Use 'Explore Current Room' to see what's here.")
    
    def update_dungeon_map(self) -> None:
        """Update dungeon mini-map"""
        dungeon_map = self.query_one("#dungeon_map", Static)
        
        if not enhanced_world.current_dungeon:
            return
        
        dungeon = enhanced_world.current_dungeon
        total_rooms = dungeon.layout.floors * dungeon.layout.rooms_per_floor
        
        # Create simple map representation
        map_text = f"🗺️ Goblin Cave Map\n\n"
        map_text += f"🏛️ Total Rooms: {total_rooms}\n"
        map_text += f"📍 Current Room: {self.current_room}\n"
        map_text += f"✅ Cleared: {enhanced_world.dungeon_progress['rooms_cleared']}\n\n"
        
        # Room status
        for room in range(1, min(11, total_rooms + 1)):
            if room < self.current_room:
                status = "✅"
            elif room == self.current_room:
                status = "📍"
            elif room <= self.current_room + 1:
                status = "❓"
            else:
                status = "🔒"
            
            map_text += f"  Room {room:02d}: {status}\n"
        
        if total_rooms > 10:
            map_text += f"  ... +{total_rooms - 10} more rooms\n"
        
        dungeon_map.update(map_text)
    
    def update_progress(self) -> None:
        """Update dungeon progress display"""
        progress = self.query_one("#progress_display", Static)
        combat_log = self.query_one("#combat_log", Static)
        
        if not enhanced_world.current_dungeon:
            return
        
        dungeon = enhanced_world.current_dungeon
        total_rooms = dungeon.layout.floors * dungeon.layout.rooms_per_floor
        cleared = enhanced_world.dungeon_progress["rooms_cleared"]
        
        progress_percent = (cleared / total_rooms) * 100
        
        progress_text = (
            f"📊 Dungeon Progress\n"
            f"📍 Cleared: {cleared}/{total_rooms} rooms\n"
            f"📈 Progress: {progress_percent:.1f}%\n"
        )
        
        if enhanced_world.dungeon_complete:
            progress_text += f"🏆 Status: COMPLETE!\n"
        
        progress.update(progress_text)
        
        # Combat log
        if enhanced_world.combat_results:
            log_text = "⚔️ Recent Combat:\n"
            for i, result in enumerate(enhanced_world.combat_results[-3:], 1):
                log_text += f"  {i}. {result.get('message', 'Combat ended')}\n"
            
            combat_log.update(log_text)
        else:
            combat_log.update("⚔️ No combat yet...")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle dungeon exploration buttons"""
        if event.button.id == "explore_room":
            await self.explore_room()
        elif event.button.id == "fight_enemy":
            await self.fight_enemy()
        elif event.button.id == "take_loot":
            await self.take_loot()
        elif event.button.id == "next_room":
            await self.next_room()
        elif event.button.id == "exit_dungeon":
            await self.exit_dungeon()
    
    async def explore_room(self) -> None:
        """Explore current room"""
        if self.current_room_explored:
            self.app.notify("ℹ️ Room already explored!", severity="info")
            return
        
        # Generate room content
        if not enhanced_world.current_dungeon:
            self.app.notify("❌ No active dungeon!", severity="error")
            return
        
        # Simulate room exploration
        dungeon = enhanced_world.current_dungeon
        
        # Roll for room content
        roll = random.randint(1, 100)
        
        if roll <= 60:  # 60% enemy
            self.current_enemy = {
                "name": f"Goblin {random.randint(1, 99)}",
                "strength": 8 + random.randint(-2, 3),
                "hp": 25 + random.randint(-5, 10),
                "attack": 10,
                "defense": 4,
                "gold_reward": 15 + random.randint(-5, 10),
                "exp_reward": 20 + random.randint(-5, 15)
            }
            self.app.notify(f"👹 Found {self.current_enemy['name']} in room!", severity="warning")
            
        elif roll <= 85:  # 25% loot
            self.current_loot = {
                "name": random.choice(["Gold Pouch", "Goblin Treasure", "Old Chest"]),
                "gold_value": 20 + random.randint(-10, 30),
                "item": random.choice(["Rusty Sword", "Health Potion", "Magic Scroll"])
            }
            self.app.notify(f"💎 Found {self.current_loot['name']} in room!", severity="success")
            
        elif roll <= 95:  # 10% trap
            damage = random.randint(5, 15)
            if enhanced_world.player_character:
                enhanced_world.player_character.hp = max(0, enhanced_world.player_character.hp - damage)
            
            self.app.notify(f"🕳️ Triggered trap! Lost {damage} HP!", severity="error")
            
        else:  # 5% empty
            self.app.notify("🏠 Empty room - time to rest!", severity="info")
        
        self.current_room_explored = True
        self.update_dungeon_display()
        
        # Grant exploration experience
        if enhanced_world.player_character:
            grant_result = grant_experience(enhanced_world.player_character.name, 10)
            self.app.notify(f"✅ {grant_result['message']}", severity="info")
    
    async def fight_enemy(self) -> None:
        """Fight current enemy"""
        if not self.current_enemy:
            self.app.notify("❌ No enemy in this room!", severity="error")
            return
        
        if not enhanced_world.player_character:
            self.app.notify("❌ No character found!", severity="error")
            return
        
        character = enhanced_world.player_character
        enemy = self.current_enemy
        
        # Create combat participants
        attacker = {
            "name": character.name,
            "attack": character.weapon_damage if hasattr(character, 'weapon_damage') else 12,
            "defense": 5,
            "hp": character.hp
        }
        
        defender = {
            "name": enemy["name"],
            "attack": enemy["attack"],
            "defense": enemy["defense"],
            "hp": enemy["hp"]
        }
        
        # Resolve combat
        combat_result = resolve_combat(attacker, defender)
        combat_result["enemy_name"] = enemy["name"]
        
        enhanced_world.combat_results.append(combat_result)
        
        if combat_result["winner"] == "character":
            # Character won
            character.hp = combat_result["character_hp"]
            character.gold += combat_result["gold_reward"]
            character.experience += combat_result["exp_reward"]
            
            self.app.notify(
                f"🏆 Victory! Gained {combat_result['gold_reward']} gold and {combat_result['exp_reward']} XP!",
                severity="success"
            )
            
            # Check level up
            level_check = check_level_up(character.name)
            if level_check["level_up"]:
                self.app.notify(f"🎉 Level Up! You are now level {level_check['new_level']}!", severity="success")
            
            # Update quest
            update_quest_progress("goblin_quest", 25)
            
            self.current_enemy = None
            
        else:
            # Character lost
            character.hp = 0
            self.app.notify(f"💀 Defeated by {enemy['name']}! Game Over!", severity="error")
            
            # Return to village
            await asyncio.sleep(2)
            self.app.pop_screen()
            self.app.push_screen(GameOverScreen())
        
        self.update_dungeon_display()
    
    async def take_loot(self) -> None:
        """Take current loot"""
        if not self.current_loot:
            self.app.notify("❌ No loot in this room!", severity="error")
            return
        
        if not enhanced_world.player_character:
            self.app.notify("❌ No character found!", severity="error")
            return
        
        character = enhanced_world.player_character
        loot = self.current_loot
        
        # Take loot
        character.gold += loot["gold_value"]
        enhanced_world.loot_found.append(loot["name"])
        
        self.app.notify(
            f"💎 Taken {loot['name']}! Gained {loot['gold_value']} gold!",
            severity="success"
        )
        
        # Add to inventory (simplified)
        if "item" in loot:
            self.app.notify(f"🎒 Found {loot['item']} in the treasure!", severity="info")
        
        self.current_loot = None
        self.update_dungeon_display()
    
    async def next_room(self) -> None:
        """Move to next room"""
        if not self.current_room_explored:
            self.app.notify("❌ Explore current room first!", severity="error")
            return
        
        if self.current_enemy:
            self.app.notify("❌ Defeat enemy before moving on!", severity="error")
            return
        
        if self.current_loot:
            self.app.notify("❌ Take loot before moving on!", severity="error")
            return
        
        # Move to next room
        self.current_room += 1
        self.current_room_explored = False
        
        # Update progress
        enhanced_world.dungeon_progress["rooms_cleared"] += 1
        update_quest_progress("goblin_quest", 20)
        
        # Check if dungeon complete
        if not enhanced_world.current_dungeon:
            return
        
        dungeon = enhanced_world.current_dungeon
        total_rooms = dungeon.layout.floors * dungeon.layout.rooms_per_floor
        
        if self.current_room > total_rooms:
            await self.complete_dungeon()
        else:
            self.app.notify(f"🚪 Moving to Room {self.current_room}...", severity="info")
            await asyncio.sleep(1)
        
        self.update_dungeon_display()
    
    async def complete_dungeon(self) -> None:
        """Complete the dungeon"""
        enhanced_world.dungeon_complete = True
        
        # Complete quest
        complete_quest("goblin_quest", enhanced_world.player_character.name)
        
        # Unlock achievement
        unlock_achievement(enhanced_world.player_character.name, "Goblin Cave Explorer")
        
        # Grant completion rewards
        if enhanced_world.player_character:
            enhanced_world.player_character.gold += 100
            enhanced_world.player_character.experience += 200
            
            grant_result = grant_experience(enhanced_world.player_character.name, 200)
            self.app.notify(f"🏆 Dungeon Complete! {grant_result['message']}", severity="success")
        
        self.app.notify("🎉 Congratulations! You cleared the Goblin Cave!", severity="success")
        
        await asyncio.sleep(3)
        
        # Return to village
        self.app.pop_screen()
        self.app.push_screen(VictoryScreen())
    
    async def exit_dungeon(self) -> None:
        """Exit the dungeon"""
        self.app.notify("🚪 Exiting Goblin Cave...", severity="info")
        await asyncio.sleep(1)
        
        # Return to village
        self.app.pop_screen()
        self.app.push_screen(GameWorldScreen())

# Import existing screens
from rpg_game_world import (
    TitleScreen, CharacterCreationScreen, GameWorldScreen,
    CharacterStatsScreen, QuestJournalScreen, InventoryScreen
)

class GameOverScreen(Screen):
    NAME = "game_over"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("💀 Game Over", classes="game_title"),
            Static("You were defeated in the Goblin Cave...", classes="game_subtitle"),
            
            Container(
                Static("📊 Your Stats", classes="section_title"),
                Static("", id="final_stats", classes="stats_display"),
                id="stats_section"
            ),
            
            Button("🔄 Try Again", id="try_again", variant="primary"),
            Button("🚪 Back to Village", id="back_village", variant="secondary"),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Display final stats"""
        if enhanced_world.player_character:
            stats = self.query_one("#final_stats", Static)
            character = enhanced_world.player_character
            
            stats_text = (
                f"👤 {character.name} - {character.class_type}\n"
                f"⚔️ Level: {character.level}\n"
                f"💰 Gold: {character.gold}\n"
                f"🏆 Rooms Cleared: {enhanced_world.dungeon_progress['rooms_cleared']}\n"
                f"💎 Loot Found: {len(enhanced_world.loot_found)}"
            )
            
            stats.update(stats_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle game over buttons"""
        if event.button.id == "try_again":
            # Reset and try again
            enhanced_world.dungeon_complete = False
            enhanced_world.dungeon_progress = {"rooms_cleared": 0, "total_rooms": 0}
            enhanced_world.combat_results = []
            enhanced_world.loot_found = []
            
            if enhanced_world.player_character:
                enhanced_world.player_character.hp = enhanced_world.player_character.max_hp
            
            self.app.pop_screen()
            self.app.push_screen(DungeonEntranceScreen())
        elif event.button.id == "back_village":
            self.app.pop_screen()
            self.app.push_screen(GameWorldScreen())

class VictoryScreen(Screen):
    NAME = "victory"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏆 Victory!", classes="game_title"),
            Static("You cleared the Goblin Cave and saved Silverbrook!", classes="game_subtitle"),
            
            Container(
                Static("🎊 Celebration", classes="section_title"),
                Static(
                    "The villagers celebrate your heroism! "
                    "Silverbrook is safe thanks to you. "
                    "You've become a true hero of the village!",
                    classes="celebration_text"
                ),
                id="celebration_section"
            ),
            
            Container(
                Static("📊 Your Rewards", classes="section_title"),
                Static("", id="rewards_display", classes="rewards_display"),
                id="rewards_section"
            ),
            
            Button("🎮 Continue Adventure", id="continue_adventure", variant="primary"),
            Button("🚪 Return to Village", id="return_village", variant="secondary"),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Display victory rewards"""
        if enhanced_world.player_character:
            rewards = self.query_one("#rewards_display", Static)
            character = enhanced_world.player_character
            
            rewards_text = (
                f"👤 Hero: {character.name}\n"
                f"⚔️ Final Level: {character.level}\n"
                f"💰 Final Gold: {character.gold}\n"
                f"⭐ Final XP: {character.experience}\n"
                f"🏆 Rooms Cleared: {enhanced_world.dungeon_progress['rooms_cleared']}\n"
                f"💎 Total Loot: {len(enhanced_world.loot_found)} items\n"
                f"🎖️ Achievement: Goblin Cave Explorer\n\n"
                f"🎉 Silverbrook is safe because of you!"
            )
            
            rewards.update(rewards_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle victory buttons"""
        if event.button.id == "continue_adventure":
            self.app.notify("🚀 More adventures coming in Sprint 4!", severity="info")
        elif event.button.id == "return_village":
            self.app.pop_screen()
            self.app.push_screen(GameWorldScreen())

class EnhancedGameWorldScreen(GameWorldScreen):
    """Enhanced game world with dungeon access"""
    
    def update_location_display(self) -> None:
        """Update location display with dungeon entrance"""
        if not enhanced_world.current_location:
            return
        
        location = enhanced_world.locations[enhanced_world.current_location]
        desc = self.query_one("#location_description", Static)
        actions = self.query_one("#available_actions", Static)
        
        # Location description
        location_info = (
            f"🏛️ {location['name']}\n"
            f"📝 {location['description']}\n\n"
            f"📍 Places to visit:\n"
        )
        
        for i, place in enumerate(location['places'], 1):
            location_info += f"  {i}. {place['name']} - {place['description']}\n"
            
            # Highlight dungeon entrance
            if place['name'] == "Goblin Cave Entrance":
                location_info += f"      ⚠️ NEW ADVENTURE AVAILABLE!\n"
        
        desc.update(location_info)
        
        # Available actions
        actions_text = "⚡ What would you like to do?\n"
        actions_text += "  • Talk to NPCs\n"
        actions_text += "  • Visit locations\n"
        actions_text += "  • 🆕 Explore Goblin Cave (NEW!)\n"
        actions_text += "  • Check your quests\n"
        actions_text += "  • Save your progress\n"
        
        # Add dungeon status
        if enhanced_world.dungeon_complete:
            actions_text += "  • ✅ Goblin Cave - CLEARED\n"
        elif enhanced_world.dungeon_progress["rooms_cleared"] > 0:
            cleared = enhanced_world.dungeon_progress["rooms_cleared"]
            actions_text += f"  • 🕳️ Goblin Cave - {cleared} rooms cleared\n"
        
        actions.update(actions_text)

class Sprint3App(App):
    """Sprint 3 - Dungeon Exploration App"""
    
    CSS = """
    .game_title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 1 0;
        font-size: 150%;
    }
    
    .game_subtitle {
        text-align: center;
        color: #888888;
        margin: 0 0 2 0;
        font-size: 110%;
    }
    
    .location_title {
        text-align: center;
        text-style: bold;
        color: #00ff00;
        margin: 1 0;
        font-size: 120%;
    }
    
    .location_subtitle {
        text-align: center;
        color: #888888;
        margin: 0 0 2 0;
        font-size: 100%;
    }
    
    .section_title {
        text-align: center;
        text-style: bold;
        color: #ffffff;
        background: #333333;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    
    .warning_text {
        color: #ffaa00;
        text-align: center;
        line-height: 1.4;
    }
    
    .status_display, .room_desc, .room_contents, .dungeon_map,
    .progress_info, .combat_log, .stats_display, .rewards_display {
        color: #cccccc;
        line-height: 1.3;
        white-space: pre;
    }
    
    .celebration_text {
        color: #00ff00;
        text-align: center;
        line-height: 1.4;
        font-style: italic;
    }
    
    #warning_section, #status_section, #prep_section, #action_section,
    #room_panel, #map_panel, #combat_panel, #action_buttons,
    #stats_section, #celebration_section, #rewards_section {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 0 1;
    }
    
    Button {
        margin: 0 1;
        min-width: 20;
    }
    
    Input, Select {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "back_to_menu", "Back to Menu"),
    ]
    
    def on_mount(self) -> None:
        self.push_screen(TitleScreen())
    
    def action_back_to_menu(self) -> None:
        self.pop_all_screens()
        self.push_screen(TitleScreen())

def main():
    """Main function for Sprint 3"""
    print("🕳️ Starting RPGSim - Sprint 3: Dungeon Exploration")
    print("🎯 PLAYABLE CONTENT EXPANSION")
    print("✅ Goblin Cave Dungeon • ✅ Real Combat • ✅ Loot & Rewards")
    print("✅ Story Progression • ✅ BDD Compliant • ✅ Playable Experience")
    
    app = Sprint3App()
    app.run()

if __name__ == "__main__":
    main()