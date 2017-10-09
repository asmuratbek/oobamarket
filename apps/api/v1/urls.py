from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # url(r'^shop/(?P<slug>[-_\w]+)/$', GetUsedCategoriesFromShop.as_view(), name="shops_used_categories"),
    url(r'^place/$', PlaceListView.as_view(), name='place_list'),
    url(r'^my-list/$', MyListView.as_view(), name='my_list'),
    url(r'^lenta/$', LentaView.as_view(), name='lenta'),
    url(r'^category/(?P<slug>[-_.\w]+)/$', CategoryDetailApiView.as_view(), name='category_detail'),
    url(r'^category/(?P<slug>[-_.\w]+)/children/$', CategoryDetailChildrenApiView.as_view(), name='category_detail'),
    url(r'^category/$', CategoryListApiView.as_view(), name='category_list'),
    url(r'^globalcategory/(?P<slug>[-_.\w]+)/$', GlobalCategoryDetailApiView.as_view(), name='globalcategory_detail'),
    url(r'^globalcategory/(?P<slug>[-_.\w]+)/children/$', GlobalCategoryGetChildrenApiView.as_view(), name='globalcategory_children'),
    url(r'^globalcategory/$', GlobalCategoryListApiView.as_view(), name='globalcategory_list'),
    url(r'^product/create/$', ProductCreateApiView.as_view(), name='product_create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<slug>[-_\w]+)/$', ProductDetailApiView.as_view(), name='product_detail'),
    url(r'^product/(?P<slug>[-_\w]+)/add-to-favorite/$', ProductAddToFavoriteView.as_view()),
    url(r'^product/(?P<slug>[-_\w]+)/add-to-cart/$', ProductAddToCartView.as_view()),
    url(r'^product/(?P<slug>[-_\w]+)/cart/$', ProductChangeCartView.as_view()),
    url(r'^product/(?P<slug>[-_\w]+)/update/$', ProductUpdateApiView.as_view(), name='product_update'),
    url(r'^product/(?P<slug>[-_\w]+)/delete/$', ProductDeleteApiView.as_view(), name='product_delete'),
    url(r'^product/$', ProductListApiView.as_view(), name='product_list'),
    url(r'^subscribe/$', Subscribe.as_view(), name='subscribe'),
    url(r'^shop/create/$', ShopCreateApiView.as_view(), name='shop_create'),
    # url(r'^category/(?P<slug>[-_\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^shop/detail/(?P<slug>[-_\w]+)/sales/$', ShopSalesView.as_view(), name="shop_sales"),
    url(r'^shop/detail/(?P<slug>[-_\w]+)/reviews/$', ShopReviewsView.as_view(), name="shop_reviews"),
    url(r'^shop/detail/(?P<slug>[-_\w]+)/contacts/$', ShopContactsView.as_view(), name="shop_contacts"),
    url(r'^shop/detail/(?P<slug>[-_\w]+)/$', ShopDetailView.as_view(), name="shop"),
    url(r'^shop/(?P<slug>[-_\w]+)/$', ShopDetailApiView.as_view(), name='shop_detail'),
    url(r'^shop/(?P<slug>[-_\w]+)/shop/for-react/$', ShopApiView.as_view(), name='shop_categories_for_react'),
    url(r'^shop/(?P<slug>[-_\w]+)/shop/$', ShopApiMobileView.as_view(), name='shop-detail'),
    # url(r'^shop/(?P<slug>[-_\w]+)/sales/$', ShopSalesApiMobileView.as_view(), name='shop-sales'),
    # url(r'^shop/(?P<slug>[-_\w]+)/sales/$', ShopSalesApiMobileView.as_view(), name='shop-sales'),
    url(r'^shop/(?P<slug>[-_\w]+)/categories/$', ShopCategoriesApiView.as_view(), name='shop_categories'),
    url(r'^shop/(?P<slug>[-_\w]+)/category/(?P<category_slug>[-_\w]+)/$', ShopCategoryChildrenApiView.as_view(), name='shop_category_children'),
    url(r'^shop/(?P<slug>[-_\w]+)/update/$', ShopUpdateApiView.as_view(), name='shop_update'),
    url(r'^shop/(?P<slug>[-_\w]+)/delete/$', ShopDeleteApiView.as_view(), name='shop_delete'),
    url(r'^shop/$', ShopListApiView.as_view(), name='shop_list'),
    # url(r'^user/(?P<pk>[0-9]+)/shops/$', UserShopsListView.as_view(), name="user_shops_list"),
    url(r'^user/cart/$', UserCartItemsView.as_view(), name="user_cart"),
    url(r'^user/favorites/$', UserFavoritesView.as_view(), name="user_cart"),
    url(r'^user/$', UserDetailView.as_view(), name="user_detail"),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
]
