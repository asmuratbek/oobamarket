Feature: Global categories list

  Scenario:
    Given prepared set of global categories
    When app sends request to "/api/v1/globalcategory/"
    Then it should get response with list of categories