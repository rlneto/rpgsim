Feature: Equipment and Magic Items

  Scenario: Item acquisition
    Given the player defeats enemies or completes quests
    When receiving rewards
    Then they should have chance to find randomized loot
    And loot quality should scale with difficulty
    And they should find approximately 200 unique magic items
    And each item should have clear effects and benefits

  Scenario: Equipment customization
    Given the player has acquired equipment
    When they manage their inventory
    Then they should be able to equip items to appropriate slots
    And equipped items should modify character stats appropriately
    And they should be able to compare items visually
    And they should be able to sell unwanted items to vendors

  Scenario: Shop interactions
    Given the player enters a shop in any city
    When they interact with the shopkeeper
    Then they should be able to buy items appropriate to the shop type
    And they should be able to sell items at reasonable rates
    And prices should vary between cities based on supply and demand
    And shopkeepers should have limited gold reserves

  Scenario: Currency management
    Given the player has acquired currency
    When managing their finances
    Then they should be able to track their wealth
    And they should be able to make strategic purchasing decisions
    And they should have opportunities to earn currency through various means
    And they should face meaningful economic choices