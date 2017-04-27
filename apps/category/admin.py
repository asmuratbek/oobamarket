from django.contrib import admin
from .models import Category, GlobalCategory
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class GlobalCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(GlobalCategory, GlobalCategoryAdmin)
