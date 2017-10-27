Feature: Change product quantity in cart

  Scenario:
    Given a product in user's cart
    When app sends request to "api_product_quantity_change_in_cart" url with quantity value
    Then it should get response with success message and new total sum value