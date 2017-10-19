Feature: Shop contacts info

  Scenario:
    Given shop with its contacts
    When app sends request to "api_shop_contacts" url containing a slug of the shop
    Then it should get response with list of contacts info

  Scenario:
    Given shop with its contacts
    When app sends request to "api_shop_contacts" url containing non-existing slug
    Then it should get 404 error code