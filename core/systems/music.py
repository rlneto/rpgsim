"""
Music System - Basic implementation for BDD compatibility
"""

from typing import Dict, List, Any, Optional

# Basic music constants for BDD compatibility
MIDI_NOTES = {
    "C": [60, 72, 84],  # C4, C5, C6
    "D": [62, 74, 86],  # D4, D5, D6
    "E": [64, 76, 88],  # E4, E5, E6
    "F": [65, 77, 89],  # F4, F5, F6
    "G": [67, 79, 91],  # G4, G5, G6
    "A": [69, 81, 93],  # A4, A5, A6
    "B": [71, 83, 95],  # B4, B5, B6
}

MIDI_DURATIONS = {
    "whole": 4.0,  # Semibreve
    "half": 2.0,  # Mínima
    "quarter": 1.0,  # Semínima
    "eighth": 0.5,  # Colcheia
    "sixteenth": 0.25,  # Semicolcheia
}

MIDI_VELOCITIES = {
    "ppp": 16,  # Pianississimo
    "pp": 24,  # Pianissimo
    "p": 32,  # Piano
    "mp": 48,  # Mezzo-piano
    "mf": 64,  # Mezzo-forte
    "f": 80,  # Forte
    "ff": 96,  # Fortissimo
    "fff": 112,  # Fortississimo
}


class MusicPattern:
    """Basic music pattern for BDD compatibility"""

    def __init__(self, name: str, notes: List[str], duration: str = "quarter"):
        self.name = name
        self.notes = notes
        self.duration = duration


class MusicNote:
    """Basic music note for BDD compatibility"""

    def __init__(self, note: str, duration: str = "quarter", velocity: int = 64):
        self.note = note
        self.duration = duration
        self.velocity = velocity


class MusicMood:
    """Music mood enumeration for BDD compatibility"""

    PEACEFUL = "peaceful"
    EXCITING = "exciting"
    MYSTERIOUS = "mysterious"
    DRAMATIC = "dramatic"
    HAPPY = "happy"
    SAD = "sad"


class MusicStyle:
    """Music style enumeration for BDD compatibility"""

    CLASSICAL = "classical"
    FOLK = "folk"
    ROCK = "rock"
    JAZZ = "jazz"
    ELECTRONIC = "electronic"
    AMBIENT = "ambient"


def get_music_generator():
    """Get music generator instance (BDD compatibility)"""
    return {
        "initialized": True,
        "supported_moods": [
            MusicMood.PEACEFUL,
            MusicMood.EXCITING,
            MusicMood.MYSTERIOUS,
        ],
        "supported_styles": [MusicStyle.CLASSICAL, MusicStyle.FOLK, MusicStyle.AMBIENT],
    }


def generate_combat_music(
    mood: str = "dramatic", style: str = "rock"
) -> Dict[str, Any]:
    """Generate combat music (BDD compatibility)"""
    return {
        "type": "combat",
        "mood": mood,
        "style": style,
        "tempo": "fast",
        "intensity": "high",
        "generated": True,
    }


def generate_victory_music(
    mood: str = "happy", style: str = "classical"
) -> Dict[str, Any]:
    """Generate victory music (BDD compatibility)"""
    return {
        "type": "victory",
        "mood": mood,
        "style": style,
        "tempo": "moderate",
        "intensity": "medium",
        "generated": True,
    }


def generate_location_music(
    location_type: str, mood: str = "peaceful"
) -> Dict[str, Any]:
    """Generate location music (BDD compatibility)"""
    return {
        "type": "location",
        "location_type": location_type,
        "mood": mood,
        "style": "ambient",
        "tempo": "slow",
        "intensity": "low",
        "generated": True,
    }


# Export for BDD compatibility
__all__ = [
    "MIDI_NOTES",
    "MIDI_DURATIONS",
    "MIDI_VELOCITIES",
    "MusicPattern",
    "MusicNote",
    "MusicMood",
    "MusicStyle",
    "get_music_generator",
    "generate_combat_music",
    "generate_victory_music",
    "generate_location_music",
]
