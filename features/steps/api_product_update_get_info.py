from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some product which wanted to be updated")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_update_get_info_')
    user_info = instances['user_info']
    product_info = instances['product_info']

    context.product_slug = product_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_product_update_get_info" url with the product slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:product_update', kwargs=dict(slug=context.product_slug)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with product's necessary data")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['images', 'product'])