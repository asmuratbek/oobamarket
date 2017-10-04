Feature: Global categories' children categories

  Scenario:
    Given prepared global category with children categories
    When app sends request to "/api/v1/globalcategory/<slug>/children/"
    Then it should get response with list of children categories