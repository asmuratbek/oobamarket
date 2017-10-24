Feature: Product info

  Scenario:
    Given a product
    When app sends request to "api_product_info" url with given product slug
    Then it should get response with all information of the product