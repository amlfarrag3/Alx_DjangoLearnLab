from django.db import models
from django.conf import settings


class Post(models.Model):
     author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Link to the User model
         on_delete=models.CASCADE,  # Delete all posts if the user is deleted
         related_name='posts',      # Allow reverse lookup of posts by the user
         verbose_name="Author"
     )
     title = models.CharField(max_length=200, verbose_name="Title")
     content = models.TextField(verbose_name="Content")
     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

     def __str__(self):
         return self.title

     class Meta:
         ordering = ['-created_at']  # Order posts by created date (latest first)

class Comment(models.Model):
    post = models.ForeignKey(
         Post,
         on_delete=models.CASCADE,  # Delete all comments if the post is deleted
         related_name='comments',    # Allow reverse lookup of comments by the post
         verbose_name="Post"
     )
    author = models.ForeignKey(
         settings.AUTH_USER_MODEL,  # Link to the User model
         on_delete=models.CASCADE,  # Delete the comment if the user is deleted
         related_name='comments',   # Allow reverse lookup of comments by the user
         verbose_name="Author"
     )
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
         return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
         ordering = ['created_at']  # Order comments by creation date (oldest first)

["models.TextField()"]

["Like"]
# Create your models here.
class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Post"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="User"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        unique_together = ('post', 'user')  # Ensure a user can like a post only once
        ordering = ['-created_at']  # Order likes by creation date (latest first)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"