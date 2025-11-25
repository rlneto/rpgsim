"""
Save and load system for RPGSim
Provides persistent game state management with auto-save and quick-save functionality
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import dataclasses
from dataclasses import dataclass, asdict


@dataclass
class GameState:
    """Represents the complete state of the game"""
    player: Any  # Would be Player class in full implementation
    current_location: str
    world_time: int
    quest_progress: Dict[str, float]
    discovered_locations: List[str] = None
    inventory: List[str] = None
    known_spells: List[str] = None
    
    def __post_init__(self):
        """Initialize default values for optional fields"""
        if self.discovered_locations is None:
            self.discovered_locations = []
        if self.inventory is None:
            self.inventory = []
        if self.known_spells is None:
            self.known_spells = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary for serialization"""
        return {
            'player': {
                'name': self.player.name,
                'class': self.player.class_type,
                'level': self.player.level,
                'hp': self.player.hp,
                'max_hp': self.player.max_hp,
                'stats': self.player.stats,
                'abilities': self.player.abilities,
                'gold': self.player.gold,
                'quests': self.player.quests,
                'reputation': self.player.reputation
            },
            'current_location': self.current_location,
            'world_time': self.world_time,
            'quest_progress': self.quest_progress,
            'discovered_locations': self.discovered_locations,
            'inventory': self.inventory,
            'known_spells': self.known_spells
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create game state from dictionary"""
        # In a real implementation, this would create a proper Player object
        # For now, we'll create a mock player object
        mock_player = type('MockPlayer', (), {
            'name': data['player']['name'],
            'class_type': data['player']['class'],
            'level': data['player']['level'],
            'hp': data['player']['hp'],
            'max_hp': data['player']['max_hp'],
            'stats': data['player']['stats'],
            'abilities': data['player']['abilities'],
            'gold': data['player']['gold'],
            'quests': data['player']['quests'],
            'reputation': data['player']['reputation']
        })()
        
        return cls(
            player=mock_player,
            current_location=data['current_location'],
            world_time=data['world_time'],
            quest_progress=data['quest_progress'],
            discovered_locations=data.get('discovered_locations', []),
            inventory=data.get('inventory', []),
            known_spells=data.get('known_spells', [])
        )
    
    def is_valid(self) -> bool:
        """Check if game state is valid"""
        return (
            self.player is not None and
            hasattr(self.player, 'name') and
            self.current_location is not None and
            isinstance(self.world_time, int) and
            self.world_time >= 0 and
            isinstance(self.quest_progress, dict)
        )


@dataclass
class SaveData:
    """Represents save file data with metadata and game state"""
    metadata: Dict[str, Any]
    game_data: Dict[str, Any]
    
    def to_json(self) -> str:
        """Convert save data to JSON string"""
        return json.dumps({
            'metadata': self.metadata,
            'game_data': self.game_data
        }, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SaveData':
        """Create save data from JSON string"""
        data = json.loads(json_str)
        return cls(
            metadata=data['metadata'],
            game_data=data['game_data']
        )
    
    def is_valid(self) -> bool:
        """Check if save data is valid"""
        return (
            isinstance(self.metadata, dict) and
            'version' in self.metadata and
            isinstance(self.game_data, dict)
        )


class SaveManager:
    """Manages game save/load operations"""
    
    def __init__(self, save_directory: str = "saves", max_save_slots: int = 10):
        """
        Initialize save manager
        
        Args:
            save_directory: Directory to store save files
            max_save_slots: Maximum number of save slots
        """
        self.save_directory = save_directory
        self.max_save_slots = max_save_slots
        self.auto_save_enabled = False
        self.auto_save_interval = 180  # 3 minutes in seconds
        self.last_auto_save_time = 0
        self.current_game_state = None
        
        # Ensure save directory exists
        os.makedirs(self.save_directory, exist_ok=True)
    
    def save_game(self, game_state: GameState, slot: int) -> str:
        """
        Save game state to specified slot
        
        Args:
            game_state: The game state to save
            slot: Save slot number (1-max_save_slots)
            
        Returns:
            Path to the saved file
            
        Raises:
            ValueError: If slot is out of range
        """
        if not 1 <= slot <= self.max_save_slots:
            raise ValueError(f"Slot must be between 1 and {self.max_save_slots}")
        
        if not game_state.is_valid():
            raise ValueError("Invalid game state")
        
        # Create save data with metadata
        metadata = {
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'player_level': game_state.player.level,
            'player_name': game_state.player.name,
            'play_time': game_state.world_time,
            'location': game_state.current_location
        }
        
        save_data = SaveData(metadata, game_state.to_dict())
        save_path = os.path.join(self.save_directory, f"save_{slot}.json")
        
        # Write save file
        with open(save_path, 'w') as f:
            f.write(save_data.to_json())
        
        return save_path
    
    def load_game(self, slot: int) -> GameState:
        """
        Load game state from specified slot
        
        Args:
            slot: Save slot number (1-max_save_slots)
            
        Returns:
            Loaded game state
            
        Raises:
            FileNotFoundError: If save file doesn't exist
            ValueError: If save file is corrupted
        """
        if not 1 <= slot <= self.max_save_slots:
            raise ValueError(f"Slot must be between 1 and {self.max_save_slots}")
        
        save_path = os.path.join(self.save_directory, f"save_{slot}.json")
        
        if not os.path.exists(save_path):
            raise FileNotFoundError(f"Save file for slot {slot} not found")
        
        try:
            with open(save_path, 'r') as f:
                json_str = f.read()
            
            save_data = SaveData.from_json(json_str)
            
            if not save_data.is_valid():
                raise ValueError("Invalid save data")
            
            return GameState.from_dict(save_data.game_data)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted save file: {e}")
    
    def list_save_files(self) -> List[Dict[str, Any]]:
        """
        List all available save files
        
        Returns:
            List of save file information
        """
        save_files = []
        
        for slot in range(1, self.max_save_slots + 1):
            save_path = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r') as f:
                        save_data = SaveData.from_json(f.read())
                    
                    save_info = {
                        'slot': slot,
                        'path': save_path,
                        'metadata': save_data.metadata
                    }
                    save_files.append(save_info)
                    
                except (json.JSONDecodeError, ValueError):
                    # Skip corrupted save files
                    save_info = {
                        'slot': slot,
                        'path': save_path,
                        'metadata': None,
                        'corrupted': True
                    }
                    save_files.append(save_info)
        
        return save_files
    
    def delete_save(self, slot: int) -> bool:
        """
        Delete save file for specified slot
        
        Args:
            slot: Save slot number (1-max_save_slots)
            
        Returns:
            True if file was deleted, False if file didn't exist
        """
        if not 1 <= slot <= self.max_save_slots:
            raise ValueError(f"Slot must be between 1 and {self.max_save_slots}")
        
        save_path = os.path.join(self.save_directory, f"save_{slot}.json")
        
        if os.path.exists(save_path):
            os.remove(save_path)
            return True
        
        return False
    
    def enable_auto_save(self, game_state: GameState, interval_seconds: int = 180):
        """
        Enable auto-save functionality
        
        Args:
            game_state: Current game state to auto-save
            interval_seconds: Auto-save interval in seconds
        """
        self.auto_save_enabled = True
        self.auto_save_interval = interval_seconds
        self.current_game_state = game_state
        self.last_auto_save_time = time.time()
    
    def disable_auto_save(self):
        """Disable auto-save functionality"""
        self.auto_save_enabled = False
        self.current_game_state = None
    
    def trigger_auto_save(self) -> bool:
        """
        Trigger auto-save if interval has passed
        
        Returns:
            True if auto-save was triggered, False otherwise
        """
        if not self.auto_save_enabled or self.current_game_state is None:
            return False
        
        current_time = time.time()
        
        if current_time - self.last_auto_save_time >= self.auto_save_interval:
            try:
                self.save_game(self.current_game_state, slot=0)  # Use slot 0 for auto-save
                self.last_auto_save_time = current_time
                return True
            except Exception:
                # In a real implementation, we would log this error
                return False
        
        return False
    
    def quick_save(self, game_state: GameState) -> str:
        """
        Perform quick save
        
        Args:
            game_state: Game state to save
            
        Returns:
            Path to quick save file
        """
        if not game_state.is_valid():
            raise ValueError("Invalid game state")
        
        # Create save data with metadata
        metadata = {
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'player_level': game_state.player.level,
            'player_name': game_state.player.name,
            'play_time': game_state.world_time,
            'save_type': 'quicksave'
        }
        
        save_data = SaveData(metadata, game_state.to_dict())
        save_path = os.path.join(self.save_directory, "quicksave.json")
        
        # Write quick save file
        with open(save_path, 'w') as f:
            f.write(save_data.to_json())
        
        return save_path
    
    def load_quick_save(self) -> GameState:
        """
        Load quick save
        
        Returns:
            Loaded game state
            
        Raises:
            FileNotFoundError: If quick save doesn't exist
            ValueError: If quick save is corrupted
        """
        save_path = os.path.join(self.save_directory, "quicksave.json")
        
        if not os.path.exists(save_path):
            raise FileNotFoundError("No quick save file found")
        
        try:
            with open(save_path, 'r') as f:
                json_str = f.read()
            
            save_data = SaveData.from_json(json_str)
            
            if not save_data.is_valid():
                raise ValueError("Invalid quick save data")
            
            return GameState.from_dict(save_data.game_data)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted quick save file: {e}")
    
    def get_save_slot_info(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific save slot
        
        Args:
            slot: Save slot number
            
        Returns:
            Save slot information or None if no save exists
        """
        if not 1 <= slot <= self.max_save_slots:
            return None
        
        save_path = os.path.join(self.save_directory, f"save_{slot}.json")
        
        if not os.path.exists(save_path):
            return None
        
        try:
            with open(save_path, 'r') as f:
                save_data = SaveData.from_json(f.read())
            
            return {
                'slot': slot,
                'path': save_path,
                'metadata': save_data.metadata
            }
            
        except (json.JSONDecodeError, ValueError):
            return {
                'slot': slot,
                'path': save_path,
                'metadata': None,
                'corrupted': True
            }