Feature: Global categories list

  Scenario:
    Given prepared set of global categories
    When app sends request to "api_global_category" url
    Then it should get response with list of global categories