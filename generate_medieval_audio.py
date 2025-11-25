#!/usr/bin/env python3
"""
Generate Medieval Music WAV Files
Creates actual audio files from the medieval music
"""

import numpy as np
import scipy.io.wavfile as wav
from core.systems.music import MusicGenerator, MusicMood, MusicStyle

def note_to_frequency(note_name, octave):
    """Convert note name and octave to frequency in Hz"""
    # A4 = 440 Hz is the reference
    note_freqs = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
    }

    base_freq = note_freqs[note_name]
    # Adjust for octave (A4 is octave 4)
    octave_adjustment = octave - 4
    frequency = base_freq * (2 ** octave_adjustment)

    return frequency

def generate_waveform(frequency, duration, sample_rate=44100, waveform_type='sine'):
    """Generate audio waveform for a single note"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    if waveform_type == 'sine':
        wave = np.sin(2 * np.pi * frequency * t)
    elif waveform_type == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform_type == 'triangle':
        wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    elif waveform_type == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:
        wave = np.sin(2 * np.pi * frequency * t)

    return wave

def apply_envelope(wave, duration, sample_rate=44100):
    """Apply ADSR envelope to make it sound more natural"""
    attack_time = 0.01  # 10ms attack
    decay_time = 0.05   # 50ms decay
    sustain_level = 0.7
    release_time = 0.1  # 100ms release

    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    sustain_samples = len(wave) - attack_samples - decay_samples - release_samples

    envelope = np.zeros_like(wave)

    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Decay
    decay_end = attack_samples + decay_samples
    envelope[attack_samples:decay_end] = np.linspace(1, sustain_level, decay_samples)

    # Sustain
    sustain_end = decay_end + sustain_samples
    envelope[decay_end:sustain_end] = sustain_level

    # Release
    envelope[sustain_end:] = np.linspace(sustain_level, 0, release_samples)

    return wave * envelope

def create_medieval_wav():
    """Generate medieval theme as WAV file"""
    print("🎵 Generating Medieval Theme WAV...")

    # Create medieval pattern
    generator = MusicGenerator()
    pattern = generator.generate_theme_music(
        mood=MusicMood.PEACEFUL,
        style=MusicStyle.MEDIEVAL,
        duration_bars=8
    )

    sample_rate = 44100
    audio_data = np.array([])

    # Convert each note to audio
    for note in pattern.notes[:32]:  # First 32 notes for reasonable length
        if hasattr(note, 'midi_note') and hasattr(note, 'note'):
            # Convert our note to frequency
            frequency = note_to_frequency(note.note, note.octave)

            # Generate waveform (using sine waves for medieval feel)
            wave = generate_waveform(frequency, note.duration, sample_rate, 'sine')

            # Apply velocity (volume)
            velocity_factor = note.velocity / 127.0
            wave = wave * velocity_factor

            # Apply envelope for more natural sound
            wave = apply_envelope(wave, note.duration, sample_rate)

            # Add small silence between notes
            silence = np.zeros(int(sample_rate * 0.05))  # 50ms silence
            wave = np.concatenate([wave, silence])

            # Append to audio data
            audio_data = np.concatenate([audio_data, wave])

    # Normalize audio
    if len(audio_data) > 0 and np.max(np.abs(audio_data)) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8  # Normalize to 80% of max

    # Convert to 16-bit PCM
    audio_data_int16 = (audio_data * 32767).astype(np.int16)

    # Save as WAV file
    filename = "medieval_theme.wav"
    wav.write(filename, sample_rate, audio_data_int16)

    duration = len(audio_data) / sample_rate
    print(f"✅ WAV file created: {filename}")
    print(f"   - Duration: {duration:.2f} seconds")
    print(f"   - Sample rate: {sample_rate} Hz")
    print(f"   - Bits: 16-bit PCM")

    return filename

def create_castle_song_wav():
    """Generate castle medieval song as WAV file"""
    print("\n🏰 Generating Castle Medieval Song WAV...")

    # Custom medieval castle song notes
    castle_notes = [
        # Opening fanfare
        {'note': 'C', 'octave': 5, 'duration': 1.0, 'velocity': 100},
        {'note': 'E', 'octave': 5, 'duration': 1.0, 'velocity': 90},
        {'note': 'G', 'octave': 5, 'duration': 2.0, 'velocity': 110},

        # Main theme
        {'note': 'A', 'octave': 4, 'duration': 1.0, 'velocity': 80},
        {'note': 'C', 'octave': 5, 'duration': 1.0, 'velocity': 85},
        {'note': 'F', 'octave': 4, 'duration': 1.0, 'velocity': 75},
        {'note': 'E', 'octave': 4, 'duration': 1.0, 'velocity': 80},

        # Bridge
        {'note': 'D', 'octave': 5, 'duration': 1.5, 'velocity': 95},
        {'note': 'G', 'octave': 5, 'duration': 0.5, 'velocity': 100},
        {'note': 'F', 'octave': 5, 'duration': 2.0, 'velocity': 85},

        # Finale
        {'note': 'C', 'octave': 5, 'duration': 1.0, 'velocity': 90},
        {'note': 'G', 'octave': 4, 'duration': 1.0, 'velocity': 85},
        {'note': 'C', 'octave': 5, 'duration': 3.0, 'velocity': 100}
    ]

    sample_rate = 44100
    audio_data = np.array([])

    for note_data in castle_notes:
        frequency = note_to_frequency(note_data['note'], note_data['octave'])

        # Use triangle waves for more medieval/medieval sound
        wave = generate_waveform(frequency, note_data['duration'], sample_rate, 'triangle')

        # Apply velocity
        velocity_factor = note_data['velocity'] / 127.0
        wave = wave * velocity_factor * 0.7  # Slightly quieter for castle feel

        # Apply envelope
        wave = apply_envelope(wave, note_data['duration'], sample_rate)

        # Add silence
        silence = np.zeros(int(sample_rate * 0.1))  # 100ms silence for dramatic effect
        wave = np.concatenate([wave, silence])

        audio_data = np.concatenate([audio_data, wave])

    # Normalize audio
    if len(audio_data) > 0 and np.max(np.abs(audio_data)) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8

    # Convert to 16-bit PCM
    audio_data_int16 = (audio_data * 32767).astype(np.int16)

    # Save as WAV file
    filename = "castle_medieval.wav"
    wav.write(filename, sample_rate, audio_data_int16)

    duration = len(audio_data) / sample_rate
    print(f"✅ Castle WAV file created: {filename}")
    print(f"   - Duration: {duration:.2f} seconds")
    print(f"   - Style: Medieval castle fanfare")

    return filename

def create_combat_music_wav():
    """Generate combat music as WAV file"""
    print("\n⚔️ Generating Combat Music WAV...")

    # Combat notes - fast, aggressive rhythm
    combat_notes = []

    # Fast rhythmic combat pattern
    base_notes = ['E', 'G', 'A', 'C']  # Minor/intense feel

    for i in range(24):  # 24 notes for intense combat
        note_data = {
            'note': base_notes[i % len(base_notes)],
            'octave': 4 if i % 3 == 0 else 5,  # Vary octaves
            'duration': 0.25 if i % 2 == 0 else 0.5,  # Fast rhythm
            'velocity': 100 + (i % 20)  # High intensity
        }
        combat_notes.append(note_data)

    sample_rate = 44100
    audio_data = np.array([])

    for note_data in combat_notes:
        frequency = note_to_frequency(note_data['note'], note_data['octave'])

        # Use square waves for aggressive combat sound
        wave = generate_waveform(frequency, note_data['duration'], sample_rate, 'square')

        # Apply velocity with high intensity
        velocity_factor = note_data['velocity'] / 127.0
        wave = wave * velocity_factor * 0.9

        # Apply shorter envelope for staccato feel
        wave = apply_envelope(wave, note_data['duration'], sample_rate)

        # Very short silence for fast rhythm
        silence = np.zeros(int(sample_rate * 0.02))  # 20ms silence
        wave = np.concatenate([wave, silence])

        audio_data = np.concatenate([audio_data, wave])

    # Normalize audio
    if len(audio_data) > 0 and np.max(np.abs(audio_data)) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.85

    # Convert to 16-bit PCM
    audio_data_int16 = (audio_data * 32767).astype(np.int16)

    # Save as WAV file
    filename = "combat_music.wav"
    wav.write(filename, sample_rate, audio_data_int16)

    duration = len(audio_data) / sample_rate
    print(f"✅ Combat WAV file created: {filename}")
    print(f"   - Duration: {duration:.2f} seconds")
    print(f"   - Style: Fast, aggressive combat rhythm")

    return filename

if __name__ == "__main__":
    print("🎼 RPGSim Audio Generator")
    print("=" * 40)

    try:
        # Generate all three music types
        medieval_file = create_medieval_wav()
        castle_file = create_castle_song_wav()
        combat_file = create_combat_music_wav()

        print("\n🎉 Audio Generation Complete!")
        print("=" * 40)
        print("📁 WAV Files Created:")
        print(f"   🏰 {medieval_file} - Peaceful medieval theme")
        print(f"   🏰 {castle_file} - Castle fanfare song")
        print(f"   ⚔️ {combat_file} - Intense combat music")
        print("\n🎧 Ready to play on any device!")

    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        import traceback
        traceback.print_exc()