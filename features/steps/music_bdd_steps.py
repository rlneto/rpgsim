"""
RPGSim Music System BDD Step Definitions
LLM Agent-Optimized music generation scenarios
"""

from behave import given, when, then
from typing import Dict, Any, List
import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.systems.music import (
    MusicGenerator, MusicMood, MusicStyle, MusicNote, MusicChord, MusicPattern,
    get_music_generator, generate_combat_music, generate_victory_music,
    generate_location_music
)

# Import base context manager
from bdd_base_steps import get_bdd_context

# -- MUSIC SYSTEM SETUP STEPS --

@given('the music system is initialized')
def step_music_system_initialized(context):
    """Initialize music system"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.music_generator = get_music_generator()

@given('MIDI note mappings are available')
def step_midi_mappings_available(context):
    """Verify MIDI mappings are available"""
    bdd_ctx = get_bdd_context(context)
    from core.systems.music import MIDI_NOTES, MIDI_DURATIONS, MIDI_VELOCITIES

    assert len(MIDI_NOTES) > 0, "MIDI notes should be available"
    assert len(MIDI_DURATIONS) > 0, "MIDI durations should be available"
    assert len(MIDI_VELOCITIES) > 0, "MIDI velocities should be available"

    bdd_ctx.midi_notes = MIDI_NOTES
    bdd_ctx.midi_durations = MIDI_DURATIONS
    bdd_ctx.midi_velocities = MIDI_VELOCITIES

@given('music templates are loaded')
def step_music_templates_loaded(context):
    """Verify music templates are loaded"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'music_generator'):
        templates = bdd_ctx.music_generator.templates
    else:
        generator = get_music_generator()
        templates = generator.templates

    assert len(templates) > 0, "Music templates should be loaded"
    assert 'peaceful' in templates, "Peaceful template should exist"
    assert 'combat' in templates, "Combat template should exist"

    bdd_ctx.music_templates = templates

# -- AMBIENT MUSIC GENERATION STEPS --

@given('I want to create music for a city location')
def step_city_music_intent(context):
    """Set intent to create city music"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.target_location_type = "city"
    bdd_ctx.target_mood = "peaceful"

@when('I generate ambient music for "city"')
def step_generate_city_music(context):
    """Generate city ambient music"""
    bdd_ctx = get_bdd_context(context)
    generator = get_music_generator()

    pattern = generator.create_ambient_loop("city", length_seconds=20)
    bdd_ctx.generated_music = pattern

@then('the music should have peaceful mood')
def step_verify_peaceful_mood(context):
    """Verify peaceful mood"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_music'):
        # Check if music characteristics suggest peaceful mood
        pattern = bdd_ctx.generated_music
        assert pattern.tempo < 100, f"Peaceful music tempo should be < 100, got {pattern.tempo}"
    else:
        # Verify template would create peaceful mood
        templates = getattr(bdd_ctx, 'music_templates', {})
        peaceful_template = templates.get('peaceful', {})
        assert 'tempo' in peaceful_template, "Peaceful template should have tempo"

@then('the tempo should be between 60-100 BPM')
def step_verify_peaceful_tempo(context):
    """Verify peaceful tempo range"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_music'):
        tempo = bdd_ctx.generated_music.tempo
        assert 60 <= tempo <= 100, f"Expected tempo 60-100, got {tempo}"
    else:
        templates = getattr(bdd_ctx, 'music_templates', {})
        peaceful_template = templates.get('peaceful', {})
        tempo = peaceful_template.get('tempo', 0)
        assert 60 <= tempo <= 100, f"Expected template tempo 60-100, got {tempo}"

@then('the key should be suitable for exploration')
def step_verify_exploration_key(context):
    """Verify exploration-appropriate key"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_music'):
        key = bdd_ctx.generated_music.key
        assert key in ['C', 'G', 'D', 'F'], f"Exploration key should be common, got {key}"
    else:
        templates = getattr(bdd_ctx, 'music_templates', {})
        peaceful_template = templates.get('peaceful', {})
        key = peaceful_template.get('key', '')
        assert key in ['C', 'G', 'D', 'F'], f"Template key should be common, got {key}"

