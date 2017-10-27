from behave import *
from features.helpers import *
from django.urls import reverse
from apps.cart.models import *
from features.steps import LOGIN_URL

use_step_matcher("re")


@given("a product which user wants to add to cart")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='prefix_one')
    user_info = instances['user_info']
    product_info = instances['product_info']

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.product_slug = product_info['slug']
    context.user = user_info['user']
    context.product = product_info['product']


@when('app sends request to "api_add_to_cart" url with given product slug')
def step_impl(context):
    context.response = context.client.post(reverse('api:product_add_to_cart', kwargs=dict(slug=context.product_slug)),
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with info that product is added to cart")
def step_impl(context):
    assert_status_code(context, context.response, 200)

    cart = Cart.objects.filter(user=context.user).first()
    cart_item = CartItem.objects.filter(cart=cart, product=context.product).first()

    context.test.assertIsNotNone(cart_item)


@given("a product which already added to cart")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='prefix_one')
    user_info = instances['user_info']
    product_info = instances['product_info']

    cart_item_info = create_cart_item(user_info['user'], product_info['product'])
    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    cart = cart_item_info['cart']

    context.auth_token = auth_token
    context.product_slug = product_info['slug']
    context.product = product_info['product']
    context.cart = cart

    context.test.assertIsNotNone(CartItem.objects.filter(cart=cart, product=product_info['product']).first())


@then("it should get response with info that product is removed from cart")
def step_impl(context):
    assert_status_code(context, context.response, 200)
    context.test.assertIsNone(CartItem.objects.filter(cart=context.cart, product=context.product).first())