from django.contrib import admin
from .models import UserCheckout, UserAddress, Order, SimpleOrder

class SimpleOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'created_at', 'is_visible']
    list_editable = ['is_visible']

admin.site.register(UserCheckout)

admin.site.register(UserAddress)

admin.site.register(Order)

admin.site.register(SimpleOrder, SimpleOrderAdmin)


# Register your models here.
