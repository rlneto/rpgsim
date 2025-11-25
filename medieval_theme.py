#!/usr/bin/env python3
"""
Generate Medieval Theme Music in MIDI format
LLM Agent-Optimized medieval music creation
"""

import json
from core.systems.music import MusicGenerator, MusicMood, MusicStyle, MusicNote, MusicPattern

def create_medieval_midi():
    """Create medieval theme and save as MIDI-compatible JSON"""
    print("🏰 Creating Medieval Theme MIDI...")

    generator = MusicGenerator()

    # Generate medieval-style theme
    medieval_pattern = generator.generate_theme_music(
        mood=MusicMood.PEACEFUL,
        style=MusicStyle.MEDIEVAL,
        duration_bars=8
    )

    print(f"✅ Medieval Theme Generated:")
    print(f"   - Tempo: {medieval_pattern.tempo} BPM")
    print(f"   - Key: {medieval_pattern.key}")
    print(f"   - Notes: {len(medieval_pattern.notes)}")

    # Convert to MIDI-compatible format
    midi_data = {
        "format": "Standard MIDI File",
        "tracks": 1,
        "tempo": medieval_pattern.tempo,
        "time_signature": f"{medieval_pattern.time_signature[0]}/{medieval_pattern.time_signature[1]}",
        "key": medieval_pattern.key,
        "instruments": [
            {
                "program": 0,  # Acoustic Grand Piano
                "channel": 0,
                "volume": 80
            }
        ],
        "events": []
    }

    # Convert notes to MIDI events
    current_time = 0
    for note_or_chord in medieval_pattern.notes:
        if hasattr(note_or_chord, 'midi_note'):  # Single note
            # Note on
            midi_data["events"].append({
                "type": "note_on",
                "note": note_or_chord.midi_note,
                "velocity": note_or_chord.velocity,
                "channel": 0,
                "time": current_time
            })

            # Note off
            midi_data["events"].append({
                "type": "note_off",
                "note": note_or_chord.midi_note,
                "velocity": 0,
                "channel": 0,
                "time": current_time + note_or_chord.duration * 240  # Convert to ticks
            })

            current_time += note_or_chord.duration * 240

    # Save as JSON (MIDI-compatible structure)
    filename = "medieval_theme.json"
    with open(filename, 'w') as f:
        json.dump(midi_data, f, indent=2)

    print(f"✅ MIDI file saved: {filename}")
    print(f"   - Total events: {len(midi_data['events'])}")
    print(f"   - Duration: {current_time} ticks")

    # Also create simple text representation
    create_midi_text_file(medieval_pattern)

    return medieval_pattern, midi_data

def create_midi_text_file(pattern):
    """Create human-readable MIDI text file"""
    filename = "medieval_theme_notes.txt"

    with open(filename, 'w') as f:
        f.write("🏰 Medieval Theme - Musical Notation\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Tempo: {pattern.tempo} BPM\n")
        f.write(f"Key: {pattern.key}\n")
        f.write(f"Time Signature: {pattern.time_signature[0]}/{pattern.time_signature[1]}\n")
        f.write(f"Total Notes: {len(pattern.notes)}\n\n")

        f.write("Musical Sequence:\n")
        f.write("-" * 30 + "\n")

        for i, note in enumerate(pattern.notes[:20], 1):  # First 20 notes
            if hasattr(note, 'note'):
                duration_beats = note.duration
                duration_name = "whole" if duration_beats == 4.0 else \
                               "half" if duration_beats == 2.0 else \
                               "quarter" if duration_beats == 1.0 else \
                               "eighth" if duration_beats == 0.5 else \
                               f"{duration_beats} beats"

                f.write(f"{i:2d}. {note.note}{note.octave} - {duration_name} (vel: {note.velocity})\n")

        if len(pattern.notes) > 20:
            f.write(f"... and {len(pattern.notes) - 20} more notes\n")

    print(f"📝 Musical notation saved: {filename}")

