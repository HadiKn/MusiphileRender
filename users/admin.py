from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'is_artist')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'is_artist')}),
    )

    list_display = ('username', 'email', 'is_staff', 'is_artist')
    search_fields = ('username', 'email')