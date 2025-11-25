Feature: Music System for RPGSim
  As an LLM agent generating game content
  I want to create dynamic music that can be generated and played
  To enhance the gaming experience with adaptive soundtracks

  Background:
    Given the music system is initialized
    And MIDI note mappings are available
    And music templates are loaded

  Scenario: Generate peaceful ambient music for city exploration
    Given I want to create music for a city location
    When I generate ambient music for "city"
    Then the music should have peaceful mood
    And the tempo should be between 60-100 BPM
    And the key should be suitable for exploration
    And the pattern should contain multiple notes
    And the music should be convertible to MIDI format

  Scenario: Generate intense combat music
    Given a battle is starting
    When I generate combat music with "medium" intensity
    Then the music should have combat mood
    And the tempo should be between 120-160 BPM
    And the rhythm should be more aggressive
    And the velocity should be higher than ambient music
    And the pattern should contain shorter note durations

  Scenario: Generate victory celebration music
    Given the player has won a battle
    When I generate victory music for "warrior" class
    Then the music should have victory mood
    And the tempo should be celebratory (100-140 BPM)
    And the style should match the player class
    And the pattern should contain ascending progressions
    And the music should feel triumphant

  Scenario: Generate location-specific dungeon music
    Given the player enters a dark dungeon
    When I generate location music for "dungeon" type
    And the location name contains "dungeon"
    Then the music should have mysterious mood
    And the tempo should be slower (60-80 BPM)
    And the velocity should be lower (quieter)
    And the key should be minor or modal
    And the pattern should create suspense

  Scenario: Generate magical fantasy music
    Given the player is in a magical location
    When I generate music with magical mood and fantasy style
    Then the music should use fantasy scales
    And the tempo should be mystical (80-120 BPM)
    And the chord progressions should be ethereal
    And the velocity should vary (dynamic)
    And the pattern should feel enchanting

  Scenario: Convert music to LLM-friendly prompt
    Given I have a generated music pattern
    And the pattern has tempo and key information
    When I convert the pattern to LLM prompt
    Then the prompt should include tempo information
    And the prompt should include key signature
    And the prompt should describe the musical sequence
    And the prompt should be readable by language models
    And the prompt should be suitable for music generation

  Scenario: Create developer-themed music
    Given the player class is "developer"
    When I generate victory music for "developer" class
    Then the music style should be "techno"
    And the mood should be "victory"
    And the pattern should reflect developer culture
    And the tempo should be modern and energetic
    And the music should feel innovative

  Scenario: Generate ambient loop of specific duration
    Given I need music for a specific scene length
    When I create ambient loop for "forest" lasting 30 seconds
    Then the loop should be approximately 30 seconds long
    And the music should repeat seamlessly
    And the mood should match forest environment
    And the pattern should be suitable for looping
    And the transition should be smooth

  Scenario: Generate music with MIDI export capability
    Given I have a music pattern
    And I want to save it as MIDI file
    When I convert the pattern to MIDI file "test_music.json"
    Then the file should be created successfully
    And the file should contain MIDI events
    And the file should include tempo information
    And the file should include note timing
    And the file should be readable by music software

  Scenario: Generate music with proper chord structure
    Given I am generating harmonic music
    When I create chord notes from root "C"
    Then the chord should contain root note
    And the chord should contain third interval
    And the chord should contain fifth interval
    And all notes should be in the same scale
    And the MIDI values should be correct

  Scenario: Generate location-agnostic music
    Given I need music for an unknown location
    When I generate ambient music for "unknown" location
    Then the system should default to peaceful mood
    And the music should be universally applicable
    And the tempo should be moderate
    And the style should be neutral
    And the music should not clash with any scene