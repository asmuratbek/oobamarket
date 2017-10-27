Feature: Create shop

  Scenario:
    Given a registered user

    When app sends request to "api_shop_create" url with all required data
    Then it should get 201 code response with an information of created shop

    When app sends request to "api_shop_create" url missing required data
    Then it should get 400 error code