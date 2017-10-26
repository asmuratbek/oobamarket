Feature: Sales wall

  Scenario:
    Given some user following a few shops
    When app sends request to "api_sales_wall" url
    Then it should get response with list of last sales of the shops
