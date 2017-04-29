from django.conf.urls import url
from apps.shop.views import ShopDetailView

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),

]
