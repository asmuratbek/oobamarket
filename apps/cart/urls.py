from django.conf.urls import url
from .views import CartDetailView


urlpatterns = [
    url(r'^$', CartDetailView.as_view(), name='detail'),
]
