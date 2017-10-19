from behave import *
from apps.shop.models import *
from django.urls import reverse
from features.helpers import *

use_step_matcher("re")

PLACES_COUNT = 5
PLACES_LIST_URL = reverse('api:place_list')
MALL_TYPE = 'mall'
MARKET_TYPE = 'market'


@given("prepared set of places \(malls/markets\)")
def step_impl(context):
    faker = context.faker

    for i in range(0, PLACES_COUNT):
        Place.objects.create(title=faker.name()[0], type=MALL_TYPE if i % 2 == 0 else MARKET_TYPE)


@when('app sends request to "api_places_list" url')
def step_impl(context):
    context.response = context.client.get(PLACES_LIST_URL)


@then("it should get response with list of places")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    items = response.json()

    context.test.assertEqual(len(items), PLACES_COUNT)

    for item in items:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'ttype'], item))