Feature: Shop reviews list

  Scenario:
    Given some shop with users' reviews
    When app sends request to "api_shop_reviews" url with the shop slug
    Then it should get response with list of all reviews