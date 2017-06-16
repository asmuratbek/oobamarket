import factory, uuid
from .models import Product
from apps.shop.factories import ShopFactory
from apps.category.factories import CategoryFactory


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    shop = factory.SubFactory(ShopFactory)
    category = factory.SubFactory(CategoryFactory)
    title = 'Some product'
    slug = factory.Sequence(lambda r: str(uuid.uuid4()))
