from behave import *
from django.urls import reverse
from features.steps import *
from features.helpers import *

use_step_matcher("re")


@given("some google and facebook accounts")
def step_impl(context):
    google_client_id = '230288808995-4c5f9sf26l43u1jpcgftv6uh8vcoipsq.apps.googleusercontent.com'
    google_secret = 'qzOus6dbh4ncyZhR_TMVr2aR'
    facebook_client_id = '115196085804923'
    facebook_secret = 'ff850821f566bdb18ec20a38a8bc2645'

    google_account_token = 'ya29.Glv0BP9I32wXOfQvux3dElqN3S9VnI9AxZ_2tNNT3BOnz7CPZ534wyBFXwmKhsv4PxhErRfYW-LhP0Q5RhUc2pHTIpMHIYF9jV1wqstrRTpjjqjZ660MyU_xBETw'
    facebook_account_token = 'EAABoxS3GH3sBADZBksZAXTAzKH7EZBO7jZAvhIZB6isyj5k33bSZBBJZCFi08kY5ZC1l8lcSBdwLTl3XblsIGdpqZCCebtchZAsYZBrIV3S7082rMv3l7ZAQgPL8r85lq4ZAKVmcBpQITKYqUhmSiFoOx22ZBabVOeCzocxiZBWYC8sUEfxahcdJrghIl2d6lSagqrSQXsoRpuoxNpynQZDZD'

    site_info = create_site_for_social_app('localhost:8000', 'localhost')
    create_social_app('google', name='Google', client_id=google_client_id,
                      secret=google_secret, site=site_info['site'])
    create_social_app('facebook', name='Facebook', client_id=facebook_client_id,
                      secret=facebook_secret, site=site_info['site'])

    context.google_account_token = google_account_token
    context.facebook_account_token = facebook_account_token


@when('app sends request to "api_social_auth" url with the google account token')
def step_impl(context):
    context.response = context.client.post(reverse('api:google_login'),
                                           data=dict(social_token=context.google_account_token))


@then("it should get response with user's token")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['key'])


@when('app sends request to "api_social_auth" url with the invalid google account token')
def step_impl(context):
    context.response = context.client.post(reverse('api:google_login'),
                                           data=dict(social_token='invalid_access_token'))


@then('it should get response with "Bad request" status')
def step_impl(context):
    assert_status_code(context, context.response, 400)


@when('app sends request to "api_social_auth" url with the facebook account token')
def step_impl(context):
    context.response = context.client.post(reverse('api:fb_login'),
                                           data=dict(social_token=context.facebook_account_token))


@when('app sends request to "api_social_auth" url with the invalid facebook account token')
def step_impl(context):
    context.response = context.client.post(reverse('api:fb_login'),
                                           data=dict(social_token='invalid_access_token'))