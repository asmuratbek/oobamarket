from behave import *
from django.urls import reverse
from apps.global_category.models import GlobalCategory
from features.helpers import *

use_step_matcher("re")

GLOBAL_CATEGORIES_QUANTITY = 5


@given("prepared set of global categories")
def step_impl(context):
    for _ in range(0, GLOBAL_CATEGORIES_QUANTITY):
        title = context.faker.name()
        GlobalCategory.objects.create(title=title, slug='slug_%s' % context.faker.words()[0])


@when('app sends request to "api_global_category" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:globalcategory_list'))


@then("it should get response with list of global categories")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    items = response.json()
    context.test.assertEqual(len(items), GLOBAL_CATEGORIES_QUANTITY)

    for item in items:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'slug', 'icon'], item))