from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("a product")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_info_')
    product_info = instances['product_info']
    user_data = instances['user_info']

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])

    context.auth_token = auth_token
    context.product_slug = product_info['slug']


@when('app sends request to "api_product_info" url with given product slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:product_detail', kwargs=dict(slug=context.product_slug)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with all information of the product")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['price', 'title', 'is_in_cart', 'is_favorite',
                                                        'images', 'short_description', 'shop'])
    json_content = response.json()

    for item in json_content['images']:
        context.test.assertTrue(dict_has_keys(['image'], item))

