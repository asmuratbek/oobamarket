import factory, random, string
from .models import Properties, Values
from apps.category.factories import CategoryFactory


class PropetiesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Properties

    title = "Some property"
    slug = factory.Sequence(lambda r: ''.join([random.choice(string.ascii_lowercase) for i in range(10)]))


class ValueFactory(factory.DjangoModelFactory):
    class Meta:
        model = Values

    properties = factory.SubFactory(PropetiesFactory)
    value = "Some value"

