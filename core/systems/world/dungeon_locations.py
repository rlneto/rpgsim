"""
World System Update for Dungeon Locations
FOCUS: Add dungeon entrances to existing world
"""

from typing import Dict, List, Optional

# Add dungeon locations to existing world
def add_dungeon_locations_to_world():
    """Add dungeon locations to world system"""
    
    # Create dungeon entrance locations
    dungeon_entrances = [
        {
            "location_id": "goblin_cave_entrance",
            "name": "Goblin Cave Entrance",
            "location_type": "dungeon",
            "description": "A dark cave entrance where goblins have been seen coming from.",
            "coordinates": {"x": 150, "y": 200},
            "connections": [],
            "features": ["dangerous", "goblin_territory"],
            "accessible": True,
            "level_requirement": 1
        },
        {
            "location_id": "abandoned_mine_entrance", 
            "name": "Abandoned Mine Entrance",
            "location_type": "dungeon",
            "description": "An old mine entrance, now home to dangerous creatures.",
            "coordinates": {"x": 300, "y": 150},
            "connections": [],
            "features": ["dark", "underground", "monster_lair"],
            "accessible": True,
            "level_requirement": 3
        }
    ]
    
    return dungeon_entrances

# Add to world service
def get_dungeon_locations():
    """Get all dungeon locations"""
    return add_dungeon_locations_to_world()

# Quick BDD function
def get_dungeon_entrance(dungeon_name: str) -> Dict:
    """Get dungeon entrance information (BDD compliant)"""
    dungeons = add_dungeon_locations_to_world()
    
    for dungeon in dungeons:
        if dungeon_name.lower() in dungeon["name"].lower():
            return {
                "location_id": dungeon["location_id"],
                "name": dungeon["name"],
                "description": dungeon["description"],
                "level_requirement": dungeon["level_requirement"],
                "features": dungeon["features"],
                "accessible": dungeon["accessible"]
            }
    
    return {"error": f"Dungeon '{dungeon_name}' not found"}
