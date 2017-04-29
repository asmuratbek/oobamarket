from django.conf.urls import url
from apps.category.views import CategoryDetailView


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='detail'),
]
