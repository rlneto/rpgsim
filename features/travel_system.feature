Feature: Travel System

  Scenario: Travel mechanics
    Given player selects destination
    When they initiate travel
    Then travel should take appropriate time
    And random events should occur during travel
    And travel should consume resources
    And character should arrive at destination
    
  Scenario: Travel safety and risks
    Given player travels through dangerous areas
    When journey is in progress
    Then encounter chance should increase with distance
    And higher character level should reduce risks
    And party size should affect encounter rates
    And safe routes should be available
    
  Scenario: Fast travel system
    Given player has discovered locations
    When they use fast travel
    Then previously visited cities should be accessible
    And fast travel should cost more resources
    And certain locations should be restricted
    And fast travel should unlock with progression
    
  Scenario: Travel costs and requirements
    Given player plans journey
    When they check travel details
    Then costs should scale with distance
    And terrain should affect travel time
    And character level should unlock routes
    And special equipment should reduce costs
    
  Scenario: Travel events and encounters
    Given player is traveling between cities
    When journey is in progress
    Then random encounters should occur
    And merchant caravans should be meetable
    And treasure discoveries should be possible
    And travel events should provide choices