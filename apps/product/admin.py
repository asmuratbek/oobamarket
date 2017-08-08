from django.contrib import admin

from .models import Product, ProductImage, FavoriteProduct


# Register your models here.


class ProductImagesInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('values',)
    search_fields = ['title']


admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProduct)
admin.site.register(ProductImage)
