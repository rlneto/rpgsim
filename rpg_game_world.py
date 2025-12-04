#!/usr/bin/env python3
"""
RPGSim - Actual RPG Game with City & Story
FOCUS: Real gameplay experience, not system demos
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, Input, Select, ListView, ListItem, Pretty
from textual.screen import Screen
from textual.binding import Binding
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, List, Optional, Tuple
import asyncio
import random

# Import game systems
from core.systems.character import create_character, get_all_character_classes
from core.systems.dungeon import generate_dungeon, explore_dungeon_room
from core.systems.equipment import generate_equipment
from core.systems.quest import create_quest, complete_quest, update_quest_progress
from core.systems.combat import resolve_combat, calculate_damage
from core.systems.gamification import grant_experience, unlock_achievement
from core.systems.game_clean import save_game, load_game

# Game World Data
class RPGWorld:
    """Central world state and story"""
    
    def __init__(self):
        self.player_character = None
        self.current_location = "silverbrook_village"
        self.game_time = 0
        self.story_progress = 0
        self.game_started = False
        
        # World locations
        self.locations = {
            "silverbrook_village": {
                "name": "Silverbrook Village",
                "type": "village",
                "description": "A peaceful village surrounded by misty mountains. The starting point of your adventure.",
                "places": [
                    {"name": "Tavern", "type": "shop", "description": "Local inn with drinks and rumors"},
                    {"name": "Blacksmith", "type": "shop", "description": "Weapon and armor shop"},
                    {"name": "Town Square", "type": "hub", "description": "Central meeting place"},
                    {"name": "Mayor's House", "type": "quest", "description": "Office of the village mayor"}
                ],
                "npcs": [
                    {"name": "Bartender", "type": "shopkeeper", "location": "Tavern"},
                    {"name": "Blacksmith", "type": "shopkeeper", "location": "Blacksmith"},
                    {"name": "Mayor Thompson", "type": "quest_giver", "location": "Mayor's House"},
                    {"name": "Old Man", "type": "lore", "location": "Town Square"},
                    {"name": "Village Guard", "type": "guard", "location": "Town Square"}
                ]
            }
        }
        
        # Story quests
        self.main_questline = {
            "intro": {
                "title": "A New Beginning",
                "description": "You've arrived in Silverbrook Village as a newcomer. The mayor wants to meet you.",
                "objectives": [
                    {"description": "Talk to Mayor Thompson", "completed": False},
                    {"description": "Learn about the village problems", "completed": False}
                ],
                "rewards": {"exp": 50, "gold": 20, "item": "Village Welcome Package"},
                "status": "active"
            },
            "first_problem": {
                "title": "Goblin Troubles",
                "description": "The village is being harassed by goblins from the nearby caves. The mayor needs your help.",
                "objectives": [
                    {"description": "Visit Goblin Cave", "completed": False},
                    {"description": "Defeat Goblin Leader", "completed": False},
                    {"description": "Return to Mayor", "completed": False}
                ],
                "rewards": {"exp": 100, "gold": 50, "item": "Goblin Slayer Badge"},
                "status": "locked"
            }
        }
        
        # NPCs with dialogue
        self.npc_dialogues = {
            "Mayor Thompson": {
                "greeting": "Welcome to Silverbrook, adventurer! I'm Mayor Thompson.",
                "intro_quest": "I'm glad you're here. We're having some... problems. Could you help us?",
                "story": "For weeks, goblins have been raiding our supplies. They come from the old caves north of here.",
                "goblin_info": "Be careful in those caves. The goblin leader is tougher than he looks.",
                "thanks": "Thank you for helping our village! Here's your reward."
            },
            "Bartender": {
                "greeting": "Welcome to the Silver Tavern! What can I get for you?",
                "rumors": "I hear strange noises from the old ruins at night...",
                "drinks": "We have ale, mead, and water. What's your choice?",
                "lore": "This village has seen many adventurers like you. Most move on to the big cities."
            },
            "Blacksmith": {
                "greeting": "Need weapons or armor? I'm the best blacksmith in the region!",
                "shop": "I have swords, axes, shields, and armor. Take a look at my wares.",
                "advice": "Keep your weapons sharp and your armor maintained. It could save your life.",
                "goblin_weakness": "Goblins fear bright light and loud noises. Use that to your advantage."
            },
            "Old Man": {
                "greeting": "Another young adventurer... I've seen many come and go.",
                "wisdom": "The path of a hero is not an easy one. Remember why you started.",
                "history": "Silverbrook was founded by refugees from the Great War 50 years ago.",
                "prophecy": "There's an old prophecy about a hero who will save this land..."
            }
        }
        
        # Shop inventories
        self.shop_inventories = {
            "Tavern": {
                "type": "drinks",
                "items": [
                    {"name": "Ale", "price": 5, "effect": "+10 HP"},
                    {"name": "Mead", "price": 8, "effect": "+15 HP"},
                    {"name": "Water", "price": 2, "effect": "+5 HP"}
                ]
            },
            "Blacksmith": {
                "type": "weapons_armor",
                "items": [
                    {"name": "Iron Sword", "price": 50, "type": "weapon", "stats": {"damage": 8}},
                    {"name": "Iron Shield", "price": 30, "type": "armor", "stats": {"defense": 5}},
                    {"name": "Leather Armor", "price": 40, "type": "armor", "stats": {"defense": 6}},
                    {"name": "Health Potion", "price": 15, "type": "consumable", "effect": "+30 HP"}
                ]
            }
        }

# Global world instance
world = RPGWorld()

class TitleScreen(Screen):
    NAME = "title"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏰 RPGSim - Silverbrook Chronicles", classes="game_title"),
            Static("📖 An Epic Adventure Begins", classes="game_subtitle"),
            
            # ASCII Art Title
            Container(
                Static("""
    🏰         RPGSim         🏰
  ╔══════════════════════════════╗
  ║   Silverbrook Chronicles   ║
  ╚══════════════════════════════╝
                """, id="ascii_title", classes="ascii_art"),
                id="title_art"
            ),
            
            # Story Intro
            Container(
                Static("📜 Story", classes="section_title"),
                Static(
                    "You arrive in the peaceful village of Silverbrook, "
                    "seeking adventure and fortune. But the village has problems... "
                    "goblins raid from nearby caves, strange noises come from ancient ruins, "
                    "and the mayor needs a hero. Your journey begins here.",
                    id="story_text", classes="story_text"
                ),
                id="story_section"
            ),
            
            # Menu Options
            Container(
                Button("🎮 New Game", id="new_game", variant="primary"),
                Button("📜 Continue Game", id="continue_game", variant="secondary"),
                Button("💾 Load Save", id="load_game", variant="default"),
                Button("🚪 Exit", id="exit", variant="error"),
                id="menu_options"
            ),
            
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle title menu options"""
        if event.button.id == "new_game":
            self.app.push_screen(CharacterCreationScreen())
        elif event.button.id == "continue_game":
            if world.game_started:
                self.app.push_screen(GameWorldScreen())
            else:
                self.app.notify("❌ No saved game found!", severity="error")
        elif event.button.id == "load_game":
            # TODO: Implement save/load
            self.app.notify("📦 Save system coming soon!", severity="info")
        elif event.button.id == "exit":
            self.app.exit()

