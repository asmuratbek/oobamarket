Feature: Shop used parent categories

  Scenario:
    Given products of some parent categories in a user's shop
    When app sends request to "api_shop_categories" url with the shop slug
    Then it should get response with list of used parent categories
