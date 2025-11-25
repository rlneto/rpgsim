# language: en
# BDD Feature: Character Creation
# Optimized for LLM agents - explicit language, no ambiguity

Feature: Character Creation
  As a RPGSim player
  I want to create a new character
  To start my adventure

  # Scenario 1: Basic Creation (First scenario - no dependencies)
  Scenario: Create Warrior character with valid data
    Given I inform the name "Aragorn" for the character
    And I select the class "warrior" for the character
    When I create the character
    Then the character must have the name "Aragorn"
    And the character must have the class "warrior"
    And the character must be at level 1
    And the character must have strength 15
    And the character must have dexterity 10
    And the character must have intelligence 8
    And the character must have wisdom 10
    And the character must have charisma 8
    And the character must have constitution 14
    And the character must have HP 60
    And the character must have maximum HP 60
    And the character must have 100 gold
    And the character must have abilities ["Attack", "Defend", "Power Strike"]
    And the character must have empty inventory

  # Scenario 2: Mage Creation (Depends on class system)
  Scenario: Create Mage character with valid data
    Given I inform the name "Gandalf" for the character
    And I select the class "mage" for the character
    When I create the character
    Then the character must have the name "Gandalf"
    And the character must have the class "mage"
    And the character must be at level 1
    And the character must have strength 8
    And the character must have dexterity 12
    And the character must have intelligence 16
    And the character must have wisdom 14
    And the character must have charisma 10
    And the character must have constitution 8
    And the character must have HP 24
    And the character must have maximum HP 24
    And the character must have 100 gold
    And the character must have abilities ["Attack", "Defend", "Fireball"]
    And the character must have empty inventory

  # Scenario 3: Name Validation (Depends on validation system)
  Scenario: Fail to create character with invalid name
    Given I inform the name "" for the character
    And I select the class "warrior" for the character
    When I attempt to create the character
    Then the creation must fail with error "Character name cannot be empty"

  Scenario: Fail to create character with too long name
    Given I inform the name "VeryLongNameThatExceedsTheAllowedLimitOfFiftyCharacters" for the character
    And I select the class "warrior" for the character
    When I attempt to create the character
    Then the creation must fail with error "Character name cannot exceed 50 characters"

  # Scenario 4: Class Validation (Depends on class system)
  Scenario: Fail to create character with invalid class
    Given I inform the name "Test" for the character
    And I select the class "nonexistent_class" for the character
    When I attempt to create the character
    Then the creation must fail with error "Invalid character class: nonexistent_class"

  # Scenario 5: All Classes Characters (Depends on complete class system)
  Scenario: Create characters for all 23 classes
    Given I have a mapping of classes and expected statistics
    When I create characters for all available classes
    Then each character must have the correct statistics for their class
    And each character must have the correct abilities for their class
    And each character must have the correct HP for their class