#!/usr/bin/env python3
"""
Minimal GUI Test - Baseline Validation
SPRINT 1: Clean Foundation
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static, Input
from textual.screen import Screen
from textual.binding import Binding
import asyncio

class MenuScreen(Screen):
    NAME = "menu"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🎮 RPGSim - Menu", classes="title"),
            Button("Start", id="start_btn"),
            Button("Exit", id="exit_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_btn":
            self.app.push_screen(GameScreen())
        elif event.button.id == "exit_btn":
            self.app.exit()

class GameScreen(Screen):
    NAME = "game"
    
    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Static("🏰 RPGSim - Game", classes="title"),
            Static("You are in the game!"),
            Button("Back to Menu", id="back_btn"),
            Footer()
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_btn":
            self.app.pop_screen()

class MinimalApp(App):
    """Minimal test app"""
    
    CSS = """
    .title {
        text-align: center;
        text-style: bold;
        color: #ffa500;
        margin: 2 0;
    }
    """
    
    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

def main():
    """Test minimal app"""
    print("🧪 Starting Minimal GUI Test...")
    app = MinimalApp()
    app.run()
    print("✅ Minimal GUI Test Complete")

if __name__ == "__main__":
    main()