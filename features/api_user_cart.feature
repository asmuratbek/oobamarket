Feature: User's cart items list

  Scenario:
    Given products in user's cart
    When app sends request to "api_user_cart" url
    Then it should get response with list of products for each shop in cart