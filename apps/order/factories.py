import factory
from apps.users.tests.factories import UserFactory
from apps.cart.factories import CartFactory
from apps.order.models import SimpleOrder


class SimpleOrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = SimpleOrder

    phone = "055555555"
    address = "Chui avenue"
    cart = factory.SubFactory(CartFactory)
    user = factory.SubFactory(UserFactory)
