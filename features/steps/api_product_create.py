from behave import *
from features.helpers import *
from django.urls import reverse
from apps.category.models import *
import random

use_step_matcher("re")

LOGIN_URL = reverse('api:rest_login')
PRODUCT_CREATE_URL = reverse('api:product_create')


def do_request(context, faker, shop_slug, category_slug):
    post_data = dict(shop=shop_slug, category=category_slug, published=True,
                     title=faker.name(), price=random.randint(50, 10000), discount=random.randint(0, 99),
                     short_description=faker.text())

    return context.client.post(PRODUCT_CREATE_URL, post_data,
                               **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@given("a user's shop")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    shop_data = create_shop(faker, user_data['user'], slug_prefix='product_create')
    global_category_data = create_category(faker, slug_prefix='product_create_section', is_global=True)
    category_data = create_category(faker, slug_prefix='product_create', is_global=False,
                                    section=global_category_data['category'])

    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])
    context.shop_slug = shop_data['slug']
    context.category_slug = category_data['slug']


@when('app sends request to "api_product_create" url with all required data')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug=context.shop_slug,
                                  category_slug=context.category_slug)


@then("it should get response with success status")
def step_impl(context):
    assert_status_code(context, context.response, 201)
    assert_response_json_keys_exist(context, context.response, ['published', 'short_description',
                                                                'price', 'category', 'title', 'shop',
                                                                'discount'])


@when('app sends request to "api_product_create" url with invalid shop slug')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug='invalid_shop_slug',
                                  category_slug=context.category_slug)


@when('app sends request to "api_product_create" url with invalid category slug')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug=context.shop_slug,
                                  category_slug='invalid_category_slug')