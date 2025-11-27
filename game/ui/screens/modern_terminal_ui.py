"""
Modern Terminal UI with Rich Graphics
Beautiful ASCII art, animations, and immersive RPG experience
"""

import asyncio
import sys
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Center
from textual.widgets import Header, Footer, Button, Static, Label, RichLog
from textual.reactive import reactive
from textual.binding import Binding
from textual.screen import Screen
from textual.timer import Timer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.columns import Columns

from .domain.ui import (
    UISession, UIState, MessageType, ScreenPosition,
    ScreenSize, ColorScheme, MenuConfig, MenuItem
)
from .services.ui_service import UIServiceFactory
from .components.ui_components import (
    CharacterDisplay, LocationDisplay, GameLog,
    MenuDisplay, StatusDisplay, DialogDisplay
)
from .assets.ascii_art import ASCIIArtAssets


# Sample game state for demonstration
@dataclass
class GameState:
    """Sample game state data"""
    player: Dict[str, Any] = None
    location: Dict[str, Any] = None
    status: Dict[str, Any] = None
    combat: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.player is None:
            self.player = {
                'name': 'Aragorn',
                'class': 'Warrior',
                'level': 5,
                'hp': 150,
                'max_hp': 150,
                'xp': 250,
                'gold': 500,
                'equipment': {'weapon': 'Long Sword', 'armor': 'Chain Mail'}
            }
        
        if self.location is None:
            self.location = {
                'name': 'Riverdale',
                'type': 'village',
                'description': 'A peaceful village by the river'
            }
        
        if self.status is None:
            self.status = {
                'hp': 150,
                'max_hp': 150,
                'mana': 30,
                'max_mana': 50,
                'stamina': 75,
                'max_stamina': 75,
                'xp': 250,
                'next_level_xp': 500
            }
        
        if self.combat is None:
            self.combat = {'active': False, 'enemy': None, 'log': []}


