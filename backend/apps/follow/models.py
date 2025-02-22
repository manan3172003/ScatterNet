from django.db import models

from ..authors.models import Author


# Create your models here.
class Follow(models.Model):
    isPending =models.BooleanField(default=True)
    actor = models.ForeignKey(Author, related_name='follow_requester', on_delete=models.CASCADE) # author requesting the follow request
    object = models.ForeignKey(Author, related_name='follow_requestee', on_delete=models.CASCADE) # author the actor wants to follow

    class Meta:
        unique_together = ('actor', 'object')