Feature: Combat System

  Scenario: Turn-based combat
    Given the player encounters an enemy
    When combat begins
    Then it should operate on a turn-based system
    And initiative should be calculated based on character stats
    And each action should have appropriate time costs
    And players should have access to all character abilities during combat

  Scenario: Enemy variety
    Given the player is exploring dungeons
    When they encounter enemies
    Then they should face 200 different enemy types
    And each enemy should have unique abilities and attacks
    And each enemy should have appropriate AI behavior
    And each enemy should have weaknesses that can be exploited

  Scenario: Boss encounters
    Given the player enters a dungeon
    When they reach the end
    Then they should encounter one of 50 unique bosses
    And each boss should have mechanics not shared with regular enemies
    And each boss should be thematically appropriate to its dungeon
    And each boss should offer unique rewards upon defeat