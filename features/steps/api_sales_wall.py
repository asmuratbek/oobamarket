from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse
import random
from apps.users.models import *

use_step_matcher("re")

SHOPS_QUANTITY = 2
SALES_QUANTITY = 10


@given("some user following a few shops")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='sales_wall_')
    user_info = instances['user_info']
    user = user_info['user']
    shops_infos = []

    for i in range(0, SHOPS_QUANTITY):
        shop_info = create_shop(faker, user=user, slug_prefix='shop_with_sales_%s' % i)

        shops_infos.append(shop_info)
        Subscription.objects.create(user=user, subscription=shop_info['shop'])

    for i in range(0, SALES_QUANTITY):
        shop = random.choice(shops_infos)['shop']
        create_sales(faker, shop=shop)

    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_sales_wall" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:lenta'),
                                          **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with list of last sales of the shops")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count'])
    json_content = response.json()

    context.test.assertEqual(json_content['count'], SALES_QUANTITY)
