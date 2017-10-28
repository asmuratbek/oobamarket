Feature: Social accounts sign in

  Scenario:
    Given some google and facebook accounts

#    When app sends request to "api_social_auth" url with the google account token
#    Then it should get response with user's token

#    When app sends request to "api_social_auth" url with the facebook account token
#    Then it should get response with user's token

    When app sends request to "api_social_auth" url with the invalid google account token
    Then it should get response with "Bad request" status

    When app sends request to "api_social_auth" url with the invalid facebook account token
    Then it should get response with "Bad request" status