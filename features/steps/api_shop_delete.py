from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some shop we want to delete")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_delete_')
    shop_info = instances['shop_info']
    user_info = instances['user_info']
    shop = shop_info['shop']

    context.shop_id = shop.id
    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_shop_delete" url with the shop slug')
def step_impl(context):
    context.response = context.client.delete(reverse('api:shop_delete', kwargs=dict(slug=context.shop_slug)),
                                             **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with shop delete success status")
def step_impl(context):
    context.test.assertIsNone(Shop.objects.filter(id=context.shop_id).first())