#!/usr/bin/env python3
"""
RPGSim - Text-based RPG Simulation
Main entry point for the game

Usage:
    python main.py [command] [options]

Commands:
    start          - Start a new game
    test           - Run all quality checks
    dev            - Development mode with test features
    help           - Show this help message
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class RPGSimCLI:
    """Command Line Interface for RPGSim"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="RPGSim - Text-based RPG Simulation",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py start           # Start a new game
  python main.py test            # Run quality checks
  python main.py dev --character # Test character creation
  python main.py help            # Show this help message
            """,
        )

        self._setup_commands()

    def _setup_commands(self):
        """Setup command line arguments"""
        subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        # Start command
        start_parser = subparsers.add_parser("start", help="Start a new game")
        start_parser.add_argument("--name", type=str, help="Character name")
        start_parser.add_argument(
            "--class", type=str, dest="class_name", help="Character class"
        )

        # Test command
        test_parser = subparsers.add_parser("test", help="Run quality checks")
        test_parser.add_argument("--system", type=str, help="Test specific system only")
        test_parser.add_argument(
            "--verbose", "-v", action="store_true", help="Verbose output"
        )

        # Development command
        dev_parser = subparsers.add_parser("dev", help="Development mode")
        dev_parser.add_argument(
            "--character", action="store_true", help="Test character creation"
        )
        dev_parser.add_argument(
            "--world", action="store_true", help="Test world system"
        )
        dev_parser.add_argument(
            "--combat", action="store_true", help="Test combat system"
        )

        # Help command
        subparsers.add_parser("help", help="Show this help message")

    def run(self, args=None):
        """Run the CLI with given arguments"""
        if args is None:
            args = sys.argv[1:]

        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command or parsed_args.command == "help":
            self.parser.print_help()
            return

        # Route to appropriate handler
        command_handlers = {
            "start": self._handle_start,
            "test": self._handle_test,
            "dev": self._handle_dev,
        }

        handler = command_handlers.get(parsed_args.command)
        if handler:
            handler(parsed_args)
        else:
            print(f"Unknown command: {parsed_args.command}")
            self.parser.print_help()

    def _handle_start(self, args):
        """Handle game start command"""
        print("Welcome to RPGSim!")
        print("=" * 50)

        try:
            # Import game engine
            from core.engine import get_game_engine

            # Start new game
            if args.name and args.class_name:
                engine = get_game_engine()
                success = engine.start_new_game(args.name, args.class_name)

                if success:
                    status = engine.get_game_status()
                    player = status["game_state"]["player"]
                    print(f"Created {args.name} the {args.class_name}")
                    print(f"   Level: {player['level']}")
                    print(f"   HP: {player['hp']}")
                    print(f"   Gold: {player['gold']}")
                    print(f"   Abilities: {player['abilities_count']}")
                    print("Game would start here...")
                else:
                    print(
                        f"Failed to create character: {args.name} ({args.class_name})"
                    )
            else:
                print("Please provide --name and --class to start game")
                print("Example: python main.py start --name Aragorn --class Warrior")

        except ImportError as e:
            print(f"Import error: {e}")
        except Exception as e:
            print(f"Error starting game: {e}")

    def _handle_test(self, args):
        """Handle testing command"""
        print("Running RPGSim Quality Checks")
        print("=" * 50)

        try:
            from tests.quality_checker import run_quality_checks

            if args.system:
                success = run_quality_checks(
                    system_only=args.system, verbose=args.verbose
                )
            else:
                success = run_quality_checks(verbose=args.verbose)

            if success:
                print("All quality checks passed!")
                sys.exit(0)
            else:
                print("Some quality checks failed!")
                sys.exit(1)

        except ImportError:
            print("Quality checker not yet implemented")
            sys.exit(1)
        except Exception as e:
            print(f"Error running tests: {e}")
            sys.exit(1)

    def _handle_dev(self, args):
        """Handle development mode command"""
        print("RPGSim Development Mode")
        print("=" * 50)

        try:
            if args.character:
                self._test_character_creation()
            elif args.world:
                print("World system testing not yet implemented")
            elif args.combat:
                print("Combat system testing not yet implemented")
            else:
                print("Available development tests:")
                print("  --character   Test character creation")
                print("  --world        Test world system (coming soon)")
                print("  --combat       Test combat system (coming soon)")
                print("\nUse: python main.py dev --[feature]")

        except Exception as e:
            print(f"Error in development mode: {e}")

    def _test_character_creation(self):
        """Test character creation interactively"""
        print("Testing Character Creation System")
        print("-" * 40)

        try:
            from core.engine import get_game_engine

            # Test basic character creation
            engine = get_game_engine()
            success = engine.start_new_game("TestCharacter", "Warrior")

            if success:
                status = engine.get_game_status()
                player = status["game_state"]["player"]
                print("Character created successfully")
                print(f"   Name: {player['name']}")
                print(f"   Class: {player['class']}")
                print(f"   Level: {player['level']}")
                print(f"   HP: {player['hp']}")
                print(f"   Gold: {player['gold']}")
                print(f"   Abilities: {player['abilities_count']}")
                print(f"   Inventory: {player['inventory_size']} items")
            else:
                print("Failed to create test character")

        except ImportError as e:
            print("Character system not yet implemented")
            print(f"Import error: {e}")
        except Exception as e:
            print(f"Character creation test error: {e}")


def main():
    """Main entry point"""
    cli = RPGSimCLI()
    cli.run()


if __name__ == "__main__":
    main()
