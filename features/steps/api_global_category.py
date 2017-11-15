from behave import *
from django.urls import reverse
from features.helpers import *

use_step_matcher("re")

GLOBAL_CATEGORIES_QUANTITY = 5


@given("prepared set of global categories")
def step_impl(context):
    for i in range(0, GLOBAL_CATEGORIES_QUANTITY):
        create_category(context.faker, slug_prefix='global_category_%s' % i, is_global=True)

    GlobalCategory.objects.create(title='global_category_hidden', slug='global_category_slug_hidden', hidden=True)


@when('app sends request to "api_global_category" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:globalcategory_list'))


@then("it should get response with list of global categories")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    items = response.json()
    context.test.assertEqual(len(items), GLOBAL_CATEGORIES_QUANTITY)
