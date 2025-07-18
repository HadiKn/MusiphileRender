from django.contrib import admin
from .models import Stream

# Register your models here.

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'song', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'song__title')
    readonly_fields = ('created_at',)
    list_select_related = ('user', 'song')
    date_hierarchy = 'created_at'
