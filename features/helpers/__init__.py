from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress

from apps.shop.models import *
from apps.category.models import *
from apps.cart.models import *
from apps.global_category.models import *
from apps.product.models import *
from apps.reviews.models import *

import random

REVIEWS_STARS = ['*', '**', '***', '****', '*****']


def dict_has_keys(keys, dict):
    non_existing_keys = []

    for k in keys:
        if k not in dict:
            non_existing_keys.append(k)

    if len(non_existing_keys) > 0:
        raise Exception('keys %s dont exist in dict' % non_existing_keys)

    return True


def assert_status_code(context, response, status_code):
    context.test.assertEqual(response['Content-Type'], 'application/json')
    context.test.assertEqual(response.status_code, status_code)


def assert_response_json_keys_exist(context, response, keys):
    context.test.assertTrue(dict_has_keys(keys, response.json()))


def create_user(faker, username_prefix=''):
    username = '%s_%s' % (faker.words()[0].replace(' ', '_'), username_prefix)
    email = '%s@somemail.com' % username
    password = '%s_password' % username

    user = get_user_model().objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    email_address = EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

    return dict(user=user, email_address=email_address, username=username, email=email, password=password)


def create_shop(faker, user=None, slug_prefix='', default_title=None, logo=None):
    title = default_title if default_title is not None else faker.words()[0]
    slug = '%s_slug_%s' % (slug_prefix, title.replace(' ', '_'))
    short_description = 'some description'

    params = dict(title=title, email=faker.email(), short_description=short_description, slug=slug)

    if logo is not None:
        params['logo'] = logo

    shop = Shop.objects.create(**params)

    if user is not None:
        shop.user = [user]
        shop.save()

    return dict(title=title, slug=slug, short_description=short_description, shop=shop)


def create_category(faker, slug_prefix='', order=0, section=None, parent_category=None, is_global=False):
    title = faker.words()[0]
    slug = '%s_slug_%s' % (slug_prefix, title.replace(' ', '_'))

    if is_global:
        category = GlobalCategory.objects.create(title=title, slug=slug)
    else:
        category = Category.objects.create(title=title, slug=slug, section=section, parent=parent_category, order=order)

    return dict(title=title, slug=slug, category=category)


def create_product(faker, shop, category, slug_prefix='', title_prefix=''):
    title = '%s %s' % (title_prefix, faker.words()[0])
    slug = '%s_product_slug_%s' % (slug_prefix, title.replace(' ', '_'))
    price = random.randint(50, 10000)
    discount = random.randint(0, 80)

    product = Product.objects.create(title=title, slug=slug, price=price, partner_price=price, discount=discount,
                                     shop=shop, category=category)

    return dict(title=title, slug=slug, price=price, discount=discount, product=product)


def create_contacts(faker, shop):
    Contacts.objects.create(address=faker.text(), phone=faker.text(), shop=shop)


def create_instances(faker, slug_prefix='', shop_logo=None):
    global_category_info = create_category(faker, slug_prefix=slug_prefix, is_global=True)
    parent_category_info = create_category(faker, slug_prefix='%s_parent_' % slug_prefix,
                                           section=global_category_info['category'])
    category_info = create_category(faker, slug_prefix=slug_prefix, section=global_category_info['category'],
                                    parent_category=parent_category_info['category'])
    user_info = create_user(faker)
    shop_info = create_shop(faker, user=user_info['user'], slug_prefix=slug_prefix, logo=shop_logo)
    product_info = create_product(faker, shop=shop_info['shop'],
                                  category=category_info['category'],
                                  slug_prefix=slug_prefix)

    return dict(category_info=category_info, user_info=user_info, shop_info=shop_info,
                product_info=product_info, global_category_info=global_category_info)


def create_cart_item(user, product, cart=None):
    if cart is None:
        cart = Cart.objects.create(user=user)

    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    return dict(cart=cart, cart_item=cart_item)


def create_cart(user):
    Cart.objects.create(user=user)


def create_favorite_product(user, product):
    FavoriteProduct.objects.create(user=user, product=product)


def create_sales(faker, shop, image=None):
    title = faker.words()[0]
    description = faker.words()

    sale = Sales.objects.create(title=title, short_description=description, description=description,
                                shop=shop, image=image)

    return dict(sale=sale)


def create_review(faker, user, shop=None, product=None):
    text = faker.text()
    stars = random.choice(REVIEW_STARS)

    if shop is not None:
        ShopReviews.objects.create(text=text, stars=stars, user=user, shop=shop)
    elif product is not None:
        ProductReviews.objects.create(text=text, stars=stars, user=user, product=product)
    else:
        raise Exception("Please provide shop or product instance")


def create_site_for_social_app(domain, name):
    site = Site.objects.create(domain=domain, name=name)

    return dict(site=site)


def create_social_app(provider, name, client_id, secret, site):
    social_app = SocialApp.objects.create(provider=provider, name=name, client_id=client_id,
                                          secret=secret)

    social_app.sites.add(site)
    social_app.save()

    return dict(social_app=social_app)


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
