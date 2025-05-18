from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'release_date', 'duration')
    list_filter = ('artist', 'album', 'release_date')
    search_fields = ('title', 'artist__username', 'album__title')

admin.site.register(Song, SongAdmin)