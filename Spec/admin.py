from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from Spec.models import Link, Genre, Category, Quality

# Register your models here.

class LinkMAdmin(ImportExportModelAdmin):
    list_display = ('uuid', 'name',)
    list_display_links = ('uuid', 'name')
    search_fields = ('uuid', 'name', 'uuid')
admin.site.register(Link, LinkMAdmin)

class GenreAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
admin.site.register(Genre, GenreAdmin)

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
admin.site.register(Category, CategoryAdmin)

class QualityAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
admin.site.register(Quality, QualityAdmin)