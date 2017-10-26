from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

SHOP_SALES_QUANTITY = 10


@given("some shop with a set of sales")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_sales_')
    shop_info = instances['shop_info']
    shop = shop_info['shop']

    for i in range(0, SHOP_SALES_QUANTITY):
        create_sales(faker, shop=shop)

    context.shop_slug = shop_info['slug']


@when('app sends request to "api_shop_sales" url with the shop\'s slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_sales', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with list of published sales of the shop")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['sales', 'status'])
    json_content = response.json()

    context.test.assertEqual(len(json_content['sales']), SHOP_SALES_QUANTITY)
