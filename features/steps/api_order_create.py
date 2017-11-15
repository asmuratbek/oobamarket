from behave import *

from apps.order.models import SimpleOrder
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

PRODUCTS_QUANTITY = 10
CART_ITEMS_QUANTITY = 10


@given("some set of products in user's cart")
def step_impl(context):
    faker = context.faker

    products_infos = []
    user_info = create_user(faker)
    global_category_info = create_category(faker, 'order_create_global', is_global=True)
    global_category = global_category_info['category']
    user = user_info['user']

    shop_info = create_shop(faker, user=user, slug_prefix='order_create_shop')
    category_info = create_category(faker, slug_prefix='order_create_global_1', section=global_category, order=1)

    cart = Cart.objects.create(user=user)

    for i in range(0, PRODUCTS_QUANTITY):
        products_infos.append(create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                                             slug_prefix='user_cart_products_%s' % i))

    for i in range(0, CART_ITEMS_QUANTITY):
        product_info = random.choice(products_infos)

        create_cart_item(user, product=product_info['product'], cart=cart)

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.user = user
    context.cart = cart


@when('app sends request to "api_order_create" url with all required data')
def step_impl(context):
    random_word = context.faker.words()[0]

    context.response = context.client.post(reverse('api:order_create'), dict(
        name=random_word, last_name=random_word, phone=random_word, address=random_word
    ), **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with order creation success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 201)
    context.test.assertTrue(SimpleOrder.objects.filter(user=context.user, cart=context.cart).exists())
