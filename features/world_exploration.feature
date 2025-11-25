Feature: World Exploration

  Scenario: Navigating between cities
    Given the player has created a character
    When they are in the game world
    Then they should be able to travel between 20 distinct cities
    And each city should have unique geography and layout
    And travel should be possible through text-based world map
    And travel should have appropriate time costs

  Scenario: City exploration
    Given the player has entered a city
    When they explore the city
    Then they should find at least 8 different building types
    And each building should serve a specific function
    And each city should have unique shops with different inventories
    And each city should have distinctive cultural elements in descriptions