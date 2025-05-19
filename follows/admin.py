from django.contrib import admin
from .models import Follow

# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'artist')
    search_fields = ('follower__username', 'artist__username')

admin.site.register(Follow, FollowAdmin)
