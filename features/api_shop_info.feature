Feature: Shop info

  Scenario:
    Given a shop

    When app sends request to "api_shop_info" url containing a slug of the shop
    Then it should get response with an information of the shop

    When app sends request to "api_shop_info" url containing non-existing slug
    Then it should get 404 error code
