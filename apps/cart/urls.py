from django.conf.urls import url
from .views import CartDetailView, CartDetailByPkUser, CartDetailByPkShop, ConfirmOrderByShop


urlpatterns = [
    url(r'^user/(?P<username>[\w.@+-]+)/(?P<pk>\d+)/$', CartDetailByPkUser.as_view(), name='detail_by_pk_user'),
    url(r'^shop/(?P<shop_slug>[\w.@+-]+)/(?P<pk>\d+)/$', CartDetailByPkShop.as_view(), name='detail_by_pk_shop'),
    url(r'^(?P<pk>\d+)/confirm/$', ConfirmOrderByShop.as_view(), name='detail_by_pk'),
    url(r'^$', CartDetailView.as_view(), name='detail'),
]
