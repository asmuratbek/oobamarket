from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

PRODUCTS_QUANTITY = 5
CART_ITEMS_QUANTITY = 5
ORDERS_QUANTITY = 5
CARTS_QUANTITY = 5


@given("some set of orders of the shop")
def step_impl(context):
    faker = context.faker

    products_infos = []
    user_info = create_user(faker)
    client_user_info = create_user(faker)
    global_category_info = create_category(faker, 'order_create_global', is_global=True)
    global_category = global_category_info['category']
    user = user_info['user']
    client_user = client_user_info['user']

    shop_info = create_shop(faker, user=user, slug_prefix='order_create_shop')
    category_info = create_category(faker, slug_prefix='order_create_global_1', section=global_category, order=1)

    for i in range(0, PRODUCTS_QUANTITY):
        products_infos.append(create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                                             slug_prefix='user_cart_products_%s' % i))

    for i in range(0, CARTS_QUANTITY):
        cart = Cart.objects.create(user=client_user)

        for i in range(0, CART_ITEMS_QUANTITY):
            product_info = random.choice(products_infos)

            create_cart_item(user, product=product_info['product'], cart=cart)

        create_order(faker, cart=cart, user=user)

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.shop_slug = shop_info['shop'].slug


@when('app sends request to "api_shop_orders" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_order_list', kwargs=dict(slug=context.shop_slug)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with the shop orders list")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    json_content = response.json()

    context.test.assertEqual(len(json_content['orders']), ORDERS_QUANTITY)
