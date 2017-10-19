from behave import *
from features.helpers import *
from apps.shop.models import *

from django.urls import reverse

use_step_matcher("re")


@given("a shop")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    user = user_data['user']

    title = faker.name()[0]
    slug = 'slug_%s' % title
    short_description = 'some description'

    shop = Shop.objects.create(title=title, email=faker.email(), short_description=short_description, slug=slug)
    shop.user = [user]
    shop.save()

    context.shop_slug = slug


@when('app sends request to "api_shop_info" url containing a slug of the shop')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop-detail', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with an information of the shop")
def step_impl(context):
    assert_status_code(context, context.response, 200)
    assert_response_json_keys_exist(context, ['is_owner', 'logo', 'title', 'description', 'is_subscribed',
                                              'short_description', 'slug'])


@when('app sends request to "api_shop_info" url containing non-existing slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop-detail', kwargs=dict(slug='slug_unknown')))


@then("it should get 404 error code")
def step_impl(context):
    assert_status_code(context, context.response, 404)