from django.contrib import admin
from .models import *
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('user',)

admin.site.register(Shop, ShopAdmin)
admin.site.register(Banners)
admin.site.register(SocialLinks)
