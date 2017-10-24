Feature: Global category's products list

  Scenario:
    Given a global category with products
    When app sends request to "api_global_category_products" url with the global category's slug
    Then it should get response with list of products of given global category