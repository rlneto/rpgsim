Feature: Quest System

  Scenario: Quest acquisition
    Given the player is exploring the game world
    When they interact with NPCs
    Then they should be able to discover at least 100 different quests
    And each quest should have a clear objective
    And each quest should have appropriate rewards
    And quests should vary in difficulty from trivial to epic

  Scenario: NPC interaction
    Given the player encounters an NPC
    When they attempt to communicate
    Then they should have dialogue options based on their character class
    And they should have options based on their reputation
    And they should have options based on quest status
    And the NPC should respond appropriately to all valid inputs

  Scenario: NPC uniqueness
    Given the game contains 100 unique NPCs
    When players interact with different NPCs
    Then each NPC should have distinct personality traits
    And each NPC should have unique dialogue
    And each NPC should offer different quests or services
    And each NPC should respond differently to player actions and reputation