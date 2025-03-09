from django.db import models
from ..authors.models import Author


# Create your models here.
visibility_options = [("PUBLIC", "PUBLIC"),
                      ("FRIENDS", "FRIENDS"),
                      ("UNLISTED", "UNLISTED"),
                      ("DELETED", "DELETED")
                      ]

class Post(models.Model):
    # TODO: remove the type field from the model and add it so only the serializer sends it
    type = models.CharField(max_length=100, default='post')
    title = models.CharField(max_length=200)
    id_url = models.URLField(unique=True)
    page = models.URLField()
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, default='PUBLIC', choices=visibility_options)


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now_add=True)
    id_url = models.URLField(unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    page = models.URLField(blank=True, null=True)


class Like(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    id_url = models.URLField(unique=True)
    object = models.URLField() #this is the id_url of the thing that was liked, post/comment

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'object'], name='unique_like')]