class GameScreen(Screen):
    """Main game screen with rich UI components"""
    
    BINDINGS = [
        Binding("escape", "game_menu", "Game Menu"),
        Binding("i", "inventory", "Inventory"),
        Binding("m", "map", "Map"),
        Binding("q", "quests", "Quests"),
        Binding("space", "interact", "Interact"),
        Binding("f5", "quick_save", "Quick Save"),
        Binding("f9", "quick_load", "Quick Load"),
        Binding("h", "help", "Help")
    ]
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.service_factory = UIServiceFactory()
        self.log_service = self.service_factory.get_log_service()
        self.asset_service = self.service_factory.get_asset_service()
        
        # UI components
        self.character_display: Optional[CharacterDisplay] = None
        self.location_display: Optional[LocationDisplay] = None
        self.game_log: Optional[GameLog] = None
        self.status_display: Optional[StatusDisplay] = None
    
    def compose(self) -> ComposeResult:
        """Compose game screen with rich components"""
        
        # Top section - Character and Location
        with Container(id="top-section"):
            yield Static("", id="character-container")
            yield Static("", id="location-container")
        
        # Middle section - Game World
        with Container(id="middle-section"):
            yield Static("🌍 Game World", id="world-title", classes="title")
            yield Static(self._get_world_content(), id="world-content")
        
        # Bottom section - Status and Log
        with Horizontal(id="bottom-section"):
            yield Static("", id="status-container")
            yield Static("", id="log-container")
    
    def on_mount(self) -> None:
        """Setup screen when mounted"""
        # Initialize log
        self.log_service.add_message("Welcome to RPGSim!", MessageType.SUCCESS)
        self.log_service.add_message("You have arrived at Riverdale.", MessageType.INFO)
        self.log_service.add_message("Press 'H' for help.", MessageType.INFO)
        
        # Create UI components
        self._create_ui_components()
        
        # Start periodic updates
        self.update_timer = Timer(1.0, self.update_displays, repeat=True)
        self.update_timer.start()
    
    def _create_ui_components(self) -> None:
        """Create UI components"""
        # Character display
        self.character_display = CharacterDisplay(
            character_data=self.game_state.player,
            id="character-display"
        )
        
        # Location display
        self.location_display = LocationDisplay(
            location_data=self.game_state.location,
            id="location-display"
        )
        
        # Status display
        self.status_display = StatusDisplay(
            status_data=self.game_state.status,
            id="status-display"
        )
        
        # Game log
        self.game_log = GameLog(
            id="game-log",
            max_messages=50
        )
        
        # Mount components
        self.mount_components()
    
    def mount_components(self) -> None:
        """Mount components to containers"""
        # Mount character display
        char_container = self.query_one("#character-container", Static)
        if char_container and self.character_display:
            self.character_display._parent = char_container
            self.character_display.mount()
        
        # Mount location display
        loc_container = self.query_one("#location-container", Static)
        if loc_container and self.location_display:
            self.location_display._parent = loc_container
            self.location_display.mount()
        
        # Mount status display
        status_container = self.query_one("#status-container", Static)
        if status_container and self.status_display:
            self.status_display._parent = status_container
            self.status_display.mount()
        
        # Mount game log
        log_container = self.query_one("#log-container", Static)
        if log_container and self.game_log:
            self.game_log._parent = log_container
            self.game_log.mount()
    
    def update_displays(self) -> None:
        """Update all displays"""
        # This would update displays with new data
        # For now, just trigger refresh
        if self.character_display:
            self.character_display.refresh()
        
        if self.location_display:
            self.location_display.refresh()
        
        if self.status_display:
            self.status_display.refresh()
    
    def _get_world_content(self) -> str:
        """Get current world content"""
        content = []
        
        # Location description
        location = self.game_state.location
        content.append(f"📍 You are in: {location['name']}")
        content.append(f"   {location['description']}")
        content.append("")
        
        # Available actions
        content.append("🎯 Available Actions:")
        content.append("• Talk to NPCs")
        content.append("• Visit Shops")
        content.append("• Explore Area")
        content.append("• Check Quests")
        content.append("")
        
        # Character summary
        player = self.game_state.player
        content.append(f"👤 {player['name']} the {player['class']}")
        content.append(f"   Level {player['level']} with {player['gold']} gold")
        content.append("")
        
        # Equipment
        equipment = player.get('equipment', {})
        weapon = equipment.get('weapon', 'None')
        armor = equipment.get('armor', 'None')
        content.append(f"⚔️ Equipped: {weapon}, {armor}")
        content.append("")
        
        # Recent events
        if self.game_state.combat and self.game_state.combat.get('log'):
            content.append("⚔️ Recent Combat:")
            for entry in self.game_state.combat['log'][-3:]:
                content.append(f"   • {entry}")
        
        return "\n".join(content)
    
    # Action handlers
    def action_game_menu(self) -> None:
        """Open game menu"""
        self.log_service.add_message("Opening game menu...", MessageType.INFO)
        # Would navigate to game menu screen
    
    def action_inventory(self) -> None:
        """Open inventory"""
        self.log_service.add_message("Opening inventory...", MessageType.INFO)
        # Would navigate to inventory screen
    
    def action_map(self) -> None:
        """Open world map"""
        self.log_service.add_message("Opening world map...", MessageType.INFO)
        # Would navigate to map screen
    
    def action_quests(self) -> None:
        """Open quest journal"""
        self.log_service.add_message("Opening quest journal...", MessageType.INFO)
        # Would navigate to quest screen
    
    def action_interact(self) -> None:
        """Interact with environment"""
        self.log_service.add_message("Interacting with environment...", MessageType.SUCCESS)
        # Would trigger interaction logic
    
    def action_quick_save(self) -> None:
        """Quick save game"""
        self.log_service.add_message("Game saved successfully!", MessageType.SUCCESS)
        # Would trigger save logic
    
    def action_quick_load(self) -> None:
        """Quick load game"""
        self.log_service.add_message("Game loaded successfully!", MessageType.SUCCESS)
        # Would trigger load logic
    
    def action_help(self) -> None:
        """Show help"""
        help_text = """
🎮 RPGSim Controls:
┌─────────────────────────────────┐
│ ESC - Game Menu                 │
│ I   - Inventory                 │
│ M   - World Map                 │
│ Q   - Quest Journal              │
│ SPACE - Interact                │
│ F5  - Quick Save               │
│ F9  - Quick Load               │
│ H   - Help                     │
└─────────────────────────────────┘
        """
        self.log_service.add_message(help_text.strip(), MessageType.INFO)