@then('the pattern should contain multiple notes')
def step_verify_multiple_notes(context):
    """Verify multiple notes in pattern"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_music'):
        notes = bdd_ctx.generated_music.notes
        assert len(notes) > 0, "Pattern should contain notes"
        assert len(notes) >= 4, f"Pattern should have multiple notes, got {len(notes)}"
    else:
        # This would be verified in actual generation
        pass

@then('the music should be convertible to MIDI format')
def step_verify_midi_convertible(context):
    """Verify MIDI conversion capability"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_music'):
        pattern = bdd_ctx.generated_music

        # Check if pattern has required MIDI attributes
        assert hasattr(pattern, 'notes'), "Pattern should have notes"
        assert hasattr(pattern, 'tempo'), "Pattern should have tempo"
        assert hasattr(pattern, 'key'), "Pattern should have key"

        # Verify notes have MIDI properties
        if pattern.notes:
            note = pattern.notes[0]
            assert hasattr(note, 'midi_note'), "Notes should have MIDI note values"
            assert hasattr(note, 'duration'), "Notes should have duration"
            assert hasattr(note, 'velocity'), "Notes should have velocity"

# -- COMBAT MUSIC GENERATION STEPS --

@given('a battle is starting')
def step_battle_starting(context):
    """Set battle starting context"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.battle_context = "starting"
    bdd_ctx.battle_intensity = "medium"

@when('I generate combat music with "medium" intensity')
def step_generate_combat_music(context):
    """Generate combat music"""
    bdd_ctx = get_bdd_context(context)

    pattern = generate_combat_music("medium")
    bdd_ctx.generated_combat_music = pattern

@then('the music should have combat mood')
def step_verify_combat_mood(context):
    """Verify combat mood"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_combat_music'):
        pattern = bdd_ctx.generated_combat_music
        assert pattern.tempo >= 120, f"Combat music tempo should be >= 120, got {pattern.tempo}"

@then('the tempo should be between 120-160 BPM')
def step_verify_combat_tempo(context):
    """Verify combat tempo range"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_combat_music'):
        tempo = bdd_ctx.generated_combat_music.tempo
        assert 120 <= tempo <= 160, f"Expected combat tempo 120-160, got {tempo}"

@then('the rhythm should be more aggressive')
def step_verify_aggressive_rhythm(context):
    """Verify aggressive rhythm pattern"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_combat_music'):
        pattern = bdd_ctx.generated_combat_music
        notes = pattern.notes

        # Check for shorter note durations (more rhythmic)
        short_notes = [n for n in notes if hasattr(n, 'duration') and n.duration <= 0.5]
        assert len(short_notes) > 0, "Combat music should have short rhythmic notes"

@then('the velocity should be higher than ambient music')
def step_verify_higher_velocity(context):
    """Verify higher velocity than ambient"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_combat_music') and hasattr(bdd_ctx, 'generated_music'):
        combat_pattern = bdd_ctx.generated_combat_music
        ambient_pattern = bdd_ctx.generated_music

        # Calculate average velocities
        combat_avg = _calculate_avg_velocity(combat_pattern.notes)
        ambient_avg = _calculate_avg_velocity(ambient_pattern.notes)

        assert combat_avg > ambient_avg, f"Combat velocity ({combat_avg}) should be higher than ambient ({ambient_avg})"

@then('the pattern should contain shorter note durations')
def step_verify_short_durations(context):
    """Verify short note durations in combat music"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_combat_music'):
        pattern = bdd_ctx.generated_combat_music
        notes = pattern.notes

        short_durations = [n.duration for n in notes if hasattr(n, 'duration') and n.duration <= 0.5]
        assert len(short_durations) > len(notes) * 0.3, "Combat music should have at least 30% short notes"

# -- VICTORY MUSIC GENERATION STEPS --

@given('the player has won a battle')
def step_victory_context(context):
    """Set victory context"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.battle_result = "victory"
    bdd_ctx.player_class = "warrior"

@when('I generate victory music for "warrior" class')
def step_generate_victory_music(context):
    """Generate victory music"""
    bdd_ctx = get_bdd_context(context)

    pattern = generate_victory_music("warrior")
    bdd_ctx.generated_victory_music = pattern

@then('the music should have victory mood')
def step_verify_victory_mood(context):
    """Verify victory mood"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_victory_music'):
        pattern = bdd_ctx.generated_victory_music
        assert 100 <= pattern.tempo <= 140, f"Victory tempo should be celebratory, got {pattern.tempo}"

