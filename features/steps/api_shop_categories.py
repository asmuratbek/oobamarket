from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

PARENT_CATEGORY_PRODUCTS_QUANTITY = 10
PARENT_CATEGORIES_COUNT = 2


@given("products of some parent categories in a user's shop")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_categories_')
    user_info = instances['user_info']
    global_category_info = instances['global_category_info']
    shop_info = create_shop(faker, user=user_info['user'], slug_prefix='shop_categories_')

    shop = shop_info['shop']
    global_category = global_category_info['category']

    first_p_category_info = create_category(faker, slug_prefix='shop_categories_parent_1', order=1,
                                            section=global_category)
    second_p_category_info = create_category(faker, slug_prefix='shop_categories_parent_2', order=2,
                                             section=global_category)

    first_category_info = create_category(faker, slug_prefix='shop_categories_1', order=3, section=global_category,
                                          parent_category=first_p_category_info['category'])
    second_category_info = create_category(faker, slug_prefix='shop_categories_2', order=4, section=global_category,
                                           parent_category=second_p_category_info['category'])

    first_category = first_category_info['category']
    second_category = second_category_info['category']

    for i in range(0, PARENT_CATEGORY_PRODUCTS_QUANTITY):
        category = first_category if i % 2 == 0 else second_category

        create_product(faker, shop=shop, category=category, slug_prefix='shop_categories_%s' % i)

    context.shop_slug = shop_info['slug']


@when('app sends request to "api_shop_categories" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_categories', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with list of used parent categories")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'categories'])
    json_content = response.json()

    context.test.assertEqual(len(json_content['categories']), PARENT_CATEGORIES_COUNT)
