from django.contrib import admin
from .models import UserCheckout, UserAddress, Order, SimpleOrder

admin.site.register(UserCheckout)

admin.site.register(UserAddress)

admin.site.register(Order)

admin.site.register(SimpleOrder)


# Register your models here.
