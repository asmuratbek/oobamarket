Feature: Global categories' children categories

  Scenario:
    Given prepared global category with children categories
    When app sends request to "api_global_category_children" url
    Then it should get response with list of children categories