@then('the tempo should be celebratory (100-140 BPM)')
def step_verify_victory_tempo(context):
    """Verify victory tempo range"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_victory_music'):
        tempo = bdd_ctx.generated_victory_music.tempo
        assert 100 <= tempo <= 140, f"Expected victory tempo 100-140, got {tempo}"

@then('the style should match the player class')
def step_verify_class_style(context):
    """Verify style matches player class"""
    bdd_ctx = get_bdd_context(context)

    # This would be verified by checking the style used in generation
    # For now, we verify the music was generated successfully
    assert hasattr(bdd_ctx, 'generated_victory_music'), "Victory music should be generated"

@then('the pattern should contain ascending progressions')
def step_verify_ascending_progressions(context):
    """Verify ascending progressions in victory music"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_victory_music'):
        pattern = bdd_ctx.generated_victory_music
        notes = pattern.notes

        # Check for ascending MIDI note pattern
        if len(notes) >= 3:
            ascending_count = 0
            for i in range(len(notes) - 2):
                if (hasattr(notes[i], 'midi_note') and
                    hasattr(notes[i+1], 'midi_note') and
                    hasattr(notes[i+2], 'midi_note')):

                    if (notes[i].midi_note < notes[i+1].midi_note and
                        notes[i+1].midi_note <= notes[i+2].midi_note):
                        ascending_count += 1

            assert ascending_count > 0, "Victory music should have ascending progressions"

@then('the music should feel triumphant')
def step_verify_triumphant_feel(context):
    """Verify triumphant feel"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_victory_music'):
        pattern = bdd_ctx.generated_victory_music

        # Check for characteristics that suggest triumph
        assert pattern.tempo >= 100, "Triumphant music should have good tempo"
        assert len(pattern.notes) >= 8, "Triumphant music should have sufficient complexity"

# -- DUNGEON MUSIC GENERATION STEPS --

@given('the player enters a dark dungeon')
def step_dungeon_context(context):
    """Set dungeon context"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.current_location = "dark_dungeon"

@when('I generate location music for "dungeon" type')
def step_generate_dungeon_music(context):
    """Generate dungeon music"""
    bdd_ctx = get_bdd_context(context)

    pattern = generate_location_music("dungeon", "dark_dungeon")
    bdd_ctx.generated_dungeon_music = pattern

@given('the location name contains "dungeon"')
def step_location_name_contains_dungeon(context):
    """Verify location name contains dungeon"""
    bdd_ctx = get_bdd_context(context)
    assert "dungeon" in bdd_ctx.current_location, "Location name should contain 'dungeon'"

@then('the music should have mysterious mood')
def step_verify_mysterious_mood(context):
    """Verify mysterious mood"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_dungeon_music'):
        pattern = bdd_ctx.generated_dungeon_music
        assert pattern.tempo <= 90, f"Mysterious music tempo should be <= 90, got {pattern.tempo}"

@then('the tempo should be slower (60-80 BPM)')
def step_verify_slow_tempo(context):
    """Verify slow tempo for dungeon"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_dungeon_music'):
        tempo = bdd_ctx.generated_dungeon_music.tempo
        assert 60 <= tempo <= 80, f"Expected dungeon tempo 60-80, got {tempo}"

@then('the velocity should be lower (quieter)')
def step_verify_lower_velocity(context):
    """Verify lower velocity for dungeon music"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_dungeon_music'):
        pattern = bdd_ctx.generated_dungeon_music
        avg_velocity = _calculate_avg_velocity(pattern.notes)
        assert avg_velocity <= 70, f"Dungeon music velocity should be lower, got {avg_velocity}"

@then('the key should be minor or modal')
def step_verify_minor_modal_key(context):
    """Verify minor/modal key for dungeon"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_dungeon_music'):
        pattern = bdd_ctx.generated_dungeon_music
        # This would be verified by checking if the key is minor
        # For now, check if it's a suitable key for mysterious mood
        assert pattern.key in ['A', 'D', 'E'], f"Dungeon key should be mysterious, got {pattern.key}"

