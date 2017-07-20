from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
# Register your models here.


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_categories', 'slug', 'parent')
    search_fields = ('title', 'slug', 'values__value')

    def get_categories(self, obj):
        return ", ".join([c.title for c in obj.category.all()])

admin.site.register(Properties, PropertiesAdmin)


class ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'get_property', 'property_slug', 'get_products')
    search_fields = ('value', 'properties__title')

    def get_products(self, obj):
        return mark_safe(
            "<br> ".join(["<a href=/admin/product/product/{}/change/>{}</a> ".format(c.id, c.title) for c in obj.products.all()])
        )

    def get_property(self, obj):
        return mark_safe(
            "<a href=/admin/properties/properties/{}/change/>{}</a> ".format(obj.properties.id, obj.properties.title)
        )

    def property_slug(self, obj):
        return obj.properties.slug

admin.site.register(Values, ValuesAdmin)
