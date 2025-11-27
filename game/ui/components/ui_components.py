"""
UI Components
Rich terminal widgets with ASCII art and animations
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple, Callable
from textual.widget import Widget
from textual.reactive import reactive
from textual.timer import Timer
from textual.message import Message
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.align import Align

from ..domain.ui import (
    UIElement, LogMessage, MessageType, UIState,
    ScreenPosition, ScreenSize, ColorScheme, MenuConfig,
    MenuItem, ProgressConfig, DialogConfig
)
from ..assets.ascii_art import ASCIIArtAssets


class UIComponentBase(Widget):
    """Base class for all UI components"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component_id = kwargs.get('id', '')
        self.position = kwargs.get('position', ScreenPosition())
        self.size = kwargs.get('size', ScreenSize())
        self.visible = kwargs.get('visible', True)
        self.enabled = kwargs.get('enabled', True)
        self.color_scheme = kwargs.get('color_scheme', ColorScheme())
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', '')
        self.z_index = kwargs.get('z_index', 0)
    
    def update_content(self, content: str) -> None:
        """Update component content"""
        self.content = content
        self.refresh()
    
    def set_visibility(self, visible: bool) -> None:
        """Set component visibility"""
        self.visible = visible
        self.display = visible
        self.refresh()


class AnimatedComponent(UIComponentBase):
    """Base class for animated components"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation_frames = kwargs.get('animation_frames', [])
        self.current_frame = 0
        self.animation_active = kwargs.get('animation_active', False)
        self.animation_speed = kwargs.get('animation_speed', 1.0)
        self.animation_timer = Timer(self.animation_speed, self.update_animation, repeat=True)
    
    def start_animation(self) -> None:
        """Start animation"""
        if self.animation_frames and not self.animation_active:
            self.animation_active = True
            self.animation_timer.start()
    
    def stop_animation(self) -> None:
        """Stop animation"""
        self.animation_active = False
        self.animation_timer.stop()
    
    def update_animation(self) -> None:
        """Update animation frame"""
        if self.animation_frames and self.animation_active:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.refresh()
    
    def get_current_frame_content(self) -> str:
        """Get current animation frame content"""
        if self.animation_frames:
            return self.animation_frames[self.current_frame]
        return ""


class CharacterDisplay(AnimatedComponent):
    """Character display with ASCII art and stats"""
    
    def __init__(self, character_data: Dict[str, Any], **kwargs):
        # Load animation frames for character
        character_class = character_data.get('class', 'warrior').lower()
        art = ASCIIArtAssets.get_character_art(character_class)
        
        super().__init__(
            animation_frames=[art] if art else [""],
            **kwargs
        )
        
        self.character_data = character_data
        self.update_timer = Timer(1.0, self.update_display, repeat=True)
        self.update_timer.start()
    
    def update_display(self) -> None:
        """Update character display"""
        self.refresh()
    
    def render(self) -> RenderResult:
        """Render character display"""
        # Get character art
        art = self.get_current_frame_content()
        
        # Create stats table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Stat", style="bold cyan", width=12)
        table.add_column("Value", style="bright_white", width=20)
        
        player = self.character_data
        table.add_row("👤 Name:", f"[bold gold1]{player.get('name', 'Unknown')}[/bold gold1]")
        table.add_row("🎭 Class:", f"[bold magenta]{player.get('class', 'Unknown')}[/bold magenta]")
        table.add_row("⭐ Level:", f"[bold green]Level {player.get('level', 1)}[/bold green]")
        
        # HP bar
        hp = player.get('hp', 100)
        max_hp = player.get('max_hp', 100)
        hp_bar = self._create_progress_bar(hp, max_hp, "❤️", "red")
        table.add_row("❤️ HP:", f"[red]{hp}/{max_hp}[/red]")
        table.add_row("", hp_bar)
        
        # XP bar
        xp = player.get('xp', 0)
        next_level_xp = player.get('level', 1) * 100
        xp_bar = self._create_progress_bar(xp, next_level_xp, "⭐", "yellow")
        table.add_row("⭐ XP:", f"[yellow]{xp}/{next_level_xp}[/yellow]")
        table.add_row("", xp_bar)
        
        table.add_row("💰 Gold:", f"[bright_yellow]{player.get('gold', 0)}[/bright_yellow]")
        
        # Combine art and stats
        if art.strip():
            content = f"""
{art}

