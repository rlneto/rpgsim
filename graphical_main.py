#!/usr/bin/env python3
"""
RPGSim Graphical Interface Launcher
MAXIMUM PRIORITY: Launch game exclusively through interactive graphical interface

Usage:
    python graphical_main.py

No CLI parameters - all interactions through GUI only
"""

import sys
import asyncio
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class RPGSimGraphicalLauncher:
    """Graphical Interface Launcher for RPGSim - GUI ONLY"""
    
    def __init__(self):
        self.game_state = None
        self.ui_system = None
        
    def launch(self):
        """Launch RPGSim exclusively through graphical interface"""
        print("Initializing RPGSim Graphical Interface...")
        print("=" * 50)
        
        try:
            # Import graphical UI systems
            from game.ui.screens.modern_terminal_ui import (
                create_terminal_ui, 
                run_terminal_ui,
                GameScreen,
                CharacterCreationScreen,
                MainMenuScreen
            )
            from game.modern_ui import ModernTerminalUI
            from core.engine import get_game_engine
            
            # Initialize graphical interface
            self.ui_system = ModernTerminalUI()
            self.ui_system.initialize()
            
            # Initialize game engine
            engine = get_game_engine()
            
            # Create terminal UI application
            app = create_terminal_ui()
            
            # Set up game state for UI
            sample_game_state = {
                'player': {
                    'name': 'Hero',
                    'class': 'Warrior',
                    'level': 1,
                    'hp': 100,
                    'max_hp': 100,
                    'gold': 50,
                    'xp': 0,
                    'abilities': ['Attack', 'Defend'],
                    'stats': {
                        'strength': 15,
                        'dexterity': 10,
                        'intelligence': 8,
                        'wisdom': 10,
                        'charisma': 8,
                        'constitution': 14
                    }
                },
                'location': {
                    'name': 'Town Square',
                    'description': 'A bustling town square with shops and adventurers',
                    'connections': ['Blacksmith', 'Inn', 'Shop', 'Gates']
                },
                'inventory': [],
                'game_time': 'Day 1 - Morning'
            }
            
            # Initialize UI with game state
            app.initialize_game_state(sample_game_state)
            
            print("✅ Graphical Interface Initialized Successfully!")
            print("🎮 Starting RPGSim in Interactive Mode...")
            print("🔥 IMPORTANT: All interactions through GUI only - No CLI access!")
            print("=" * 50)
            
            # Run the graphical interface application
            asyncio.run(run_terminal_ui(app))
            
        except ImportError as e:
            print(f"❌ Failed to import graphical interface: {e}")
            print("🔧 Please ensure Textual and Rich are installed:")
            print("   pip install textual rich")
            sys.exit(1)
            
        except Exception as e:
            print(f"❌ Failed to launch graphical interface: {e}")
            print("🔧 Please check your graphical UI system installation")
            sys.exit(1)
    
    def demonstrate_ui(self):
        """Demonstrate the graphical interface capabilities"""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table
            from rich.text import Text
            from rich.align import Align
            
            console = Console()
            
            # Create a beautiful demonstration
            title = Text("🏰 RPGSim - Graphical Interface Demo 🏰", style="bold blue")
            subtitle = Text("Interactive Terminal RPG with Rich Graphics", style="italic cyan")
            
            # Show current state
            state_table = Table(title="Current Game State")
            state_table.add_column("Property", style="bold green")
            state_table.add_column("Value", style="yellow")
            
            state_table.add_row("Character", "Aragorn - Warrior")
            state_table.add_row("Level", "1")
            state_table.add_row("HP", "100/100")
            state_table.add_row("Gold", "50")
            state_table.add_row("Location", "Town Square")
            state_table.add_row("Interface", "Graphical Only")
            
            instructions = Panel(
                "[bold green]🎮 Instructions:[/bold green]\n"
                "• All interactions through graphical interface\n"
                "• No command-line access\n"
                "• Real-time updates\n"
                "• Interactive menus and buttons\n"
                "• Rich ASCII art and animations\n"
                "\n"
                "[bold yellow]🚀 Features:[/bold yellow]\n"
                "• Character creation GUI\n"
                "• World navigation map\n"
                "• Combat animations\n"
                "• Inventory management\n"
                "• Shop interactions\n"
                "• Quest system\n"
                "\n"
                "[bold red]🔥 MAXIMUM PRIORITY:[/bold red]\n"
                "• EXCLUSIVE graphical interface\n"
                "• NO text-based fallback\n"
                "• NO CLI gameplay access",
                title="📋 GUI Requirements",
                border_style="red"
            )
            
            # Clear screen and show demo
            console.clear()
            console.print(Align.center(title))
            console.print(Align.center(subtitle))
            console.print("")
            console.print(state_table)
            console.print("")
            console.print(instructions)
            console.print("")
            
            # Show character creation demo
            creation_demo = Panel(
                "[bold cyan]Character Creation GUI:[/bold cyan]\n"
                "• Visual class selector with icons\n"
                "• Real-time stat preview\n"
                "• Interactive name input field\n"
                "• Graphical confirmation button\n"
                "• Animated creation sequence\n"
                "\n"
                "[bold green]Game World GUI:[/bold green]\n"
                "• Interactive location map\n"
                "• Click-to-travel navigation\n"
                "• Animated travel sequences\n"
                "• Real-time location discovery\n"
                "\n"
                "[bold yellow]Combat System GUI:[/bold yellow]\n"
                "• Turn-based button actions\n"
                "• Animated damage numbers\n"
                "• Real-time health bars\n"
                "• Combat log display\n"
                "• Victory/defeat animations",
                title="🎨 GUI Features",
                border_style="green"
            )
            
            console.print(creation_demo)
            console.print("")
            console.print(Align.center(Text("Press Enter to continue...", style="dim italic")))
            input()
            
        except Exception as e:
            print(f"Demo failed: {e}")


def main():
    """Main launcher entry point - GUI ONLY"""
    launcher = RPGSimGraphicalLauncher()
    
    # Show demonstration first
    launcher.demonstrate_ui()
    
    # Launch full graphical interface
    launcher.launch()


if __name__ == "__main__":
    main()