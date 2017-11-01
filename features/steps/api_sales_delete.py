from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some sale of a shop we want to delete")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='sales_update_get_info_')
    shop_info = instances['shop_info']
    user_info = instances['user_info']
    sale_info = create_sales(faker, shop=shop_info['shop'])
    sale = sale_info['sale']

    context.shop_slug = shop_info['slug']
    context.sale_id = sale.id
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_sales_delete" url with the shop slug and the sale id')
def step_impl(context):
    context.response = context.client.post(reverse('api:shop_sales_delete', kwargs=dict(slug=context.shop_slug,
                                                                                          pk=context.sale_id)),
                                             **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with sale delete success status")
def step_impl(context):
    context.test.assertIsNone(Sales.objects.filter(id=context.sale_id).first())
