from django.conf.urls import url
from apps.global_category.views import GlobalDetailView


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', GlobalDetailView.as_view(), name='detail'),
]
