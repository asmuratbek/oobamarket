from django.conf.urls import url
from .views import CartDetailView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', CartDetailView.as_view(), name='detail'),
]
