"""
Test modular UI system
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all imports"""
    try:
        print("🧪 Testing modular UI imports...")
        
        # Test core system
        from game.ui import UISystem, get_ui_system, initialize_ui
        print("✅ Core UI system imports successful")
        
        # Test domain models
        from game.ui.domain.ui import UISession, UIState, MessageType
        print("✅ Domain models imports successful")
        
        # Test services
        from game.ui.services.ui_service import UIServiceFactory
        print("✅ Services imports successful")
        
        # Test assets
        from game.ui.assets.ascii_art import ASCIIArtAssets
        print("✅ Assets imports successful")
        
        # Test components
        from game.ui.components.ui_components import CharacterDisplay
        print("✅ Components imports successful")
        
        # Test screens
        from game.ui.screens.modern_terminal_ui import GameState
        print("✅ Screens imports successful")
        
        # Test main UI
        from game.ui.modular_ui import ModernTerminalUI
        print("✅ Main UI imports successful")
        
        print("\n🎉 All modular UI imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_ascii_art():
    """Test ASCII art loading"""
    try:
        print("\n🎨 Testing ASCII art loading...")
        
        from game.ui.assets.ascii_art import ASCIIArtAssets
        
        # Test character art
        warrior_art = ASCIIArtAssets.get_character_art("warrior")
        print(f"✅ Warrior art loaded: {bool(warrior_art)}")
        
        # Test location art
        city_art = ASCIIArtAssets.get_location_art("city")
        print(f"✅ City art loaded: {bool(city_art)}")
        
        # Test item art
        sword_art = ASCIIArtAssets.get_item_art("sword")
        print(f"✅ Sword art loaded: {bool(sword_art)}")
        
        # Test effect art
        explosion_art = ASCIIArtAssets.get_effect_art("explosion")
        print(f"✅ Explosion art loaded: {bool(explosion_art)}")
        
        print("\n🎨 ASCII art loading test successful!")
        return True
        
    except Exception as e:
        print(f"❌ ASCII art test error: {e}")
        return False

def test_ui_system():
    """Test UI system initialization"""
    try:
        print("\n🖥️ Testing UI system initialization...")
        
        from game.ui import UISystem
        
        # Create UI system
        ui_system = UISystem()
        print("✅ UI system created")
        
        # Test initialization
        initialized = ui_system.initialize_ui()
        print(f"✅ UI system initialized: {initialized}")
        
        # Test logging
        log_success = ui_system.log_message("Test message", "info")
        print(f"✅ Logging test: {log_success}")
        
        # Test asset loading
        art = ui_system.get_ascii_art("warrior")
        print(f"✅ Asset loading test: {bool(art)}")
        
        # Test UI status
        status = ui_system.get_ui_status()
        print(f"✅ UI status: {status}")
        
        # Cleanup
        cleanup_success = ui_system.cleanup_ui()
        print(f"✅ UI system cleanup: {cleanup_success}")
        
        print("\n🖥️ UI system test successful!")
        return True
        
    except Exception as e:
        print(f"❌ UI system test error: {e}")
        return False

def test_game_state():
    """Test game state handling"""
    try:
        print("\n🎮 Testing game state...")
        
        from game.ui.screens.modern_terminal_ui import GameState
        
        # Create game state
        game_state = GameState()
        print("✅ Game state created")
        
        # Test default player data
        player = game_state.player
        print(f"✅ Player name: {player['name']}")
        print(f"✅ Player class: {player['class']}")
        print(f"✅ Player level: {player['level']}")
        
        # Test status data
        status = game_state.status
        print(f"✅ HP: {status['hp']}/{status['max_hp']}")
        print(f"✅ Mana: {status['mana']}/{status['max_mana']}")
        
        print("\n🎮 Game state test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Game state test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 RPGSim Modular UI - System Test")
    print("═" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("ASCII Art Test", test_ascii_art),
        ("UI System Test", test_ui_system),
        ("Game State Test", test_game_state)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "═" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Modular UI system is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)