from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

GLOBAL_CATEGORY_PRODUCTS_QUANTITY = 10


@given("a global category with products")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='category_products_')
    category_info = instances['category_info']
    shop_info = instances['shop_info']
    global_category_info = instances['global_category_info']

    for i in range(0, GLOBAL_CATEGORY_PRODUCTS_QUANTITY):
        create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                       slug_prefix='category_products_%s' % i)

    context.global_category_slug = global_category_info['slug']


@when('app sends request to "api_global_category_products" url with the global category\'s slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:globalcategory_detail', kwargs=dict(slug=context.global_category_slug)))


@then("it should get response with list of products of given global category")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'products'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 'success')

    for item in json_content['products']:
        context.test.assertTrue(dict_has_keys(['title', 'slug', 'short_description', 'shop', 'main_image',
                                               'price', 'is_favorite', 'is_in_cart'], item))