{Panel(table, title="🎭 Character Stats", border_style="bright_blue")}
            """
        else:
            content = Panel(table, title="🎭 Character Stats", border_style="bright_blue")
        
        return content
    
    def _create_progress_bar(self, current: int, maximum: int, icon: str, color: str) -> str:
        """Create a progress bar"""
        if maximum <= 0:
            return "░" * 20
        
        progress = min(current / maximum, 1.0)
        filled_length = int(20 * progress)
        bar_length = 20
        
        if color == "red":
            bar_char = "█"
        elif color == "yellow":
            bar_char = "▓"
        else:
            bar_char = "▲"
        
        filled_bar = bar_char * filled_length
        empty_bar = "░" * (bar_length - filled_length)
        
        return f"[{color}]{filled_bar}[/{color}]{empty_bar}"


class LocationDisplay(AnimatedComponent):
    """Location display with ASCII art and info"""
    
    def __init__(self, location_data: Dict[str, Any], **kwargs):
        # Load animation frames for location
        location_type = location_data.get('type', 'city').lower()
        art_frames = ASCIIArtAssets.get_animation_frames("location", location_type)
        
        super().__init__(
            animation_frames=art_frames if art_frames else [""],
            **kwargs
        )
        
        self.location_data = location_data
        self.update_timer = Timer(2.0, self.update_display, repeat=True)
        self.update_timer.start()
    
    def update_display(self) -> None:
        """Update location display"""
        self.refresh()
    
    def render(self) -> RenderResult:
        """Render location display"""
        # Get location art
        art = self.get_current_frame_content()
        
        # Create info table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Info", style="bold green", width=15)
        table.add_column("Details", style="bright_white", width=30)
        
        loc = self.location_data
        table.add_row("📍 Location:", f"[bold cyan]{loc.get('name', 'Unknown')}[/bold cyan]")
        table.add_row("🕐 Time:", self._get_game_time())
        table.add_row("🌤️ Weather:", self._get_weather())
        table.add_row("🚶 Travel:", self._get_travel_info())
        
        # Combine art and info
        if art.strip():
            content = f"""
{art}

{Panel(table, title="🗺️ Current Location", border_style="bright_green")}
            """
        else:
            content = Panel(table, title="🗺️ Current Location", border_style="bright_green")
        
        return content
    
    def _get_game_time(self) -> str:
        """Get current game time"""
        current_time = time.strftime("%H:%M")
        hour = int(current_time[:2])
        
        if 6 <= hour < 12:
            return f"[gold1]Morning {current_time}[/gold1] ☀️"
        elif 12 <= hour < 18:
            return f"[yellow]Afternoon {current_time}[/yellow] 🌞"
        elif 18 <= hour < 22:
            return f"[orange1]Evening {current_time}[/orange1] 🌅"
        else:
            return f"[blue]Night {current_time}[/blue] 🌙"
    
    def _get_weather(self) -> str:
        """Get current weather"""
        import random
        weather_options = [
            ("Clear", "[bright_white]Clear[/bright_white] ☀️"),
            ("Cloudy", "[gray]Cloudy[/gray] ☁️"),
            ("Rainy", "[blue]Rainy[/blue] 🌧️"),
            ("Stormy", "[red]Stormy[/red] ⛈️")
        ]
        return random.choice(weather_options)[1]
    
    def _get_travel_info(self) -> str:
        """Get travel information"""
        import random
        times = ["5 min", "15 min", "30 min", "1 hour"]
        return f"[cyan]{random.choice(times)}[/cyan] 🚶"


class GameLog(UIComponentBase):
    """Game log with rich formatting and message types"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages: List[LogMessage] = []
        self.max_messages = kwargs.get('max_messages', 100)
        self.auto_scroll = kwargs.get('auto_scroll', True)
    
    def add_message(self, message: str, message_type: MessageType = MessageType.INFO) -> None:
        """Add message to log"""
        log_message = LogMessage(
            message=message,
            message_type=message_type
        )
        
        self.messages.append(log_message)
        
        # Keep only most recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        self.refresh()
    
    def clear_log(self) -> None:
        """Clear all messages"""
        self.messages.clear()
        self.refresh()
    
    def render(self) -> RenderResult:
        """Render game log"""
        if not self.messages:
            content = Panel(
                "[dim]No messages yet...[/dim]",
                title="📝 Game Log",
                border_style="bright_white"
            )
            return content
        
        # Build message lines
        lines = []
        
        # Add title line
        lines.append("📝 [bold]Game Log[/bold]")
        lines.append("─" * 50)
        
        # Add recent messages
        recent_messages = self.messages[-20:]  # Show last 20 messages
        
        for message in recent_messages:
            timestamp = message.get_timestamp_string()
            icon = message.icon
            color = message.color
            
            lines.append(f"[dim][{timestamp}][/dim] {icon} [{color}]{message.message}[/{color}]")
        
        content = "\n".join(lines)
        
        # Wrap in panel
        panel_content = Panel(
            content,
            title="📝 Game Log",
            border_style="bright_white",
            title_align="left"
        )
        
        return panel_content


