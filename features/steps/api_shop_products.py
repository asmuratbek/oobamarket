from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

SHOP_PRODUCTS_QUANTITY = 10


@given("some shop with products")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_products_')
    shop_info = instances['shop_info']
    category_info = instances['category_info']
    category = category_info['category']
    shop = shop_info['shop']

    for i in range(0, SHOP_PRODUCTS_QUANTITY):
        create_product(faker, shop=shop, category=category, slug_prefix='shop_products_%s' % i)

    context.shop_slug = shop_info['slug']


@when('app sends request to "api_shop_products" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_detail', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with products list of given shop")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    json_content = response.json()

    for item in json_content['results']:
        context.test.assertTrue(dict_has_keys(['update_url', 'delete_url', 'id', 'title',
                                               'short_description', 'long_description',
                                               'slug', 'category_title', 'shop', 'currency',
                                               'published', 'is_owner', 'main_image', 'is_in_cart',
                                               'is_favorite', 'created_at',
                                               'updated_at', 'get_category_title', 'type'], item))