class CharacterCreationScreen(Screen):
    NAME = "character_creation"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("👤 Create Your Hero", classes="game_title"),
            Static("📋 Choose your path in Silverbrook", classes="game_subtitle"),
            
            # Character Creation Form
            Container(
                Static("⚙️ Hero Information", classes="section_title"),
                Input(placeholder="Enter your hero's name...", id="name_input"),
                Select(
                    options=get_all_character_classes(),
                    id="class_select",
                    value="Warrior"
                ),
                Static("", id="class_preview"),
                Button("🎯 Create Hero", id="create_hero", variant="primary"),
                Button("🎲 Random Hero", id="random_hero", variant="secondary"),
                id="creation_form"
            ),
            
            Footer()
        )
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Update class preview"""
        self.update_class_preview(event.value)
    
    def update_class_preview(self, class_name: str) -> None:
        """Update class description preview"""
        class_descriptions = {
            "Warrior": "Strong and brave. Masters of combat and weapons.",
            "Mage": "Intelligent and wise. Wielders of arcane magic.",
            "Rogue": "Agile and stealthy. Experts in shadows and precision.",
            "Cleric": "Devoted and holy. Healers and protectors.",
            "Ranger": "Skilled and patient. Masters of archery and survival."
        }
        
        preview = self.query_one("#class_preview", Static)
        description = class_descriptions.get(class_name, "A brave adventurer ready for challenges.")
        preview.update(f"📖 {description}")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle character creation"""
        if event.button.id == "create_hero":
            await self.create_hero()
        elif event.button.id == "random_hero":
            await self.random_hero()
    
    async def create_hero(self) -> None:
        """Create character from form"""
        name_input = self.query_one("#name_input", Input)
        class_select = self.query_one("#class_select", Select)
        
        name = name_input.value.strip()
        character_class = class_select.value
        
        if not name:
            self.app.notify("❌ Please enter a name for your hero!", severity="error")
            return
        
        try:
            character = create_character(name, character_class)
            world.player_character = character
            world.game_started = True
            
            self.app.notify(f"✅ Welcome to Silverbrook, {name} the {character_class}!", severity="success")
            await asyncio.sleep(1)
            
            self.app.push_screen(GameWorldScreen())
        except Exception as e:
            self.app.notify(f"❌ Error creating hero: {str(e)}", severity="error")
    
    async def random_hero(self) -> None:
        """Generate random character"""
        names = ["Marcus", "Elena", "Thorin", "Lyra", "Gareth", "Isabella", "Roland", "Aria"]
        character_class = random.choice([cls[0] for cls in get_all_character_classes()])
        
        name = random.choice(names)
        
        # Update form
        name_input = self.query_one("#name_input", Input)
        class_select = self.query_one("#class_select", Select)
        
        name_input.value = name
        class_select.value = character_class
        
        self.update_class_preview(character_class)
        self.app.notify(f"🎲 Randomized: {name} the {character_class}!", severity="info")