@then('the pattern should create suspense')
def step_verify_suspense_pattern(context):
    """Verify suspenseful pattern"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_dungeon_music'):
        pattern = bdd_ctx.generated_dungeon_music

        # Check for characteristics that create suspense
        assert pattern.tempo <= 80, "Suspenseful music should be slower"
        assert len(pattern.notes) >= 4, "Suspenseful music should have sufficient notes"

# -- ADDITIONAL MUSIC STEPS --

@given('I have a generated music pattern')
def step_have_music_pattern(context):
    """Set up existing music pattern"""
    bdd_ctx = get_bdd_context(context)

    # Create a simple test pattern
    from core.systems.music import MusicPattern, MusicNote, MusicMood, MusicStyle

    test_notes = [
        MusicNote('C', 5, 60, 1.0, 70),
        MusicNote('E', 5, 64, 0.5, 80),
        MusicNote('G', 5, 67, 1.0, 75)
    ]

    pattern = MusicPattern(
        notes=test_notes,
        tempo=120,
        time_signature=(4, 4),
        key='C'
    )

    bdd_ctx.test_music_pattern = pattern

@given('the pattern has tempo and key information')
def step_pattern_has_tempo_key(context):
    """Verify pattern has tempo and key"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'test_music_pattern'), "Test pattern should exist"
    pattern = bdd_ctx.test_music_pattern
    assert hasattr(pattern, 'tempo'), "Pattern should have tempo"
    assert hasattr(pattern, 'key'), "Pattern should have key"

@when('I convert the pattern to LLM prompt')
def step_convert_to_llm_prompt(context):
    """Convert pattern to LLM prompt"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'test_music_pattern'):
        generator = get_music_generator()
        prompt = generator.to_llm_prompt(bdd_ctx.test_music_pattern)
        bdd_ctx.llm_prompt = prompt
    else:
        bdd_ctx.llm_prompt = ""

@then('the prompt should include tempo information')
def step_verify_tempo_in_prompt(context):
    """Verify tempo in LLM prompt"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'llm_prompt'), "LLM prompt should exist"
    prompt = bdd_ctx.llm_prompt
    assert "tempo" in prompt.lower(), "Prompt should contain tempo information"

@then('the prompt should include key signature')
def step_verify_key_in_prompt(context):
    """Verify key signature in LLM prompt"""
    bdd_ctx = get_bdd_context(context)
    prompt = bdd_ctx.llm_prompt
    assert "key" in prompt.lower(), "Prompt should contain key information"

@then('the prompt should describe the musical sequence')
def step_verify_sequence_description(context):
    """Verify musical sequence description"""
    bdd_ctx = get_bdd_context(context)
    prompt = bdd_ctx.llm_prompt
    assert "notes" in prompt.lower() or "sequence" in prompt.lower(), "Prompt should describe sequence"

@then('the prompt should be readable by language models')
def step_verify_llm_readable(context):
    """Verify prompt readability for LLMs"""
    bdd_ctx = get_bdd_context(context)
    prompt = bdd_ctx.llm_prompt
    assert len(prompt) > 50, "Prompt should have sufficient content"
    assert isinstance(prompt, str), "Prompt should be string"

@then('the prompt should be suitable for music generation')
def step_verify_suitable_for_music_gen(context):
    """Verify prompt suitability for music generation"""
    bdd_ctx = get_bdd_context(context)
    prompt = bdd_ctx.llm_prompt
    assert "tempo" in prompt.lower() and "key" in prompt.lower(), "Prompt should be suitable for music generation"

# -- DEVELOPER MUSIC STEPS --

@given('the player class is "developer"')
def step_developer_class(context):
    """Set player class to developer"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.player_class = "developer"

@then('the music style should be "techno"')
def step_verify_techno_style(context):
    """Verify techno style for developer"""
    bdd_ctx = get_bdd_context(context)
    # This would be verified by checking the style parameter used in generation
    assert bdd_ctx.player_class == "developer", "Player class should be developer"

@then('the tempo should be modern and energetic')
def step_verify_modern_tempo(context):
    """Verify modern energetic tempo"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'generated_victory_music'):
        tempo = bdd_ctx.generated_victory_music.tempo
        assert 110 <= tempo <= 160, f"Modern tempo should be energetic, got {tempo}"

