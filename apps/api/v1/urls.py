from django.conf.urls import url, include
from .views import (
    CategoryListApiView,
    CategoryDetailApiView,
    GetUsedCategoriesFromShop,
    GlobalCategoryListApiView,
    GlobalCategoryDetailApiView,
    ProductListApiView,
    ProductDetailApiView,
    ProductUpdateApiView,
    ProductDeleteApiView,
    ProductCreateApiView,
    ShopListApiView,
    ShopDetailApiView,
    ShopApiView,
    ShopUpdateApiView,
    ShopDeleteApiView,
    ShopCreateApiView,
    FacebookLogin,
    GoogleLogin
)
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    # url(r'^shop/(?P<slug>[-_\w]+)/$', GetUsedCategoriesFromShop.as_view(), name="shops_used_categories"),
    url(r'^category/(?P<slug>[-_.\w]+)/$', CategoryDetailApiView.as_view(), name='category_detail'),
    url(r'^category/$', CategoryListApiView.as_view(), name='category_list'),
    url(r'^globalcategory/(?P<slug>[-_.\w]+)/$', GlobalCategoryDetailApiView.as_view(), name='globalcategory_detail'),
    url(r'^globalcategory/$', GlobalCategoryListApiView.as_view(), name='globalcategory_list'),
    url(r'^product/create/$', ProductCreateApiView.as_view(), name='product_create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<slug>[-_\w]+)/$', ProductDetailApiView.as_view(), name='product_detail'),
    url(r'^product/(?P<slug>[-_\w]+)/update/$', ProductUpdateApiView.as_view(), name='product_update'),
    url(r'^product/(?P<slug>[-_\w]+)/delete/$', ProductDeleteApiView.as_view(), name='product_delete'),
    url(r'^product/$', ProductListApiView.as_view(), name='product_list'),
    url(r'^shop/create/$', ShopCreateApiView.as_view(), name='shop_create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^shop/(?P<slug>[-_\w]+)/$', ShopDetailApiView.as_view(), name='shop_detail'),
    url(r'^shop/(?P<slug>[-_\w]+)/shop/$', ShopApiView.as_view(), name='shop_categories'),
    url(r'^shop/(?P<slug>[-_\w]+)/update/$', ShopUpdateApiView.as_view(), name='shop_update'),
    url(r'^shop/(?P<slug>[-_\w]+)/delete/$', ShopDeleteApiView.as_view(), name='shop_delete'),
    url(r'^shop/$', ShopListApiView.as_view(), name='shop_list'),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
]