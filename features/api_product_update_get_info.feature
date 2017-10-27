Feature: Get updating product info

  Scenario:
    Given some product which wanted to be updated
    When app sends request to "api_product_update_get_info" url with the product slug
    Then it should get response with product's necessary data