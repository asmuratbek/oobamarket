from django.conf.urls import url
from .views import CartDetailView, CartDetailByPk


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', CartDetailByPk.as_view(), name='detail_by_pk'),
    url(r'^$', CartDetailView.as_view(), name='detail'),
]