class GameWorldScreen(Screen):
    NAME = "game_world"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏰 Silverbrook Village", classes="location_title"),
            
            # Character Status Bar
            Container(
                Static("", id="character_status", classes="status_bar"),
                id="status_container"
            ),
            
            # Main Game Area
            Horizontal(
                # Location Description
                ScrollableContainer(
                    Static("📍 Current Location", classes="section_title"),
                    Static("", id="location_description", classes="location_desc"),
                    Static("", id="available_actions", classes="actions_list"),
                    id="location_panel"
                ),
                
                # NPCs and Interactions
                ScrollableContainer(
                    Static("👥 People Here", classes="section_title"),
                    Static("", id="npcs_here", classes="npcs_list"),
                    Static("", id="dialogue_box", classes="dialogue_box"),
                    id="npc_panel"
                )
            ),
            
            # Action Buttons
            Container(
                Static("⚡ Actions", classes="section_title"),
                Horizontal(
                    Button("🗺️ Explore", id="explore_btn", variant="primary"),
                    Button("👤 Character", id="character_btn", variant="secondary"),
                    Button("📜 Quests", id="quests_btn", variant="secondary"),
                    Button("🎒 Inventory", id="inventory_btn", variant="default"),
                ),
                Horizontal(
                    Button("💾 Save", id="save_btn", variant="default"),
                    Button("🚪 Exit", id="exit_btn", variant="error"),
                ),
                id="action_buttons"
            ),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Initialize game world when screen loads"""
        self.update_game_display()
    
    def update_game_display(self) -> None:
        """Update all game display elements"""
        self.update_character_status()
        self.update_location_display()
        self.update_npcs_display()
    
    def update_character_status(self) -> None:
        """Update character status bar"""
        if not world.player_character:
            return
        
        status = self.query_one("#character_status", Static)
        
        character = world.player_character
        status_text = (
            f"👤 {character.name} | "
            f"⚔️ {character.class_type} | "
            f"🏆 Level {character.level} | "
            f"❤️ HP: {character.hp}/{character.max_hp} | "
            f"💰 Gold: {character.gold} | "
            f"⭐ XP: {character.experience}"
        )
        
        status.update(status_text)
    
    def update_location_display(self) -> None:
        """Update current location display"""
        if not world.current_location:
            return
        
        location = world.locations[world.current_location]
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
        
        desc.update(location_info)
        
        # Available actions
        actions_text = "⚡ What would you like to do?\n"
        actions_text += "  • Talk to NPCs\n"
        actions_text += "  • Visit locations\n"
        actions_text += "  • Explore the area\n"
        actions_text += "  • Check your quests\n"
        
        actions.update(actions_text)
    
    def update_npcs_display(self) -> None:
        """Update NPCs display"""
        if not world.current_location:
            return
        
        location = world.locations[world.current_location]
        npcs = self.query_one("#npcs_here", Static)
        dialogue = self.query_one("#dialogue_box", Static)
        
        # NPCs list
        npcs_text = "👥 People you can talk to:\n"
        for npc in location['npcs']:
            npcs_text += f"  • {npc['name']} - {npc['type']}\n"
        
        npcs.update(npcs_text)
        
        # Dialogue box
        dialogue.update("💬 Talk to someone to see their dialogue...")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle action buttons"""
        if event.button.id == "explore_btn":
            await self.explore_area()
        elif event.button.id == "character_btn":
            self.app.push_screen(CharacterStatsScreen())
        elif event.button.id == "quests_btn":
            self.app.push_screen(QuestJournalScreen())
        elif event.button.id == "inventory_btn":
            self.app.push_screen(InventoryScreen())
        elif event.button.id == "save_btn":
            await self.save_game()
        elif event.button.id == "exit_btn":
            self.app.push_screen(TitleScreen())
    
    async def explore_area(self) -> None:
        """Explore current area"""
        location = world.locations[world.current_location]
        
        # Show exploration results
        if world.current_location == "silverbrook_village":
            # Show NPC interactions
            npcs = location['npcs']
            npc = random.choice(npcs)
            
            dialogue = self.query_one("#dialogue_box", Static)
            
            if npc['name'] in world.npc_dialogues:
                npc_dialogue = world.npc_dialogues[npc['name']]
                greeting = npc_dialogue['greeting']
                
                dialogue.update(
                    f"💬 {npc['name']}:\n"
                    f"\"{greeting}\"\n\n"
                    f"📍 Location: {npc['location']}"
                )
                
                # Give some experience for talking
                if world.player_character:
                    grant_result = grant_experience(world.player_character.name, 5)
                    self.update_character_status()
    
    async def save_game(self) -> None:
        """Save current game"""
        if world.player_character:
            save_data = {
                "character": world.player_character.name,
                "location": world.current_location,
                "story_progress": world.story_progress,
                "game_time": world.game_time
            }
            
            result = save_game("silverbrook_save", save_data)
            self.app.notify(f"✅ {result['message']}", severity="success")
        else:
            self.app.notify("❌ No game to save!", severity="error")

