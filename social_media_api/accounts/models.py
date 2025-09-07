from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, help_text="A short bio about the user.")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null = True,
                                        help_text="Upload a profile picture.")
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followed_by',  blank=True,
                                       help_text="Users who are following this user.")
    following = models.ManyToManyField('self', symmetrical=False, related_name='following_users', blank=True,
                                        help_text="Users that this user is following.")
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True, 
                                    help_text="The groups this user belongs to.")
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True,
                                              help_text="Specific permissions for this user.")

    def __str__(self):
        return self.username
    
# Create your models here.