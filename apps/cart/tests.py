import json
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from apps.product.factories import ProductFactory
from .factories import CartFactory, CartItemFactory


class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart = CartFactory()

    def test_should_return_cart_if_item_is_null(self):
        cart_session = self.client.session
        cart_session['cart_id'] = self.cart.id
        cart_session.save()
        response = self.client.get(reverse('cart:detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.cart)

    def test_should_add_item_if_called_item(self):
        cart_session = self.client.session
        cart_session['cart_id'] = self.cart.id
        cart_session.save()
        product = ProductFactory(price=150)
        data = {'item': product.id, 'delete': False, 'qty': 1}
        response = self.client.get(reverse('cart:detail'), data=data,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['id'], product.id)

    def test_should_remove_item_if_delete_true(self):
        cart_session = self.client.session
        cart_session['cart_id'] = self.cart.id
        cart_session.save()
        product = ProductFactory(price=150)
        data = {'item': product.id, 'delete': True, 'qty': 0}
        response = self.client.get(reverse('cart:detail'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['total_items'], 0)
