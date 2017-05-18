from django.conf.urls import url, include

from .views import product_detail, ProductCreateView, ProductUpdateView, ProductIndexCreateView

urlpatterns = [
    url(r'^$', product_detail, name='product_detail'),
    url(r'^api/', include('apps.product.api.urls')),
    url(r'^add-product/$', ProductIndexCreateView.as_view(), name='add_product_index'),
    url(r'^(?P<slug>[\w-]+)/add-product/$', ProductCreateView.as_view(), name='add_product'),
    url(r'^(?P<slug>[\w-]+)/update-product/$', ProductUpdateView.as_view(), name='update_product'),
]
