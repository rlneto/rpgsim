#!/usr/bin/env python3
"""
Simple GUI with ASCII Animated Art
FOCUS: Visual gameplay experience
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static
from textual.screen import Screen
from textual.binding import Binding
from textual.reactive import reactive
from textual.timer import Timer
import asyncio
import random

# ASCII Art Assets
PLAYER_ASCII = """
      @
     /|\\
     / \\
"""

WALKING_RIGHT = """
       @
      /|\\
     / \\
"""

WALKING_LEFT = """
    @
   //|
  / \\
"""

ENEMY_GOBLIN = """
    👾
   /|\\
   / \\
"""

CITY_MAP = """
┌─────────────────────────────────┐
│     @      🏪 Shop 🏪       │
│              │               │
│      🏰 Inn 🏰              │
│              │               │
│    🏛️ Dungeon 🏛️          │
│                             │
└─────────────────────────────────┘
"""

DUNGEON_ROOM = """
┌─────────────────────┐
│    🕸️  @  👾     │
│                   │
│  💎    💀        │
│                   │
└─────────────────────┘
"""

class ArtMainMenuScreen(Screen):
    NAME = "art_menu"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎮 RPGSim - ASCII Adventure", classes="title"),
            Static("⚔️ Epic Journey RPG", classes="subtitle"),
            Static("🎨 Art by ASCII Animation", classes="version"),
            
            # Animated ASCII Title
            Container(
                Static("""
    🏰      RPGSim      🏰
  ╔══════════════════════════╗
  ║  ASCII ANIMATED ADVENTURE ║
  ╚══════════════════════════╝
                """, id="ascii_title"),
                classes="ascii-art"
            ),
            
            Container(
                Button("🎮 New Game", id="new_game_btn", variant="primary"),
                Button("📜 Continue", id="continue_btn", variant="secondary"),
                Button("⚙️ Settings", id="settings_btn", variant="default"),
                Button("🚪 Exit", id="exit_btn", variant="error"),
                id="menu_buttons"
            ),
            Footer()
        )

class ArtGameScreen(Screen):
    NAME = "art_game"
    
    player_anim_state = reactive("idle")
    player_pos = reactive([1, 5])  # [y, x] coordinates
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏰 RPGSim - ASCII Adventure", classes="title"),
            
            # Character Status Panel
            Container(
                Static("⚔️ Character Status", classes="panel-title"),
                Static("Name: Hero", id="char_name"),
                Static("Level: 1", id="char_level"),
                Static("HP: 50/50", id="char_hp"),
                Static("Gold: 100", id="char_gold"),
                id="status_panel"
            ),
            
            # Main ASCII Game Display
            Container(
                Static(CITY_MAP, id="ascii_map", classes="ascii-map"),
                Static("📍 Location: Starting City", id="location_text"),
                id="game_display"
            ),
            
            # Action Panel
            Container(
                Static("⚡ Actions", classes="panel-title"),
                Static("[↑↓←→] Walk", id="walk_info"),
                Button("Enter Shop", id="shop_btn", variant="primary"),
                Button("Enter Inn", id="inn_btn", variant="success"),
                Button("Enter Dungeon", id="dungeon_btn", variant="warning"),
                Button("Rest", id="rest_btn", variant="secondary"),
                id="action_panel"
            ),
            Footer()
        )
    
    def on_mount(self) -> None:
        """Start animations when screen loads"""
        self.animate_player()
    
    def animate_player(self) -> None:
        """Animate player movement"""
        async def player_loop():
            states = ["idle", "walk_right", "idle", "walk_left"]
            i = 0
            while True:
                self.player_anim_state = states[i]
                await asyncio.sleep(0.5)
                i = (i + 1) % len(states)
        
        asyncio.create_task(player_loop())

class ArtDungeonScreen(Screen):
    NAME = "art_dungeon"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏛️ Dungeon - ASCII Adventure", classes="title"),
            
            # Combat Status
            Container(
                Static("⚔️ Combat Status", classes="panel-title"),
                Static("Hero HP: 50/50", id="hero_hp"),
                Static("Goblin HP: 30/30", id="enemy_hp"),
                id="combat_status"
            ),
            
            # Main Combat Display
            Container(
                Static(DUNGEON_ROOM, id="dungeon_map", classes="ascii-map"),
                Static("⚔️ Combat! You encountered a Goblin!", id="combat_text"),
                id="combat_display"
            ),
            
            # Combat Actions
            Container(
                Static("⚡ Combat Actions", classes="panel-title"),
                Button("⚔️ Attack", id="attack_btn", variant="primary"),
                Button("🛡️ Defend", id="defend_btn", variant="success"),
                Button("💨 Run", id="run_btn", variant="error"),
                id="combat_actions"
            ),
            Footer()
        )

class ArtASCIIApp(App):
    """Simple ASCII Art GUI App"""
    
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
        margin: 0 0 1 0;
    }
    
    .version {
        text-align: center;
        color: #666666;
        margin: 0 0 2 0;
    }
    
    .ascii-art {
        background: #1a1a1a;
        border: solid #444444;
        padding: 2;
        margin: 0 1;
        height: auto;
        text-align: center;
        color: #00ff00;
        font-family: monospace;
    }
    
    .ascii-map {
        background: #000000;
        border: solid #444444;
        padding: 2;
        margin: 0 1;
        height: auto;
        text-align: center;
        color: #ffffff;
        font-family: monospace;
        font-size: 150%;
    }
    
    .panel-title {
        text-align: center;
        text-style: bold;
        color: #ffffff;
        background: #333333;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    
    #status_panel, #game_display, #action_panel,
    #combat_status, #combat_display, #combat_actions {
        background: #222222;
        border: solid #444444;
        padding: 1;
        margin: 0 1;
        height: auto;
    }
    
    #menu_buttons {
        width: 30;
        margin: 0 1;
    }
    
    Button {
        margin: 0 1;
        min-width: 20;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("up", "move_up", "Move Up"),
        Binding("down", "move_down", "Move Down"),
        Binding("left", "move_left", "Move Left"),
        Binding("right", "move_right", "Move Right"),
    ]
    
    def on_mount(self) -> None:
        self.push_screen(ArtMainMenuScreen())

def main():
    """Main function for ASCII art GUI"""
    print("🎨 Starting RPGSim - ASCII Adventure...")
    print("📊 Focus: Animated ASCII Art Experience")
    
    app = ArtASCIIApp()
    app.run()

if __name__ == "__main__":
    main()