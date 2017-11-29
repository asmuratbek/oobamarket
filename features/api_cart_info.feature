Feature: Get cart items info

  Scenario:
    Given some cart with items
    When app sends request to "api_cart_info" url with the cart id
    Then it should get response with the cart items info
