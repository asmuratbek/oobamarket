import factory,random, string
from django.core.files.base import ContentFile

from .models import Product, ProductImage
from apps.shop.factories import ShopFactory
from apps.category.factories import CategoryFactory


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    shop = factory.SubFactory(ShopFactory)
    category = factory.SubFactory(CategoryFactory)
    title = 'Some product'
    slug = factory.Sequence(lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(10)]))


class ProductImageFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.LazyAttribute(lambda _: ContentFile(factory.django.ImageField()._make_data(
                                    {'width': 500, 'height': 350}
                                ), 'some_image.jpg'))