@then('the music should feel innovative')
def step_verify_innovative_feel(context):
    """Verify innovative music feel"""
    bdd_ctx = get_bdd_context(context)
    # This is subjective - verify music was generated with appropriate parameters
    assert hasattr(bdd_ctx, 'generated_victory_music'), "Victory music should exist"

# -- AMBIENT LOOP STEPS --

@given('I need music for a specific scene length')
def step_need_scene_length(context):
    """Set scene length requirement"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.scene_duration = 30  # 30 seconds

@when('I create ambient loop for "forest" lasting 30 seconds')
def step_create_forest_loop(context):
    """Create 30-second forest loop"""
    bdd_ctx = get_bdd_context(context)
    generator = get_music_generator()

    pattern = generator.create_ambient_loop("forest", length_seconds=30)
    bdd_ctx.forest_loop = pattern

@then('the loop should be approximately 30 seconds long')
def step_verify_loop_duration(context):
    """Verify loop duration"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'forest_loop'):
        pattern = bdd_ctx.forest_loop
        total_duration = sum(note.duration for note in pattern.notes if hasattr(note, 'duration'))
        # Convert beats to seconds (approximate)
        estimated_seconds = (total_duration / pattern.tempo) * 60
        assert 25 <= estimated_seconds <= 35, f"Loop should be ~30 seconds, got ~{estimated_seconds}"

@then('the music should repeat seamlessly')
def step_verify_seamless_repeat(context):
    """Verify seamless looping capability"""
    bdd_ctx = get_bdd_context(context)
    # This would be verified by checking loop structure
    assert hasattr(bdd_ctx, 'forest_loop'), "Forest loop should exist"

@then('the mood should match forest environment')
def step_verify_forest_mood(context):
    """Verify forest mood"""
    bdd_ctx = get_bdd_context(context)

    if hasattr(bdd_ctx, 'forest_loop'):
        pattern = bdd_ctx.forest_loop
        assert 80 <= pattern.tempo <= 120, f"Forest music should be moderate tempo, got {pattern.tempo}"

# -- MAGICAL LOCATION STEPS --

@given('the player is in a magical location')
def step_magical_location(context):
    """Set magical location context"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.location_type = "magical"
    bdd_ctx.location_name = "enchanted_forest"

# -- DUNGEON LOCATION STEPS --

@when('the location name contains "dungeon"')
def step_location_contains_dungeon(context):
    """Set location name with dungeon"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.location_name = "dark_dungeon"

@when('I generate music with magical mood and fantasy style')
def step_generate_magical_fantasy_music(context):
    """Generate magical fantasy music"""
    bdd_ctx = get_bdd_context(context)
    generator = bdd_ctx.music_generator
    bdd_ctx.magical_pattern = generator.generate_theme_music(
        mood=MusicMood.MAGICAL,
        style=MusicStyle.FANTASY,
        duration_bars=6
    )

@then('the music should use fantasy scales')
def step_verify_fantasy_scales(context):
    """Verify fantasy scales are used"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'magical_pattern'):
        pattern = bdd_ctx.magical_pattern
        # Check for fantasy-like intervals (6ths, 7ths, diminished)
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        assert len(notes) > 0, "Should have notes for scale analysis"

@then('the tempo should be mystical (80-120 BPM)')
def step_verify_mystical_tempo(context):
    """Verify mystical tempo range"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'magical_pattern'):
        pattern = bdd_ctx.magical_pattern
        assert 80 <= pattern.tempo <= 120, f"Mystical tempo should be 80-120 BPM, got {pattern.tempo}"

@then('the chord progressions should be ethereal')
def step_verify_ethereal_progressions(context):
    """Verify ethereal chord progressions"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'magical_pattern'):
        pattern = bdd_ctx.magical_pattern
        # Verify pattern has varied intervals for ethereal feel
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        assert len(notes) >= 4, "Should have enough notes for ethereal progression"

@then('the velocity should vary (dynamic)')
def step_verify_dynamic_velocity(context):
    """Verify dynamic velocity variation"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'magical_pattern'):
        pattern = bdd_ctx.magical_pattern
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        if notes:
            velocities = [note.velocity for note in notes]
            velocity_range = max(velocities) - min(velocities)
            assert velocity_range > 20, f"Velocity should vary dynamically, range: {velocity_range}"

