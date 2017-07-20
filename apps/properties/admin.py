from django.contrib import admin
from .models import *
# Register your models here.


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_categories', 'slug', 'parent')
    search_fields = ('title', 'slug')

    def get_categories(self, obj):
        return ", ".join([c.title for c in obj.category.all()])

admin.site.register(Properties, PropertiesAdmin)


class ValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'properties', 'property_slug', 'get_products')
    search_fields = ('value',)

    def get_products(self, obj):
        return ", ".join([c.title for c in obj.products.all()])

    def property_slug(self, obj):
        return obj.properties.slug

admin.site.register(Values, ValuesAdmin)
