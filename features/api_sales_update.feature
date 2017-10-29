Feature: Shop sale update

  Scenario:
    Given some shop's sale
    When app sends request to "api_sales_update" url will all required data
    Then it should get response with shop sale update success status