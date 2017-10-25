from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

from apps.users.models import *

use_step_matcher("re")


@given("some shop and a user")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_subscribe_')
    shop_info = instances['shop_info']
    user_info = create_user(faker, username_prefix='subscriber_')

    context.user = user_info['user']
    context.shop = shop_info['shop']
    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_shop_subscribe" url')
def step_impl(context):
    context.response = context.client.post(reverse('api:subscribe'), dict(shop=context.shop_slug),
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with subscription success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])

    context.test.assertIsNotNone(Subscription.objects.filter(user=context.user, subscription=context.shop).first())


@given("some shop and its subscriber user")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_subscribe_2_')
    shop_info = instances['shop_info']
    user_info = create_user(faker, username_prefix='subscriber_2_')
    shop = shop_info['shop']
    user = user_info['user']

    Subscription.objects.create(subscription=shop, user=user)

    context.user = user
    context.shop = shop
    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@then("it should get response with unsubscription success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])

    context.test.assertIsNone(Subscription.objects.filter(user=context.user, subscription=context.shop).first())