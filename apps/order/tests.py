from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from apps.cart.factories import CartFactory, CartItemFactory
from apps.product.factories import ProductFactory
from apps.users.tests.factories import UserFactory
from apps.order.factories import SimpleOrderFactory
# Create your tess here.


class OrderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_create_order(self):
        cart = CartFactory()
        product = ProductFactory(price=150)
        CartItemFactory(cart=cart, product=product, quantity=3)
        data = {
            'name': 'Dan',
            'last_name': 'Tynybekov',
            'phone': '05555555',
            'address': 'Chui avenue',
            'cart': cart}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('order:create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.simpleorder_set.count(), 1)
        self.assertEqual(self.user.simpleorder_set.last().name, 'Dan')
