
from haystack import indexes
from apps.product.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    price = indexes.CharField(model_attr='price')
    get_shop_title = indexes.CharField(model_attr='get_shop_title')
    get_main_image = indexes.CharField(model_attr='get_main_image')
    get_absolute_url = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Product
