import factory
from .models import Category
from apps.global_category.factories import GlobalCategoryFactory


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    # parent = factory.SubFactory('CategoryFactory')
    title = "Some category"
    slug = "some-category"
    section = factory.SubFactory(GlobalCategoryFactory)
