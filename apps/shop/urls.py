from django.conf.urls import url

from apps.shop.views import ShopDetailView, ShopCreateView

urlpatterns = [
    url(r'^create/$', ShopCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),

]