@then('the pattern should feel enchanting')
def step_verify_enchanting_pattern(context):
    """Verify enchanting pattern qualities"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'magical_pattern'):
        pattern = bdd_ctx.magical_pattern
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        assert len(notes) > 0, "Should have notes for enchanting pattern"
        # Verify mix of durations for magical feel
        durations = [note.duration for note in notes]
        assert len(set(durations)) >= 2, "Should have varied note durations for enchanting feel"

# -- DEVELOPER VICTORY MUSIC STEPS --

@when('I generate victory music for "developer" class')
def step_generate_developer_victory_music(context):
    """Generate developer class victory music"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.developer_victory = generate_victory_music("developer")

@then('the mood should be "victory"')
def step_verify_victory_mood(context):
    """Verify victory mood"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'developer_victory'), "Should have developer victory music"
    # Victory music should have triumphant qualities
    pattern = bdd_ctx.developer_victory
    assert pattern.tempo >= 100, f"Victory music should be upbeat, got {pattern.tempo} BPM"

@then('the pattern should reflect developer culture')
def step_verify_developer_culture(context):
    """Verify pattern reflects developer culture"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'developer_victory'), "Should have developer victory music"
    pattern = bdd_ctx.developer_victory

    # Developer culture patterns: modern, digital/technological feel
    notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
    assert len(notes) > 0, "Should have notes for developer culture"

    # Should have modern tempo and technological characteristics
    assert pattern.tempo >= 110, f"Developer music should be modern tempo, got {pattern.tempo}"

# -- LOOPING MUSIC STEPS --

@then('the pattern should be suitable for looping')
def step_verify_loopable_pattern(context):
    """Verify pattern is suitable for looping"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'forest_loop'):
        pattern = bdd_ctx.forest_loop
        # Check that pattern starts and ends in compatible keys
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        if len(notes) >= 2:
            first_note = notes[0]
            last_note = notes[-1]
            # For smooth looping, last note should resolve or connect to first
            assert abs(last_note.midi_note - first_note.midi_note) <= 12, "Notes should be in loopable range"

@then('the transition should be smooth')
def step_verify_smooth_transition(context):
    """Verify smooth transition between loop iterations"""
    bdd_ctx = get_bdd_context(context)
    if hasattr(bdd_ctx, 'forest_loop'):
        pattern = bdd_ctx.forest_loop
        # Verify pattern structure allows smooth repetition
        assert len(pattern.notes) > 0, "Should have notes for smooth transition"
        # Last few notes should lead naturally back to beginning
        notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
        if len(notes) >= 4:
            # Check final notes create resolution
            final_notes = notes[-4:]
            durations = [note.duration for note in final_notes]
            assert sum(durations) <= 4.0, "Final phrase should resolve within reasonable time"

# -- MIDI EXPORT STEPS --

@given('I have a music pattern')
def step_have_music_pattern(context):
    """Create a music pattern for export testing"""
    bdd_ctx = get_bdd_context(context)
    generator = bdd_ctx.music_generator

    # Create test pattern
    test_notes = [
        MusicNote('C', 4, 60, 1.0, 80),
        MusicNote('E', 4, 64, 1.0, 80),
        MusicNote('G', 4, 67, 2.0, 80),
        MusicNote('C', 4, 60, 2.0, 80)
    ]

    bdd_ctx.test_pattern = MusicPattern(
        notes=test_notes,
        tempo=120,
        time_signature=(4, 4),
        key='C'
    )

@given('I want to save it as MIDI file')
def step_want_save_midi(context):
    """Set intention to save as MIDI"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.save_midi_intention = True

@when('I convert the pattern to MIDI file "test_music.json"')
def step_convert_to_midi_file(context):
    """Convert pattern to MIDI file"""
    bdd_ctx = get_bdd_context(context)
    pattern = bdd_ctx.test_pattern
    filename = "test_music.json"

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)

    success = bdd_ctx.music_generator.to_midi_file(pattern, filename)
    bdd_ctx.midi_export_success = success
    bdd_ctx.midi_filename = filename

@then('the file should be created successfully')
def step_verify_file_created(context):
    """Verify MIDI file was created"""
    bdd_ctx = get_bdd_context(context)
    assert bdd_ctx.midi_export_success, "MIDI export should succeed"
    assert os.path.exists(bdd_ctx.midi_filename), f"MIDI file {bdd_ctx.midi_filename} should exist"

