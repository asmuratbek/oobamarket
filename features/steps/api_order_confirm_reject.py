from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some order of a shop which is going to be confirmed/rejected")
def step_impl(context):
    faker = context.faker

    user_info = create_user(faker)
    shop_info = create_shop(faker, user=user_info['user'], slug_prefix='order_confirm_reject_shop_')
    cart_info = create_cart(user=user_info['user'])
    global_category_info = create_category(faker, 'order_confirm_reject_global', is_global=True)
    global_category = global_category_info['category']
    category_info = create_category(faker, slug_prefix='order_confirm_reject_global_1', section=global_category, order=1)
    product_info = create_product(faker, shop=shop_info['shop'], category=category_info['category'])
    shop = shop_info['shop']
    cart = cart_info['cart']

    create_order(faker, cart_info['cart'], user_info['user'])
    create_cart_item(user=user_info['user'], product=product_info['product'], cart=cart)

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.cart_id = cart.pk
    context.shop_slug = shop.slug


@when('app sends request to "api_order_confirm_reject" with the order\'s cart id, the shop slug and confirm action')
def step_impl(context):
    context.response = context.client.post(reverse('api:cart_detail_history', kwargs=dict(pk=context.cart_id)),
                                           dict(flag='shop', action='confirm', shop=context.shop_slug),
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with success status and shop should be in confirmed shops list of the order")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    cart = Cart.objects.get(pk=context.cart_id)
    shop = Shop.objects.get(slug=context.shop_slug)

    context.test.assertTrue(shop in cart.simpleorder.confirm_shops.all())


@when('app sends request to "api_order_confirm_reject" with the order\'s cart id, the shop slug and reject action')
def step_impl(context):
    context.response = context.client.post(reverse('api:cart_detail_history', kwargs=dict(pk=context.cart_id)),
                                           dict(flag='shop', action='reject', shop=context.shop_slug),
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with success status and shop should be in rejected shops list of the order")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    cart = Cart.objects.get(pk=context.cart_id)
    shop = Shop.objects.get(slug=context.shop_slug)

    context.test.assertTrue(shop in cart.simpleorder.rejected_shops.all())
