from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("already added shop sale")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='sales_update_get_info_')
    shop_info = instances['shop_info']
    user_info = instances['user_info']
    sale_info = create_sales(faker, shop=shop_info['shop'])
    sale = sale_info['sale']

    context.shop_slug = shop_info['slug']
    context.sale_id = sale.id
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_sales_update_get_info" url with the shop slug and sale id')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_sales_update', kwargs=dict(slug=context.shop_slug,
                                                                      pk=context.sale_id)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with the sale info")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'sale'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 0)