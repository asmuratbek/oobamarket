Feature: Shop update

  Scenario:
    Given some shop which info we want to update
    When app sends request to "api_shop_update" url with all required data
    Then it should get response with shop update success status