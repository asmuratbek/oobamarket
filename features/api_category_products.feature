Feature: Category's products list

  Scenario:
    Given a category with products
    When app sends request to "api_category_products" url with the category's slug
    Then it should get response with list of products of given category