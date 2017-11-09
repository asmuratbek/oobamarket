from django.contrib import admin
from .models import IndexBlocks, PremiumIndexBlocks, IndexBanner, Help
# Register your models here.


class IndexAdmin(admin.ModelAdmin):
    list_filter = ['column']

admin.site.register(IndexBlocks, IndexAdmin)
admin.site.register(PremiumIndexBlocks)
admin.site.register(IndexBanner)
admin.site.register(Help)