class CharacterCreationScreen(Screen):
    """Beautiful character creation screen"""
    
    BINDINGS = [
        Binding("up", "navigate_up", "Up"),
        Binding("down", "navigate_down", "Down"),
        Binding("enter", "select_class", "Select"),
        Binding("escape", "back_to_menu", "Back")
    ]
    
    selected_class: reactive[int] = reactive(0)
    
    character_classes = [
        ("warrior", "⚔️ Warrior", "Strong melee fighter with heavy armor"),
        ("mage", "🔮 Mage", "Powerful spellcaster with arcane magic"),
        ("rogue", "🗡️ Rogue", "Stealthy assassin with precision attacks"),
        ("cleric", "✨ Cleric", "Divine healer with holy powers"),
        ("ranger", "🏹 Ranger", "Skilled archer with nature knowledge"),
        ("paladin", "🛡️ Paladin", "Holy warrior with divine protection")
    ]
    
    def compose(self) -> ComposeResult:
        """Compose character creation screen"""
        with Center():
            yield Static("🎭 RPGSim - Character Creation", classes="title")
            
            with Container(id="character-creation"):
                # Class selection
                yield Static("Choose Your Class:", id="class-title", classes="subtitle")
                yield Static("", id="class-art", classes="art-display")
                yield Static("", id="class-info", classes="info-display")
                
                # Class list
                yield Static("", id="class-list", classes="class-list")
                
                # Actions
                with Horizontal(id="actions"):
                    yield Button("Create Character", id="create", variant="primary")
                    yield Button("Back", id="back", variant="default")
    
    def on_mount(self) -> None:
        """Setup when mounted"""
        self.update_display()
        self.update_timer = Timer(2.0, self.update_display, repeat=True)
        self.update_timer.start()
    
    def update_display(self) -> None:
        """Update character creation display"""
        # Get selected class
        class_id, class_name, class_desc = self.character_classes[self.selected_class]
        
        # Get ASCII art
        art = ASCIIArtAssets.get_character_art(class_id)
        
        # Update displays
        self._update_art_display(art if art else "No art available")
        self._update_info_display(class_name, class_desc)
        self._update_class_list()
    
    def _update_art_display(self, art: str) -> None:
        """Update ASCII art display"""
        art_container = self.query_one("#class-art", Static)
        content = Panel(
            art,
            title="Character Preview",
            border_style="bright_blue",
            title_align="center"
        )
        art_container.update(content)
    
    def _update_info_display(self, class_name: str, class_desc: str) -> None:
        """Update class info display"""
        info_container = self.query_one("#class-info", Static)
        
        table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        table.add_column("Stat", style="bold cyan", width=15)
        table.add_column("Value", style="bright_white", width=20)
        
        # Sample stats for each class
        if "Warrior" in class_name:
            stats = [("Strength", "18"), ("Defense", "16"), ("Magic", "8"), ("Speed", "12")]
        elif "Mage" in class_name:
            stats = [("Strength", "10"), ("Defense", "12"), ("Magic", "18"), ("Speed", "14")]
        elif "Rogue" in class_name:
            stats = [("Strength", "14"), ("Defense", "12"), ("Magic", "10"), ("Speed", "16")]
        elif "Cleric" in class_name:
            stats = [("Strength", "14"), ("Defense", "14"), ("Magic", "14"), ("Speed", "12")]
        elif "Ranger" in class_name:
            stats = [("Strength", "15"), ("Defense", "13"), ("Magic", "12"), ("Speed", "15")]
        elif "Paladin" in class_name:
            stats = [("Strength", "16"), ("Defense", "16"), ("Magic", "12"), ("Speed", "11")]
        else:
            stats = [("Strength", "12"), ("Defense", "12"), ("Magic", "12"), ("Speed", "12")]
        
        for stat, value in stats:
            table.add_row(stat, value)
        
        content = f"""
{Panel(table, title=class_name, border_style="bright_green", title_align="left")}

{Panel(class_desc, title="Description", border_style="bright_yellow", title_align="center")}
        """
        
        info_container.update(content)
    
    def _update_class_list(self) -> None:
        """Update class selection list"""
        list_container = self.query_one("#class-list", Static)
        
        lines = ["┌─────────────────────────────┐"]
        lines.append("│     Available Classes       │")
        lines.append("├─────────────────────────────┤")
        
        for i, (class_id, class_name, _) in enumerate(self.character_classes):
            if i == self.selected_class:
                lines.append(f"│ ▶️ {class_name:<22} │")
            else:
                lines.append(f"│    {class_name:<22} │")
        
        lines.append("└─────────────────────────────┘")
        
        content = "\n".join(lines)
        list_container.update(content)
    
    def action_navigate_up(self) -> None:
        """Navigate up in class selection"""
        self.selected_class = (self.selected_class - 1) % len(self.character_classes)
        self.update_display()
    
    def action_navigate_down(self) -> None:
        """Navigate down in class selection"""
        self.selected_class = (self.selected_class + 1) % len(self.character_classes)
        self.update_display()
    
    def action_select_class(self) -> None:
        """Select current class and continue"""
        class_id, class_name, _ = self.character_classes[self.selected_class]
        self.notify(f"Selected {class_name}! Creating character...")
        # Would proceed to name selection or game start
    
    def action_back_to_menu(self) -> None:
        """Return to main menu"""
        self.app.pop_screen()


