Feature: Shop used children categories

  Scenario:
    Given products of some children categories in a user's shop
    When app sends request to "api_shop_children_categories" url with the shop slug and the parent category slug
    Then it should get response with list of used children categories of given parent category