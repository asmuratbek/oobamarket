Feature: Shop review create

  Scenario:
    Given some shop we want to create a review for

    When app sends request to "api_review_create" url with the shop slug and valid required data
    Then it should get response with review create success status

    When app sends request to "api_review_create" url with the shop slug and invalid required data
    Then it should get response with review create fail status