class MainMenuScreen(Screen):
    """Beautiful main menu screen"""
    
    BINDINGS = [
        Binding("up", "navigate_up", "Up"),
        Binding("down", "navigate_down", "Down"),
        Binding("enter", "select", "Select"),
        Binding("escape, q", "quit", "Quit")
    ]
    
    selected_index: reactive[int] = reactive(0)
    
    menu_items = [
        ("new_character", "🎭 New Character", "Start a new adventure"),
        ("load_game", "💾 Load Game", "Continue a saved game"),
        ("settings", "⚙️  Settings", "Configure game options"),
        ("help", "📖 Help", "View help and instructions"),
        ("quit", "🚪 Exit", "Exit to desktop")
    ]
    
    def compose(self) -> ComposeResult:
        """Compose main menu"""
        with Center():
            yield Static("🎮 RPGSim", classes="title")
            yield Static("Console RPG Adventure", classes="subtitle")
            yield Static("─" * 40, classes="separator")
            
            yield Static("", id="menu-display", classes="menu-display")
            
            yield Static("", id="menu-description", classes="menu-description")
            
            yield Static("[dim]↑↓ Navigate | Enter Select | Q Quit[/dim]", classes="help")
    
    def on_mount(self) -> None:
        """Setup when mounted"""
        self.update_display()
    
    def watch_selected_index(self, index: int) -> None:
        """Watch for selection changes"""
        self.update_display()
    
    def update_display(self) -> None:
        """Update menu display"""
        menu_container = self.query_one("#menu-display", Static)
        desc_container = self.query_one("#menu-description", Static)
        
        # Create menu display
        lines = ["┌─────────────────────────────┐"]
        lines.append("│         MAIN MENU           │")
        lines.append("├─────────────────────────────┤")
        
        for i, (_, label, _) in enumerate(self.menu_items):
            if i == self.selected_index:
                lines.append(f"│ ▶️ {label:<22} │")
            else:
                lines.append(f"│    {label:<22} │")
        
        lines.append("└─────────────────────────────┘")
        
        menu_content = "\n".join(lines)
        menu_container.update(menu_content)
        
        # Update description
        _, _, description = self.menu_items[self.selected_index]
        desc_content = Panel(
            description,
            title="Description",
            border_style="bright_cyan",
            title_align="center"
        )
        desc_container.update(desc_content)
    
    def action_navigate_up(self) -> None:
        """Navigate up"""
        self.selected_index = (self.selected_index - 1) % len(self.menu_items)
    
    def action_navigate_down(self) -> None:
        """Navigate down"""
        self.selected_index = (self.selected_index + 1) % len(self.menu_items)
    
    def action_select(self) -> None:
        """Select current menu item"""
        action_id, label, _ = self.menu_items[self.selected_index]
        
        if action_id == "new_character":
            self.app.push_screen(CharacterCreationScreen())
        elif action_id == "load_game":
            self.notify("Load game feature coming soon")
        elif action_id == "settings":
            self.notify("Settings feature coming soon")
        elif action_id == "help":
            self.notify("Help feature coming soon")
        elif action_id == "quit":
            self.app.exit()
    
    def action_quit(self) -> None:
        """Quit application"""
        self.app.exit()


class RPGSimApp(App):
    """Main application class with rich terminal UI"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
        font-size: 200%;
    }
    
    .subtitle {
        text-align: center;
        color: $text-muted;
        margin: 0 0 1 0;
        font-size: 120%;
    }
    
    .separator {
        text-align: center;
        color: $text-muted;
        margin: 0 0 2 0;
    }
    
    .menu-display {
        text-align: center;
        margin: 2 0;
    }
    
    .menu-description {
        margin: 2 0;
    }
    
    .help {
        text-align: center;
        color: $text-muted;
        margin: 2 0 0 0;
        font-size: 90%;
    }
    
    .art-display {
        text-align: center;
        margin: 2 0;
    }
    
    .info-display {
        margin: 2 0;
    }
    
    .class-list {
        text-align: center;
        margin: 2 0;
        font-family: monospace;
    }
    
    #character-creation {
        width: 80;
        height: 25;
        align: center middle;
    }
    
    #actions {
        margin: 2 0 0 0;
    }
    
    #actions Button {
        margin: 0 2;
    }
    
    #top-section {
        height: 25;
        padding: 1;
    }
    
    #middle-section {
        height: 15;
        padding: 1;
    }
    
    #bottom-section {
        height: 20;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.game_state = GameState()
    
    def on_mount(self) -> None:
        """Setup app when mounted"""
        self.title = "RPGSim: Console RPG Adventure"
        self.sub_title = "Modern Terminal RPG"
        
        # Push main menu screen
        self.push_screen(MainMenuScreen())


def create_terminal_ui() -> RPGSimApp:
    """Create and return terminal UI app"""
    return RPGSimApp()


def run_terminal_ui() -> None:
    """Run terminal UI"""
    app = create_terminal_ui()
    app.run()


if __name__ == "__main__":
    run_terminal_ui()