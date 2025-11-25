"""
Modern Terminal UI for RPGSim using Textual framework
Provides reactive, beautiful terminal interface with keyboard navigation
"""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Static, Label, 
    DataTable, ProgressBar, ListView, ListItem
)
from textual.reactive import reactive
from textual.binding import Binding
from textual.screen import Screen
from textual.message import Message
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align


@dataclass
class GameState:
    """Game state data structure"""
    player: Dict[str, Any] = None
    location: str = "Unknown"
    inventory: List[Dict[str, Any]] = None
    quests: Dict[str, Any] = None
    combat: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.player is None:
            self.player = {
                'name': 'Hero',
                'level': 1,
                'hp': 100,
                'max_hp': 100,
                'gold': 0,
                'class': 'Warrior'
            }
        if self.inventory is None:
            self.inventory = []
        if self.quests is None:
            self.quests = {'active': [], 'completed': []}
        if self.combat is None:
            self.combat = {'active': False, 'enemy': None, 'log': []}


class PlayerInfo(Static):
    """Widget displaying player information"""
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
    
    def render(self) -> Static:
        """Render player info panel"""
        player = self.game_state.player
        
        # Create Rich table for player stats
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Stat", style="cyan", width=12)
        table.add_column("Value", style="white", width=20)
        
        table.add_row("Name:", f"[bold]{player['name']}[/bold]")
        table.add_row("Class:", f"[yellow]{player['class']}[/yellow]")
        table.add_row("Level:", f"[green]Level {player['level']}[/green]")
        table.add_row("HP:", f"[red]{player['hp']}/{player['max_hp']}[/red]")
        table.add_row("Gold:", f"[yellow]{player['gold']}[/yellow]")
        
        panel = Panel(
            table,
            title="👤 Character",
            border_style="bright_blue",
            title_align="left"
        )
        
        return Static(panel)


class LocationInfo(Static):
    """Widget displaying current location"""
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
    
    def render(self) -> Static:
        """Render location info panel"""
        location = self.game_state.location
        
        text = Text.from_markup(
            f"📍 [bold blue]Current Location:[/bold blue] {location}",
            justify="center"
        )
        
        panel = Panel(
            Align.center(text),
            title="🗺️ Location",
            border_style="green",
            title_align="center"
        )
        
        return Static(panel)


class GameLog(ListView):
    """Widget displaying game events and combat log"""
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.max_entries = 100
    
    def add_log_entry(self, message: str, style: str = "white") -> None:
        """Add an entry to the log"""
        # Add timestamp
        import time
        timestamp = time.strftime("%H:%M:%S")
        
        entry = ListItem(
            Text(f"[{timestamp}] [{style}]{message}[/{style}]")
        )
        
        self.append(entry)
        
        # Keep log size manageable
        if len(self.children) > self.max_entries:
            self.remove_child(self.children[0])
    
    def update_from_game_state(self) -> None:
        """Update log from game state"""
        if self.game_state.combat and self.game_state.combat['log']:
            for entry in self.game_state.combat['log'][-5:]:  # Show last 5 entries
                self.add_log_entry(entry, "red")


