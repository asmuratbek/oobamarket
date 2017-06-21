import factory, random, string
from .models import Shop


class ShopFactory(factory.DjangoModelFactory):
    class Meta:
        model = Shop

    title = "Some shop"
    slug = factory.Sequence(lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(10)]))
    phone = "05552222444"
    email = "someshop@email.com"
    short_description = 'Some text'
    description = 'Some description'
