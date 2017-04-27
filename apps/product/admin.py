from django.contrib import admin
from .models import Product, ProductImage
# Register your models here.


class ProductImagesInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline,]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, ProductAdmin)
