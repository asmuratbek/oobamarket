from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    ShopListApiView,
    ShopDetailApiView,
    ShopUpdateApiView,
    ShopDeleteApiView,
    ShopCreateApiView
)

urlpatterns = [
    url(r'^create/$', ShopCreateApiView.as_view(), name='create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<slug>[-_\w]+)/$', ShopDetailApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[-_\w]+)/update/$', ShopUpdateApiView.as_view(), name='update'),
    url(r'^(?P<slug>[-_\w]+)/delete/$', ShopDeleteApiView.as_view(), name='delete'),
    url(r'^$', ShopListApiView.as_view(), name='list'),

]
