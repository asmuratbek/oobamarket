Feature: Product delete

  Scenario:
    Given some product we want to delete
    When app sends request to "api_product_delete" url with the product slug
    Then it should get response with product delete success status