class MenuDisplay(UIComponentBase):
    """Menu display with navigation and selection"""
    
    def __init__(self, menu_config: MenuConfig, **kwargs):
        super().__init__(**kwargs)
        self.menu_config = menu_config
        self.selected_index = 0
        self.callbacks: Dict[str, Callable] = {}
    
    def set_callback(self, item_id: str, callback: Callable) -> None:
        """Set callback for menu item"""
        self.callbacks[item_id] = callback
    
    def navigate_up(self) -> None:
        """Navigate to previous item"""
        if self.menu_config.items:
            self.selected_index = (self.selected_index - 1) % len(self.menu_config.items)
            self.refresh()
    
    def navigate_down(self) -> None:
        """Navigate to next item"""
        if self.menu_config.items:
            self.selected_index = (self.selected_index + 1) % len(self.menu_config.items)
            self.refresh()
    
    def select_current(self) -> Optional[MenuItem]:
        """Select current menu item"""
        if not self.menu_config.items:
            return None
        
        current_item = self.menu_config.items[self.selected_index]
        if current_item.enabled:
            # Execute callback if exists
            callback = self.callbacks.get(current_item.id)
            if callback:
                callback(current_item)
            return current_item
        return None
    
    def render(self) -> RenderResult:
        """Render menu"""
        if not self.menu_config.items:
            return Panel("No items available", title=self.menu_config.title)
        
        # Create menu table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("", width=4)  # Selection indicator
        table.add_column("", width=4)  # Icon
        table.add_column("", width=30)  # Label
        
        for index, item in enumerate(self.menu_config.items):
            # Selection indicator
            if index == self.selected_index:
                indicator = "▶️"
                label_style = "bold white"
            else:
                indicator = "  "
                label_style = "white" if item.enabled else "dim"
            
            # Item label
            label = item.get_display_label()
            
            # Add row
            table.add_row(
                indicator,
                item.icon,
                f"[{label_style}]{label}[/{label_style}]"
            )
        
        # Wrap in panel
        content = Panel(
            table,
            title=self.menu_config.title,
            border_style="bright_yellow",
            title_align="center"
        )
        
        return content


