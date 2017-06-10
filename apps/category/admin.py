from django.contrib import admin
from .models import Category, GlobalCategory
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
from suit.admin import SortableModelAdmin

# Register your models here.


class CategoryAdmin(DjangoMpttAdmin, SortableModelAdmin ):
    list_display = ('title', 'parent', 'slug', 'section', 'published', 'order',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published', 'order')
    sortable = 'order'



admin.site.register(Category, CategoryAdmin)


class GlobalCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(GlobalCategory, GlobalCategoryAdmin)
