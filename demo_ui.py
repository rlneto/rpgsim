"""
Demo script for modular UI system
Showcases rich terminal interface with ASCII art and animations
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from game.ui import (
    UISystem, GameState, UIState, MessageType,
    get_ui_system, initialize_ui, run_ui
)


def demo_character_creation():
    """Demo character creation with ASCII art"""
    print("🎭 RPGSim - Character Creation Demo")
    print("━" * 50)
    
    # Initialize UI system
    ui = get_ui_system()
    if not initialize_ui():
        print("❌ Failed to initialize UI")
        return
    
    # Create sample character data
    character_classes = [
        ("warrior", "⚔️ Warrior", "Strong melee fighter"),
        ("mage", "🔮 Mage", "Powerful spellcaster"),
        ("rogue", "🗡️ Rogue", "Stealthy assassin"),
        ("cleric", "✨ Cleric", "Divine healer"),
        ("ranger", "🏹 Ranger", "Skilled archer"),
        ("paladin", "🛡️ Paladin", "Holy warrior")
    ]
    
    for i, (class_id, class_name, description) in enumerate(character_classes):
        print(f"\n{i+1}. {class_name}")
        print(f"   {description}")
        
        # Show ASCII art
        art = ui.get_ascii_art(class_id)
        if art:
            print(art)
        
        # Show stats
        if class_id == "warrior":
            stats = "STR: 18 | DEF: 16 | MAG: 8  | SPD: 12"
        elif class_id == "mage":
            stats = "STR: 10 | DEF: 12 | MAG: 18 | SPD: 14"
        elif class_id == "rogue":
            stats = "STR: 14 | DEF: 12 | MAG: 10 | SPD: 16"
        elif class_id == "cleric":
            stats = "STR: 14 | DEF: 14 | MAG: 14 | SPD: 12"
        elif class_id == "ranger":
            stats = "STR: 15 | DEF: 13 | MAG: 12 | SPD: 15"
        elif class_id == "paladin":
            stats = "STR: 16 | DEF: 16 | MAG: 12 | SPD: 11"
        else:
            stats = "STR: 12 | DEF: 12 | MAG: 12 | SPD: 12"
        
        print(f"   {stats}")
        print()


def demo_locations():
    """Demo location displays with ASCII art"""
    print("🌍 RPGSim - Location Demo")
    print("━" * 50)
    
    ui = get_ui_system()
    
    locations = [
        ("riverdale", "village", "Riverdale Village"),
        ("stonecrest", "city", "Stonecrest City"),
        ("dark_forest", "forest", "Dark Forest"),
        ("dungeon", "dungeon", "Ancient Dungeon"),
        ("castle", "castle", "Royal Castle")
    ]
    
    for loc_id, loc_type, loc_name in locations:
        print(f"\n📍 {loc_name}")
        
        # Show location art
        art = ui.get_ascii_art(loc_type)
        if art:
            print(art)
        else:
            print(f"   No art available for {loc_type}")
        
        print(f"   Type: {loc_type.title()}")
        print(f"   Description: A mysterious {loc_type} full of adventure")
        print()


def demo_combat():
    """Demo combat ASCII art"""
    print("⚔️ RPGSim - Combat Demo")
    print("━" * 50)
    
    ui = get_ui_system()
    
    combat_types = ["sword", "shield", "magic", "arrow"]
    
    for combat_type in combat_types:
        print(f"\n{combat_type.title()} Attack:")
        
        art = ui.get_ascii_art(f"combat_{combat_type}")
        if art:
            print(art)
        else:
            art = ui.get_ascii_art(combat_type)
            if art:
                print(art)
        
        print()
    
    # Show combat animations
    print("💥 Combat Effects:")
    effects = ["explosion", "sparkle", "heal", "poison"]
    
    for effect in effects:
        art = ui.get_ascii_art(effect)
        if art:
            print(art)
        print()


def demo_items():
    """Demo item ASCII art"""
    print("🎒 RPGSim - Item Demo")
    print("━" * 50)
    
    ui = get_ui_system()
    
    item_types = ["sword", "shield", "potion", "gold", "scroll"]
    
    for item_type in item_types:
        print(f"\n{item_type.title()}:")
        
        art = ui.get_ascii_art(item_type)
        if art:
            print(art)
        else:
            print(f"   No art available for {item_type}")
        
        # Show item info
        if item_type == "sword":
            info = "Damage: 15-25 | Type: One-handed"
        elif item_type == "shield":
            info = "Defense: +10 | Type: Heavy"
        elif item_type == "potion":
            info = "Heal: +50 HP | Type: Consumable"
        elif item_type == "gold":
            info = "Value: 100 coins | Type: Currency"
        elif item_type == "scroll":
            info = "Spell: Fireball | Type: Magical"
        else:
            info = "Unknown item properties"
        
        print(f"   {info}")
        print()


def demo_game_log():
    """Demo game log with rich formatting"""
    print("📝 RPGSim - Game Log Demo")
    print("━" * 50)
    
    ui = get_ui_system()
    
    # Different message types
    messages = [
        ("Welcome to RPGSim!", "success"),
        ("You have entered Riverdale Village.", "info"),
        ("A goblin attacks!", "combat"),
        ("You found 50 gold coins!", "loot"),
        ("New quest available: Slay the Dragon", "quest"),
        ("You discovered a secret passage!", "discovery"),
        ("Low health! Use healing potion.", "warning"),
        ("Invalid action.", "error"),
    ]
    
    print("📜 Game Log Messages:")
    print("─" * 40)
    
    for message, msg_type in messages:
        # Convert to MessageType
        type_map = {
            "success": MessageType.SUCCESS,
            "info": MessageType.INFO,
            "combat": MessageType.COMBAT,
            "loot": MessageType.LOOT,
            "quest": MessageType.QUEST,
            "discovery": MessageType.DISCOVERY,
            "warning": MessageType.WARNING,
            "error": MessageType.ERROR
        }
        
        message_type = type_map.get(msg_type, MessageType.INFO)
        ui.log_message(message, message_type)
        
        # Show formatted message
        timestamp = time.strftime("%H:%M:%S")
        
        # Get icon and color based on type
        icon_map = {
            MessageType.SUCCESS: "✅",
            MessageType.INFO: "📝",
            MessageType.COMBAT: "⚔️",
            MessageType.LOOT: "💰",
            MessageType.QUEST: "📜",
            MessageType.DISCOVERY: "🔍",
            MessageType.WARNING: "⚠️",
            MessageType.ERROR: "❌"
        }
        
        color_map = {
            MessageType.SUCCESS: "green",
            MessageType.INFO: "cyan",
            MessageType.COMBAT: "red",
            MessageType.LOOT: "yellow",
            MessageType.QUEST: "magenta",
            MessageType.DISCOVERY: "cyan",
            MessageType.WARNING: "yellow",
            MessageType.ERROR: "red"
        }
        
        icon = icon_map.get(message_type, "📝")
        color = color_map.get(message_type, "white")
        
        print(f"[{timestamp}] {icon} {message}")
    
    print()


def demo_full_ui():
    """Demo the full UI application"""
    print("🎮 RPGSim - Full UI Demo")
    print("━" * 50)
    print("Launching full terminal UI application...")
    print("Use arrow keys to navigate, Enter to select, ESC to quit")
    print()
    
    try:
        # Run the full UI
        run_ui()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ UI demo failed: {e}")


def main():
    """Main demo function"""
    print("🎮 RPGSim - Modular UI System Demo")
    print("═" * 60)
    print()
    print("This demo showcases the refactored modular UI system with:")
    print("• Rich ASCII art for characters, locations, and items")
    print("• Animated combat and effects")
    print("• Formatted game log with message types")
    print("• Beautiful terminal interface with Textual framework")
    print("• Clean modular architecture following DDD principles")
    print()
    
    # Demo menu
    while True:
        print("🎯 Choose demo option:")
        print("1. Character Creation (ASCII Art)")
        print("2. Locations & Environments")
        print("3. Combat & Effects")
        print("4. Items & Equipment")
        print("5. Game Log & Messages")
        print("6. Full UI Application")
        print("0. Exit")
        print()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Thanks for trying RPGSim UI Demo!")
                break
            elif choice == "1":
                demo_character_creation()
            elif choice == "2":
                demo_locations()
            elif choice == "3":
                demo_combat()
            elif choice == "4":
                demo_items()
            elif choice == "5":
                demo_game_log()
            elif choice == "6":
                demo_full_ui()
                break
            else:
                print("❌ Invalid choice. Please enter 0-6.")
            
            print("\n" + "─" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Demo error: {e}")
            break


if __name__ == "__main__":
    main()