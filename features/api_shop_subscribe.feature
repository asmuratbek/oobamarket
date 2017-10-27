Feature: User's shop subscribe/unsubscribe

  Scenario:
    Given some shop and a user
    When app sends request to "api_shop_subscribe" url
    Then it should get response with subscription success status

  Scenario:
    Given some shop and its subscriber user
    When app sends request to "api_shop_subscribe" url
    Then it should get response with unsubscription success status