class CharacterStatsScreen(Screen):
    NAME = "character_stats"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("👤 Character Information", classes="game_title"),
            
            Container(
                Static("", id="character_details", classes="character_info"),
                id="character_panel"
            ),
            
            Button("🔙 Back to Game", id="back_btn", variant="primary"),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Display character stats when screen loads"""
        self.display_character_stats()
    
    def display_character_stats(self) -> None:
        """Display detailed character information"""
        if not world.player_character:
            return
        
        details = self.query_one("#character_details", Static)
        character = world.player_character
        
        # Create character info
        info_text = f"""
👤 Name: {character.name}
⚔️ Class: {character.class_type}
🏆 Level: {character.level}
❤️ HP: {character.hp}/{character.max_hp}
💰 Gold: {character.gold}
⭐ Experience: {character.experience}

📊 Character Stats:
"""
        
        # Add stats if available
        if hasattr(character, 'stats'):
            stats = character.stats
            info_text += f"  • Strength: {stats.strength}\n"
            info_text += f"  • Dexterity: {stats.dexterity}\n"
            info_text += f"  • Intelligence: {stats.intelligence}\n"
            info_text += f"  • Constitution: {stats.constitution}\n"
        
        # Add skills if available
        if hasattr(character, 'skills'):
            info_text += f"\n🎯 Skills:\n"
            for skill in character.skills:
                info_text += f"  • {skill}\n"
        
        details.update(info_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle back button"""
        if event.button.id == "back_btn":
            self.app.pop_screen()

class QuestJournalScreen(Screen):
    NAME = "quest_journal"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("📜 Quest Journal", classes="game_title"),
            
            Container(
                Static("", id="quest_list", classes="quest_info"),
                id="quest_panel"
            ),
            
            Button("🔙 Back to Game", id="back_btn", variant="primary"),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Display quest journal when screen loads"""
        self.display_quests()
    
    def display_quests(self) -> None:
        """Display active and completed quests"""
        quest_list = self.query_one("#quest_list", Static)
        
        info_text = "📖 Active Quests:\n\n"
        
        # Display main questline
        for quest_key, quest in world.main_questline.items():
            if quest['status'] == 'active':
                info_text += f"🔶 {quest['title']}\n"
                info_text += f"   {quest['description']}\n\n"
                info_text += f"   Objectives:\n"
                
                for obj in quest['objectives']:
                    status = "✅" if obj['completed'] else "❌"
                    info_text += f"     {status} {obj['description']}\n"
                
                info_text += f"\n   Rewards: {quest['rewards']['exp']} XP, {quest['rewards']['gold']} Gold\n\n"
            elif quest['status'] == 'completed':
                info_text += f"✅ {quest['title']} - COMPLETED\n\n"
        
        if info_text == "📖 Active Quests:\n\n":
            info_text += "No active quests. Talk to the Mayor to get started!\n"
        
        quest_list.update(info_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle back button"""
        if event.button.id == "back_btn":
            self.app.pop_screen()

