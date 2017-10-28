Feature: Get updating shop info

  Scenario:
    Given some shop which wanted to be updated
    When app sends request to "api_shop_update_get_info" url with the shop slug
    Then it should get response with shop's necessary data

  Scenario:
    Given some shop without any contact and logo
    When app sends request to "api_shop_update_get_info" url with the shop slug
    Then it should get response with shop's necessary data