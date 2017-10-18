Feature: Subcategories' child categories list

  Scenario:
    Given prepared subcategory with children categories
    When app sends request to "/api/v1/category/<slug>/children/"
    Then it should get response with list of given subcategory's children categories