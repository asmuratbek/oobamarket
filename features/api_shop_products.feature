Feature: Shop's products list

  Scenario:
    Given some shop with products
    When app sends request to "api_shop_products" url with the shop slug
    Then it should get response with products list of given shop