class StatusDisplay(UIComponentBase):
    """Status display with health, mana, etc."""
    
    def __init__(self, status_data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.status_data = status_data
        self.update_timer = Timer(0.5, self.update_display, repeat=True)
        self.update_timer.start()
    
    def update_display(self) -> None:
        """Update status display"""
        self.refresh()
    
    def render(self) -> RenderResult:
        """Render status display"""
        status = self.status_data
        
        # Create status table
        table = Table(show_header=False, box=ROUNDED, padding=(0, 1))
        table.add_column("Stat", style="bold", width=12)
        table.add_column("Bar", width=30)
        
        # Health
        hp = status.get('hp', 100)
        max_hp = status.get('max_hp', 100)
        hp_bar = self._create_status_bar(hp, max_hp, "❤️", "red")
        table.add_row("HP:", hp_bar)
        
        # Mana
        mana = status.get('mana', 50)
        max_mana = status.get('max_mana', 50)
        mana_bar = self._create_status_bar(mana, max_mana, "💙", "blue")
        table.add_row("Mana:", mana_bar)
        
        # Stamina
        stamina = status.get('stamina', 75)
        max_stamina = status.get('max_stamina', 75)
        stamina_bar = self._create_status_bar(stamina, max_stamina, "🟡", "yellow")
        table.add_row("Stamina:", stamina_bar)
        
        # Experience
        xp = status.get('xp', 0)
        next_level = status.get('next_level_xp', 100)
        xp_bar = self._create_status_bar(xp, next_level, "⭐", "green")
        table.add_row("XP:", xp_bar)
        
        content = Panel(
            table,
            title="📊 Status",
            border_style="bright_cyan",
            title_align="left"
        )
        
        return content
    
    def _create_status_bar(self, current: int, maximum: int, icon: str, color: str) -> str:
        """Create a status bar"""
        if maximum <= 0:
            return f"{icon} ░░░░░░░░░░░░░░░░░░"
        
        progress = min(current / maximum, 1.0)
        filled_length = int(25 * progress)
        bar_length = 25
        
        filled_bar = "█" * filled_length
        empty_bar = "░" * (bar_length - filled_length)
        
        percentage = int(progress * 100)
        
        return f"{icon} [{color}]{filled_bar}[/{color}]{empty_bar} {percentage:3d}%"


class DialogDisplay(UIComponentBase):
    """Dialog display for messages and confirmations"""
    
    def __init__(self, dialog_config: DialogConfig, **kwargs):
        super().__init__(**kwargs)
        self.dialog_config = dialog_config
        self.result: Optional[str] = None
    
    def set_result(self, result: str) -> None:
        """Set dialog result"""
        self.result = result
        self.visible = False
        self.refresh()
    
    def get_result(self) -> Optional[str]:
        """Get dialog result"""
        return self.result
    
    def render(self) -> RenderResult:
        """Render dialog"""
        if not self.visible:
            return ""
        
        dialog = self.dialog_config
        
        # Create content based on type
        if dialog.type == MessageType.WARNING:
            border_style = "yellow"
            title_icon = "⚠️"
        elif dialog.type == MessageType.ERROR:
            border_style = "red"
            title_icon = "❌"
        elif dialog.type == MessageType.SUCCESS:
            border_style = "green"
            title_icon = "✅"
        else:
            border_style = "blue"
            title_icon = "ℹ️"
        
        # Create message panel
        message_panel = Panel(
            dialog.message,
            title=f"{title_icon} {dialog.title}",
            border_style=border_style,
            title_align="center"
        )
        
        content = message_panel
        
        # Add buttons if any
        if dialog.buttons:
            content += "\n\n"
            
            button_lines = []
            for button in dialog.buttons:
                if button.enabled:
                    button_lines.append(f"  {button.icon} {button.label}")
            
            if button_lines:
                content += "\n".join(button_lines)
        
        # Wrap in outer panel
        final_content = Panel(
            content,
            border_style=border_style,
            title="Dialog",
            title_align="center"
        )
        
        return final_content


# Message classes for component communication
class MenuItemSelected(Message):
    """Message sent when menu item is selected"""
    
    def __init__(self, item: MenuItem) -> None:
        self.item = item
        super().__init__()


class DialogClosed(Message):
    """Message sent when dialog is closed"""
    
    def __init__(self, result: str) -> None:
        self.result = result
        super().__init__()


class LogMessageAdded(Message):
    """Message sent when log message is added"""
    
    def __init__(self, message: LogMessage) -> None:
        self.message = message
        super().__init__()