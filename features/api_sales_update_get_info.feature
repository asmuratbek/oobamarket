Feature: Updating shop sales get info

  Scenario:
    Given already added shop sale
    When app sends request to "api_sales_update_get_info" url with the shop slug and sale id
    Then it should get response with the sale info