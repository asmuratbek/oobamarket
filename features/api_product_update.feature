Feature: Product update

  Scenario:
    Given some product which should be updated

    When app sends request to "api_product_update" url with all required data
    Then it should get response with update success status

    When app sends request to "api_product_update" url with invalid shop slug
    Then it should get 404 error code

    When app sends request to "api_product_update" url with invalid category slug
    Then it should get 404 error code