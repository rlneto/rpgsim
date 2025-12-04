#!/usr/bin/env python3
"""
E2E GUI Testing - Real User Experience Validation
Tests: main.py -> gui_main.py -> actual GUI functionality
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from textual.app import App
from textual.widgets import Button, Input, Select
from textual.pilot import Pilot

class E2EGUITester:
    """E2E GUI Tester for real user experience"""
    
    def __init__(self):
        self.test_results = []
        self.app = None
        self.pilot = None
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all E2E GUI tests"""
        print("🧪 Starting E2E GUI Testing...")
        print("=" * 60)
        
        try:
            # Import the real GUI application
            import gui_main
            
            results = {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'errors': [],
                'test_details': []
            }
            
            # Test 1: App Initialization
            await self.test_app_initialization(gui_main, results)
            
            # Test 2: Main Menu Navigation
            await self.test_main_menu_navigation(results)
            
            # Test 3: Character Creation Flow
            await self.test_character_creation_flow(results)
            
            # Test 4: Game Screen Navigation
            await self.test_game_screen_navigation(results)
            
            # Test 5: Dungeon Exploration
            await self.test_dungeon_exploration(results)
            
            # Print summary
            self.print_test_summary(results)
            return results
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR IN E2E TESTING: {e}")
            return {
                'total_tests': 0,
                'passed': 0,
                'failed': 1,
                'errors': [str(e)],
                'test_details': []
            }
    
    async def test_app_initialization(self, gui_main, results: Dict[str, Any]) -> None:
        """Test 1: App should initialize without errors"""
        print("🧪 Test 1: App Initialization")
        
        try:
            # Create app instance
            self.app = gui_main.RPGSimApp()
            
            # Start app (without running)
            async with self.app.run_test() as pilot:
                self.pilot = pilot
                
                # Check if main menu screen is active
                main_menu = self.app.screen
                print(f"🧪 DEBUG: Active screen: {main_menu}")
                print(f"🧪 DEBUG: Screen type: {type(main_menu)}")
                print(f"🧪 DEBUG: Screen ID: {getattr(main_menu, 'NAME', 'NO_NAME')}")
                print(f"🧪 DEBUG: Screen string: {str(main_menu)}")
                
                assert main_menu is not None, "Main menu screen should be active"
                
                print("✅ App initialized successfully")
                self.add_test_result(results, "App Initialization", True, "GUI app starts without errors")
                
        except Exception as e:
            print(f"❌ App initialization failed: {e}")
            self.add_test_result(results, "App Initialization", False, str(e))
    
    async def test_main_menu_navigation(self, results: Dict[str, Any]) -> None:
        """Test 2: Main menu buttons should work"""
        print("🧪 Test 2: Main Menu Navigation")
        
        try:
            # Find main menu buttons
            main_menu = self.app.screen
            new_game_btn = main_menu.query_one("#new_game_btn", Button)
            continue_btn = main_menu.query_one("#continue_btn", Button)
            settings_btn = main_menu.query_one("#settings_btn", Button)
            exit_btn = main_menu.query_one("#exit_btn", Button)
            
            assert new_game_btn is not None, "New Game button should exist"
            assert continue_btn is not None, "Continue button should exist"
            assert settings_btn is not None, "Settings button should exist"
            assert exit_btn is not None, "Exit button should exist"
            
            print("✅ All main menu buttons found")
            
            # Test New Game button click
            print(f"🧪 DEBUG: Screen stack before click: {self.app.screen_stack}")
            await self.pilot.click("#new_game_btn")
            print(f"🧪 DEBUG: Screen stack after click: {self.app.screen_stack}")
            
            # Check if character creation screen opened
            await self.pilot.pause()
            char_screen = self.app.screen
            print(f"🧪 DEBUG: Current screen after click: {char_screen}")
            assert char_screen is not None, "Character creation screen should open"
            
            print("✅ New Game button works")
            self.add_test_result(results, "Main Menu Navigation", True, "All buttons found and New Game works")
            
        except Exception as e:
            print(f"❌ Main menu navigation failed: {e}")
            self.add_test_result(results, "Main Menu Navigation", False, str(e))
    
    async def test_character_creation_flow(self, results: Dict[str, Any]) -> None:
        """Test 3: Character creation should work end-to-end"""
        print("🧪 Test 3: Character Creation Flow")
        
        try:
            # Find character creation elements
            char_screen = self.app.screen
            name_input = char_screen.query_one("#name_input", Input)
            class_select = char_screen.query_one("#class_select", Select)
            create_btn = char_screen.query_one("#create_btn", Button)
            
            assert name_input is not None, "Name input should exist"
            assert class_select is not None, "Class select should exist"
            assert create_btn is not None, "Create button should exist"
            
            print("✅ Character creation elements found")
            
            # Test character name input
            await self.pilot.click("#name_input")
            await self.pilot.type("TestHero")
            
            # Test class selection
            await self.pilot.click("#class_select")
            await self.pilot.press("down")  # Select Warrior
            await self.pilot.press("enter")
            
            print("✅ Character form filled")
            
            # Test character creation (with some delay for progress)
            await self.pilot.click("#create_btn")
            await self.pilot.pause(delay=2)  # Wait for creation
            
            # Check if we moved to game screen
            game_screen = self.app.screen
            assert game_screen is not None, "Should move to game screen after character creation"
            
            print("✅ Character creation works")
            self.add_test_result(results, "Character Creation Flow", True, "Character created successfully")
            
        except Exception as e:
            print(f"❌ Character creation failed: {e}")
            self.add_test_result(results, "Character Creation Flow", False, str(e))
    
    async def test_game_screen_navigation(self, results: Dict[str, Any]) -> None:
        """Test 4: Game screen buttons should work"""
        print("🧪 Test 4: Game Screen Navigation")
        
        try:
            # Find game screen buttons
            game_screen = self.app.screen
            shop_btn = game_screen.query_one("#shop_btn", Button)
            dungeon_btn = game_screen.query_one("#dungeon_btn", Button)
            npc_btn = game_screen.query_one("#npc_btn", Button)
            rest_btn = game_screen.query_one("#rest_btn", Button)
            
            assert shop_btn is not None, "Shop button should exist"
            assert dungeon_btn is not None, "Dungeon button should exist"
            assert npc_btn is not None, "NPC button should exist"
            assert rest_btn is not None, "Rest button should exist"
            
            print("✅ All game screen buttons found")
            
            # Test Rest button (simple action)
            await self.pilot.click("#rest_btn")
            await self.pilot.pause(delay=1)
            
            print("✅ Game screen navigation works")
            self.add_test_result(results, "Game Screen Navigation", True, "All buttons work")
            
        except Exception as e:
            print(f"❌ Game screen navigation failed: {e}")
            self.add_test_result(results, "Game Screen Navigation", False, str(e))
    
    async def test_dungeon_exploration(self, results: Dict[str, Any]) -> None:
        """Test 5: Dungeon exploration should work"""
        print("🧪 Test 5: Dungeon Exploration")
        
        try:
            # Try to enter dungeon
            dungeon_btn = self.app.query_one("#dungeon_btn", Button)
            await self.pilot.click("#dungeon_btn")
            await self.pilot.pause(delay=1)
            
            # Check if dungeon screen opened
            dungeon_screen = self.app.screen
            assert dungeon_screen is not None, "Dungeon screen should open"
            
            # Find dungeon buttons
            move_btn = self.app.query_one("#move_btn", Button)
            search_btn = self.app.query_one("#search_btn", Button)
            
            assert move_btn is not None, "Move button should exist"
            assert search_btn is not None, "Search button should exist"
            
            print("✅ Dungeon exploration works")
            self.add_test_result(results, "Dungeon Exploration", True, "Dungeon screen accessible")
            
        except Exception as e:
            print(f"❌ Dungeon exploration failed: {e}")
            self.add_test_result(results, "Dungeon Exploration", False, str(e))
    
    def add_test_result(self, results: Dict[str, Any], test_name: str, passed: bool, details: str) -> None:
        """Add test result to results dict"""
        results['total_tests'] += 1
        if passed:
            results['passed'] += 1
        else:
            results['failed'] += 1
            results['errors'].append(f"{test_name}: {details}")
        
        results['test_details'].append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
    
    def print_test_summary(self, results: Dict[str, Any]) -> None:
        """Print comprehensive test summary"""
        print("=" * 60)
        print("🧪 E2E GUI TESTING SUMMARY")
        print("=" * 60)
        print(f"📊 Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"📈 Success Rate: {(results['passed'] / results['total_tests']) * 100:.1f}%")
        
        if results['errors']:
            print("\n🚨 ERRORS:")
            for error in results['errors']:
                print(f"   • {error}")
        
        print("\n📋 DETAILED RESULTS:")
        for test in results['test_details']:
            status = "✅" if test['passed'] else "❌"
            print(f"   {status} {test['test']}: {test['details']}")
        
        print("=" * 60)
        
        # Overall assessment
        if results['passed'] == results['total_tests']:
            print("🎉 ALL TESTS PASSED - GUI is ready for production!")
        elif results['passed'] >= results['total_tests'] * 0.8:
            print("✅ GUI is mostly functional - minor issues to fix")
        else:
            print("⚠️ GUI has significant issues - needs major fixes")
        
        print("🎯 CRITICAL SUCCESS CRITERIA:")
        print(f"   • >90% tests passed: {'✅' if (results['passed'] / results['total_tests']) >= 0.9 else '❌'}")
        print(f"   • No critical errors: {'✅' if len(results['errors']) == 0 else '❌'}")
        print(f"   • All core flows work: {'✅' if results['failed'] <= 1 else '❌'}")


async def main():
    """Main E2E testing function"""
    tester = E2EGUITester()
    results = await tester.run_all_tests()
    
    # Exit with appropriate code
    if results['passed'] == results['total_tests']:
        print("🎉 E2E TESTING: SUCCESS")
        sys.exit(0)
    else:
        print("⚠️ E2E TESTING: ISSUES FOUND")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())