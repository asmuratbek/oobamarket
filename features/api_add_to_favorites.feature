Feature: Add a product to favorites list/Remove a product from favorites list

  Scenario:
    Given a product which user wants to add to favorites list
    When app sends request to "api_add_to_favorites" url with given product slug
    Then it should get response with info that product is added to favorites

  Scenario:
    Given a product which already added to favorites list
    When app sends request to "api_add_to_favorites" url with given product slug
    Then it should get response with info that product is removed from favorites
