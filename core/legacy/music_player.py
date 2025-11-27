"""
Music Player System for RPGSim
LLM Agent-Optimized playback system using MusicPy
Supports immediate audio validation for AI-generated music
"""

import os
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

# Music imports for playback and synthesis
try:
    from musicpy import C, play, stop, export, sine, square, triangle, sawtooth, white_noise
    MUSICPY_AVAILABLE = True
except ImportError:
    MUSICPY_AVAILABLE = False
    print("MusicPy not available - audio playback disabled")

from core.systems.music import MusicPattern, MusicNote, MusicChord, MusicMood

@dataclass
class PlaybackSettings:
    """Audio playback settings"""
    sample_rate: int = 44100
    bit_rate: int = 16
    channels: int = 2
    volume: float = 0.7  # 0.0 to 1.0
    tempo_multiplier: float = 1.0  # Speed adjustment

class MusicPlayer:
    """LLM Agent-Optimized music player with immediate validation"""

    def __init__(self):
        self.settings = PlaybackSettings()
        self.currently_playing = None
        self.audio_cache = {}

    def play_pattern_immediately(self, pattern: MusicPattern, mood: MusicMood = MusicMood.PEACEFUL) -> bool:
        """
        Convert and play pattern immediately for AI validation

        Args:
            pattern: Music pattern to play
            mood: Music mood for timbre selection

        Returns:
            bool: Success status
        """
        if not MUSICPY_AVAILABLE:
            print("MusicPy not available for audio playback")
            return False

        try:
            # Convert our pattern to MusicPy format
            musicpy_chord = self._convert_to_musicpy(pattern, mood)

            # Play immediately for validation
            play(musicpy_chord)

            # Cache for replay
            cache_key = f"pattern_{hash(str(pattern.notes))}_{mood.value}"
            self.audio_cache[cache_key] = musicpy_chord

            return True

        except Exception as e:
            print(f"Playback failed: {e}")
            return False

    def _convert_to_musicpy(self, pattern: MusicPattern, mood: MusicMood):
        """Convert our MusicPattern to MusicPy chord format"""

        # Select appropriate timbre based on mood
        timbre_functions = {
            MusicMood.PEACEFUL: sine,
            MusicMood.COMBAT: square,
            MusicMood.MYSTERIOUS: triangle,
            MusicMood.VICTORY: sawtooth,
            MusicMood.MAGICAL: sine  # Sine with effects
        }

        wave_function = timbre_functions.get(mood, sine)

        # Convert notes to MusicPy format
        chord_notes = []

        for note_or_chord in pattern.notes:
            if isinstance(note_or_chord, MusicNote):
                # Single note - convert pitch to MusicPy format
                pitch_name = f"{note_or_chord.note}{note_or_chord.octave}"

                # Generate audio with appropriate waveform
                duration = note_or_chord.duration * 4  # Convert to quarter notes
                volume = note_or_chord.velocity / 127.0  # Normalize to 0-1

                if mood == MusicMood.MAGICAL:
                    # Add magical effect with slight modulation
                    note_wave = wave_function(pitch_name, duration=duration, volume=volume)
                    # Apply subtle effects (would need MusicPy's effects)
                else:
                    note_wave = wave_function(pitch_name, duration=duration, volume=volume)

                chord_notes.append(note_wave)

        # Combine all notes into a chord
        if chord_notes:
            # MusicPy can combine multiple audio segments
            # This is simplified - in real implementation would need proper timing
            return C('chord', notes=chord_notes)
        else:
            # Generate simple ambient sound if no notes
            return white_noise(duration=1000, volume=self.settings.volume * 20)

    def generate_test_tones(self) -> List[str]:
        """Generate test tones for AI validation"""
        if not MUSICPY_AVAILABLE:
            return ["MusicPy not available"]

        test_results = []

        try:
            # Test sine wave (peaceful)
            test_sine = sine('C4', duration=1, volume=50)
            test_results.append("✅ Sine wave: C4 peaceful tone generated")

            # Test square wave (combat)
            test_square = square('C4', duration=1, volume=50)
            test_results.append("✅ Square wave: C4 combat tone generated")

            # Test triangle wave (mysterious)
            test_triangle = triangle('C4', duration=1, volume=50)
            test_results.append("✅ Triangle wave: C4 mysterious tone generated")

            # Test sawtooth wave (victory)
            test_sawtooth = sawtooth('C4', duration=1, volume=50)
            test_results.append("✅ Sawtooth wave: C4 victory tone generated")

            # Test white noise (ambient)
            test_noise = white_noise(duration=500, volume=20)
            test_results.append("✅ White noise: ambient effect generated")

        except Exception as e:
            test_results.append(f"❌ Test failed: {e}")

        return test_results

    def play_mood_demo(self, mood: MusicMood) -> Dict[str, Any]:
        """
        Play demonstration of mood-based music

        Args:
            mood: Music mood to demonstrate

        Returns:
            Dict with demonstration results
        """
        if not MUSICPY_AVAILABLE:
            return {
                'success': False,
                'message': 'MusicPy not available for playback',
                'mood': mood.value
            }

        try:
            # Create simple demonstration pattern for mood
            demo_pattern = self._create_demo_pattern(mood)

            # Play immediately
            success = self.play_pattern_immediately(demo_pattern, mood)

            return {
                'success': success,
                'mood': mood.value,
                'pattern_notes': len(demo_pattern.notes),
                'tempo': demo_pattern.tempo,
                'message': f"Playing {mood.value} mood demonstration"
            }

        except Exception as e:
            return {
                'success': False,
                'message': f"Demo failed: {e}",
                'mood': mood.value
            }

    def _create_demo_pattern(self, mood: MusicMood) -> MusicPattern:
        """Create demonstration pattern for mood"""

        demo_notes = []

        if mood == MusicMood.PEACEFUL:
            # Simple ascending peaceful melody
            demo_notes = [
                MusicNote('C', 4, 60, 1.0, 50),
                MusicNote('E', 4, 64, 1.0, 60),
                MusicNote('G', 4, 67, 2.0, 70),
                MusicNote('F', 4, 65, 1.0, 65)
            ]
            tempo = 80

        elif mood == MusicMood.COMBAT:
            # Fast rhythmic combat pattern
            demo_notes = [
                MusicNote('E', 4, 64, 0.5, 100),
                MusicNote('E', 4, 64, 0.5, 0),   # Rest
                MusicNote('E', 4, 64, 0.5, 100),
                MusicNote('G', 4, 67, 0.5, 110),
                MusicNote('E', 4, 64, 1.0, 100)
            ]
            tempo = 140

        elif mood == MusicMood.VICTORY:
            # Triumphant ascending pattern
            demo_notes = [
                MusicNote('C', 4, 60, 1.0, 80),
                MusicNote('E', 4, 64, 1.0, 90),
                MusicNote('G', 4, 67, 1.0, 100),
                MusicNote('C', 5, 72, 2.0, 110)
            ]
            tempo = 120

        elif mood == MusicMood.MYSTERIOUS:
            # Slow, mysterious pattern
            demo_notes = [
                MusicNote('A', 3, 57, 2.0, 40),
                MusicNote('C', 4, 60, 1.0, 50),
                MusicNote('D', 4, 62, 1.0, 45),
                MusicNote('E', 4, 64, 2.0, 50)
            ]
            tempo = 70

        else:  # MAGICAL
            # Ethereal magical pattern
            demo_notes = [
                MusicNote('D', 4, 62, 1.5, 60),
                MusicNote('F#', 4, 66, 1.0, 70),
                MusicNote('A', 4, 69, 1.5, 65),
                MusicNote('D', 5, 74, 2.0, 75)
            ]
            tempo = 100

        return MusicPattern(
            notes=demo_notes,
            tempo=tempo,
            time_signature=(4, 4),
            key='C'
        )

    def stop_current_playback(self) -> bool:
        """Stop all currently playing audio"""
        if not MUSICPY_AVAILABLE:
            return False

        try:
            stop()
            self.currently_playing = None
            return True
        except:
            return False

    def export_pattern_to_file(self, pattern: MusicPattern, filename: str,
                             mood: MusicMood = MusicMood.PEACEFUL) -> bool:
        """
        Export pattern to audio file for validation

        Args:
            pattern: Music pattern to export
            filename: Output filename
            mood: Music mood for timbre

        Returns:
            bool: Success status
        """
        if not MUSICPY_AVAILABLE:
            print("MusicPy not available for export")
            return False

        try:
            # Convert to MusicPy format
            musicpy_chord = self._convert_to_musicpy(pattern, mood)

            # Export to WAV file
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            export(musicpy_chord, filename)

            return True

        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def validate_music_quality(self, pattern: MusicPattern) -> Dict[str, Any]:
        """
        Validate music quality using MusPy metrics (if available)

        Args:
            pattern: Music pattern to validate

        Returns:
            Dict with quality metrics
        """
        try:
            # Try to import MusPy for validation
            import muspy

            # Convert pattern to MusPy format
            music_obj = self._convert_to_muspy(pattern)

            # Calculate quality metrics
            metrics = {
                'note_diversity': muspy.n_pitches_used(music_obj),
                'pitch_range': muspy.pitch_range(music_obj),
                'polyphony_rate': muspy.polyphony_rate(music_obj),
                'scale_consistency': muspy.scale_consistency(music_obj),
                'groove_consistency': muspy.groove_consistency(music_obj, 96) if len(music_obj) > 0 else 0
            }

            # Quality score (0-100)
            quality_score = min(100, (
                metrics['note_diversity'] * 5 +  # Up to 50 points
                metrics['scale_consistency'] * 30 +  # Up to 30 points
                min(metrics['polyphony_rate'] * 20, 20)  # Up to 20 points
            ))

            return {
                'success': True,
                'metrics': metrics,
                'quality_score': quality_score,
                'recommendations': self._generate_quality_recommendations(metrics)
            }

        except ImportError:
            return {
                'success': False,
                'message': 'MusPy not available for detailed validation',
                'basic_validation': self._basic_validation(pattern)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Validation failed: {e}',
                'basic_validation': self._basic_validation(pattern)
            }

    def _convert_to_muspy(self, pattern: MusicPattern):
        """Convert our pattern to MusPy format"""
        # This would implement conversion to MusPy Music object
        # Simplified for now
        pass

    def _generate_quality_recommendations(self, metrics):
        """Generate improvement recommendations based on metrics"""
        recommendations = []

        if metrics['note_diversity'] < 8:
            recommendations.append("Increase note diversity for more interesting melody")

        if metrics['pitch_range'] < 12:
            recommendations.append("Expand pitch range for more dynamic music")

        if metrics['scale_consistency'] < 0.7:
            recommendations.append("Improve scale consistency for more harmonious music")

        if metrics['polyphony_rate'] > 0.8:
            recommendations.append("Consider reducing polyphony for clearer melody")

        return recommendations

    def _basic_validation(self, pattern: MusicPattern):
        """Basic validation without MusPy"""
        notes = pattern.notes

        return {
            'note_count': len(notes),
            'has_tempo': hasattr(pattern, 'tempo') and pattern.tempo > 0,
            'has_key': hasattr(pattern, 'key') and pattern.key,
            'tempo_reasonable': 60 <= pattern.tempo <= 180,
            'duration_range': self._calculate_duration_range(notes)
        }

    def _calculate_duration_range(self, notes):
        """Calculate duration statistics"""
        durations = [note.duration for note in notes if hasattr(note, 'duration')]
        if not durations:
            return {'min': 0, 'max': 0, 'avg': 0}

        return {
            'min': min(durations),
            'max': max(durations),
            'avg': sum(durations) / len(durations)
        }

# Global music player instance
_music_player: Optional[MusicPlayer] = None

def get_music_player() -> MusicPlayer:
    """Get or create global music player"""
    global _music_player
    if _music_player is None:
        _music_player = MusicPlayer()
    return _music_player

def play_mood_immediately(mood: MusicMood) -> Dict[str, Any]:
    """Convenience function to play mood immediately"""
    player = get_music_player()
    return player.play_mood_demo(mood)

def validate_music_for_ai(pattern: MusicPattern) -> Dict[str, Any]:
    """Convenience function for AI music validation"""
    player = get_music_player()
    return player.validate_music_quality(pattern)
