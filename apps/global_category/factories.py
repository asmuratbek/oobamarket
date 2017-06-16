import factory
from django.core.files.base import ContentFile

from .models import GlobalCategory


class GlobalCategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = GlobalCategory

    title = "Some global category"
    slug = 'some-global-category'
    icon = factory.LazyAttribute(lambda _: ContentFile(factory.django.ImageField()._make_data(
                                    {'width': 300, 'height': 250}
                                ), 'some_icon.jpg'))

