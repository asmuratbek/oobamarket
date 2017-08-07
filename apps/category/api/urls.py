from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    CategoryListApiView,
    CategoryDetailApiView,
    GetUsedCategoriesFromShop
)

urlpatterns = [
    # url(r'^shop/(?P<slug>[-_\w]+)/$', GetUsedCategoriesFromShop.as_view(), name="shops_used_categories"),
    url(r'^$', CategoryListApiView.as_view(), name='list'),
    url(r'^(?P<slug>[-_.\w]+)/$', CategoryDetailApiView.as_view(), name='detail'),


]
