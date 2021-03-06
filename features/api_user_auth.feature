Feature: User authentication

  Scenario:
    Given registered user

    When app sends right credentials
    Then it should get authentication token

    When app sends credentials with wrong username
    Then it should get message saying that username is invalid

    When app sends credentials with wrong password
    Then it should get message saying that password is invalid
