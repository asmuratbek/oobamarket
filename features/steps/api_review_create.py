from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse
import random

use_step_matcher("re")


@given("some shop we want to create a review for")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='review_create_')
    shop_info = instances['shop_info']
    user_info = instances['user_info']

    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_review_create" url with the shop slug and valid required data')
def step_impl(context):
    faker = context.faker
    post_data = dict(stars=random.randint(1, 5), text=faker.words())

    context.response = context.client.post(reverse('api:shop_reviews', kwargs=dict(slug=context.shop_slug)), data=post_data,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with review create success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 0)


@when('app sends request to "api_review_create" url with the shop slug and invalid required data')
def step_impl(context):
    post_data = dict(stars=random.randint(1, 5))

    context.response = context.client.post(reverse('api:shop_reviews', kwargs=dict(slug=context.shop_slug)), data=post_data,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with review create fail status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 1)