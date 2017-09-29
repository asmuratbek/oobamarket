from django.contrib.sitemaps import Sitemap
from django.urls import reverse
import datetime

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop


class SectionSitemap(Sitemap):
    def items(self):
        return GlobalCategory.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()

    def changefreq(self, obj):
        return 'always'


    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ShopSitemap(Sitemap):
    def items(self):
        return Shop.objects.all()

    def changefreq(self, obj):
        return 'always'

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
