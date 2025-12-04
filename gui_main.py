#!/usr/bin/env python3
"""
RPGSim - Graphical Main Entry Point
DEMO: Single City Experience
SPRINT 1: GUI Foundation
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Label, Input, Select, Static, ProgressBar
from textual.reactive import reactive
from textual.screen import Screen
from textual.binding import Binding
from rich.console import Console
import asyncio
from datetime import datetime
import random

# Import modular systems
from core.systems.character.facade import create_character, get_all_character_classes
from core.systems.world.facade import _world_system

console = Console()

class CharacterCreationScreen(Screen):
    """Character creation GUI screen"""
    
    NAME = "character_creation"  # Define explicit screen ID
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("enter", "create_character", "Create"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Static("🎮 RPGSim - Character Creation", classes="title"),
            Container(
                Label("Character Name:"),
                Input(placeholder="Enter your character name...", id="name_input"),
                Label("Class Selection:"),
                Select(
                    options=get_all_character_classes(),
                    id="class_select",
                    value="Warrior"
                ),
                Label("Difficulty:"),
                Select(
                    options=[
                        ("Normal", "normal"),
                        ("Hard", "hard"), 
                        ("Nightmare", "nightmare")
                    ],
                    id="difficulty_select",
                    value="normal"
                ),
                Label("Class Stats:"),
                Static("Strength: 10 | Dexterity: 10 | Intelligence: 10", id="class_stats"),
                ProgressBar(total=100, show_eta=False, id="creation_progress"),
                Horizontal(
                    Button("Create Character", id="create_btn", variant="primary"),
                    Button("Cancel", id="cancel_btn", variant="error"),
                    classes="button-row"
                ),
                id="creation_form"
            ),
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "create_btn":
            await self.create_character()
        elif event.button.id == "cancel_btn":
            self.app.pop_screen()
    
    async def create_character(self) -> None:
        """Create character from form data"""
        name_input = self.query_one("#name_input", Input)
        class_select = self.query_one("#class_select", Select)
        difficulty_select = self.query_one("#difficulty_select", Select)
        progress_bar = self.query_one("#creation_progress", ProgressBar)
        
        name = name_input.value.strip()
        character_class = class_select.value
        difficulty = difficulty_select.value
        
        # Validation
        if not name:
            self.app.notify("Please enter a character name!", severity="error")
            return
        
        if len(name) < 3:
            self.app.notify("Name must be at least 3 characters!", severity="error")
            return
            
        if len(name) > 50:
            self.app.notify("Name is too long! (max 50 characters)", severity="error")
            return
        
        # Show progress
        progress_bar.advance(25)
        self.app.notify(f"Creating {character_class} {name}...", severity="info")
        await asyncio.sleep(0.5)
        
        progress_bar.advance(50)
        await asyncio.sleep(0.5)
        
        # Create character using modular system
        try:
            character = create_character(name, character_class)
            if character:
                progress_bar.advance(25)
                self.app.notify(f"✅ Created {character_class} {name}!", severity="success")
                await asyncio.sleep(0.5)
                self.app.pop_screen()
                # Switch to game screen with character data
                self.app.push_screen(GameScreen(character))
            else:
                self.app.notify(f"❌ Failed to create {character_class}!", severity="error")
        except Exception as e:
            self.app.notify(f"⚠️ Error: {str(e)}", severity="error")
        finally:
            progress_bar.progress = 0


class GameScreen(Screen):
    """Main game screen with city, dungeon, quests"""
    
    NAME = "game_screen"  # Define explicit screen ID
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("i", "toggle_inventory", "Inventory"),
        Binding("m", "toggle_map", "Map"),
        Binding("j", "toggle_quest_journal", "Quests"),
    ]
    
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.world_system = _world_system
        
    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Static(f"🏰 {self.character.name} - {self.character.class_type}", classes="title"),
            Container(
                # Character Status Panel
                Container(
                    Static("⚔️ Character Status", classes="panel-title"),
                    Label(f"Level: {self.character.level}"),
                    Label(f"HP: {self.character.hp}/{self.character.max_hp}"),
                    ProgressBar(total=self.character.max_hp, show_eta=False, current=self.character.hp),
                    Label(f"Gold: {self.character.gold}"),
                    Label(f"Location: Starting City"),
                    id="character_panel"
                ),
                # City Actions
                Container(
                    Static("🏙️ City Actions", classes="panel-title"),
                    Button("Visit Shop", id="shop_btn", variant="primary"),
                    Button("Enter Dungeon", id="dungeon_btn", variant="warning"),
                    Button("Talk to NPCs", id="npc_btn", variant="success"),
                    Button("Rest at Inn", id="rest_btn", variant="secondary"),
                    id="city_actions"
                ),
                # Quest Progress
                Container(
                    Static("📜 Quest Progress", classes="panel-title"),
                    Label("Active Quests: 2/3"),
                    Label("Main Quest: Explore the Dungeon"),
                    Label("Side Quest: Help the Merchant"),
                    Label("Daily Quest: Defeat 5 Enemies"),
                    id="quest_panel"
                ),
                classes="game-layout"
            ),
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle game actions"""
        if event.button.id == "shop_btn":
            await self.open_shop()
        elif event.button.id == "dungeon_btn":
            await self.enter_dungeon()
        elif event.button.id == "npc_btn":
            await self.talk_to_npcs()
        elif event.button.id == "rest_btn":
            await self.rest_at_inn()
    
    async def open_shop(self) -> None:
        """Open shop interface"""
        self.app.notify("🛒 Opening shop interface...", severity="info")
        # TODO: Implement shop screen
        
    async def enter_dungeon(self) -> None:
        """Enter dungeon"""
        if self.character.gold >= 50:
            self.app.notify("🏰 Entering Dungeon...", severity="warning")
            self.character.gold -= 50
            # Update gold display
            panel = self.query_one("#character_panel")
            labels = panel.query("Label")
            for label in labels:
                if "Gold:" in str(label.renderable):
                    label.update(f"Gold: {self.character.gold}")
            # TODO: Implement dungeon screen
            self.app.push_screen(DungeonScreen(self.character))
        else:
            self.app.notify("💰 Need 50 gold to enter dungeon!", severity="error")
    
    async def talk_to_npcs(self) -> None:
        """Talk to NPCs"""
        self.app.notify("💬 Talking to city NPCs...", severity="info")
        # TODO: Implement NPC dialogue
    
    async def rest_at_inn(self) -> None:
        """Rest at inn"""
        if self.character.gold >= 10:
            self.character.gold -= 10
            self.character.hp = self.character.max_hp
            self.app.notify("💤 Rested at inn! HP fully restored.", severity="success")
            # Update UI dynamically
            panel = self.query_one("#character_panel")
            labels = panel.query("Label")
            for label in labels:
                if "HP:" in str(label.renderable):
                    label.update(f"HP: {self.character.hp}/{self.character.max_hp}")
                    hp_bar = panel.query("ProgressBar")
                    if hp_bar:
                        hp_bar[0].current = self.character.hp
                elif "Gold:" in str(label.renderable):
                    label.update(f"Gold: {self.character.gold}")
        else:
            self.app.notify("💰 Need 10 gold to rest at inn!", severity="error")


