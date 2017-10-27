from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse
import random

use_step_matcher("re")


@given("some shop we want to create a sales for")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='sales_create_')
    user_info = instances['user_info']
    shop_info = instances['shop_info']

    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_sales_create" url with all sales required data')
def step_impl(context):
    faker = context.faker
    image = open(IMAGE_ASSET_PATH, 'rb')
    post_data = dict(title=faker.words(), short_description=faker.words(), description=faker.words(), image=image,
                     discount=random.randint(0, 90))

    context.response = context.client.post(reverse('api:shop_sales_create', kwargs=dict(slug=context.shop_slug)),
                                           data=post_data, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))

    image.close()


@then("it should get response with sales create success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 0)


@when('app sends request to "api_sales_create" url with invalid data')
def step_impl(context):
    faker = context.faker
    post_data = dict(description=faker.words(), discount=random.randint(0, 90))

    context.response = context.client.post(reverse('api:shop_sales_create', kwargs=dict(slug=context.shop_slug)),
                                           data=post_data, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with sales create fail status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 1)