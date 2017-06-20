import json

from django.http import HttpResponseBadRequest
from django.test import TestCase, Client
from django.urls import reverse

from .factories import CategoryFactory
from apps.global_category.factories import GlobalCategoryFactory
from apps.users.models import User
from apps.users.tests.factories import UserFactory
# Create your tests here.


class CategoriesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = CategoryFactory()
        self.user = User.objects.create_superuser('admin', 'admin@mail.ru', 'password')

    def test_should_return_404_if_called_without_value(self):
        response = self.client.get(reverse('categories:property_list_ajax'))
        self.assertEqual(response.status_code, 404)

    def test_should_return_default_global_category_if_value_doesnt_exist(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('categories:get-category'), data={'cat_id': 1234})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['cat_null'], True)

    def test_should_return_default_global_category_if_value_is_not_valid(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('categories:get-category'), data={'cat_id': 'some-str'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['cat_null'], True)

    def test_should_return_bad_request_if_user_is_not_admin(self):
        user = UserFactory()
        self.client.login(username=user.username, password='password')
        response = self.client.get(reverse('categories:get-category'), data={'cat_id': self.category.id})
        self.assertEqual(response.status_code, 400)
