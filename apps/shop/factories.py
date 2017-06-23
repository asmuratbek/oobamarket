import factory, random, string
from django.core.files.base import ContentFile

from .models import Shop, Banners, SocialLinks


class ShopFactory(factory.DjangoModelFactory):
    class Meta:
        model = Shop

    title = "Some shop"
    slug = factory.Sequence(lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(10)]))
    phone = "05552222444"
    email = "someshop@email.com"
    short_description = 'Some text'
    description = 'Some description'


class BannerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Banners

    image = factory.LazyAttribute(lambda _: ContentFile(factory.django.ImageField()._make_data(
                                    {'width': 500, 'height': 350}
                                ), 'some_banner.jpg'))
    shop = factory.SubFactory(ShopFactory)


class SocialLinksFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialLinks

    shop = factory.SubFactory(ShopFactory)
