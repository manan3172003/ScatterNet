from django.db import models

# Create your models here.

class Author(models.Model):
    displayName = models.CharField(max_length=256)
    host = models.URLField()
    github = models.URLField()
    #not sure if this is gonna be just the url the frontend pulls or straight up the image, so it could be models.ImageField()
    profileImageURL = models.URLField()
    page = models.URLField()