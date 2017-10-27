from behave import *
from django.urls import reverse
from features.steps import *
from features.helpers import *

use_step_matcher("re")

PRODUCT_NEW_QUANTITY = 5


@given("a product in user's cart")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='prefix_one')
    user_info = instances['user_info']
    product_info = instances['product_info']

    cart_item_info = create_cart_item(user_info['user'], product_info['product'])
    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.product_slug = product_info['slug']
    context.product = product_info['product']
    context.cart = cart_item_info['cart']


@when('app sends request to "api_product_quantity_change_in_cart" url with quantity value')
def step_impl(context):
    context.response = context.client.post(
        reverse('api:product_change_quantity_in_cart',
                kwargs=dict(slug=context.product_slug)), dict(quantity=PRODUCT_NEW_QUANTITY),
        **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with success message and new total sum value")
def step_impl(context):
    assert_status_code(context, context.response, 200)

    cart_item = CartItem.objects.filter(cart=context.cart, product=context.product).first()

    context.test.assertIsNotNone(cart_item)
    context.test.assertEqual(cart_item.quantity, PRODUCT_NEW_QUANTITY)
