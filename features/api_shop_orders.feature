Feature: Get shop orders list

  Scenario:
    Given some set of orders of the shop
    When app sends request to "api_shop_orders" url with the shop slug
    Then it should get response with the shop orders list
