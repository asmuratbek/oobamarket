from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    ProductListApiView,
    ProductDetailApiView,
    ProductUpdateApiView,
    ProductDeleteApiView,
    ProductCreateApiView
)

urlpatterns = [
    url(r'^create/$', ProductCreateApiView.as_view(), name='create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<slug>[-_\w]+)/$', ProductDetailApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[-_\w]+)/update/$', ProductUpdateApiView.as_view(), name='update'),
    url(r'^(?P<slug>[-_\w]+)/delete/$', ProductDeleteApiView.as_view(), name='delete'),
    url(r'^$', ProductListApiView.as_view(), name='list'),

]
