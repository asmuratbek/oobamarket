Feature: My list

  Scenario:
    Given some user having set of shops, favorite products and cart items
    When app sends request to "api_my_list" url
    Then it should get response with the info listed above