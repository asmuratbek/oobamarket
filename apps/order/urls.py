from apps.order.views import OrderDetail, SimpleOrderCreateView, ThankYouView, SimpleOrderListView, \
    SimpleOrderDetailView, SimpleOrderShopListView
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', SimpleOrderCreateView.as_view(), name='create'),
    url(r'^thank-you/$', ThankYouView.as_view(), name="thanks"),
    url(r'^(?P<pk>\d+)/$', SimpleOrderDetailView.as_view(), name='simple_detail'),
    url(r'^(?P<slug>[\w.@+-]+)/order-list/$', SimpleOrderShopListView.as_view(), name='shop_order_list'),
    url(r'^(?P<pk>\d+)/$', OrderDetail.as_view(), name='detail'),

    url(
        regex=r'^(?P<username>[\w.@+-]+)/order-history/$',
        view=SimpleOrderListView.as_view(),
        name='order-history'
    ),

]
