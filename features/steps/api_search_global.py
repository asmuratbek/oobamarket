from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

PRODUCTS_WITH_SAME_TITLE_KEYWORD_QUANTITY = 5
TITLE_KEYWORD = 'some keyword'
OTHER_PRODUCTS_QUANTITY = 3


@given("set of products")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='search_global_')
    category_info = instances['category_info']
    shop_info = instances['shop_info']
    category = category_info['category']
    shop = shop_info['shop']

    for i in range(0, PRODUCTS_WITH_SAME_TITLE_KEYWORD_QUANTITY):
        create_product(faker, shop=shop, category=category, slug_prefix='search_global_%s' % i,
                       title_prefix=TITLE_KEYWORD)

    for i in range(0, OTHER_PRODUCTS_QUANTITY):
        create_product(faker, shop=shop, category=category, slug_prefix='search_global_2_%s' % i)


@when('app sends request to "api_search_global" url with keyword param')
def step_impl(context):
    context.response = context.client.get(reverse('api:search_products'), dict(q=TITLE_KEYWORD))


@then("it should get response with list of products containing given keyword in title")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['result'])
    json_content = response.json()

    context.test.assertEqual(len(json_content['result']), PRODUCTS_WITH_SAME_TITLE_KEYWORD_QUANTITY)
