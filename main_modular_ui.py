"""
Main entry point for RPGSim with modular UI
Runs the beautiful terminal interface
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import modular UI
from game.ui import (
    ModernTerminalUI, create_modern_ui, run_modern_terminal_ui
)
from game.ui.modular_ui import UISystem, GameState


def main():
    """Main entry point"""
    print("🎮 Starting RPGSim with Modular UI...")
    print("═" * 50)
    
    try:
        # Initialize modular UI system
        ui_system = UISystem()
        
        if not ui_system.initialize_ui():
            print("❌ Failed to initialize UI system")
            return 1
        
        # Create sample game state
        game_state = GameState(
            player={
                'name': 'Aragorn',
                'class': 'Warrior',
                'level': 5,
                'hp': 150,
                'max_hp': 150,
                'xp': 250,
                'gold': 500,
                'equipment': {
                    'weapon': 'Long Sword', 
                    'armor': 'Chain Mail'
                }
            },
            location={
                'name': 'Riverdale',
                'type': 'village',
                'description': 'A peaceful village by the river'
            },
            status={
                'hp': 150,
                'max_hp': 150,
                'mana': 30,
                'max_mana': 50,
                'stamina': 75,
                'max_stamina': 75,
                'xp': 250,
                'next_level_xp': 500
            },
            combat={'active': False, 'enemy': None, 'log': []}
        )
        
        # Set game state
        ui_system.set_game_state(game_state)
        
        # Log welcome message
        ui_system.log_message("Welcome to RPGSim! Modern terminal RPG adventure.", "success")
        ui_system.log_message("Game state loaded successfully.", "info")
        
        # Run the UI
        ui_system.run_ui()
        
        print("\n👋 RPGSim closed gracefully.")
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 RPGSim interrupted by user.")
        return 0
    except Exception as e:
        print(f"\n❌ RPGSim crashed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)