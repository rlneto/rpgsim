Feature: Dungeon Exploration

  Scenario: Dungeon structure
    Given the player enters a dungeon
    When they explore it
    Then they should find unique layouts and environmental challenges
    And they should encounter puzzles appropriate to the theme
    And they should find secrets and hidden areas
    And each of the 50 dungeons should have a distinct theme

  Scenario: Dungeon progression
    Given the player is exploring a dungeon
    When they navigate through it
    Then they should face increasing difficulty
    And they should find progressively better rewards
    And they should have opportunities for strategic decisions
    And they should find clues about the dungeon's lore