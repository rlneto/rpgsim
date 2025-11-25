Feature: Character Creation and Classes

  Scenario: Creating a new character
    Given a new player wants to start the game
    When they access the character creation screen
    Then they should be presented with 23 unique character classes to choose from
    And each class should have distinct starting stats
    And each class should have unique gameplay mechanics
    And each class should have access to at least 10 unique abilities
    And the character creation should include name selection
    And the character creation should include visual customization (text-based)

  Scenario: Character class balance
    Given the game has 23 character classes
    When comparing class statistics
    Then no class should be more than 15% more powerful than any other class
    And each class should have clear strengths and weaknesses
    And each class should have at least one unique mechanic not shared by other classes