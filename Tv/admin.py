from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from Tv.models import Series, Season, Episode
from Spec.models import Link

# Register your models here.

class LinkAdmin(GenericTabularInline):
    model = Link
    extra = 5

class SeriesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'tmdb_id', 'created_date')
    list_display_links = ('id', 'title', 'tmdb_id')
    search_fields = ('id', 'title', 'tmdb_id')
admin.site.register(Series, SeriesAdmin)

class SeasonAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'series', 'created_date')
    list_display_links = ('id', 'title', 'series')
    search_fields = ('id', 'title', 'series')
    inlines = [LinkAdmin]

admin.site.register(Season, SeasonAdmin)

class EpisodeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'season', 'created_date')
    list_display_links = ('id', 'title', 'season')
    search_fields = ('id', 'title', 'season')
    inlines = [LinkAdmin]

admin.site.register(Episode, EpisodeAdmin)