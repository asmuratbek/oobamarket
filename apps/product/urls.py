from django.conf.urls import url
from .views import product_detail, FavoriteCreateView, ProductCreateView, ProductUpdateView

urlpatterns = [
    url(r'^$', product_detail, name='product_detail'),
    url(r'^(?P<slug>[\w-]+)/add-product/$', ProductCreateView.as_view(), name='add_product'),
    url(r'^(?P<slug>[\w-]+)/update-product/$', ProductUpdateView.as_view(), name='update_product'),
]
