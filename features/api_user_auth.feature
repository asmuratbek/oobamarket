Feature: User authentication

  Scenario:
    Given registered user
    When app sends right credentials to "/api/v1/rest-auth/login/"
    Then it should get authentication token

  Scenario:
    Given registered user
    When app sends credentials with wrong username to "/api/v1/rest-auth/login/"
    Then it should get message saying that username is invalid

  Scenario Outline:
    Given registered user
    When app sends credentials with wrong password to "/api/v1/rest-auth/login/"
    Then it should get message saying that password is invalid