#!/usr/bin/env python3
"""
Test Medieval Music Generation and Playback
LLM Agent-Optimized validation script
"""

import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core.systems.music import MusicGenerator, MusicMood, MusicStyle, MusicNote, MusicPattern
from core.systems.music_player import get_music_player, play_mood_immediately

def create_medieval_theme():
    """Create a medieval-themed musical pattern"""
    print("🎵 Creating Medieval Theme Music...")

    generator = MusicGenerator()

    # Generate medieval-style music
    medieval_pattern = generator.generate_theme_music(
        mood=MusicMood.PEACEFUL,
        style=MusicStyle.MEDIEVAL,
        duration_bars=8
    )

    print(f"✅ Medieval pattern generated:")
    print(f"   - Tempo: {medieval_pattern.tempo} BPM")
    print(f"   - Key: {medieval_pattern.key}")
    print(f"   - Notes: {len(medieval_pattern.notes)}")
    print(f"   - Time Signature: {medieval_pattern.time_signature}")

    return medieval_pattern

def test_music_validation():
    """Test music quality validation"""
    print("\n🔍 Testing Music Quality Validation...")

    medieval_pattern = create_medieval_theme()
    player = get_music_player()

    # Validate quality
    validation_result = player.validate_music_quality(medieval_pattern)

    print("📊 Validation Results:")
    if validation_result['success']:
        metrics = validation_result['metrics']
        print(f"   - Quality Score: {validation_result['quality_score']}/100")
        print(f"   - Note Diversity: {metrics.get('note_diversity', 'N/A')}")
        print(f"   - Pitch Range: {metrics.get('pitch_range', 'N/A')} semitones")
        print(f"   - Scale Consistency: {metrics.get('scale_consistency', 'N/A'):.2%}")
    else:
        basic = validation_result['basic_validation']
        print(f"   - Basic Check: {basic}")
        print(f"   - Message: {validation_result.get('message', 'No detailed validation')}")

    return validation_result

def test_immediate_playback():
    """Test immediate audio playback"""
    print("\n🔊 Testing Immediate Audio Playback...")

    try:
        # Test different moods
        moods = [MusicMood.PEACEFUL, MusicMood.COMBAT, MusicMood.VICTORY, MusicMood.MYSTERIOUS]

        for mood in moods:
            print(f"\n🎭 Playing {mood.value} mood demo...")
            result = play_mood_immediately(mood)

            if result['success']:
                print(f"   ✅ {mood.value} playback started")
                print(f"   🎵 Pattern: {result.get('pattern_notes', 'N/A')} notes")
                print(f"   ⚡ Tempo: {result.get('tempo', 'N/A')} BPM")
            else:
                print(f"   ❌ {mood.value} playback failed: {result.get('message')}")

            # Wait a moment between demos
            import time
            time.sleep(2)

    except Exception as e:
        print(f"❌ Playback test failed: {e}")

def test_music_generation_with_prompts():
    """Test LLM-friendly prompt generation"""
    print("\n🤖 Testing LLM Prompt Generation...")

    medieval_pattern = create_medieval_theme()
    generator = MusicGenerator()

    # Generate LLM prompt
    prompt = generator.to_llm_prompt(medieval_pattern)

    print("📝 LLM-Friendly Prompt Generated:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)

    return prompt

def create_custom_medieval_song():
    """Create custom medieval song with specific structure"""
    print("\n🏰 Creating Custom Medieval Castle Song...")

    # Create custom medieval notes (C major scale with medieval feel)
    medieval_notes = [
        # Opening fanfare
        MusicNote('C', 4, 60, 1.0, 80),
        MusicNote('E', 4, 64, 1.0, 85),
        MusicNote('G', 4, 67, 2.0, 90),

        # Main theme
        MusicNote('A', 3, 57, 1.0, 70),
        MusicNote('C', 4, 60, 1.0, 75),
        MusicNote('F', 4, 65, 1.0, 80),
        MusicNote('E', 4, 64, 1.0, 75),

        # Bridge
        MusicNote('D', 4, 62, 1.5, 85),
        MusicNote('G', 4, 67, 0.5, 90),
        MusicNote('F', 4, 65, 2.0, 80),

        # Finale
        MusicNote('C', 4, 60, 1.0, 70),
        MusicNote('G', 3, 55, 1.0, 75),
        MusicNote('C', 4, 60, 2.0, 85)
    ]

    custom_song = MusicPattern(
        notes=medieval_notes,
        tempo=90,  # Moderate medieval tempo
        time_signature=(4, 4),
        key='C'
    )

    print(f"✅ Custom Medieval Song Created:")
    print(f"   - Structure: {len(medieval_notes)} notes")
    print(f"   - Progression: Fanfare → Theme → Bridge → Finale")
    print(f"   - Duration: ~{sum(note.duration for note in medieval_notes)} beats")

    return custom_song

def export_melody_to_file():
    """Export melody to audio file"""
    print("\n💾 Exporting Melody to Audio File...")

    medieval_pattern = create_medieval_theme()
    player = get_music_player()

    # Export to WAV file
    filename = "medieval_theme_test.wav"
    success = player.export_pattern_to_file(
        medieval_pattern,
        filename,
        MusicMood.PEACEFUL
    )

    if success:
        print(f"✅ Successfully exported to {filename}")
        print(f"📁 File size: {os.path.getsize(filename)} bytes")
    else:
        print(f"❌ Export failed - MusicPy may not be available")

    return success

def main():
    """Main test function"""
    print("🎮 RPGSim Music System Test")
    print("=" * 50)

    try:
        # Test 1: Medieval Theme Generation
        medieval_pattern = create_medieval_theme()

        # Test 2: Quality Validation
        validation_result = test_music_validation()

        # Test 3: LLM Prompt Generation
        prompt = test_music_generation_with_prompts()

        # Test 4: Custom Medieval Song
        custom_song = create_custom_medieval_song()

        # Test 5: Export to File
        export_result = export_melody_to_file()

        # Test 6: Immediate Playback (if available)
        test_immediate_playback()

        print("\n🎉 Medieval Music System Test Complete!")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)