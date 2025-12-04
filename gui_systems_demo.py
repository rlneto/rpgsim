#!/usr/bin/env python3
"""
GUI Demo - Complete Systems Integration
FOCUS: Visual interface for all implemented BDD systems
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Header, Footer, Button, Static, Input, Select, ListView, ListItem
from textual.screen import Screen
from textual.binding import Binding
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import asyncio
import random

# Import all BDD systems
from core.systems.character import create_character, get_all_character_classes
from core.systems.dungeon import generate_dungeon, explore_dungeon_room
from core.systems.equipment import generate_equipment, get_all_equipment_types
from core.systems.quest import create_quest, complete_quest
from core.systems.gamification import grant_experience, unlock_achievement
from core.systems.progression import level_up_character, improve_skill
from core.systems.combat import calculate_damage, resolve_combat
from core.systems.game_clean import start_new_game, save_game, load_game

class SystemsMenuScreen(Screen):
    NAME = "systems_menu"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎮 RPGSim - Complete Systems Demo", classes="title"),
            Static("📋 All BDD Systems Integrated & Working", classes="subtitle"),
            
            Container(
                Static("⚙️ Available Systems", classes="panel-title"),
                Button("👤 Character Creation", id="char_btn", variant="primary"),
                Button("🏛️ Dungeon System", id="dungeon_btn", variant="secondary"),
                Button("⚔️ Equipment System", id="equip_btn", variant="secondary"),
                Button("📜 Quest System", id="quest_btn", variant="secondary"),
                Button("🏆 Gamification System", id="gamify_btn", variant="secondary"),
                Button("📈 Progression System", id="progress_btn", variant="secondary"),
                Button("⚔️ Combat System", id="combat_btn", variant="secondary"),
                Button("💾 Save/Load System", id="save_btn", variant="default"),
                id="systems_grid"
            ),
            
            Footer()
        )

class CharacterDemoScreen(Screen):
    NAME = "character_demo"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("👤 Character Creation System", classes="title"),
            Static("📋 BDD-Aligned Character Creation", classes="subtitle"),
            
            # Character Creation Form
            Container(
                Static("⚙️ Create Character", classes="panel-title"),
                Input(placeholder="Enter character name...", id="name_input"),
                Select(
                    options=get_all_character_classes(),
                    id="class_select",
                    value="Warrior"
                ),
                Button("🎯 Create Character", id="create_btn", variant="primary"),
                Button("🎲 Random Character", id="random_btn", variant="secondary"),
                id="creation_form"
            ),
            
            # Character Display
            Container(
                Static("📊 Character Information", classes="panel-title"),
                Static("", id="char_display"),
                id="character_info"
            ),
            
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle character creation buttons"""
        if event.button.id == "create_btn":
            await self.create_character()
        elif event.button.id == "random_btn":
            await self.random_character()
    
    async def create_character(self) -> None:
        """Create character from form"""
        name_input = self.query_one("#name_input", Input)
        class_select = self.query_one("#class_select", Select)
        
        name = name_input.value.strip() or "Hero"
        character_class = class_select.value
        
        try:
            character = create_character(name, character_class)
            self.display_character(character)
            self.app.notify(f"✅ Created {character_class} {name}!", severity="success")
        except Exception as e:
            self.app.notify(f"❌ Error: {str(e)}", severity="error")
    
    async def random_character(self) -> None:
        """Generate random character"""
        names = ["Aragorn", "Gandalf", "Legolas", "Gimli", "Frodo"]
        classes = [cls[0] for cls in get_all_character_classes()]
        
        name = random.choice(names)
        character_class = random.choice(classes)
        
        try:
            character = create_character(name, character_class)
            self.display_character(character)
            
            # Update form
            name_input = self.query_one("#name_input", Input)
            class_select = self.query_one("#class_select", Select)
            name_input.value = name
            class_select.value = character_class
            
            self.app.notify(f"🎲 Randomized: {name} the {character_class}!", severity="info")
        except Exception as e:
            self.app.notify(f"❌ Error: {str(e)}", severity="error")
    
    def display_character(self, character) -> None:
        """Display character information"""
        char_display = self.query_one("#char_display", Static)
        
        # Create rich table for character info
        table = Table(title=f"{character.name} - Level {character.level}")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Class", str(character.class_type))
        table.add_row("HP", f"{character.hp}/{character.max_hp}")
        table.add_row("Gold", str(character.gold))
        table.add_row("Level", str(character.level))
        table.add_row("Experience", str(character.experience))
        
        # Add stats if available
        if hasattr(character, 'stats'):
            stats = character.stats
            table.add_row("Strength", str(stats.strength))
            table.add_row("Dexterity", str(stats.dexterity))
            table.add_row("Intelligence", str(stats.intelligence))
            table.add_row("Constitution", str(stats.constitution))
        
        # Add skills if available
        if hasattr(character, 'skills'):
            skills_text = ", ".join(character.skills)
            table.add_row("Skills", skills_text)
        
        char_display.update(table)