class DungeonScreen(Screen):
    """Dungeon exploration screen"""
    
    NAME = "dungeon_screen"  # Define explicit screen ID
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("w", "move_forward", "Forward"),
        Binding("s", "move_backward", "Back"),
        Binding("a", "turn_left", "Left"),
        Binding("d", "turn_right", "Right"),
    ]
    
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.dungeon_floor = 1
        self.enemies_defeated = 0
        
    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Static(f"🏰 Dungeon Floor {self.dungeon_floor}", classes="title"),
            Container(
                Static("⚔️ Dungeon Status", classes="panel-title"),
                Label(f"Floor: {self.dungeon_floor}/3"),
                Label(f"Enemies Defeated: {self.enemies_defeated}"),
                Label(f"Character HP: {self.character.hp}/{self.character.max_hp}"),
                ProgressBar(total=self.character.max_hp, show_eta=False, current=self.character.hp),
                id="dungeon_status"
            ),
            Container(
                Static("🗺️ Dungeon View", classes="panel-title"),
                Static("🏛️ You see a dark hallway ahead...", id="dungeon_view"),
                Static("🦜 You hear echo from the distance..."),
                id="dungeon_info"
            ),
            Container(
                Static("⚡ Actions", classes="panel-title"),
                Button("Move Forward", id="move_btn", variant="primary"),
                Button("Search", id="search_btn", variant="secondary"),
                Button("Rest", id="dungeon_rest_btn", variant="success"),
                Button("Escape Dungeon", id="escape_btn", variant="error"),
                id="dungeon_actions"
            ),
            classes="dungeon-layout"
        ),
        Footer()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle dungeon actions"""
        if event.button.id == "move_btn":
            await self.move_forward()
        elif event.button.id == "search_btn":
            await self.search_area()
        elif event.button.id == "dungeon_rest_btn":
            await self.dungeon_rest()
        elif event.button.id == "escape_btn":
            await self.escape_dungeon()
    
    async def move_forward(self) -> None:
        """Move forward in dungeon"""
        if random.random() < 0.4:  # 40% enemy encounter
            await self.combat_encounter()
        else:
            self.app.notify("🚶 You move deeper into the dungeon...", severity="info")
            dungeon_view = self.query_one("#dungeon_view")
            dungeon_view.update("🏛️ The corridor continues ahead...")
    
    async def combat_encounter(self) -> None:
        """Random combat encounter"""
        enemies = ["Goblin", "Skeleton", "Bat", "Spider"]
        enemy = random.choice(enemies)
        self.app.notify(f"⚔️ Combat! You encountered a {enemy}!", severity="warning")
        
        # Simulate combat
        if random.random() < 0.7:  # 70% win chance
            self.character.hp -= random.randint(5, 15)
            self.enemies_defeated += 1
            self.app.notify(f"✅ Victory! You defeated the {enemy}!", severity="success")
            self.app.notify(f"🎁 Found {random.randint(10, 30)} gold!", severity="success")
            self.character.gold += random.randint(10, 30)
        else:
            self.character.hp -= random.randint(20, 40)
            self.app.notify(f"💔 Defeat! The {enemy} was too strong!", severity="error")
        
        # Check for floor completion
        if self.enemies_defeated >= 2:
            await self.advance_floor()
        
        # Check for death
        if self.character.hp <= 0:
            self.app.notify("💀 You have been defeated! Escaping dungeon...", severity="error")
            self.app.pop_screen()
    
    async def advance_floor(self) -> None:
        """Advance to next floor"""
        if self.dungeon_floor < 3:
            self.dungeon_floor += 1
            self.enemies_defeated = 0
            self.app.notify(f"🎊 Advanced to Floor {self.dungeon_floor}!", severity="success")
            
            # Update floor display
            floor_label = self.query_one("#dungeon_status").query("Label")[0]
            floor_label.update(f"Floor: {self.dungeon_floor}/3")
            
            dungeon_view = self.query_one("#dungeon_view")
            dungeon_view.update("🏛️ You descend deeper into darkness...")
            
            if self.dungeon_floor == 3:
                self.app.notify("👑 Boss Floor! Prepare for battle!", severity="warning")
        else:
            # Boss battle
            await self.boss_battle()
    
    async def boss_battle(self) -> None:
        """Final boss battle"""
        self.app.notify("👑 BOSS BATTLE: Dungeon Lord!", severity="error")
        
        # Simulate epic boss fight
        boss_hp = 100
        player_damage = 0
        
        while boss_hp > 0 and self.character.hp > 0:
            player_damage = random.randint(15, 35)
            boss_hp -= player_damage
            self.character.hp -= random.randint(10, 25)
            
            self.app.notify(f"⚔️ You deal {player_damage} damage! Boss HP: {max(0, boss_hp)}", severity="info")
            
            if self.character.hp <= 0:
                break
        
        if boss_hp <= 0:
            self.app.notify("🎉 VICTORY! You defeated the Dungeon Lord!", severity="success")
            self.app.notify("🏆 Dungeon Complete! Quest Fulfilled!", severity="success")
            self.app.notify("💰 Treasure found: 500 gold!", severity="success")
            self.character.gold += 500
            self.app.pop_screen()  # Return to city
        else:
            self.app.notify("💀 Defeated! Escaping dungeon...", severity="error")
            self.app.pop_screen()
    
    async def search_area(self) -> None:
        """Search current area"""
        if random.random() < 0.3:
            gold_found = random.randint(5, 20)
            self.character.gold += gold_found
            self.app.notify(f"🎁 Found {gold_found} gold in treasure chest!", severity="success")
        else:
            self.app.notify("🔍 Nothing found here...", severity="info")
    
    async def dungeon_rest(self) -> None:
        """Rest in dungeon"""
        if random.random() < 0.5:
            heal_amount = random.randint(10, 20)
            self.character.hp = min(self.character.max_hp, self.character.hp + heal_amount)
            self.app.notify(f"💤 Rested! Healed {heal_amount} HP", severity="success")
        else:
            self.app.notify("👹 Disturbed by monsters while resting!", severity="error")
            self.character.hp -= 5
    
    async def escape_dungeon(self) -> None:
        """Escape from dungeon"""
        self.app.notify("🚪 Escaping dungeon...", severity="warning")
        await asyncio.sleep(1)
        self.app.pop_screen()


class MainMenuScreen(Screen):
    """Main menu screen"""
    
    NAME = "main_menu"  # Define explicit screen ID
    
    BINDINGS = [
        Binding("escape", "app.bell", "Bell"),
        Binding("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Static("🎮 RPGSim", classes="game-title"),
            Static("🏰 Epic Journey RPG", classes="subtitle"),
            Static("Demo: Single City Experience", classes="version"),
            Static("Sprint 1: GUI Foundation", classes="version"),
            Container(
                Button("New Game", id="new_game_btn", variant="primary"),
                Button("Continue", id="continue_btn", variant="default"),
                Button("Settings", id="settings_btn", variant="default"),
                Button("Exit", id="exit_btn", variant="error"),
                id="menu_buttons"
            ),
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle menu actions"""
        if event.button.id == "new_game_btn":
            self.app.push_screen(CharacterCreationScreen())
        elif event.button.id == "continue_btn":
            self.app.notify("No saved game found!", severity="warning")
        elif event.button.id == "settings_btn":
            self.app.notify("Settings coming soon!", severity="info")
        elif event.button.id == "exit_btn":
            self.app.bell()
            self.app.exit()


