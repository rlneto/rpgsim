#!/usr/bin/env python3
"""
Refactored GUI - Based on Working Minimal
SPRINT 1: Clean Foundation
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static, Input, Select, ProgressBar
from textual.screen import Screen
from textual.binding import Binding
import asyncio
import random

# Import character system
from core.systems.character.facade import create_character, get_all_character_classes

class MenuScreen(Screen):
    NAME = "menu"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎮 RPGSim - Epic Journey RPG", classes="title"),
            Static("Demo: Single City Experience", classes="subtitle"),
            Button("New Game", id="new_game_btn"),
            Button("Exit", id="exit_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_game_btn":
            self.app.push_screen(CharacterCreationScreen())
        elif event.button.id == "exit_btn":
            self.app.exit()

class CharacterCreationScreen(Screen):
    NAME = "character_creation"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎮 Create Character", classes="title"),
            Input(placeholder="Character name...", id="name_input"),
            Select(
                options=get_all_character_classes(),
                id="class_select",
                value="Warrior"
            ),
            Button("Create", id="create_btn"),
            Button("Back", id="back_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create_btn":
            asyncio.create_task(self.create_character())
        elif event.button.id == "back_btn":
            self.app.pop_screen()
    
    async def create_character(self) -> None:
        """Create character with validation"""
        name_input = self.query_one("#name_input", Input)
        class_select = self.query_one("#class_select", Select)
        
        name = name_input.value.strip()
        character_class = class_select.value
        
        # Simple validation
        if not name:
            self.app.notify("Enter character name!", severity="error")
            return
        
        # Create character
        try:
            character = create_character(name, character_class)
            self.app.notify(f"✅ Created {character_class} {name}!", severity="success")
            self.app.pop_screen()
            self.app.push_screen(GameScreen(character))
        except Exception as e:
            self.app.notify(f"❌ Error: {e}", severity="error")

class GameScreen(Screen):
    NAME = "game"
    
    def __init__(self, character):
        super().__init__()
        self.character = character
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static(f"🏰 {self.character.name} - {self.character.class_type}", classes="title"),
            Static(f"Level: {self.character.level} | Gold: {self.character.gold}"),
            Button("Enter Dungeon", id="dungeon_btn"),
            Button("Rest at Inn", id="rest_btn"),
            Button("Back to Menu", id="menu_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "dungeon_btn":
            asyncio.create_task(self.enter_dungeon())
        elif event.button.id == "rest_btn":
            self.rest_at_inn()
        elif event.button.id == "menu_btn":
            self.app.pop_screen()
    
    async def enter_dungeon(self) -> None:
        """Enter dungeon"""
        if self.character.gold >= 10:
            self.character.gold -= 10
            self.app.notify("🏰 Entering dungeon...", severity="warning")
            self.app.push_screen(DungeonScreen(self.character))
        else:
            self.app.notify("💰 Need 10 gold!", severity="error")
    
    def rest_at_inn(self) -> None:
        """Rest at inn"""
        if self.character.gold >= 5:
            self.character.gold -= 5
            self.app.notify("💤 Rested at inn!", severity="success")
            # Update display
            title = self.query_one("Static.title")
            title.update(f"🏰 {self.character.name} - {self.character.class_type}")
        else:
            self.app.notify("💰 Need 5 gold!", severity="error")

class DungeonScreen(Screen):
    NAME = "dungeon"
    
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.floor = 1
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static(f"🏰 Dungeon Floor {self.floor}", classes="title"),
            Static("You explore the dark dungeon..."),
            Button("Explore", id="explore_btn"),
            Button("Fight Enemy", id="fight_btn"),
            Button("Escape", id="escape_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "explore_btn":
            asyncio.create_task(self.explore())
        elif event.button.id == "fight_btn":
            asyncio.create_task(self.fight_enemy())
        elif event.button.id == "escape_btn":
            self.app.pop_screen()
    
    async def explore(self) -> None:
        """Explore dungeon"""
        self.floor += 1
        title = self.query_one("Static.title")
        title.update(f"🏰 Dungeon Floor {self.floor}")
        
        if self.floor >= 3:
            await self.boss_battle()
    
    async def fight_enemy(self) -> None:
        """Fight enemy"""
        if random.random() < 0.7:  # 70% win chance
            gold = random.randint(5, 20)
            self.character.gold += gold
            self.app.notify(f"✅ Victory! Found {gold} gold!", severity="success")
        else:
            self.app.notify("💔 Defeated!", severity="error")
            self.app.pop_screen()
    
    async def boss_battle(self) -> None:
        """Boss battle"""
        if random.random() < 0.6:  # 60% win chance
            self.character.gold += 100
            self.app.notify("🎉 VICTORY! Boss defeated! +100 gold!", severity="success")
            self.app.pop_screen()
        else:
            self.app.notify("💀 Defeated by boss!", severity="error")
            self.app.pop_screen()

class RefactoredApp(App):
    """Clean refactored app"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 2 0;
    }
    
    .subtitle {
        text-align: center;
        color: #888888;
        margin: 0 0 2 0;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
    ]
    
    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

def main():
    """Main function"""
    print("🎮 Starting Refactored RPGSim...")
    app = RefactoredApp()
    app.run()

if __name__ == "__main__":
    main()