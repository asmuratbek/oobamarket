Feature: User info

  Scenario:
    Given user with list of shops
    When app sends request with auth token
    Then it should get response with user information

  Scenario:
    Given user with list of shops
    When app sends request without auth token/with wrong auth token
    Then it should get 401 error status code