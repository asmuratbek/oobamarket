Feature: Subcategories' child categories list

  Scenario:
    Given prepared subcategory with children categories
    When app sends request to "api_category_children" url
    Then it should get response with list of given subcategory's children categories