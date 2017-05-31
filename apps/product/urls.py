from django.conf.urls import url, include

from .views import product_detail, ProductCreateView, ProductUpdateView, ProductIndexCreateView, upload_images, \
    remove_uploaded_image, ProductDeleteView, change_publish_status

urlpatterns = [
    url(r'^$', product_detail, name='product_detail'),
    url(r'^(?P<slug>[\w-]+)/add-product/$', ProductCreateView.as_view(), name='add_product'),
    url(r'^(?P<slug>[\w-]+)/update-product/$', ProductUpdateView.as_view(), name='update_product'),
    url(r'^(?P<slug>[\w-]+)/delete-product/$', ProductDeleteView.as_view(), name='delete_product'),
    url(r'^change_publish_status/$', change_publish_status, name='add_product_index'),
    url(r'^api/', include('apps.product.api.urls')),
    url(r'^add-product/$', ProductIndexCreateView.as_view(), name='add_product_index'),
    url(r'^upload/images/$', upload_images, name='upload_images'),
    url(r'^remove/images/$', remove_uploaded_image, name='remove_images'),

]
