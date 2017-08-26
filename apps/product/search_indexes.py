from haystack import indexes
from apps.product.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    get_price_function = indexes.CharField(model_attr='get_price')
    created_at = indexes.DateField(model_attr='created_at')
    category_title = indexes.CharField(model_attr='get_category_title')
    published = indexes.BooleanField(model_attr='published')
    currency = indexes.CharField(model_attr='currency')
    get_shop_title = indexes.CharField(model_attr='get_shop_title')
    get_shop_url = indexes.CharField(model_attr='get_shop_url')
    main_image = indexes.CharField(model_attr='get_main_image')
    get_absolute_url = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Product
