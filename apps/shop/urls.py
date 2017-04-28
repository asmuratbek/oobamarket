from django.conf.urls import url

from apps.category.views import fixtures
from apps.shop.views import ShopDetailView
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='detail'),

]
