from django.contrib import admin
from .models import Album

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__username')

admin.site.register(Album, AlbumAdmin)