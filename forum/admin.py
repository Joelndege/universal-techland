from django.contrib import admin
from .models import ForumPost, Comment

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    """
    Admin interface for ForumPost model.
    """
    list_display = ('title', 'author', 'created_at', 'updated_at', 'comment_count')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model.
    """
    list_display = ('content_snippet', 'author', 'post', 'created_at')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'
