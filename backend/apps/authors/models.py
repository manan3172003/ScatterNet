from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='author_profile'
    )

    displayName = models.CharField(max_length=256)
    host = models.URLField()
    github = models.URLField()
    #not sure if this is gonna be just the url the frontend pulls or straight up the image, so it could be models.ImageField()
    profileImageURL = models.URLField()
    page = models.URLField()

    # basically we'll use this in the future to identify whether or not our current Author is from another node
    is_local = models.BooleanField(default=True)
    username = models.CharField(max_length=128, unique=True)

    #we'll use this to identify which authors haven't been onboarded into the system or soft deleted
    allowed_states = (
        ('PENDING', 'PENDING'),
        ('ACTIVE', 'ACTIVE'),
        ('DELETED', 'DELETED')
    )
    state = models.CharField(max_length=7, choices=allowed_states, default='PENDING')