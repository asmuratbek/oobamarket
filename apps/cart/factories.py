import factory
from .models import Cart, CartItem
from apps.users.tests.factories import UserFactory
from apps.product.factories import ProductFactory


class CartFactory(factory.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
