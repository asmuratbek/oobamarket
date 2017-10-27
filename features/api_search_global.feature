Feature: Global search

  Scenario:
    Given set of products
    When app sends request to "api_search_global" url with keyword param
    Then it should get response with list of products containing given keyword in title