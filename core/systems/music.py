"""
Music System for RPGSim
LLM Agent-Optimized music generation system with MIDI support
Supports dynamic music generation for different game scenarios
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

# Music generation constants
MIDI_NOTES = {
    'C': [60, 72, 84],     # C4, C5, C6
    'D': [62, 74, 86],     # D4, D5, D6
    'E': [64, 76, 88],     # E4, E5, E6
    'F': [65, 77, 89],     # F4, F5, F6
    'G': [67, 79, 91],     # G4, G5, G6
    'A': [69, 81, 93],     # A4, A5, A6
    'B': [71, 83, 95],     # B4, B5, B6
}

MIDI_DURATIONS = {
    'whole': 4.0,      # Semibreve
    'half': 2.0,       # Mínima
    'quarter': 1.0,    # Semínima
    'eighth': 0.5,     # Colcheia
    'sixteenth': 0.25, # Semicolcheia
}

MIDI_VELOCITIES = {
    'piano': 40,       # Suave
    'mezzo': 70,      # Médio
    'forte': 100,     # Forte
    'fortissimo': 127  # Muito forte
}

class MusicMood(Enum):
    """Music moods for different game situations"""
    PEACEFUL = "peaceful"
    COMBAT = "combat"
    TENSE = "tense"
    VICTORY = "victory"
    MYSTERIOUS = "mysterious"
    SAD = "sad"
    EPIC = "epic"
    MAGICAL = "magical"

class MusicStyle(Enum):
    """Musical styles for different locations/classes"""
    MEDIEVAL = "medieval"
    FANTASY = "fantasy"
    ORCHESTRAL = "orchestral"
    AMBIENT = "ambient"
    TRIBAL = "tribal"
    TECHNO = "techno"
    CLASSICAL = "classical"
    MAGICAL = "magical"

@dataclass
class MusicNote:
    """Single musical note with MIDI properties"""
    note: str           # Note name (C, D, E, etc.)
    octave: int         # Octave number (4-6 common)
    midi_note: int      # MIDI note number (0-127)
    duration: float     # Duration in beats
    velocity: int       # Volume/attack (0-127)
    channel: int = 0     # MIDI channel (0-15)

@dataclass
class MusicChord:
    """Musical chord with multiple notes"""
    notes: List[MusicNote]
    name: str = ""

    def to_midi_events(self) -> List[Dict[str, Any]]:
        """Convert chord to MIDI events"""
        events = []
        for note in self.notes:
            events.append({
                'type': 'note_on',
                'note': note.midi_note,
                'velocity': note.velocity,
                'channel': note.channel,
                'time': 0
            })
            events.append({
                'type': 'note_off',
                'note': note.midi_note,
                'velocity': 0,
                'channel': note.channel,
                'time': note.duration
            })
        return events

@dataclass
class MusicPattern:
    """Musical pattern for generation"""
    notes: List[Union[MusicNote, MusicChord]]
    tempo: int = 120      # BPM
    time_signature: Tuple[int, int] = (4, 4)  # (numerator, denominator)
    key: str = "C"        # Musical key

class MusicGenerator:
    """LLM Agent-Optimized music generator for RPGSim"""

    def __init__(self):
        self.templates = self._initialize_music_templates()
        self.current_playing = {}
        self.music_history = []

    def _initialize_music_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize pre-defined music templates for different moods"""
        return {
            'peaceful': {
                'tempo': 80,
                'key': 'C',
                'scale': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
                'progression': ['C', 'G', 'A', 'F'],
                'rhythm_pattern': [1.0, 0.5, 0.5, 1.0],
                'velocity_range': (40, 70)
            },
            'combat': {
                'tempo': 140,
                'key': 'E',
                'scale': ['E', 'F#', 'G', 'A', 'B', 'C#', 'D#'],
                'progression': ['E', 'F#', 'C#', 'A'],
                'rhythm_pattern': [0.5, 0.25, 0.25, 0.5, 0.5],
                'velocity_range': (80, 120)
            },
            'mysterious': {
                'tempo': 70,
                'key': 'A',
                'scale': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                'progression': ['Am', 'G', 'C', 'F'],
                'rhythm_pattern': [1.0, 0.5, 1.0, 0.5],
                'velocity_range': (30, 60)
            },
            'victory': {
                'tempo': 120,
                'key': 'G',
                'scale': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                'progression': ['G', 'D', 'Em', 'C'],
                'rhythm_pattern': [1.0, 0.5, 0.5, 0.5, 0.5],
                'velocity_range': (90, 120)
            },
            'magical': {
                'tempo': 100,
                'key': 'D',
                'scale': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
                'progression': ['Dm', 'G', 'Am', 'Dm'],
                'rhythm_pattern': [0.75, 0.25, 0.5, 0.5],
                'velocity_range': (50, 80)
            }
        }

    def generate_theme_music(self, mood: MusicMood, style: MusicStyle,
                           duration_bars: int = 4) -> MusicPattern:
        """
        Generate theme music based on mood and style

        Args:
            mood: Music mood for the situation
            style: Musical style to apply
            duration_bars: Number of bars to generate

        Returns:
            MusicPattern: Generated musical pattern
        """
        template = self.templates.get(mood.value, self.templates['peaceful'])

        # Generate melody notes
        melody = []
        progression = template['progression']
        rhythm_pattern = template['rhythm_pattern']

        for bar in range(duration_bars):
            for chord_idx, chord_name in enumerate(progression):
                base_note = chord_name.replace('m', '')  # Remove minor indicator

                # Create notes for this chord
                chord_notes = self._create_chord_notes(
                    base_note,
                    template['scale'],
                    template['velocity_range']
                )

                # Apply rhythm pattern
                for i, duration in enumerate(rhythm_pattern):
                    if i < len(chord_notes):
                        note = MusicNote(
                            note=chord_notes[i][0],
                            octave=chord_notes[i][1],
                            midi_note=chord_notes[i][2],
                            duration=duration,
                            velocity=chord_notes[i][3]
                        )
                        melody.append(note)

        return MusicPattern(
            notes=melody,
            tempo=template['tempo'],
            time_signature=(4, 4),
            key=template['key']
        )

    def _create_chord_notes(self, root: str, scale: List[str],
                           velocity_range: Tuple[int, int]) -> List[Tuple[str, int, int, int]]:
        """Create chord notes with MIDI values"""
        chord_notes = []

        # Map notes to MIDI
        note_to_midi = {
            'C': [60, 72, 84], 'D': [62, 74, 86], 'E': [64, 76, 88],
            'F': [65, 77, 89], 'G': [67, 79, 91], 'A': [69, 81, 93],
            'B': [71, 83, 95]
        }

        # Simple chord (root, third, fifth)
        root_idx = scale.index(root[0]) if root[0] in scale else 0

        # Root note
        if root[0] in note_to_midi:
            chord_notes.append((root[0], 5, note_to_midi[root[0]][1],
                             velocity_range[0]))

        # Third
        if root_idx + 2 < len(scale):
            third_note = scale[root_idx + 2]
            if third_note in note_to_midi:
                chord_notes.append((third_note, 5, note_to_midi[third_note][1],
                                 velocity_range[1]))

        # Fifth
        if root_idx + 4 < len(scale):
            fifth_note = scale[root_idx + 4]
            if fifth_note in note_to_midi:
                chord_notes.append((fifth_note, 5, note_to_midi[fifth_note][1],
                                 velocity_range[1]))

        return chord_notes

    def to_midi_file(self, pattern: MusicPattern, filename: str) -> bool:
        """
        Convert music pattern to MIDI file

        Args:
            pattern: Music pattern to convert
            filename: Output filename

        Returns:
            bool: Success status
        """
        try:
            # Create simple MIDI file format
            midi_data = {
                'format': 'MIDI_FILE',
                'tracks': 1,
                'tempo': pattern.tempo,
                'time_signature': pattern.time_signature,
                'key': pattern.key,
                'events': []
            }

            # Convert notes to MIDI events
            current_time = 0
            for note_or_chord in pattern.notes:
                if isinstance(note_or_chord, MusicNote):
                    midi_data['events'].extend([
                        {
                            'type': 'note_on',
                            'note': note_or_chord.midi_note,
                            'velocity': note_or_chord.velocity,
                            'time': current_time
                        },
                        {
                            'type': 'note_off',
                            'note': note_or_chord.midi_note,
                            'velocity': 0,
                            'time': current_time + note_or_chord.duration
                        }
                    ])
                current_time += note_or_chord.duration

            # Save to file (simplified format)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(midi_data, f, indent=2)

            return True

        except Exception as e:
            return False

    def to_llm_prompt(self, pattern: MusicPattern) -> str:
        """
        Convert music pattern to LLM-friendly prompt

        Args:
            pattern: Music pattern to convert

        Returns:
            str: LLM prompt describing the music
        """
        prompt = f"""
Generate music with the following characteristics:
- Tempo: {pattern.tempo} BPM
- Key: {pattern.key}
- Time Signature: {pattern.time_signature[0]}/{pattern.time_signature[1]}
- Notes: {len(pattern.notes)} notes/chords

Musical sequence:
"""

        for i, note_or_chord in enumerate(pattern.notes[:10]):  # First 10 notes
            if isinstance(note_or_chord, MusicNote):
                prompt += f"- {note_or_chord.note}{note_or_chord.octave} (duration: {note_or_chord.duration}, velocity: {note_or_chord.velocity})\n"

        if len(pattern.notes) > 10:
            prompt += f"... and {len(pattern.notes) - 10} more notes\n"

        return prompt

    def create_ambient_loop(self, location_type: str, length_seconds: int = 30) -> MusicPattern:
        """
        Create ambient music loop for locations

        Args:
            location_type: Type of location (city, dungeon, forest, etc.)
            length_seconds: Desired loop length in seconds

        Returns:
            MusicPattern: Generated ambient pattern
        """
        # Map locations to moods
        location_moods = {
            'city': MusicMood.PEACEFUL,
            'dungeon': MusicMood.MYSTERIOUS,
            'forest': MusicMood.MAGICAL,
            'battle': MusicMood.COMBAT,
            'temple': MusicMood.EPIC,
            'tavern': MusicMood.PEACEFUL,
            'shop': MusicMood.PEACEFUL
        }

        mood = location_moods.get(location_type, MusicMood.PEACEFUL)

        # Generate loop
        pattern = self.generate_theme_music(mood, MusicStyle.AMBIENT,
                                           duration_bars=4)

        # Adjust for loop length
        total_duration = sum(note.duration for note in pattern.notes)
        if total_duration > 0:
            repeat_count = int((length_seconds * pattern.tempo / 60) / total_duration)

            # Repeat pattern
            original_notes = pattern.notes.copy()
            for _ in range(repeat_count - 1):
                pattern.notes.extend(original_notes)

        return pattern

