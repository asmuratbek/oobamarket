from django.conf.urls import url
from .views import ProductDetailView


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),
]
