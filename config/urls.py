from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from apps.global_category.views import IndexView
from apps.product.views import FavoriteCreateView, product_reviews
from apps.shop.views import agreement, shop_reviews
from apps.product.views import search_predict_html, search
from apps.utils.views import counter
from apps.users.views import SubscribeListView
from apps.category.views import mail_confirm_view
from config.settings.sitemap import ProductSitemap, ShopSitemap, SectionSitemap, CategorySitemap
from django.contrib.sitemaps.views import sitemap
from apps.meta.views import ClaimCreate

sitemaps = {
    'sections': SectionSitemap,
    'category': CategorySitemap,
    'products': ProductSitemap,
    'shops': ShopSitemap,

}

urlpatterns = [
                  url(r'^$', IndexView.as_view(), name='home'),
                  url(r'^api/v1/', include('apps.api.v1.urls', namespace='api')),
                  url(r'^docs/', include('rest_framework_docs.urls')),
                  url(r'^favorite/add/', FavoriteCreateView.as_view(), name="create_favorite"),
                  url(r'^shops/', include('apps.shop.urls', namespace='shops')),
                  url(r'^order/', include('apps.order.urls', namespace='order')),
                  url(r'^cart/', include('apps.cart.urls', namespace='cart')),
                  url(r'^product/', include('apps.product.urls', namespace='product')),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
                  url(r'^agreement/$', agreement, name='agreement'),
                  url(r'^search_predict_html', search_predict_html, name='search_predict_html'),
                  url(r'^sub-list/$', SubscribeListView.as_view(), name='sub_list'),
                  url(r'^counter/$', counter, name='counter'),
                  url(r'^search_results', search_predict_html),
                  url(r'^search', search),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^landing/', ClaimCreate.as_view(), name='landing'),
                  url(r'^product_reviews/$', product_reviews, name='product_reviews'),
                  url(r'^shop_reviews/$', shop_reviews, name='shop_reviews'),
                  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

                  # Django Admin, use {% url 'admin:index' %}
                  url(r'^jet/', include('jet.urls', 'jet')),
                  url(settings.ADMIN_URL, admin.site.urls),

                  # User management
                  url(r'^users/', include('apps.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),
                  url(r'^b85b738ce8c6.html/', mail_confirm_view),
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
