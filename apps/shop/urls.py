from django.conf.urls import url

from apps.shop.views import ShopDetailView, ShopCreateView, ShopBannersView, ShopUpdateView, ShopSocialLinksUpdateView, \
                            CreateBanners, delete_banners


# ProductFormView

# from apps.shop.views import shop_add

urlpatterns = [
    # url(r'^create/$', shop_add, name='create'),
    url(r'^delete-banners/$', delete_banners, name='delete-banners'),
    url(r'^create/$', ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', ShopUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/add-banners/$', CreateBanners.as_view(), name='add_banner'),
    url(r'^(?P<slug>[\w-]+)/update-social/$', ShopSocialLinksUpdateView.as_view(), name='update_social'),

]
