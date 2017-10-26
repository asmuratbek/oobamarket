Feature: Shop sale delete

  Scenario:
    Given some sale of a shop we want to delete
    When app sends request to "api_sales_delete" url with the shop slug and the sale id
    Then it should get response with sale delete success status