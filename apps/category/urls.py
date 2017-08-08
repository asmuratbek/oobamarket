from django.conf.urls import url, include
from apps.category.views import category_detail, get_category_from_global_category, get_subcategory_from_category, \
    get_category, get_product_by_filter, get_property_list
from apps.global_category.views import GlobalDetailView

urlpatterns = [
    url(r'^get_category_list', get_category_from_global_category, name="category_list_ajax"),
    url(r'^get-category', get_category, name='get-category'),
    url(r'^get_subcategory_list', get_subcategory_from_category, name="subcategory_list_ajax"),
    url(r'^get_property_list', get_property_list, name="property_list_ajax"),
    url(r'^get_product', get_product_by_filter, name='filter_detail'),
    url(r'^(?P<global_slug>[\w-]+)/(?P<category_slug>[.\w-]+)/(?P<slug>[\w-]+)/', include('apps.product.urls')),
    url(r'^(?P<global_slug>[\w-]+)/(?P<slug>[.\w-]+)/$', category_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', GlobalDetailView.as_view(), name='global_detail'),


]
