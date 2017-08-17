from apps.order.views import OrderDetail, SimpleOrderCreateView, ThankYouView, SimpleOrderListView, \
    SimpleOrderUpdateView, SimpleOrderShopDetailView, simple_order_shop_list_update, DeleteSimpleOrderShop, \
    change_status, delete_simple_order_list
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', SimpleOrderCreateView.as_view(), name='create'),
    url(r'^thank-you/$', ThankYouView.as_view(), name="thanks"),
    url(r'^(?P<pk>\d+)/$', SimpleOrderUpdateView.as_view(), name='simple_update'),
    url(r'^(?P<slug>[\w.@+-]+)/order-list/$', simple_order_shop_list_update, name='shop_order_list'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteSimpleOrderShop.as_view(), name='shop_order_delete'),
    url(r'^(?P<slug>[\w.@+-]+)/order-detail/(?P<pk>\d+)/$', SimpleOrderShopDetailView.as_view(), name='shop_order_detail'),
    url(r'^(?P<pk>\d+)/$', OrderDetail.as_view(), name='detail'),
    url(r'^change_status/$', change_status, name='change_status'),
    url(r'^delete_items/$', delete_simple_order_list, name='delete_items'),

    url(
        regex=r'^(?P<username>[\w.@+-]+)/order-history/$',
        view=SimpleOrderListView.as_view(),
        name='order-history'
    ),

]
