from django.contrib import admin
from .models import Playlist

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')

admin.site.register(Playlist,PlaylistAdmin)