Feature: User's favorite products list

  Scenario:
    Given products in user's favorites
    When app sends request to "api_user_favorites" url
    Then it should get response with list of favorite products