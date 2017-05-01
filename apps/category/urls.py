from django.conf.urls import url, include
from apps.category.views import category_detail
from apps.global_category.views import GlobalDetailView

urlpatterns = [
    url(r'^(?P<global_slug>[\w-]+)/(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/', include('apps.product.urls')),
    url(r'^(?P<global_slug>[\w-]+)/(?P<slug>[\w-]+)/$', category_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', GlobalDetailView.as_view(), name='global_detail'),

]
