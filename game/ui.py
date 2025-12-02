"""
Modern Terminal UI for RPGSim using Rich and Textual
Provides beautiful, responsive terminal interface with keyboard navigation
"""

import os
import sys
from typing import Optional, Callable, Dict, Any, List
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.columns import Columns


@dataclass
class UIState:
    """Represents current UI state"""

    screen: str = "main"
    selected_index: int = 0
    menu_items: List[str] = None
    data: Dict[str, Any] = None

    def __post_init__(self):
        if self.menu_items is None:
            self.menu_items = []


class TerminalUI:
    """Modern terminal UI with Rich components"""

    def __init__(self):
        self.console = Console()
        self.state = UIState()
        self.running = True
        self.game_data = {}
        self.width = 80
        self.height = 24

        # Try to get terminal dimensions
        try:
            self.width, self.height = os.get_terminal_size()
        except:
            pass  # Use defaults if detection fails

    def clear(self) -> None:
        """Clear the screen"""
        self.console.clear()

    def get_centered_text(self, text: str, style: str = "white") -> Text:
        """Get centered text"""
        return Text(text, style=style, justify="center")

    def create_title(self, title: str) -> Panel:
        """Create title panel"""
        return Panel(
            self.get_centered_text(title, "bold cyan"),
            border_style="bright_blue",
            padding=(1, 2),
        )

    def create_menu_table(self, items: List[str], selected: int = 0) -> Table:
        """Create interactive menu table"""
        table = Table(show_header=False, box=None, padding=0)

        for i, item in enumerate(items):
            if i == selected:
                table.add_row(f"▶ [bold yellow]{item}[/bold yellow]")
            else:
                table.add_row(f"  {item}")

        return table

    def create_status_bar(self) -> Panel:
        """Create status bar with player info"""
        player_info = self.game_data.get("player", {})

        hp_text = f"[bold green]HP:[/bold green] {player_info.get('hp', 0)}/{player_info.get('max_hp', 0)}"
        mp_text = f"[bold blue]MP:[/bold blue] {player_info.get('mp', 0)}/{player_info.get('max_mp', 0)}"
        gold_text = f"[bold yellow]Gold:[/bold yellow] {player_info.get('gold', 0)}"
        status_text = f"{hp_text} | {mp_text} | {gold_text}"

        return Panel(status_text, border_style="dim", height=1)

    def create_main_menu(self) -> Layout:
        """Create main menu layout"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", size=15),
            Layout(name="footer", size=3),
        )

        # Header
        title = self.create_title("RPGSim: Console RPG Adventure")
        layout["header"].update(title)

        # Body - Menu items
        menu_items = ["New Character", "Load Game", "Options", "Exit"]

        menu_table = self.create_menu_table(menu_items, self.state.selected_index)
        menu_panel = Panel(menu_table, title="Main Menu", border_style="green")
        layout["body"].update(Align.center(menu_panel))

        # Footer - Status and help
        footer_text = "[dim]↑↓ Navigate | Enter Select | Esc Back | F5 Quick Save | F8 Quick Load[/dim]"
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def create_character_creation(self) -> Layout:
        """Create character creation screen"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", size=18),
            Layout(name="footer", size=3),
        )

        # Header
        title = self.create_title("Character Creation")
        layout["header"].update(title)

        # Body - Character creation form
        creation_data = self.state.data or {}

        # Name input
        name = creation_data.get("name", "")

        # Class selection
        classes = [
            "Warrior",
            "Mage",
            "Rogue",
            "Cleric",
            "Ranger",
            "Paladin",
            "Warlock",
            "Druid",
            "Monk",
            "Barbarian",
            "Bard",
            "Sorcerer",
            "Fighter",
            "Necromancer",
            "Illusionist",
            "Alchemist",
            "Berserker",
            "Assassin",
            "Healer",
            "Summoner",
            "Shapeshifter",
            "Elementalist",
            "Ninja",
        ]

        body_content = []

        # Name field
        if self.state.selected_index == 0:
            name_field = f"[bold yellow]Name:[/bold yellow] {name}_"
        else:
            name_field = f"Name: {name}"
        body_content.append(name_field)

        body_content.append("")  # Spacer

        # Class selection
        body_content.append("[bold]Select Class:[/bold]")
        for i, class_name in enumerate(classes):
            class_index = i + 1
            if class_index == self.state.selected_index:
                body_content.append(f"  ▶ [bold yellow]{class_name}[/bold yellow]")
            else:
                body_content.append(f"    {class_name}")

        # Preview area
        body_content.append("")
        body_content.append("[dim]Class Stats Preview:[/dim]")

        selected_class = classes[min(self.state.selected_index - 1, len(classes) - 1)]
        if self.state.selected_index > 0:
            body_content.append(f"  {selected_class}: Balanced combat specialist")

        layout["body"].update(Panel("\n".join(body_content), border_style="cyan"))

        # Footer
        footer_text = "[dim]↑↓ Select | Tab Next Field | Enter Confirm | Esc Back[/dim]"
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def create_game_screen(self) -> Layout:
        """Create main game screen"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", size=17),
            Layout(name="footer", size=4),
        )

        # Header - Player info
        header_content = self.create_character_info_panel()
        layout["header"].update(header_content)

        # Main - Game world
        main_content = self.create_game_world_panel()
        layout["main"].update(main_content)

        # Footer - Status and actions
        footer_content = self.create_status_bar()
        layout["footer"].update(footer_content)

        return layout

    def create_character_info_panel(self) -> Panel:
        """Create character information panel"""
        player = self.game_data.get("player", {})

        info_table = Table(show_header=False, box=None, padding=0)
        info_table.add_row(f"[bold cyan]{player.get('name', 'Unknown')}[/bold cyan]")
        info_table.add_row(
            f"Level {player.get('level', 1)} {player.get('class', 'Warrior')}"
        )
        info_table.add_row(f"HP: {player.get('hp', 100)}/{player.get('max_hp', 100)}")
        info_table.add_row(f"Gold: {player.get('gold', 0)}")

        return Panel(info_table, title="Character", border_style="green", width=30)

    def create_game_world_panel(self) -> Panel:
        """Create game world display panel"""
        location = self.game_data.get("location", "Unknown Location")
        events = self.game_data.get("events", [])

        world_content = []
        world_content.append(f"[bold blue]Current Location:[/bold blue] {location}")
        world_content.append("")

        if events:
            world_content.append("[bold]Recent Events:[/bold]")
            for event in events[-5:]:  # Show last 5 events
                world_content.append(f"• {event}")
        else:
            world_content.append("[dim]The world awaits your actions...[/dim]")

        return Panel("\n".join(world_content), title="Game World", border_style="blue")

    def create_inventory_screen(self) -> Layout:
        """Create inventory management screen"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", size=15),
            Layout(name="footer", size=6),
        )

        # Header
        title = self.create_title("Inventory")
        layout["header"].update(title)

        # Body - Inventory items
        inventory = self.game_data.get("inventory", [])

        if inventory:
            inventory_table = Table(box=None, show_header=True)
            inventory_table.add_column("Item", style="white")
            inventory_table.add_column("Type", style="cyan")
            inventory_table.add_column("Value", style="yellow")

            for i, item in enumerate(inventory):
                item_style = (
                    "bold yellow" if i == self.state.selected_index else "white"
                )
                inventory_table.add_row(
                    f"[{item_style}]{item.get('name', 'Unknown')}[/{item_style}]",
                    item.get("type", "Unknown"),
                    str(item.get("value", 0)),
                )

            layout["body"].update(Panel(inventory_table, border_style="green"))
        else:
            empty_msg = Align.center("[dim]Your inventory is empty[/dim]")
            layout["body"].update(Panel(empty_msg, border_style="red"))

        # Footer
        footer_text = (
            "[dim]↑↓ Select | Enter Use/Equip | Drop Key | Backspace Back[/dim]"
        )
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def create_save_load_screen(self, screen_type: str = "save") -> Layout:
        """Create save/load screen"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", size=15),
            Layout(name="footer", size=6),
        )

        # Header
        title_text = f"{screen_type.title()} Game"
        title = self.create_title(title_text)
        layout["header"].update(title)

        # Body - Save slots
        saves = self.game_data.get("saves", [])

        if saves:
            saves_table = Table(box=None, show_header=True)
            saves_table.add_column("Slot", style="cyan")
            saves_table.add_column("Character", style="white")
            saves_table.add_column("Level", style="yellow")
            saves_table.add_column("Location", style="green")
            saves_table.add_column("Time", style="dim")

            for i, save in enumerate(saves):
                save_style = (
                    "bold yellow" if i == self.state.selected_index else "white"
                )
                saves_table.add_row(
                    f"[{save_style}]Slot {i + 1}[/{save_style}]",
                    f"[{save_style}]{save.get('player_name', 'Unknown')}[/{save_style}]",
                    f"[{save_style}]Level {save.get('level', 1)}[/{save_style}]",
                    f"[{save_style}]{save.get('location', 'Unknown')}[/{save_style}]",
                    f"[{save_style}]{save.get('play_time', '0:00')}[/{save_style}]",
                )

            layout["body"].update(Panel(saves_table, border_style="blue"))
        else:
            empty_msg = Align.center(f"[dim]No {screen_type} files found[/dim]")
            layout["body"].update(Panel(empty_msg, border_style="red"))

        # Footer
        if screen_type == "save":
            footer_text = "[dim]↑↓ Select | Enter Save | Esc Back[/dim]"
        else:
            footer_text = "[dim]↑↓ Select | Enter Load | Delete Key | Esc Back[/dim]"
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def create_combat_screen(self) -> Layout:
        """Create combat screen"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="combat", size=14),
            Layout(name="footer", size=6),
        )

        # Header - Combat info
        combat_data = self.game_data.get("combat", {})
        player = self.game_data.get("player", {})
        enemy = combat_data.get("enemy", {})

        header_table = Table(box=None, show_header=False, padding=1)
        header_table.add_column("Player", style="green", width=30)
        header_table.add_column("Enemy", style="red", width=30)
        header_table.add_row(f"{player.get('name', 'You')}", enemy.get("name", "Enemy"))
        header_table.add_row(
            f"HP: {player.get('hp', 100)}/{player.get('max_hp', 100)}",
            f"HP: {enemy.get('hp', 50)}/{enemy.get('max_hp', 50)}",
        )
        header_table.add_row(
            f"Round {combat_data.get('round', 1)}",
            f"Status: {combat_data.get('status', 'Active')}",
        )

        layout["header"].update(Panel(header_table, border_style="yellow"))

        # Body - Combat log
        combat_log = combat_data.get("log", [])
        log_content = []

        for entry in combat_log[-10:]:  # Show last 10 entries
            log_content.append(f"• {entry}")

        layout["combat"].update(
            Panel("\n".join(log_content), title="Combat Log", border_style="red")
        )

        # Footer - Actions
        actions = ["Attack", "Defend", "Ability", "Item", "Flee"]
        action_buttons = []

        for i, action in enumerate(actions):
            if i == self.state.selected_index:
                action_buttons.append(f"[bold yellow]▶ {action}[/bold yellow]")
            else:
                action_buttons.append(f"  {action}")

        footer_content = " | ".join(action_buttons)
        layout["footer"].update(
            Panel(footer_content, title="Actions", border_style="cyan")
        )

        return layout

    def show_loading_screen(self, message: str = "Loading...") -> None:
        """Show loading screen with spinner"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task(message, total=None)
            # This would be updated by actual loading process

    def show_error_message(self, message: str) -> None:
        """Show error message"""
        error_panel = Panel(
            f"[bold red]ERROR:[/bold red] {message}", border_style="red", title="Error"
        )
        self.console.print(error_panel)

    def show_success_message(self, message: str) -> None:
        """Show success message"""
        success_panel = Panel(
            f"[bold green]SUCCESS:[/bold green] {message}",
            border_style="green",
            title="Success",
        )
        self.console.print(success_panel)

    def get_text_input(self, prompt: str, default: str = "") -> str:
        """Get text input from user"""
        return Prompt.ask(prompt, default=default)

    def get_confirmation(self, prompt: str) -> bool:
        """Get yes/no confirmation from user"""
        return Confirm.ask(prompt)

    def update_game_data(self, data: Dict[str, Any]) -> None:
        """Update game data for UI display"""
        self.game_data.update(data)

    def handle_input(self, key: str) -> None:
        """Handle keyboard input"""
        if self.state.screen == "main":
            self.handle_main_menu_input(key)
        elif self.state.screen == "character_creation":
            self.handle_character_creation_input(key)
        elif self.state.screen == "game":
            self.handle_game_input(key)
        elif self.state.screen == "inventory":
            self.handle_inventory_input(key)
        elif self.state.screen == "save":
            self.handle_save_load_input(key)
        elif self.state.screen == "load":
            self.handle_save_load_input(key)
        elif self.state.screen == "combat":
            self.handle_combat_input(key)

    def handle_main_menu_input(self, key: str) -> None:
        """Handle main menu input"""
        menu_items = ["New Character", "Load Game", "Options", "Exit"]

        if key in ["up", "k"]:
            self.state.selected_index = (self.state.selected_index - 1) % len(
                menu_items
            )
        elif key in ["down", "j"]:
            self.state.selected_index = (self.state.selected_index + 1) % len(
                menu_items
            )
        elif key == "enter":
            if self.state.selected_index == 0:  # New Character
                self.state.screen = "character_creation"
                self.state.selected_index = 0
                self.state.data = {"name": "", "class": None}
            elif self.state.selected_index == 1:  # Load Game
                self.state.screen = "load"
                self.state.selected_index = 0
            elif self.state.selected_index == 2:  # Options
                # Would open options screen
                pass
            elif self.state.selected_index == 3:  # Exit
                self.running = False
        elif key == "F5":  # Quick save
            # Handle quick save
            pass
        elif key == "F8":  # Quick load
            # Handle quick load
            pass

    def handle_character_creation_input(self, key: str) -> None:
        """Handle character creation input"""
        if key in ["up", "k"]:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key in ["down", "j"]:
            self.state.selected_index = min(23, self.state.selected_index + 1)
        elif key == "enter":
            if self.state.selected_index == 0:
                # Enter name mode
                name = self.get_text_input("Enter character name:")
                self.state.data["name"] = name
            else:
                # Select class
                self.state.data["class"] = self.state.selected_index
                # Would start game with new character
                self.state.screen = "game"
        elif key == "esc":
            self.state.screen = "main"
            self.state.selected_index = 0

    def handle_game_input(self, key: str) -> None:
        """Handle game screen input"""
        if key == "i":  # Inventory
            self.state.screen = "inventory"
            self.state.selected_index = 0
        elif key == "F5":  # Quick save
            # Handle quick save
            pass
        elif key == "F8":  # Quick load
            # Handle quick load
            pass
        elif key == "esc":
            self.state.screen = "main"
            self.state.selected_index = 0

    def handle_inventory_input(self, key: str) -> None:
        """Handle inventory input"""
        inventory = self.game_data.get("inventory", [])

        if key in ["up", "k"]:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key in ["down", "j"]:
            self.state.selected_index = min(
                len(inventory) - 1, self.state.selected_index + 1
            )
        elif key == "enter":
            # Use/equip selected item
            if inventory:
                selected_item = inventory[self.state.selected_index]
                # Handle item usage
                pass
        elif key in ["backspace", "esc"]:
            self.state.screen = "game"
            self.state.selected_index = 0

    def handle_save_load_input(self, key: str) -> None:
        """Handle save/load screen input"""
        saves = self.game_data.get("saves", [])

        if key in ["up", "k"]:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key in ["down", "j"]:
            self.state.selected_index = min(
                len(saves) - 1, self.state.selected_index + 1
            )
        elif key == "enter":
            if self.state.screen == "save":
                # Save to selected slot
                pass
            elif self.state.screen == "load":
                # Load from selected slot
                pass
        elif key == "delete" and self.state.screen == "load":
            # Delete selected save
            pass
        elif key in ["esc", "backspace"]:
            self.state.screen = "game"
            self.state.selected_index = 0

    def handle_combat_input(self, key: str) -> None:
        """Handle combat input"""
        actions = ["Attack", "Defend", "Ability", "Item", "Flee"]

        if key in ["up", "k"]:
            self.state.selected_index = max(0, self.state.selected_index - 1)
        elif key in ["down", "j"]:
            self.state.selected_index = min(
                len(actions) - 1, self.state.selected_index + 1
            )
        elif key == "enter":
            # Execute selected action
            action = actions[self.state.selected_index]
            # Handle combat action
            pass

    def render(self) -> None:
        """Render current screen"""
        self.clear()

        if self.state.screen == "main":
            layout = self.create_main_menu()
        elif self.state.screen == "character_creation":
            layout = self.create_character_creation()
        elif self.state.screen == "game":
            layout = self.create_game_screen()
        elif self.state.screen == "inventory":
            layout = self.create_inventory_screen()
        elif self.state.screen == "save":
            layout = self.create_save_load_screen("save")
        elif self.state.screen == "load":
            layout = self.create_save_load_screen("load")
        elif self.state.screen == "combat":
            layout = self.create_combat_screen()
        else:
            layout = self.create_main_menu()  # Fallback

        self.console.print(layout)

    def run(self) -> None:
        """Run the UI main loop"""
        # Show loading screen
        self.show_loading_screen("Starting RPGSim...")

        # Main loop
        while self.running:
            self.render()

            # In a real implementation, you'd use a proper input library
            # For this demo, we'll simulate with simple prompts
            try:
                self.handle_input("enter")  # Simulate input
            except KeyboardInterrupt:
                self.running = False
                break


class KeyHandler:
    """Handles keyboard input for terminal UI"""

    def __init__(self):
        self.key_callbacks: Dict[str, Callable] = {}

    def register_callback(self, key: str, callback: Callable) -> None:
        """Register a callback for a key"""
        self.key_callbacks[key] = callback

    def handle_key(self, key: str) -> None:
        """Handle a key press"""
        if key in self.key_callbacks:
            self.key_callbacks[key]()

    def get_key(self) -> Optional[str]:
        """Get a key from user input"""
        try:
            import sys

            if sys.stdin.isatty():
                import termios, tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    return key
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            pass

        return None


# Export main UI class
__all__ = ["TerminalUI", "UIState"]