# Global music generator instance
_music_generator: Optional[MusicGenerator] = None

def get_music_generator() -> MusicGenerator:
    """Get or create global music generator"""
    global _music_generator
    if _music_generator is None:
        _music_generator = MusicGenerator()
    return _music_generator

def generate_combat_music(battle_intensity: str = "medium") -> MusicPattern:
    """Generate combat music with specified intensity"""
    generator = get_music_generator()

    if battle_intensity == "light":
        mood = MusicMood.COMBAT
        style = MusicStyle.TRIBAL
    elif battle_intensity == "heavy":
        mood = MusicMood.EPIC
        style = MusicStyle.ORCHESTRAL
    else:  # medium
        mood = MusicMood.COMBAT
        style = MusicStyle.FANTASY

    return generator.generate_theme_music(mood, style, duration_bars=8)

def generate_victory_music(player_class: str = "warrior") -> MusicPattern:
    """Generate victory music based on player class"""
    generator = get_music_generator()

    # Class-specific victory styles
    class_styles = {
        'warrior': MusicStyle.ORCHESTRAL,
        'mage': MusicStyle.MAGICAL,
        'rogue': MusicStyle.MEDIEVAL,
        'developer': MusicStyle.TECHNO
    }

    style = class_styles.get(player_class, MusicStyle.FANTASY)
    return generator.generate_theme_music(MusicMood.VICTORY, style, duration_bars=4)

def generate_location_music(location_type: str, location_name: str = "") -> MusicPattern:
    """Generate location-specific ambient music"""
    generator = get_music_generator()

    # Special locations get unique treatment
    if "dungeon" in location_name.lower():
        mood = MusicMood.MYSTERIOUS
        style = MusicStyle.AMBIENT
    elif "city" in location_name.lower():
        mood = MusicMood.PEACEFUL
        style = MusicStyle.MEDIEVAL
    elif "temple" in location_name.lower():
        mood = MusicMood.EPIC
        style = MusicStyle.CLASSICAL
    else:
        mood = MusicMood.PEACEFUL
        style = MusicStyle.FANTASY

    return generator.create_ambient_loop(location_type, length_seconds=20)