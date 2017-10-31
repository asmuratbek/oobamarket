from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

FAVORITE_PRODUCTS_QUANTITY = 5
PRODUCTS_QUANTITY = 5


@given("some user having set of shops, favorite products and cart items")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='my_list_')
    user_info = instances['user_info']
    user = user_info['user']

    other_user = create_user(faker, username_prefix='other_user_')['user']
    other_shop = create_shop(faker, user=other_user, slug_prefix='my_list_other_shop_')['shop']

    category = instances['category_info']['category']
    products_infos = []

    for i in range(0, PRODUCTS_QUANTITY):
        products_infos.append(create_product(faker, shop=other_shop, category=category, slug_prefix='my_list_%s' % i))

    for i in range(0, FAVORITE_PRODUCTS_QUANTITY):
        product = random.choice(products_infos)['product']
        create_favorite_product(user=user, product=product)


    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_my_list" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:my_list'),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with the info listed above")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)