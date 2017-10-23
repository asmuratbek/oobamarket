from behave import *
from features.steps import *
from features.helpers import *
import random
from django.urls import reverse

use_step_matcher("re")

SHOPS_QUANTITY = 2
CATEGORIES_QUANTITY = 2
PRODUCTS_QUANTITY = 10
CART_ITEMS_QUANTITY = 10


@given("products in user's cart")
def step_impl(context):
    faker = context.faker

    shops_infos = []
    categories_infos = []
    products_infos = []
    user_info = create_user(faker)
    global_category_info = create_category(faker, 'user_cart_global_', is_global=True)
    global_category = global_category_info['category']
    user = user_info['user']

    cart = Cart.objects.create(user=user)

    for i in range(0, SHOPS_QUANTITY):
        shops_infos.append(create_shop(faker, user=user, slug_prefix='user_cart_%s' % i))

    for i in range(0, CATEGORIES_QUANTITY):
        categories_infos.append(create_category(faker, slug_prefix='user_cart_category_%s' % i, section=global_category, order=i))

    for i in range(0, PRODUCTS_QUANTITY):
        shop_info = random.choice(shops_infos)
        category_info = random.choice(categories_infos)

        products_infos.append(create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                                             slug_prefix='user_cart_products_%s' % i))

    for i in range(0, CART_ITEMS_QUANTITY):
        product_info = random.choice(products_infos)

        create_cart_item(user, product=product_info['product'], cart=cart)

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token


@when('app sends request to "api_user_cart" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:user_cart'),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with list of products for each shop in cart")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['shops', 'status'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 'success')

    for shop in json_content['shops']:
        context.test.assertTrue(dict_has_keys(['title', 'logo', 'items'], shop))

        for item in shop['items']:
            context.test.assertTrue(dict_has_keys(['title', 'quantity', 'slug', 'short_description',
                                                   'shop', 'price', 'total', 'image',
                                                   'is_favorite', 'is_in_cart'], item))