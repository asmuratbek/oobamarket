from django.contrib import admin

from .models import Product, ProductImage, FavoriteProduct, Media


# Register your models here.


class ProductImagesInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class MediaInline(admin.StackedInline):
    model = Product.media_set.through
    verbose_name_plural = "Изображения товара"
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, MediaInline]
    prepopulated_fields = {'slug': ('title',)}
    # filter_horizontal = ('images',)


admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProduct)
admin.site.register(ProductImage)
admin.site.register(Media)
