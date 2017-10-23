Feature: Add a product to cart/Remove a product from cart

  Scenario:
    Given a product which user wants to add to cart
    When app sends request to "api_add_to_cart" url with given product slug
    Then it should get response with info that product is added to cart

  Scenario:
    Given a product which already added to cart
    When app sends request to "api_add_to_cart" url with given product slug
    Then it should get response with info that product is removed from cart