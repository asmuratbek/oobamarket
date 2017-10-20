Feature: Product create

  Scenario:
    Given a user's shop

    When app sends request to "api_product_create" url with all required data
    Then it should get response with success status

    When app sends request to "api_product_create" url with invalid shop slug
    Then it should get 404 error code

    When app sends request to "api_product_create" url with invalid category slug
    Then it should get 404 error code