class RPGSimApp(App):
    """Main RPGSim Application"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 1 0;
    }
    
    .game-title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 2 0;
    }
    
    .subtitle {
        text-align: center;
        color: #888888;
        margin: 0 0 1 0;
    }
    
    .version {
        text-align: center;
        color: #666666;
        margin: 0 0 2 0;
    }
    
    .panel-title {
        text-align: center;
        text-style: bold;
        color: #ffffff;
        background: #333333;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    
    .game-layout {
        display: block;
        margin: 1;
        height: 100%;
    }
    
    .dungeon-layout {
        display: block;
        margin: 1;
        height: 100%;
    }
    
    #character_panel, #city_actions, #quest_panel,
    #dungeon_status, #dungeon_info, #dungeon_actions {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 0 1;
        height: 100%;
    }
    
    #menu_buttons {
        width: 30;
        margin: 0 1;
    }
    
    .button-row {
        width: 50;
        margin: 1 1;
    }
    
    #creation_form {
        width: 60;
        margin: 0 1;
        padding: 2;
    }
    
    Button {
        margin: 0 1;
        min-width: 15;
    }
    
    ProgressBar {
        width: 100%;
        height: 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True, priority=True),
    ]
    
    def on_mount(self) -> None:
        """Initialize app"""
        self.title = "RPGSim - Epic Journey RPG"
        self.sub_title = "Demo: Single City Experience"
        # Push main menu screen
        self.push_screen(MainMenuScreen())


def main():
    """Main entry point"""
    print("🎮 Starting RPGSim - Epic Journey RPG")
    print("🏰 Demo: Single City Experience")
    print("⚡ Sprint 1: GUI Foundation")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create and run app
    app = RPGSimApp()
    app.run()
    
    print(f"🏁 Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()