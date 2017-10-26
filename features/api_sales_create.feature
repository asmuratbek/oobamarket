Feature: Create shop sales

  Scenario:
    Given some shop we want to create a sales for

    When app sends request to "api_sales_create" url with all sales required data
    Then it should get response with sales create success status

    When app sends request to "api_sales_create" url with invalid data
    Then it should get response with sales create fail status