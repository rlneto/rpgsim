Feature: Shop System

  Scenario: Shop inventory management
    Given player enters any shop
    When they browse available items
    Then shop should have 15-30 items in stock
    And inventory should refresh periodically
    And rare items should appear occasionally
    And shop type should determine inventory focus
    
  Scenario: Dynamic pricing system
    Given player wants to buy items
    When they check prices across cities
    Then prices should vary by location
    And supply should affect pricing
    And player reputation should influence costs
    And bulk purchases should offer discounts
    
  Scenario: Shop economy simulation
    Given shop operates in game world
    When player interacts with shop over time
    Then shop should have limited gold reserves
    And buying should deplete shop inventory
    And selling should increase shop inventory
    And shop should restock based on trade routes
    
  Scenario: Shop types and specializations
    Given player explores different cities
    When they visit various shops
    Then they should find weapon specialists
    And they should find armor merchants
    And they should find magic item dealers
    And they should find general traders
    And each shop type should have unique inventory
    
  Scenario: Trading and bartering system
    Given player wants to sell items
    When they interact with shopkeeper
    Then they should receive fair market value
    And rare items should fetch higher prices
    And shopkeeper gold should limit purchases
    And reputation should affect sell prices