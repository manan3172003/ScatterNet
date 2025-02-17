from django.db import models
from ..authors.models import Author
from datetime import datetime

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    id_url = models.URLField()
    page = models.URLField()
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(default=datetime.now)



#i also feel like comments and likes should be added as models HERE, since they make up the whole post object, they are dependent on that to exist