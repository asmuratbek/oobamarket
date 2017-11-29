from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

PRODUCTS_QUANTITY = 5
CART_ITEMS_QUANTITY = 5


@given("some cart with items")
def step_impl(context):
    faker = context.faker

    products_infos = []
    other_user_info = create_user(faker)
    user_info = create_user(faker)
    client_user_info = create_user(faker)
    global_category_info = create_category(faker, 'cart_info_global', is_global=True)
    global_category = global_category_info['category']
    user = user_info['user']
    client_user = client_user_info['user']
    other_user = other_user_info['user']

    shop_info = create_shop(faker, user=user, slug_prefix='cart_info_shop')
    other_shop_info = create_shop(faker, user=other_user, slug_prefix='cart_info_other_shop')
    category_info = create_category(faker, slug_prefix='cart_info_global_1', section=global_category, order=1)

    cart = Cart.objects.create(user=client_user)

    for i in range(0, PRODUCTS_QUANTITY):
        products_infos.append(create_product(faker, shop=shop_info['shop'], category=category_info['category'],
                                             slug_prefix='cart_info_products_%s' % i))

    other_product_info = create_product(faker, shop=other_shop_info['shop'], category=category_info['category'],
                                        slug_prefix='cart_info_products_%s' % (PRODUCTS_QUANTITY + 1))

    create_cart_item(user=client_user, product=other_product_info['product'], cart=cart)

    for i in range(0, CART_ITEMS_QUANTITY):
        product_info = random.choice(products_infos)

        create_cart_item(client_user, product=product_info['product'], cart=cart)

    create_order(faker, cart=cart, user=user)

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.cart_id = cart.pk
    context.shop = shop_info['shop']


@when('app sends request to "api_cart_info" url with the cart id')
def step_impl(context):
    context.response = context.client.get(reverse('api:cart_detail_history', kwargs=dict(pk=context.cart_id)),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with the cart items info")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    json_content = response.json()

    context.test.assertEqual(len(json_content['items']), CART_ITEMS_QUANTITY)

    for item in json_content['items']:
        product = Product.objects.get(id=item['product'])
        context.test.assertEqual(product.shop, context.shop)
