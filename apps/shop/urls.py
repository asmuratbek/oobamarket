from django.conf.urls import url

from apps.shop.views import *

# ProductFormView

# from apps.shop.views import shop_add

urlpatterns = [
    url(r'^delete-banners/$', delete_banners, name='delete-banners'),
    url(r'^remove-logo/$', remove_logo, name='remove_logo'),
    url(r'^create/$', ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/contacts$', ShopContactsView.as_view(), name='contacts_detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', ShopUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', ShopDeleteView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/add-banners/$', CreateBanners.as_view(), name='add_banner'),
    url(r'^(?P<slug>[\w-]+)/update-social/$', ShopSocialLinksUpdateView.as_view(), name='update_social'),

]
