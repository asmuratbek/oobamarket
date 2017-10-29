from behave import *
from features.helpers import *
from django.urls import reverse
from apps.category.models import *
import random
from features.steps import IMAGE_ASSET_PATH
from features.steps import LOGIN_URL

use_step_matcher("re")

PRODUCT_CREATE_URL = reverse('api:product_create')


def do_request(context, faker, shop_slug, category_slug, image_path=None):
    image = None
    post_data = dict(shop=shop_slug, category=category_slug, published=True,
                     title=faker.name(), price=random.randint(50, 10000), discount=random.randint(0, 99),
                     short_description=faker.text())

    if image_path is not None:
        image = open(image_path, 'rb')
        post_data['images_files'] = [image]

    response = context.client.post(PRODUCT_CREATE_URL, post_data,
                                   **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))

    if image is not None:
        image.close()

    return response


@given("a user's shop")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_create_')
    user_data = instances['user_info']
    shop_data = instances['shop_info']
    category_data = instances['category_info']

    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])
    context.shop_slug = shop_data['slug']
    context.category_slug = category_data['slug']


@when('app sends request to "api_product_create" url with all required data')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug=context.shop_slug,
                                  category_slug=context.category_slug, image_path=IMAGE_ASSET_PATH)


@then("it should get response with success status")
def step_impl(context):
    assert_status_code(context, context.response, 201)


@when('app sends request to "api_product_create" url with invalid shop slug')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug='invalid_shop_slug',
                                  category_slug=context.category_slug, image_path=IMAGE_ASSET_PATH)


@when('app sends request to "api_product_create" url with invalid category slug')
def step_impl(context):
    context.response = do_request(context, context.faker, shop_slug=context.shop_slug,
                                  category_slug='invalid_category_slug', image_path=IMAGE_ASSET_PATH)
