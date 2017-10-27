from behave import *
from django.urls import reverse

from features.helpers import *

use_step_matcher("re")

SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY = 5


@given("prepared subcategory with children categories")
def step_impl(context):
    faker = context.faker

    global_category_data = create_category(faker, slug_prefix='category_children', is_global=True)
    global_category = global_category_data['category']

    subcategory_data = create_category(faker, slug_prefix='subcategory', section=global_category)
    subcategory = subcategory_data['category']

    for i in range(0, SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY):
        create_category(faker, section=global_category, slug_prefix='subcategory_with_parent_%s' % i, order=i,
                        parent_category=subcategory)

    context.subcategory_slug = subcategory_data['slug']


@when('app sends request to "api_category_children" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:category_children', kwargs={'slug': context.subcategory_slug}))


@then("it should get response with list of given subcategory's children categories")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    items = response.json()
    context.test.assertEqual(len(items), SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY)
