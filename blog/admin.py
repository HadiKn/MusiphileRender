from django.contrib import admin
from .models import BlogPost, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'user__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
