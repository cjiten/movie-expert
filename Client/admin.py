from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from Client.models import Client, ClientLink

# Register your models here.

class ClientAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
admin.site.register(Client, ClientAdmin)

class ClientLinkAdmin(ImportExportModelAdmin):
    list_display = ('id', 'link')
    list_display_links = ('id', 'link')
    search_fields = ('id', 'link')
admin.site.register(ClientLink, ClientLinkAdmin)