def create_custom_medieval_song():
    """Create a custom medieval castle song"""
    print("\n🏰 Creating Custom Medieval Castle Song...")

    # Create custom medieval notes
    medieval_notes = [
        # Opening fanfare
        MusicNote('C', 5, 72, 1.0, 100),  # C5 - strong opening
        MusicNote('E', 5, 76, 1.0, 90),   # E5 - ascending
        MusicNote('G', 5, 79, 2.0, 110),  # G5 - fanfare peak

        # Main theme - medieval melody
        MusicNote('A', 4, 69, 1.0, 80),   # A4 - melodic
        MusicNote('C', 5, 72, 1.0, 85),   # C5 - resolution
        MusicNote('F', 4, 65, 1.0, 75),   # F4 - harmonic
        MusicNote('E', 4, 64, 1.0, 80),   # E4 - descending

        # Bridge - emotional section
        MusicNote('D', 5, 74, 1.5, 95),   # D5 - emotional
        MusicNote('G', 5, 79, 0.5, 100),  # G5 - tension
        MusicNote('F', 5, 77, 2.0, 85),   # F5 - release

        # Finale - triumphant ending
        MusicNote('C', 5, 72, 1.0, 90),   # C5 - strong
        MusicNote('G', 4, 67, 1.0, 85),   # G4 - foundation
        MusicNote('C', 5, 72, 3.0, 100)   # C5 - final chord
    ]

    custom_song = MusicPattern(
        notes=medieval_notes,
        tempo=90,  # Noble medieval tempo
        time_signature=(4, 4),
        key='C'
    )

    print(f"✅ Custom Medieval Castle Song Created:")
    print(f"   - Structure: {len(medieval_notes)} notes")
    print(f"   - Duration: ~{sum(note.duration for note in medieval_notes)} beats")
    print(f"   - Sections: Fanfare → Theme → Bridge → Finale")

    # Save custom song
    save_pattern_to_midi(custom_song, "castle_medieval.json")
    save_pattern_to_midi_text(custom_song, "castle_medieval_notes.txt")

    return custom_song

def save_pattern_to_midi(pattern, filename):
    """Save music pattern as MIDI JSON"""
    midi_data = {
        "format": "Standard MIDI File",
        "tracks": 1,
        "tempo": pattern.tempo,
        "time_signature": f"{pattern.time_signature[0]}/{pattern.time_signature[1]}",
        "key": pattern.key,
        "instruments": [{"program": 0, "channel": 0, "volume": 80}],
        "events": []
    }

    current_time = 0
    for note in pattern.notes:
        midi_data["events"].extend([
            {
                "type": "note_on",
                "note": note.midi_note,
                "velocity": note.velocity,
                "channel": 0,
                "time": current_time
            },
            {
                "type": "note_off",
                "note": note.midi_note,
                "velocity": 0,
                "channel": 0,
                "time": current_time + note.duration * 240
            }
        ])
        current_time += note.duration * 240

    with open(filename, 'w') as f:
        json.dump(midi_data, f, indent=2)

    print(f"📁 MIDI saved: {filename}")

def save_pattern_to_midi_text(pattern, filename):
    """Save pattern as readable text"""
    with open(filename, 'w') as f:
        f.write(f"🏰 Medieval Theme - {filename.replace('.txt', '').replace('_', ' ').title()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Tempo: {pattern.tempo} BPM\n")
        f.write(f"Key: {pattern.key} Major\n")
        f.write(f"Notes: {len(pattern.notes)}\n\n")

        f.write("Musical Score:\n")
        for i, note in enumerate(pattern.notes, 1):
            note_name = f"{note.note}{note.octave}"
            duration = note.duration
            f.write(f"{i:2d}. {note_name:^6} - Duration: {duration:4.1f} beats - Velocity: {note.velocity:3d}\n")

if __name__ == "__main__":
    # Create medieval theme
    medieval_pattern, midi_data = create_medieval_midi()

    # Create custom medieval castle song
    custom_song = create_custom_medieval_song()

    print("\n🎉 Medieval Music Creation Complete!")
    print("=" * 50)
    print("📁 Files Created:")
    print("   🎵 medieval_theme.json - MIDI data structure")
    print("   📝 medieval_theme_notes.txt - Musical notation")
    print("   🏰 castle_medieval.json - Custom castle song MIDI")
    print("   📜 castle_medieval_notes.txt - Castle song notation")
    print("\n🎹 Ready to import into any MIDI software!")