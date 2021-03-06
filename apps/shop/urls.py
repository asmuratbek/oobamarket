from django.conf.urls import url, include

from apps.shop.views import *

# ProductFormView

# from apps.shop.views import shop_add

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/sale/(?P<pk>[0-9]+)/$', sale_detail, name='sale_detail'),
    url(r'^delete-banners/$', delete_banners, name='delete-banners'),
    url(r'^create/$', ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/about-us/$', ShopAboutUsDetailView.as_view(), name='about_us'),
    url(r'^(?P<slug>[\w-]+)/contacts/$', ShopContactsView.as_view(), name='contacts_detail'),
    url(r'^(?P<slug>[\w-]+)/sale/create/$', SalesCreateView.as_view(), name='add_sale'),
    url(r'^(?P<slug>[\w-]+)/sale/(?P<pk>[0-9]+)/update$', SalesUpdateView.as_view(), name='update_sale'),
    url(r'^(?P<slug>[\w-]+)/sale/$', ShopSaleListView.as_view(), name='sale'),
    url(r'^(?P<slug>[\w-]+)/sale/archive$', ShopSaleArchiveView.as_view(), name='sale_archive'),
    url(r'^(?P<slug>[\w-]+)/update/$', ShopUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', ShopDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/add-banners/$', CreateBanners.as_view(), name='add_banner'),
    url(r'^(?P<slug>[\w-]+)/update-social/$', ShopSocialLinksUpdateView.as_view(), name='update_social'),
    url(r'^$', ShopListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/review/$', ShopReviewListView.as_view(), name='review'),
    url(r'^(?P<slug>[\w-]+)/add-review/$', add_shop_review, name='add_review'),
    url(r'^(?P<slug>[\w-]+)/update-review/(?P<pk>[0-9]+)/$', update_shop_review, name='update_review'),

]
