Feature: Shop sales list

  Scenario:
    Given some shop with a set of sales
    When app sends request to "api_shop_sales" url with the shop's slug
    Then it should get response with list of published sales of the shop