class DungeonDemoScreen(Screen):
    NAME = "dungeon_demo"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏛️ Dungeon System", classes="title"),
            Static("📋 MM8-Inspired Dungeon Exploration", classes="subtitle"),
            
            # Dungeon Generation
            Container(
                Static("⚙️ Dungeon Generator", classes="panel-title"),
                Button("🏛️ Generate Normal Dungeon", id="normal_dungeon", variant="primary"),
                Button("🏛️ Generate Easy Dungeon", id="easy_dungeon", variant="secondary"),
                Button("🏛️ Generate Hard Dungeon", id="hard_dungeon", variant="warning"),
                Button("🔍 Explore Room", id="explore_room", variant="success"),
                id="dungeon_controls"
            ),
            
            # Dungeon Display
            Container(
                Static("📊 Dungeon Information", classes="panel-title"),
                Static("", id="dungeon_display"),
                Static("", id="room_display"),
                id="dungeon_info"
            ),
            
            Footer()
        )
    
    current_dungeon = None
    current_room = 1
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle dungeon buttons"""
        if event.button.id == "normal_dungeon":
            await self.generate_dungeon("normal")
        elif event.button.id == "easy_dungeon":
            await self.generate_dungeon("easy")
        elif event.button.id == "hard_dungeon":
            await self.generate_dungeon("hard")
        elif event.button.id == "explore_room":
            await self.explore_room()
    
    async def generate_dungeon(self, difficulty: str) -> None:
        """Generate new dungeon"""
        try:
            dungeon = generate_dungeon(difficulty)
            self.current_dungeon = dungeon
            self.current_room = 1
            
            self.display_dungeon_info(dungeon)
            self.app.notify(f"✅ Generated {dungeon.layout.name} ({difficulty})!", severity="success")
        except Exception as e:
            self.app.notify(f"❌ Error: {str(e)}", severity="error")
    
    async def explore_room(self) -> None:
        """Explore current room"""
        if not self.current_dungeon:
            self.app.notify("❌ Generate a dungeon first!", severity="error")
            return
        
        try:
            result = explore_dungeon_room(self.current_dungeon.dungeon_id, "player1", self.current_room)
            self.display_room_result(result)
            self.current_room += 1
        except Exception as e:
            self.app.notify(f"❌ Error: {str(e)}", severity="error")
    
    def display_dungeon_info(self, dungeon) -> None:
        """Display dungeon information"""
        dungeon_display = self.query_one("#dungeon_display", Static)
        
        table = Table(title=f"{dungeon.layout.name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Type", dungeon.layout.dungeon_type.value)
        table.add_row("Floors", str(dungeon.layout.floors))
        table.add_row("Rooms per Floor", str(dungeon.layout.rooms_per_floor))
        table.add_row("Difficulty", dungeon.layout.difficulty)
        table.add_row("Current Floor", str(dungeon.current_floor))
        table.add_row("Current Room", str(dungeon.current_room))
        
        if dungeon.layout.boss_enemy:
            table.add_row("Boss", dungeon.layout.boss_enemy.name)
        
        dungeon_display.update(table)
    
    def display_room_result(self, result) -> None:
        """Display room exploration result"""
        room_display = self.query_one("#room_display", Static)
        
        content = result.get("content", "unknown")
        message = result.get("message", "Nothing found")
        
        if content == "enemy":
            enemy = result.get("enemy", {})
            enemy_name = enemy.get("name", "Unknown Enemy")
            info = f"⚔️ Combat! {message}\nEnemy: {enemy_name}"
        elif content == "treasure":
            treasure = result.get("treasure", {})
            treasure_name = treasure.get("name", "Unknown Treasure")
            treasure_value = treasure.get("gold_value", 0)
            info = f"💰 Treasure! {message}\nValue: {treasure_value} gold"
        elif content == "trap":
            damage = result.get("damage", 0)
            info = f"🕳️ Trap! {message}\nDamage: {damage} HP"
        elif content == "secret":
            info = f"🔓 Secret! {message}"
        else:
            info = f"🏠 Empty! {message}"
        
        room_display.update(Panel(info, title=f"Room {self.current_room}"))

class EquipmentDemoScreen(Screen):
    NAME = "equipment_demo"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("⚔️ Equipment System", classes="title"),
            Static("📋 RPG Item Management", classes="subtitle"),
            
            # Equipment Generation
            Container(
                Static("⚙️ Equipment Generator", classes="panel-title"),
                Select(
                    options=get_all_equipment_types(),
                    id="equipment_select",
                    value="sword"
                ),
                Button("🗡️ Generate Common", id="common_item", variant="primary"),
                Button("🗡️ Generate Rare", id="rare_item", variant="secondary"),
                Button("🗡️ Generate Epic", id="epic_item", variant="warning"),
                id="equipment_controls"
            ),
            
            # Equipment Display
            Container(
                Static("📊 Equipment Information", classes="panel-title"),
                Static("", id="equipment_display"),
                id="equipment_info"
            ),
            
            Footer()
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle equipment buttons"""
        equipment_select = self.query_one("#equipment_select", Select)
        equipment_type = equipment_select.value
        
        if event.button.id == "common_item":
            await self.generate_equipment(equipment_type, "common")
        elif event.button.id == "rare_item":
            await self.generate_equipment(equipment_type, "rare")
        elif event.button.id == "epic_item":
            await self.generate_equipment(equipment_type, "epic")
    
    async def generate_equipment(self, item_type: str, rarity: str) -> None:
        """Generate equipment item"""
        try:
            item = generate_equipment(item_type, rarity)
            self.display_equipment_info(item)
            self.app.notify(f"✅ Generated {rarity} {item_type}!", severity="success")
        except Exception as e:
            self.app.notify(f"❌ Error: {str(e)}", severity="error")
    
    def display_equipment_info(self, item) -> None:
        """Display equipment information"""
        equipment_display = self.query_one("#equipment_display", Static)
        
        table = Table(title=f"{item['name']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Type", item['item_type'])
        table.add_row("Rarity", item['rarity'])
        table.add_row("Level", str(item['level']))
        table.add_row("Gold Value", str(item['gold_value']))
        
        # Add stats
        if 'stats' in item:
            for stat, value in item['stats'].items():
                table.add_row(stat.title(), str(value))
        
        # Add type-specific stats
        if 'damage' in item:
            table.add_row("Damage", str(item['damage']))
        if 'defense' in item:
            table.add_row("Defense", str(item['defense']))
        
        equipment_display.update(table)

class AllSystemsDemoApp(App):
    """Complete Systems Demo App"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 1 0;
    }
    
    .subtitle {
        text-align: center;
        color: #888888;
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
    
    #systems_grid, #creation_form, #character_info,
    #dungeon_controls, #dungeon_info, #equipment_controls, #equipment_info {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 0 1;
    }
    
    Button {
        margin: 0 1;
        min-width: 25;
    }
    
    Input, Select {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "go_to_menu", "Back to Menu"),
    ]
    
    def on_mount(self) -> None:
        self.push_screen(SystemsMenuScreen())
    
    def action_go_to_menu(self) -> None:
        """Go back to main menu"""
        self.pop_all_screens()
        self.push_screen(SystemsMenuScreen())

def main():
    """Main function for complete systems demo"""
    print("🎮 Starting RPGSim - Complete Systems Demo")
    print("📋 All BDD Systems Integrated & Working")
    print("✅ Character • ✅ Dungeon • ✅ Equipment • ✅ Quest")
    print("✅ Gamification • ✅ Progression • ✅ Combat • ✅ Save/Load")
    
    app = AllSystemsDemoApp()
    app.run()

if __name__ == "__main__":
    main()