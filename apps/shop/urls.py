from django.conf.urls import url

from apps.shop.views import ShopDetailView, ShopCreateView, ShopBannersView, ShopUpdateView

# ProductFormView

# from apps.shop.views import shop_add

urlpatterns = [
    # url(r'^create/$', shop_add, name='create'),
    url(r'^create/$', ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', ShopUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/add-banners/$', ShopBannersView.as_view(), name='add_banner'),

]
