from django.conf.urls import url
from apps.category.views import IndexView, GlobalDetailView


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', GlobalDetailView.as_view(), name='global_detail'),

]
