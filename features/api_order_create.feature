Feature: Create order

  Scenario:
    Given some set of products in user's cart
    When app sends request to "api_order_create" url with all required data
    Then it should get response with order creation success status
