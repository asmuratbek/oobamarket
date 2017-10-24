from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse
import random

use_step_matcher("re")

SHOP_REVIEWS_QUANTITY = 10
USERS_QUANTITY = 5


@given("some shop with users' reviews")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_sales')
    shop_info = instances['shop_info']
    shop = shop_info['shop']
    users_infos = []

    for i in range(0, USERS_QUANTITY):
        users_infos.append(create_user(faker))

    for i in range(0, SHOP_REVIEWS_QUANTITY):
        user = random.choice(users_infos)['user']
        create_review(faker, user=user, shop=shop)

    context.shop_slug = shop_info['slug']


@when('app sends request to "api_shop_reviews" url with the shop slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_reviews', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with list of all reviews")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['reviews', 'status'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 'success')
    context.test.assertEqual(len(json_content['reviews']), SHOP_REVIEWS_QUANTITY)

    for item in json_content['reviews']:
        context.test.assertTrue(dict_has_keys(['user', 'text', 'stars'], item))