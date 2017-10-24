from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

CHILDREN_PRODUCTS_QUANTITY = 10
CHILDREN_CATEGORIES_QUANTITY = 2


@given("products of some children categories in a user's shop")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_child_categories_')
    global_category_info = instances['global_category_info']
    shop_info = instances['shop_info']
    shop = shop_info['shop']
    global_category = global_category_info['category']

    p_category_info = create_category(faker, slug_prefix='shop_child_categories_parent_1', order=1,
                                      section=global_category)

    p_category = p_category_info['category']

    first_child_category_info = create_category(faker, slug_prefix='shop_child_categories_2', order=2,
                                                section=global_category,
                                                parent_category=p_category)
    second_child_category_info = create_category(faker, slug_prefix='shop_child_categories_3', order=3,
                                                 section=global_category,
                                                 parent_category=p_category)

    first_child_category = first_child_category_info['category']
    second_child_category = second_child_category_info['category']

    for i in range(0, CHILDREN_PRODUCTS_QUANTITY):
        category = first_child_category if i % 2 == 0 else second_child_category

        create_product(faker, shop=shop, category=category, slug_prefix='shop_child_categories_%s' % i)

    context.shop_slug = shop_info['slug']
    context.parent_category_slug = p_category_info['slug']


@when('app sends request to "api_shop_children_categories" url with the shop slug and the parent category slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_category_children', kwargs=dict(slug=context.shop_slug,
                                                                                            category_slug=context.parent_category_slug)))


@then("it should get response with list of used children categories of given parent category")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'children'])
    json_content = response.json()

    context.test.assertEqual(len(json_content['children']), CHILDREN_CATEGORIES_QUANTITY)

    for item in json_content['children']:
        context.test.assertTrue(dict_has_keys(['id', 'slug', 'title'], item))
