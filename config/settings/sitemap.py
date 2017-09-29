from django.contrib.sitemaps import Sitemap
from django.urls import reverse
import datetime

from twisted.web.server import Site

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop

class SiteMapDomainMixin(Sitemap):

    def get_urls(self, page=1, site=None, protocol=None):
        # give a check in https://github.com/django/django/blob/1.5.1/django/contrib/sitemaps/__init__.py
        # There's also a "protocol" argument.
        fake_site = Site(domain='oobamarket.kg', name='oobamarket.kg')
        return super(SiteMapDomainMixin, self).get_urls(page, fake_site, protocol=None)


class SectionSitemap(SiteMapDomainMixin):
    def items(self):
        return GlobalCategory.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(SiteMapDomainMixin):
    def items(self):
        return Category.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(SiteMapDomainMixin):
    def items(self):
        return Product.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at


    def location(self, obj):
        return obj.get_absolute_url()


class ShopSitemap(SiteMapDomainMixin):
    def items(self):
        return Shop.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return self.get_absolute_url()
