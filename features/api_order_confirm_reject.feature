Feature: Confirm/Reject an order by a shop

  Scenario:
    Given some order of a shop which is going to be confirmed/rejected
    When app sends request to "api_order_confirm_reject" with the order's cart id, the shop slug and confirm action
    Then it should get response with success status and shop should be in confirmed shops list of the order

  Scenario:
    Given some order of a shop which is going to be confirmed/rejected
    When app sends request to "api_order_confirm_reject" with the order's cart id, the shop slug and reject action
    Then it should get response with success status and shop should be in rejected shops list of the order
