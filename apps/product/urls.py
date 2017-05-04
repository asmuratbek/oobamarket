from django.conf.urls import url
from .views import product_detail, FavoriteDetailView


urlpatterns = [
    url(r'^$', product_detail, name='product_detail'),
    url(r'^$', FavoriteDetailView.as_view(), name='is_favorite'),
]
