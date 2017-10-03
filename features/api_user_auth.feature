Feature: User authentication

  Scenario Outline:
    Given registered user with username <username>, email <email> and password <password>
    When app sends credentials to "/api/v1/rest-auth/login/"
    Then it should get authentication token

    Examples: Users
    | username  | email                  | password      |
    | test_user | test_user@somemail.com | test_password |

  Scenario Outline:
    Given registered user with username <username>, email <email> and password <password>
    When app sends credentials with wrong username <username_wrong> to "/api/v1/rest-auth/login/"
    Then it should get message saying that username is invalid

    Examples: Users
    | username   | email                    | password       | username_wrong  |
    | test_user1 | test_user1@somemail.com  | test_password1 | test_user_wrong |

  Scenario Outline:
    Given registered user with username <username>, email <email> and password <password>
    When app sends credentials with wrong password <password_wrong> to "/api/v1/rest-auth/login/"
    Then it should get message saying that password is invalid

    Examples: Users
    | username   | email                    | password       | password_wrong      |
    | test_user2 | test_user2@somemail.com  | test_password2 | test_password_wrong |