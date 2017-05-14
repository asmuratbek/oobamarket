from apps.order.views import OrderDetail, SimpleOrderCreateView, ThankYouView, SimpleOrderListView
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', SimpleOrderCreateView.as_view(), name='create'),
    url(r'^thank-you/$', ThankYouView.as_view(), name="thanks"),
    url(r'^(?P<pk>\d+)/$', OrderDetail.as_view(), name='detail'),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/order-history/$',
        view=SimpleOrderListView.as_view(),
        name='order-history'
    ),

]
