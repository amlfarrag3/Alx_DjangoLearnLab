from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import title
from django.contrib.auth.models import content
from django.contrib.auth.models import author
from django.contrib.auth.models import published_date



#from taggit.managers import TaggableManager
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    #tag = TaggableManager() 
    
    def __str__(self):
        return self.title
    
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     posts = models.ManyToManyField(Post)
