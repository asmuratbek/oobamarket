from django.contrib import admin
from .models import *
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.


class CategoryAdmin(DjangoMpttAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
