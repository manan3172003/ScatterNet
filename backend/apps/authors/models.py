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
    host = models.URLField(default=None) #this needs to be removed to be nullable later
    profileImage = models.URLField(default=None, blank=True, null=True)
    page = models.URLField(default=None, blank=True, null=True) #this too
    # basically we'll use this in the future to identify whether our current Author is from another node
    is_local = models.BooleanField(default=True)
    is_node = models.BooleanField(default=False, null=False, blank=False)
    username = models.CharField(max_length=128, unique=True)

    #we'll use this to identify which authors haven't been onboarded into the system or soft deleted
    allowed_states = (
        ('PENDING', 'PENDING'),
        ('ACTIVE', 'ACTIVE'),
        ('DELETED', 'DELETED')
    )
    state = models.CharField(max_length=7, choices=allowed_states, default='PENDING')
    id_url = models.URLField(unique=True)

class Host(models.Model):
    host=models.URLField(null=False, blank=False, unique=True)
    username=models.CharField(max_length=128, unique=True)
    password=models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)