from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

SHOP_PRODUCTS_QUANTITY = 3
SHOP_PRODUCTS_OF_CATEGORY_QUANTITY = 2
FAVORITE_PRODUCTS_QUANTITY = 2


@given("some shop with products")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_products_')

    user_info = instances['user_info']
    shop_info = create_shop(faker, user=user_info['user'], slug_prefix='shop_products_')
    category_info = instances['category_info']

    global_category = instances['global_category_info']['category']
    category2_info = create_category(faker, slug_prefix='shop_products_2', order=2, section=global_category)

    category = category_info['category']
    category2 = category2_info['category']
    shop = shop_info['shop']
    user = user_info['user']

    products_infos = []

    for i in range(0, SHOP_PRODUCTS_QUANTITY):
        products_infos.append(create_product(faker, shop=shop, category=category, slug_prefix='shop_products_%s' % i))

    for i in range(0, SHOP_PRODUCTS_OF_CATEGORY_QUANTITY):
        create_product(faker, shop=shop, category=category2, slug_prefix='shop_products_2_%s' % i)

    for i in range(0, FAVORITE_PRODUCTS_QUANTITY):
        product = random.choice(products_infos)['product']
        create_favorite_product(user=user, product=product)

    context.shop_slug = shop_info['slug']
    context.search_by_category_slug = category2.slug
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_shop_products" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_detail', kwargs=dict(slug=context.shop_slug)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with products list of given shop")
def step_impl(context):
    response = context.response

    favorite_products_quantity = 0

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    json_content = response.json()

    context.test.assertEqual(json_content['count'], SHOP_PRODUCTS_OF_CATEGORY_QUANTITY + SHOP_PRODUCTS_QUANTITY)

    for item in json_content['results']:
        if item['is_favorite']:
            favorite_products_quantity += 1

    context.test.assertEqual(favorite_products_quantity, FAVORITE_PRODUCTS_QUANTITY)


@when('app sends request to "api_shop_products" url with the shop and the category slugs')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_detail', kwargs=dict(slug=context.shop_slug)),
                                                 dict(category=context.search_by_category_slug))


@then("it should get response with products list of the category in the shop")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    json_content = response.json()

    context.test.assertEqual(json_content['count'], SHOP_PRODUCTS_OF_CATEGORY_QUANTITY)