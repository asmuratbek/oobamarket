from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some shop which wanted to be updated")
def step_impl(context):
    faker = context.faker
    shop_logo = SimpleUploadedFile(name=IMAGE_ASSET_NAME, content=open(IMAGE_ASSET_PATH, 'rb').read(),
                                   content_type=IMAGE_ASSET_TYPE)

    instances = create_instances(faker, slug_prefix='shop_update_get_info_', shop_logo=shop_logo)
    shop_info = instances['shop_info']
    user_info = instances['user_info']

    create_contacts(faker, shop_info['shop'])

    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_shop_update_get_info" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_update', kwargs=dict(slug=context.shop_slug)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with shop's necessary data")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['logo', 'users', 'contact'])


@given("some shop without any contact and logo")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_update_get_info_2')
    shop_info = instances['shop_info']
    user_info = instances['user_info']

    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])