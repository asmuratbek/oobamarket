from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from apps.global_category.views import IndexView, landing
from apps.product.views import FavoriteCreateView
from apps.shop.views import agreement
from apps.product.views import search, search_predict_html

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'favorite/add/', FavoriteCreateView.as_view(), name="create_favorite"),
    url(r'^shops/', include('apps.shop.urls', namespace='shops')),
    url(r'^order/', include('apps.order.urls', namespace='order')),
    url(r'^cart/', include('apps.cart.urls', namespace='cart')),
    url(r'^product/', include('apps.product.urls', namespace='product')),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^agreement/$', agreement, name='agreement'),
    url(r'^api/product/', include('apps.product.api.urls', namespace="product_api")),
    url(r'^api/shop/', include('apps.shop.api.urls', namespace="shop_api")),
    url(r'^api/category/', include('apps.category.api.urls', namespace="category_api")),
    url(r'^search_predict_html', search_predict_html, name='search_predict_html'),
    # url(r'^search/', include('haystack.urls')),
    url(r'^search_results', search_predict_html),
    url(r'^search/', search, name='search'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^landing/', landing, name='landing'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('apps.category.urls', namespace='categories')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
