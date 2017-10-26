Feature: Update user info

  Scenario:
    Given some user we want to update

    When app sends request to "api_user_update" url with valid data
    Then it should get response with user update success status

    When app sends request to "api_user_update" url with invalid data
    Then it should get response with user update fail status