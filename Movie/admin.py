from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from Movie.models import Movie
from Spec.models import Link

# Register your models here.

class LinkAdmin(GenericTabularInline):
    model = Link
    extra = 5

class MovieAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'tmdb_id', 'created_date')
    list_display_links = ('id', 'title', 'tmdb_id')
    search_fields = ('id', 'title', 'tmdb_id')
    inlines = [LinkAdmin]

admin.site.register(Movie, MovieAdmin)