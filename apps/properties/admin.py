from django.contrib import admin
from .models import *
# Register your models here.


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'slug', 'parent')

    def get_categories(self, obj):
        return ", ".join([c.title for c in obj.category.all()])

admin.site.register(Properties, PropertiesAdmin)


class ValuesAdmin(admin.ModelAdmin):
    list_display = ('value', 'properties', 'get_products')

    def get_products(self, obj):
        return ", ".join([c.title for c in obj.products.all()])

admin.site.register(Values, ValuesAdmin)