class CharacterCreationScreen(Screen):
    """Character creation screen"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("tab", "next_field", "Next Field"),
        Binding("enter", "create_character", "Create")
    ]
    
    def compose(self) -> ComposeResult:
        """Compose character creation screen"""
        with Container():
            yield Static("🎭 Character Creation", classes="title")
            yield Label("Name:")
            # Would use proper text input widget
            yield Static("Character classes available...")
            yield Button("Warrior", id="warrior")
            yield Button("Mage", id="mage")
            yield Button("Rogue", id="rogue")
            yield Button("Create Character", id="create", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        button_id = event.button.id
        
        if button_id in ["warrior", "mage", "rogue"]:
            # Handle class selection
            self.notify(f"Selected class: {button_id}")
        elif button_id == "create":
            # Create character and start game
            self.notify("Creating character...")
            self.app.pop_screen()


class MainMenuScreen(Screen):
    """Main menu screen"""
    
    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("enter", "select", "Select"),
        Binding("f5", "quick_save", "Quick Save"),
        Binding("f8", "quick_load", "Quick Load"),
        Binding("escape, q", "quit", "Quit")
    ]
    
    selected_index: reactive[int] = reactive(0)
    
    menu_items = [
        ("🎭 New Character", "new_character"),
        ("💾 Load Game", "load_game"),
        ("⚙️  Options", "options"),
        ("📖 Help", "help"),
        ("🚪 Exit", "quit")
    ]
    
    def compose(self) -> ComposeResult:
        """Compose main menu"""
        with Container(id="main-menu"):
            yield Static("🎮 RPGSim: Console RPG Adventure", classes="title")
            yield Static("", classes="spacer")
            
            with Vertical(id="menu-items"):
                for text, action in self.menu_items:
                    yield Button(text, id=action, variant="default")
            
            yield Static("", classes="spacer")
            yield Static("[dim]↑↓ Navigate | Enter Select | F5 Save | F8 Load[/dim]", classes="help")
    
    def watch_selected_index(self, index: int) -> None:
        """Watch selected index changes"""
        menu_buttons = self.query("Button")
        for i, button in enumerate(menu_buttons):
            if i == index:
                button.add_class("selected")
            else:
                button.remove_class("selected")
    
    def action_move_up(self) -> None:
        """Move selection up"""
        self.selected_index = (self.selected_index - 1) % len(self.menu_items)
    
    def action_move_down(self) -> None:
        """Move selection down"""
        self.selected_index = (self.selected_index + 1) % len(self.menu_items)
    
    def action_select(self) -> None:
        """Select current menu item"""
        _, action = self.menu_items[self.selected_index]
        
        if action == "new_character":
            self.app.push_screen(CharacterCreationScreen())
        elif action == "load_game":
            self.notify("Load game feature coming soon")
        elif action == "options":
            self.notify("Options feature coming soon")
        elif action == "help":
            self.notify("Help feature coming soon")
        elif action == "quit":
            self.app.exit()
    
    def action_quick_save(self) -> None:
        """Handle quick save"""
        self.notify("Quick saved!")
    
    def action_quick_load(self) -> None:
        """Handle quick load"""
        self.notify("Quick loaded!")


class GameScreen(Screen):
    """Main game screen"""
    
    BINDINGS = [
        Binding("i", "inventory", "Inventory"),
        Binding("j", "journal", "Journal"),
        Binding("m", "map", "Map"),
        Binding("escape", "main_menu", "Main Menu"),
        Binding("f5", "quick_save", "Quick Save"),
        Binding("f8", "quick_load", "Quick Load"),
        Binding("space", "interact", "Interact")
    ]
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
    
    def compose(self) -> ComposeResult:
        """Compose game screen"""
        with Container(id="game-screen"):
            # Top bar - Player and location info
            with Horizontal(id="top-bar"):
                yield PlayerInfo(self.game_state)
                yield LocationInfo(self.game_state)
            
            # Main game area
            with Container(id="game-area"):
                yield Static("🌍 Game World", classes="title")
                # Game world content would go here
                yield Static(self._get_world_content(), id="world-content")
            
            # Bottom bar - Game log and controls
            with Horizontal(id="bottom-bar"):
                yield GameLog(self.game_state, id="game-log")
                yield Static("[dim]I:Inv | J:Journal | M:Map | Space:Interact[/dim]", classes="controls")
    
    def _get_world_content(self) -> str:
        """Get current world content"""
        content = []
        
        # Location description
        content.append(f"📍 You are in: {self.game_state.location}")
        content.append("")
        
        # Available actions
        content.append("Available actions:")
        content.append("• Talk to townsfolk")
        content.append("• Visit shops")
        content.append("• Explore the area")
        content.append("• Check quests")
        content.append("")
        
        # Recent events
        if self.game_state.combat and self.game_state.combat['log']:
            content.append("Recent activity:")
            for entry in self.game_state.combat['log'][-3:]:
                content.append(f"• {entry}")
        
        return "\n".join(content)
    
    def action_inventory(self) -> None:
        """Open inventory screen"""
        self.app.push_screen(InventoryScreen(self.game_state))
    
    def action_journal(self) -> None:
        """Open journal screen"""
        self.notify("Journal feature coming soon")
    
    def action_map(self) -> None:
        """Open map screen"""
        self.notify("Map feature coming soon")
    
    def action_main_menu(self) -> None:
        """Return to main menu"""
        self.app.push_screen(MainMenuScreen())
    
    def action_quick_save(self) -> None:
        """Handle quick save"""
        self.notify("Game saved!")
    
    def action_quick_load(self) -> None:
        """Handle quick load"""
        self.notify("Game loaded!")
    
    def action_interact(self) -> None:
        """Handle interaction"""
        self.notify("Interacting with environment...")


class InventoryScreen(Screen):
    """Inventory management screen"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("enter", "use_item", "Use/Equip"),
        Binding("delete", "drop_item", "Drop"),
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down")
    ]
    
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
    
    def compose(self) -> ComposeResult:
        """Compose inventory screen"""
        with Container(id="inventory-screen"):
            yield Static("🎒 Inventory", classes="title")
            
            # Inventory table
            yield DataTable(id="inventory-table")
            
            # Item details
            yield Static("Select an item to see details", id="item-details")
            
            # Controls help
            yield Static("[dim]↑↓ Select | Enter Use | Delete Drop | Esc Back[/dim]", classes="controls")
    
    def on_mount(self) -> None:
        """Setup inventory screen when mounted"""
        table = self.query_one("#inventory-table", DataTable)
        
        # Add columns
        table.add_column("Name", key="name", width=20)
        table.add_column("Type", key="type", width=12)
        table.add_column("Value", key="value", width=8)
        table.add_column("Quality", key="quality", width=10)
        
        # Add inventory items
        for item in self.game_state.inventory:
            table.add_row(
                item.get('name', 'Unknown'),
                item.get('type', 'Unknown'),
                str(item.get('value', 0)),
                item.get('quality', 'Common')
            )


class RPGSimApp(App):
    """Main application class"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
    }
    
    .spacer {
        height: 1;
    }
    
    .help {
        text-align: center;
        color: $text-muted;
        margin: 1;
    }
    
    .controls {
        text-align: center;
        color: $text-muted;
        margin: 1;
    }
    
    #main-menu {
        align: center middle;
        width: 50;
        height: 25;
    }
    
    #menu-items Button {
        margin: 1;
        width: 100%;
    }
    
    #menu-items Button.selected {
        background: $accent;
        color: $primary;
    }
    
    #game-screen {
        height: 100%;
    }
    
    #top-bar {
        height: 10;
    }
    
    #game-area {
        height: 30;
        padding: 1;
    }
    
    #bottom-bar {
        height: 20;
    }
    
    #inventory-screen {
        align: center middle;
        width: 80;
        height: 25;
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
    """Run the terminal UI"""
    app = create_terminal_ui()
    app.run()


if __name__ == "__main__":
    run_terminal_ui()