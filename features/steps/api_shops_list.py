from behave import *
from apps.shop.models import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

MALL_TYPE = 'mall'
MARKET_TYPE = 'market'
SHOPS_WITH_SAME_TITLE_QUANTITY = 2
SHOPS_IN_MALL_QUANTITY = 1
SHOP_TITLE_TEMPLATE = 'MyShop_%s'
KEYWORD = 'my'
SHOPS_LIST_URL = reverse('api:shop_list')


def assert_json_response(context, json_result, results_quantity):
    results = json_result['results']

    context.test.assertEqual(len(results), results_quantity)

    for item in results:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'slug', 'user', 'email',
                                               'phone', 'places', 'is_authenticated',
                                               'is_subscribed', 'is_owner', 'description',
                                               'short_description', 'created_at',
                                               'updated_at', 'logo', 'get_absolute_url'], item))


@given("prepared set of shops")
def step_impl(context):
    faker = context.faker
    place = Place.objects.create(title=faker.name()[0], type=MALL_TYPE)

    user_data = create_user(faker)
    user = user_data['user']

    for i in range(0, SHOPS_WITH_SAME_TITLE_QUANTITY):
        title = SHOP_TITLE_TEMPLATE % i
        slug = 'slug_%s_%s' % (title, i)
        short_description = 'some description'

        shop = Shop.objects.create(title=title, email=faker.email(), short_description=short_description, slug=slug)
        shop.user = [user]
        shop.save()

    mall_shop_title = faker.name()[0]
    mall_shop_slug = 'slug_mall_%s' % mall_shop_title

    shop_in_mall = Shop.objects.create(title=mall_shop_title, email=faker.email(), short_description='',
                                       slug=mall_shop_slug)

    Contacts.objects.create(shop=shop_in_mall, place=place)

    context.place_id = place.id


@when('app sends request to "api_shops_list" url with keyword param')
def step_impl(context):
    context.response = context.client.get(SHOPS_LIST_URL, dict(q=KEYWORD))


@then("it should get response with list of shops, matching keyword query")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    assert_json_response(context, response.json(), SHOPS_WITH_SAME_TITLE_QUANTITY)


@when('app sends request to "api_shops_list" url with place param')
def step_impl(context):
    context.response = context.client.get(SHOPS_LIST_URL, dict(place=context.place_id))


@then("it should get response with list of shops, which belong to given place")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['count', 'next', 'previous', 'results'])
    assert_json_response(context, response.json(), SHOPS_IN_MALL_QUANTITY)
