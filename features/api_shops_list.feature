Feature: Shops list

  Scenario:
    Given prepared set of shops

    When app sends request to "api_shops_list" url with keyword param
    Then it should get response with list of shops, matching keyword query

    When app sends request to "api_shops_list" url with place param
    Then it should get response with list of shops, which belong to given place
