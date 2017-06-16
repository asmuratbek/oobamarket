import factory, random, string
from .models import Shop


class ShopFactory(factory.DjangoModelFactory):
    class Meta:
        model = Shop

    title = "Some shop"
    slug = "some-shop"
    phone = "05552222444"
    email = "someshop@email.com"
    short_description = 'Some text'
    description = 'Some description'
