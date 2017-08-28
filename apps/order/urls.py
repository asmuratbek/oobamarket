from apps.order.views import OrderDetail, SimpleOrderCreateView, ThankYouView, UserSimpleOrderListView, \
    ShopSimpleOrderUpdateView, ShopSimpleOrderDetailView, ShopSimpleOrderListView, \
    shop_change_status, UserSimpleOrderDetailView, shop_delete_cartitem_product
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', SimpleOrderCreateView.as_view(), name='create'),
    url(r'^thank-you/$', ThankYouView.as_view(), name="thanks"),
    url(r'^change_status/$', shop_change_status, name='change_status'),
    url(r'^delete_product/$', shop_delete_cartitem_product, name='delete_product'),
    url(r'^(?P<slug>[\w.@+-]+)/order-list/$', ShopSimpleOrderListView.as_view(), name='shop_order_list'),
    url(r'^(?P<slug>[\w.@+-]+)/order-detail/(?P<pk>\d+)/$', ShopSimpleOrderDetailView.as_view(), name='shop_simple_order_detail'),
    url(r'^(?P<pk>\d+)/shop_detail$', ShopSimpleOrderUpdateView.as_view(), name='shop_simple_order_update'),
    # url(r'^(?P<pk>\d+)/delete/$', DeleteSimpleOrderShop.as_view(), name='shop_order_delete'),
    # url(r'^(?P<pk>\d+)/$', OrderDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/user_detail$', UserSimpleOrderDetailView.as_view(), name='user_order_detail'),
    url(r'^(?P<username>[\w.@+-]+)/order_list/$', UserSimpleOrderListView.as_view(), name='user_order_list'),



]
