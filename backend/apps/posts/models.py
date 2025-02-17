from django.db import models
from ..authors.models import Author
from datetime import datetime

# Create your models here.

class Post(models.Model):
    type = models.CharField(max_length=100, default='post')
    title = models.CharField(max_length=200)
    id_url = models.URLField(unique=True)
    page = models.URLField()
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.now)
    visibility = models.CharField(max_length=10, default='public')


#i also feel like comments and likes should be added as models HERE, since they make up the whole post object, they are dependent on that to exist
class Comment(models.Model):
    type = models.CharField(max_length=100, default='comment')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=100)
    published = models.DateTimeField(default=datetime.now)
    id_url = models.URLField(unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Like(models.Model):
    type = models.CharField(max_length=100, default='like')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.now)
    id_url = models.URLField(unique=True)
    object = models.URLField()