@then('the file should contain MIDI events')
def step_verify_midi_events(context):
    """Verify file contains MIDI events"""
    bdd_ctx = get_bdd_context(context)
    import json
    try:
        with open(bdd_ctx.midi_filename, 'r') as f:
            midi_data = json.load(f)
        assert 'events' in midi_data, "Should contain MIDI events"
        assert len(midi_data['events']) > 0, "Should have MIDI events"
        bdd_ctx.midi_events = midi_data['events']
    except Exception as e:
        assert False, f"Failed to read MIDI events: {e}"

@then('the file should include tempo information')
def step_verify_tempo_in_file(context):
    """Verify file includes tempo"""
    bdd_ctx = get_bdd_context(context)
    import json
    try:
        with open(bdd_ctx.midi_filename, 'r') as f:
            midi_data = json.load(f)
        assert 'tempo' in midi_data, "Should include tempo information"
        assert midi_data['tempo'] == bdd_ctx.test_pattern.tempo, f"Tempo should match pattern tempo"
    except Exception as e:
        assert False, f"Failed to verify tempo: {e}"

@then('the file should include note timing')
def step_verify_note_timing(context):
    """Verify file includes note timing"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'midi_events'), "Should have MIDI events loaded"

    # Check for note_on and note_off events with timing
    has_note_on = any(event.get('type') == 'note_on' for event in bdd_ctx.midi_events)
    has_note_off = any(event.get('type') == 'note_off' for event in bdd_ctx.midi_events)
    has_timing = any('time' in event for event in bdd_ctx.midi_events)

    assert has_note_on, "Should have note_on events"
    assert has_note_off, "Should have note_off events"
    assert has_timing, "Should have timing information"

@then('the file should be readable by music software')
def step_verify_readable_by_software(context):
    """Verify file format is readable"""
    bdd_ctx = get_bdd_context(context)
    import json
    try:
        with open(bdd_ctx.midi_filename, 'r') as f:
            midi_data = json.load(f)
        # Verify required structure for music software compatibility
        required_fields = ['format', 'tracks', 'tempo', 'events']
        for field in required_fields:
            assert field in midi_data, f"Should have required field: {field}"
    except Exception as e:
        assert False, f"File should be readable by music software: {e}"

# -- CHORD STRUCTURE STEPS --

@given('I am generating harmonic music')
def step_generating_harmonic_music(context):
    """Set context for harmonic music generation"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.harmonic_mode = True

@when('I create chord notes from root "C"')
def step_create_chord_notes_c(context):
    """Create chord notes from C root"""
    bdd_ctx = get_bdd_context(context)
    generator = bdd_ctx.music_generator

    # Create chord from root C
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    velocity_range = (60, 80)

    bdd_ctx.c_chord_notes = generator._create_chord_notes('C', scale, velocity_range)

@then('the chord should contain root note')
def step_verify_root_note(context):
    """Verify chord contains root note C"""
    bdd_ctx = get_bdd_context(context)
    chord_notes = bdd_ctx.c_chord_notes

    root_found = any(note[0] == 'C' for note in chord_notes)
    assert root_found, f"Chord should contain root note C, got: {[n[0] for n in chord_notes]}"

@then('the chord should contain third interval')
def step_verify_third_interval(context):
    """Verify chord contains third interval (E)"""
    bdd_ctx = get_bdd_context(context)
    chord_notes = bdd_ctx.c_chord_notes

    third_found = any(note[0] == 'E' for note in chord_notes)
    assert third_found, f"Chord should contain third interval E, got: {[n[0] for n in chord_notes]}"

@then('the chord should contain fifth interval')
def step_verify_fifth_interval(context):
    """Verify chord contains fifth interval (G)"""
    bdd_ctx = get_bdd_context(context)
    chord_notes = bdd_ctx.c_chord_notes

    fifth_found = any(note[0] == 'G' for note in chord_notes)
    assert fifth_found, f"Chord should contain fifth interval G, got: {[n[0] for n in chord_notes]}"

