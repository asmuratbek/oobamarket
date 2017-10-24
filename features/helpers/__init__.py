__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress

from apps.shop.models import *
from apps.category.models import *
from apps.cart.models import *
from apps.global_category.models import *
from apps.product.models import *

import random


def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True


def assert_status_code(context, response, status_code):
    context.test.assertEqual(response['Content-Type'], 'application/json')
    context.test.assertEqual(response.status_code, status_code)


def assert_response_json_keys_exist(context, response, keys):
    json_content = response.json()

    context.test.assertTrue(dict_has_keys(keys, json_content))


def create_user(faker):
    username = faker.name()[0]
    email = '%s@somemail.com' % username
    password = '%s_password' % username

    user = get_user_model().objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    email_address = EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

    return dict(user=user, email_address=email_address, username=username, email=email, password=password)


def create_shop(faker, user=None, slug_prefix='', default_title=None):
    title = default_title if default_title is not None else faker.name()[0]
    slug = '%s_slug_%s' % (slug_prefix, title)
    short_description = 'some description'

    shop = Shop.objects.create(title=title, email=faker.email(), short_description=short_description, slug=slug)

    if user is not None:
        shop.user = [user]
        shop.save()

    return dict(title=title, slug=slug, short_description=short_description, shop=shop)


def create_category(faker, slug_prefix='', order=0, section=None, parent_category=None, is_global=False):
    title = faker.name()[0]
    slug = '%s_slug_%s' % (slug_prefix, title)

    if is_global:
        category = GlobalCategory.objects.create(title=title, slug=slug)
    else:
        category = Category.objects.create(title=title, slug=slug, section=section, parent=parent_category, order=order)

    return dict(title=title, slug=slug, category=category)


def create_product(faker, shop, category, slug_prefix=''):
    title = faker.name()[0]
    slug = '%s_product_slug_%s' % (slug_prefix, title)
    price = random.randint(50, 10000)
    discount = random.randint(0, 80)

    product = Product.objects.create(title=title, slug=slug, price=price, partner_price=price, discount=discount,
                                     shop=shop, category=category)

    return dict(title=title, slug=slug, price=price, discount=discount, product=product)


def create_instances(faker, slug_prefix=''):
    global_category_info = create_category(faker, slug_prefix='%s_add_to_cart_global_' % slug_prefix, is_global=True)
    category_info = create_category(faker, slug_prefix='%s_add_to_cart_' % slug_prefix, section=global_category_info['category'])
    user_info = create_user(faker)
    shop_info = create_shop(faker, user=user_info['user'], slug_prefix='%s_add_to_cart_' % slug_prefix)
    product_info = create_product(faker, shop=shop_info['shop'],
                                  category=category_info['category'],
                                  slug_prefix='%s_add_to_cart_' % slug_prefix)

    return dict(category_info=category_info, user_info=user_info, shop_info=shop_info,
                product_info=product_info, global_category_info=global_category_info)


def create_cart_item(user, product, cart=None):
    if cart is None:
        cart = Cart.objects.create(user=user)

    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    return dict(cart=cart, cart_item=cart_item)


def create_favorite_product(user, product):
    FavoriteProduct.objects.create(user=user, product=product)


def do_request_to_login(context, url, email, password):
    return context.client.post(url, {
        'email': email, 'password': password
    })


def login_and_get_auth_token(context, url, email, password):
    response = do_request_to_login(context, url, email, password)

    assert_status_code(context, response, 200)
    json_content = response.json()

    if 'key' not in json_content:
        raise Exception('login action failed')

    return json_content['key']