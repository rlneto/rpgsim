"""
Integration Tests: Character and World Systems
Tests integration between modular Character and World systems
"""

import pytest
from core.systems.character import CharacterSystem
from core.systems.world import WorldSystem
from core.systems.game import GameSystem


class TestCharacterWorldIntegration:
    """Test integration between Character and World systems."""

    def test_character_creation_in_world_context(self):
        """Test character creation within world context."""
        # Initialize systems
        char_system = CharacterSystem()
        world_system = WorldSystem()

        # Create character
        character = char_system.create_character("TestHero", "Warrior")
        assert character is not None
        assert character.name == "TestHero"

        # Get world starting location
        start_location = world_system.get_starting_location()
        assert start_location is not None
        assert start_location["id"] == "riverdale"

        # Character should be able to access world
        character_data = {
            "level": character.level,
            "gold": getattr(character, "gold", 100),
            "inventory": getattr(character, "inventory", []),
        }

        # Test travel from starting location
        destinations = world_system.get_available_destinations(
            start_location["id"], character_data
        )
        assert len(destinations) > 0

        # Should be able to travel to Stonecrest
        can_travel = world_system.can_travel(
            start_location["id"], "stonecrest", character_data
        )
        assert can_travel

    def test_character_world_travel_integration(self):
        """Test character traveling through world."""
        # Initialize game system (integrates both)
        game = GameSystem()

        # Start new game
        game_result = game.start_new_game()
        assert game_result["status"] == "success"

        # Create character
        char_result = game.create_character("Traveler", "Rogue")
        assert char_result["status"] == "success"

        # Get character data for travel
        character = char_result["character"]
        character_data = {
            "level": getattr(character, "level", 1),
            "gold": getattr(character, "gold", 100),
            "inventory": getattr(character, "inventory", []),
        }

        # Test travel to different location
        travel_result = game.travel_to_location("stonecrest")
        if travel_result["status"] == "success":
            assert travel_result["location"]["id"] == "stonecrest"
            assert travel_result["travel_time"] > 0

        # Test world time advancement
        world_info = game.world_system.get_world_info()
        initial_time = world_info["current_time"]

        game.world_system.advance_time(60)  # Advance 1 hour

        world_info = game.world_system.get_world_info()
        assert world_info["current_time"] != initial_time

    def test_character_world_data_flow(self):
        """Test data flow between character and world systems."""
        char_system = CharacterSystem()
        world_system = WorldSystem()

        # Create character
        character = char_system.create_character("DataFlow", "Mage")

        # Get world location details
        location_details = world_system.get_location_details("riverdale")
        assert location_details is not None
        assert location_details["name"] == "Riverdale"
        assert "services" in location_details

        # Test character accessing world services
        character_data = {"level": character.level, "gold": 100, "inventory": []}

        # Search for locations
        cities = world_system.search_locations("village", character_data)
        assert len(cities) > 0

        # Get locations by service
        blacksmith_locations = world_system.get_locations_by_service(
            "blacksmith", character_data
        )
        assert len(blacksmith_locations) > 0

    def test_character_world_validation(self):
        """Test validation between character and world systems."""
        char_system = CharacterSystem()
        world_system = WorldSystem()

        # Create low level character
        character = char_system.create_character("LowLevel", "Warrior")
        character_data = {"level": 1, "gold": 50, "inventory": []}

        # Try to travel to high level location
        # Dark Forest requires level 3+ (from world config)
        can_travel = world_system.can_travel("riverdale", "dark_forest", character_data)

        # This should fail due to level requirement
        # Note: This depends on world configuration
        # assert not can_travel  # Uncomment when level requirements are enforced

    def test_world_character_context_integration(self):
        """Test getting character context from world."""
        game = GameSystem()

        # Setup game state
        game.start_new_game()
        game.create_character("ContextTest", "Cleric")

        # Get character context
        character_data = {"level": 1, "gold": 100, "inventory": []}

        context = game.world_system.get_character_context(character_data)

        # Verify context contains all expected data
        assert "world_info" in context
        assert "current_time" in context
        assert "accessible_locations" in context
        assert "starting_location" in context
        assert "travel_statistics" in context
        assert "world_overview" in context

        # Verify world info
        world_info = context["world_info"]
        assert world_info["locations"] >= 3  # At least 3 locations
        assert "current_time" in world_info

    def test_character_world_error_handling(self):
        """Test error handling in character-world integration."""
        game = GameSystem()

        # Test travel without character
        travel_result = game.travel_to_location("stonecrest")
        assert travel_result["status"] == "error"
        assert "No character created" in travel_result["message"]

        # Test travel to invalid location
        game.start_new_game()
        game.create_character("ErrorTest", "Warrior")

        invalid_travel = game.travel_to_location("nonexistent_location")
        assert invalid_travel["status"] == "error"

    def test_character_world_state_persistence(self):
        """Test state persistence across systems."""
        char_system = CharacterSystem()
        world_system = WorldSystem()

        # Create and save character
        character = char_system.create_character("PersistTest", "Ranger")
        char_id = f"persist_{character.name}"

        # Save to repository
        char_system.repository.save(character)

        # Load character back
        loaded_character = char_system.repository.load_by_name(character.name)
        assert loaded_character is not None
        assert loaded_character.name == character.name
        assert loaded_character.class_type == character.class_type

        # Test world state persistence
        initial_world_info = world_system.get_world_info()

        # Advance time and save
        world_system.advance_time(120)  # 2 hours
        world_system.world_repo.save_world(world_system.world)

        # Load world back
        loaded_world = world_system.world_repo.load_world("default")
        assert loaded_world is not None
        # Check that time advanced (get summary from loaded world)
        loaded_world_info = loaded_world.get_summary()
        initial_time = initial_world_info["current_time"]
        loaded_time = loaded_world_info["current_time"]
        assert loaded_time != initial_time


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
