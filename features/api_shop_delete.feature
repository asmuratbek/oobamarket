Feature: Shop delete

  Scenario:
    Given some shop we want to delete
    When app sends request to "api_shop_delete" url with the shop slug
    Then it should get response with shop delete success status