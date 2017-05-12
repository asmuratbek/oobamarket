from apps.order.views import OrderDetail
from django.conf.urls import url

urlpatterns = [
    # url(r'^create/$', shop_add, name='create'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='detail'),

]
