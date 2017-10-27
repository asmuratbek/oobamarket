from behave import *
from django.urls import reverse

from features.helpers import *

use_step_matcher("re")

GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY = 5


@given("prepared global category with children categories")
def step_impl(context):
    faker = context.faker

    global_category_data = create_category(faker, slug_prefix='gc_children', is_global=True)
    global_category = global_category_data['category']

    for i in range(0, GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY):
        create_category(faker, slug_prefix='child_slug_%s' % i, section=global_category, order=i)

    context.global_category_slug = global_category_data['slug']


@when('app sends request to "api_global_category_children" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:globalcategory_children', kwargs={'slug': context.global_category_slug}))


@then("it should get response with list of children categories")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    items = response.json()
    context.test.assertEqual(len(items), GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY)