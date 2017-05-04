from django.conf.urls import url
from .views import product_detail


urlpatterns = [
    url(r'^$', product_detail, name='product_detail'),
]
