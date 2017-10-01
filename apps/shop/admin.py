from django.contrib import admin
from .models import *
# Register your models here.


class ContactsInline(admin.TabularInline):
    model = Contacts


class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('user',)
    inlines = [ContactsInline]


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    fields = ['title', 'type', 'longitude', 'latitude']

admin.site.register(Shop, ShopAdmin)
admin.site.register(Banners)
admin.site.register(SocialLinks)
admin.site.register(Contacts)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Sales)
