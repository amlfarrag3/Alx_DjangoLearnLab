from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="User"
        
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications',
        verbose_name="Recipient"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications',
        verbose_name="Actor"
    )
    verb = models.CharField(max_length=50, verbose_name="Verb")
    target = models.ForeignKey(generic.ForeignKey, on_delete=models.CASCADE, null=True, blank=True, related_name='target_notifications', verbose_name="Target")
    action_object = models.ForeignKey(generic.ForeignKey, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."

    class Meta:
        ordering = ['-created_at']  # Order notifications by creation date (latest first)

