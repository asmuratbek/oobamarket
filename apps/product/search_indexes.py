from haystack import indexes

from apps.product.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    pk = indexes.IntegerField(model_attr='pk')
    title = indexes.FacetCharField(model_attr='title')
    slug = indexes.CharField(model_attr='slug')
    get_price_function = indexes.FacetIntegerField(model_attr='get_price')
    created_at = indexes.DateField(model_attr='created_at')
    category_title = indexes.CharField(model_attr='get_category_title')
    category_id = indexes.FacetIntegerField(model_attr='get_category_id')
    category_slug = indexes.CharField(model_attr='get_category_slug')
    parent_category_slug = indexes.CharField(model_attr='get_parent_category_slug')
    parent_category_id = indexes.CharField(model_attr='get_parent_category_id')
    global_slug = indexes.CharField(model_attr='get_global_slug')
    published = indexes.BooleanField(model_attr='published')
    currency = indexes.CharField(model_attr='currency')
    shop = indexes.CharField(model_attr='get_shop_title')
    shop_slug = indexes.CharField(model_attr='get_shop_slug')
    short_description = indexes.CharField(model_attr='short_description')
    get_shop_url = indexes.CharField(model_attr='get_shop_url')
    main_image = indexes.CharField(model_attr='get_main_image')
    detail_view = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Product
