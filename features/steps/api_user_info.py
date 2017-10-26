from behave import *
from django.urls import reverse
from features.helpers import *
from apps.shop.models import *
import random
from features.steps import LOGIN_URL

use_step_matcher("re")

SHOPS_QUANTITY = 5
USER_INFO_URL = reverse('api:user_detail')

SHOPS_ALREADY_CREATED = False


@given("user with list of shops")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    user = user_data['user']
    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])

    for i in range(0, SHOPS_QUANTITY):
        create_shop(faker, user=user, slug_prefix='user_info_%s_%s' % (random.randint(0, 1000), i))

    context.auth_token = auth_token


@when('app sends request with auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with user information")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'address', 'favorites_count', 'cart_count', 'email',
                                                        'first_name', 'phone', 'shops', 'username', 'last_name'])


@when('app sends request without auth token/with wrong auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATIOn='Token wrongtoken'))


@then("it should get 401 error status code")
def step_impl(context):
    assert_status_code(context, context.response, 401)
