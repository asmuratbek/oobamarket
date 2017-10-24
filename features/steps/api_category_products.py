from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

CATEGORY_PRODUCTS_QUANTITY = 10


@given("a category with products")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='category_products_')
    category_info = instances['category_info']
    shop_info = instances['shop_info']

    for i in range(0, CATEGORY_PRODUCTS_QUANTITY):
        create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                       slug_prefix='category_products_%s' % i)

    context.category_slug = category_info['slug']


@when('app sends request to "api_category_products" url with the category\'s slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:category_detail', kwargs=dict(slug=context.category_slug)))


@then("it should get response with list of products of given category")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    json_content = response.json()

    for item in json_content['results']:
        context.test.assertTrue(dict_has_keys(['detail_url', 'update_url', 'delete_url', 'id', 'title',
                                               'short_description', 'slug', 'category_title', 'shop',
                                               'price', 'sell_count', 'discount', 'currency',
                                               'delivery_type', 'delivery_cost', 'availability',
                                               'published', 'is_owner', 'main_image', 'is_in_cart',
                                               'delivery_type_display', 'is_favorite', 'get_price_function',
                                               'detail_view', 'update_view', 'delete_view',
                                               'created_at', 'updated_at', 'get_category_title', 'type'], item))
