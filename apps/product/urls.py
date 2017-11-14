from django.conf.urls import url, include

from .views import ProductCreateView, ProductUpdateView, ProductIndexCreateView, upload_images, \
    remove_uploaded_image, ProductDeleteView, change_publish_status, upload_images_product_update, \
    delete_product_images, add_product_review, ProductListView, update_product_review, ProductDetailView, delete_product

urlpatterns = [
    url(r'^$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^all/$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<slug>[\w-]+)/add-product/$', ProductCreateView.as_view(), name='add_product'),
    url(r'^(?P<slug>[\w-]+)/update-product/$', ProductUpdateView.as_view(), name='update_product'),
    url(r'^(?P<slug>[\w-]+)/upload-product-images/$', upload_images_product_update, name='upload_product_images'),
    url(r'^(?P<slug>[\w-]+)/delete-product/$', delete_product, name='delete_product'),
    url(r'^add-product/$', ProductIndexCreateView.as_view(), name='add_product_index'),
    url(r'^delete-product-images/$', delete_product_images, name='delete_product_images'),
    url(r'^upload/images/$', upload_images, name='upload_images'),
    url(r'^remove/images/$', remove_uploaded_image, name='remove_images'),
    url(r'^(?P<slug>[\w-]+)/add-review/$', add_product_review, name='add_review'),
    url(r'^(?P<slug>[\w-]+)/update-review/(?P<pk>[0-9]+)/$$', update_product_review, name='update_review'),


]
