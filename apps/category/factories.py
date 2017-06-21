import factory, random, string
from .models import Category
from apps.global_category.factories import GlobalCategoryFactory


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    title = "Some category"
    slug = factory.Sequence(lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(10)]))
    section = factory.SubFactory(GlobalCategoryFactory)
