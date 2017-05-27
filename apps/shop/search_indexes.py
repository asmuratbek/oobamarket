from haystack import indexes
from apps.shop.models import Shop


class ShopIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    get_products_count = indexes.CharField(model_attr='get_products_count')
    get_logo = indexes.CharField(model_attr='get_logo')
    get_absolute_url = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Shop
