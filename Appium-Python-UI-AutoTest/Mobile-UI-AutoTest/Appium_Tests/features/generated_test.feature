Feature: Calculate Simple Interest

  Scenario: Calculate interest with valid inputs
    Given the user is on the simple interest calculator screen
    When the user enters "10000" into the principal input field
    And the user enters "3" into the interest rate input field
    And the user enters "3" into the period input field
    And the user taps the calculate button
    Then the result should be "900.00"