class InventoryScreen(Screen):
    NAME = "inventory"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎒 Inventory", classes="game_title"),
            
            Container(
                Static("", id="inventory_display", classes="inventory_info"),
                id="inventory_panel"
            ),
            
            Button("🔙 Back to Game", id="back_btn", variant="primary"),
            
            Footer()
        )
    
    def on_mount(self) -> None:
        """Display inventory when screen loads"""
        self.display_inventory()
    
    def display_inventory(self) -> None:
        """Display character inventory"""
        inventory_display = self.query_one("#inventory_display", Static)
        
        if not world.player_character:
            return
        
        character = world.player_character
        
        info_text = f"💰 Gold: {character.gold}\n\n"
        info_text += "🎒 Items:\n"
        
        # Simple inventory display
        if hasattr(character, 'inventory') and character.inventory:
            for item in character.inventory:
                info_text += f"  • {item}\n"
        else:
            info_text += "  (Empty inventory)\n"
        
        info_text += f"\n⚔️ Equipped Items:\n"
        info_text += f"  • Basic Starting Equipment\n"
        
        inventory_display.update(info_text)
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle back button"""
        if event.button.id == "back_btn":
            self.app.pop_screen()

class RPGGameApp(App):
    """Main RPG Game Application"""
    
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
    
    .section_title {
        text-align: center;
        text-style: bold;
        color: #ffffff;
        background: #333333;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    
    .ascii_art {
        background: #1a1a1a;
        border: solid #444444;
        padding: 2;
        margin: 0 1;
        height: auto;
        text-align: center;
        color: #00ff00;
        font-family: monospace;
    }
    
    .story_text {
        text-align: justify;
        color: #cccccc;
        margin: 0 1;
        line-height: 1.4;
    }
    
    .status_bar {
        background: #1a1a1a;
        border: solid #444444;
        padding: 1;
        margin: 0 0 1 0;
        color: #ffffff;
        text-style: bold;
    }
    
    .location_desc {
        color: #cccccc;
        line-height: 1.3;
        white-space: pre;
    }
    
    .actions_list {
        color: #888888;
        margin-top: 1;
        white-space: pre;
    }
    
    .npcs_list {
        color: #cccccc;
        white-space: pre;
    }
    
    .dialogue_box {
        background: #222222;
        border: solid #666666;
        padding: 1;
        margin-top: 1;
        color: #ffff00;
        white-space: pre;
        font-style: italic;
    }
    
    .character_info, .quest_info, .inventory_info {
        color: #cccccc;
        line-height: 1.3;
        white-space: pre;
    }
    
    #creation_form, #location_panel, #npc_panel, #action_buttons,
    #character_panel, #quest_panel, #inventory_panel {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 0 1;
    }
    
    #story_section, #menu_options {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 1 1;
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
        Binding("escape", "back_to_game", "Back to Game"),
    ]
    
    def on_mount(self) -> None:
        """Start with title screen"""
        self.push_screen(TitleScreen())
    
    def action_back_to_game(self) -> None:
        """Go back to main game screen"""
        if world.game_started:
            self.pop_all_screens()
            self.push_screen(GameWorldScreen())
        else:
            self.pop_all_screens()
            self.push_screen(TitleScreen())

def main():
    """Main function for RPG game"""
    print("🎮 Starting RPGSim - Silverbrook Chronicles")
    print("🏰 A Real RPG Game with City, Story, and Adventure")
    print("✅ Character Creation • ✅ Village Hub • ✅ NPCs & Dialogues")
    print("✅ Quest System • ✅ Story Progression • ✅ Immersive World")
    
    app = RPGGameApp()
    app.run()

if __name__ == "__main__":
    main()