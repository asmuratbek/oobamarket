from behave import *
from features.helpers import *

from django.urls import reverse

use_step_matcher("re")


@given("a shop")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    user = user_data['user']

    shop_data = create_shop(faker, user=user)
    context.shop_slug = shop_data['slug']


@when('app sends request to "api_shop_info" url containing a slug of the shop')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop-detail', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with an information of the shop")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['is_owner', 'logo', 'title', 'description', 'is_subscribed',
                                              'short_description', 'slug'])


@when('app sends request to "api_shop_info" url containing non-existing slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop-detail', kwargs=dict(slug='slug_unknown')))