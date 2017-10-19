Feature: Places list

  Scenario:
    Given prepared set of places (malls/markets)
    When app sends request to "api_places_list" url
    Then it should get response with list of places