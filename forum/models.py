from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumPost(models.Model):
    """
    Model for forum posts in the Tourist Safety Alert System.
    Allows users to share experiences, tips, and discussions about travel safety.
    """
    title = models.CharField(max_length=200, help_text="Title of the forum post")
    content = models.TextField(help_text="Main content of the post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Forum Post"
        verbose_name_plural = "Forum Posts"

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_snippet(self):
        """Return a short snippet of the content for list views."""
        return self.content[:150] + "..." if len(self.content) > 150 else self.content


class Comment(models.Model):
    """
    Model for comments on forum posts.
    Users can comment on posts to engage in discussions.
    """
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(help_text="Comment content")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