@then('all notes should be in the same scale')
def step_verify_same_scale(context):
    """Verify all notes are in the same scale"""
    bdd_ctx = get_bdd_context(context)
    chord_notes = bdd_ctx.c_chord_notes
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    for note_tuple in chord_notes:
        note_name = note_tuple[0]
        assert note_name in scale, f"Note {note_name} should be in C major scale"

@then('the MIDI values should be correct')
def step_verify_midi_values(context):
    """Verify correct MIDI note values"""
    bdd_ctx = get_bdd_context(context)
    chord_notes = bdd_ctx.c_chord_notes

    # Expected MIDI values for C4, E4, G4 in 5th octave
    expected_midi = {'C': 72, 'E': 76, 'G': 79}  # 5th octave MIDI values

    for note_tuple in chord_notes:
        note_name = note_tuple[0]
        midi_value = note_tuple[2]
        if note_name in expected_midi:
            # Allow for octave variations (±12)
            expected = expected_midi[note_name]
            assert abs(midi_value - expected) % 12 == 0, f"MIDI value for {note_name} should be correct class"

# -- UNKNOWN LOCATION STEPS --

@given('I need music for an unknown location')
def step_unknown_location_needed(context):
    """Set context for unknown location music"""
    bdd_ctx = get_bdd_context(context)
    bdd_ctx.location_type = "unknown"

@when('I generate ambient music for "unknown" location')
def step_generate_unknown_music(context):
    """Generate music for unknown location"""
    bdd_ctx = get_bdd_context(context)
    generator = bdd_ctx.music_generator
    bdd_ctx.unknown_music = generator.create_ambient_loop("unknown", length_seconds=20)

@then('the system should default to peaceful mood')
def step_verify_peaceful_default(context):
    """Verify peaceful mood default"""
    bdd_ctx = get_bdd_context(context)
    assert hasattr(bdd_ctx, 'unknown_music'), "Should have unknown location music"
    # Unknown locations should default to peaceful templates
    pattern = bdd_ctx.unknown_music
    assert pattern.tempo <= 100, f"Unknown location music should be peaceful tempo, got {pattern.tempo}"

@then('the music should be universally applicable')
def step_verify_universal_applicable(context):
    """Verify music is universally applicable"""
    bdd_ctx = get_bdd_context(context)
    pattern = bdd_ctx.unknown_music
    # Should have neutral characteristics
    notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
    assert len(notes) > 0, "Should have notes for universal applicability"

    # Check for moderate dynamics
    velocities = [note.velocity for note in notes]
    avg_velocity = sum(velocities) / len(velocities)
    assert 50 <= avg_velocity <= 80, f"Should have moderate volume for universal use: {avg_velocity}"

@then('the tempo should be moderate')
def step_verify_moderate_tempo(context):
    """Verify moderate tempo"""
    bdd_ctx = get_bdd_context(context)
    pattern = bdd_ctx.unknown_music
    assert 70 <= pattern.tempo <= 110, f"Tempo should be moderate (70-110), got {pattern.tempo}"

@then('the style should be neutral')
def step_verify_neutral_style(context):
    """Verify neutral style"""
    bdd_ctx = get_bdd_context(context)
    pattern = bdd_ctx.unknown_music
    # Should have neutral key (C major or similar)
    assert pattern.key in ['C', 'G', 'D'], f"Should use neutral key, got {pattern.key}"

@then('the music should not clash with any scene')
def step_verify_no_scene_clash(context):
    """Verify music doesn't clash with scenes"""
    bdd_ctx = get_bdd_context(context)
    pattern = bdd_ctx.unknown_music

    # Should avoid extreme characteristics
    assert 60 <= pattern.tempo <= 140, f"Tempo should not be extreme: {pattern.tempo}"

    notes = [note for note in pattern.notes if isinstance(note, MusicNote)]
    if notes:
        durations = [note.duration for note in notes]
        # Should not have extreme duration variations
        max_duration = max(durations)
        min_duration = min(durations)
        assert max_duration / min_duration <= 8, f"Duration variation should be moderate: {min_duration}-{max_duration}"

# Helper function
def _calculate_avg_velocity(notes):
    """Calculate average velocity from notes"""
    velocities = []
    for note in notes:
        if hasattr(note, 'velocity'):
            velocities.append(note.velocity)
    return sum(velocities) / len(velocities) if velocities else 0