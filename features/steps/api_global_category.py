from behave import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from apps.global_category.models import GlobalCategory
import os
from features.helpers import *

use_step_matcher("re")

GLOBAL_CATEGORIES_QUANTITY = 5


@given("prepared set of global categories")
def step_impl(context):
    img = SimpleUploadedFile(name='category.png', content=open('%s/../assets/category_icon.png' % os.path.dirname(os.path.abspath(__file__)), 'rb').read(),
                             content_type='image/png')

    for _ in range(0, GLOBAL_CATEGORIES_QUANTITY):
        title = context.faker.name()
        category = GlobalCategory.objects.create(title=title, slug='slug_%s' % context.faker.words()[0], icon=img)
        category.save()


@when('app sends request to "api_global_category" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:globalcategory_list'))


@then("it should get response with list of global categories")
def step_impl(context):
    response = context.response

    assert_status_code_and_content_type(context, response, 200, 'application/json')

    items = response.json()
    context.test.assertEqual(len(items), GLOBAL_CATEGORIES_QUANTITY)

    for item in items:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'slug', 'icon'], item))