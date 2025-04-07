from django.db import models
from django.utils import timezone
from ..authors.models import Author
import uuid

class Reel(models.Model):
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends Only'),
        ('UNLISTED', 'Unlisted')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reels')
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    view_count = models.PositiveIntegerField(default=0)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    duration = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-created_at']

class ReelComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    contentType = models.CharField(max_length=20, default='text/plain')
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at'] # Ordering query results by created_at so most recent first

class ReelCommentLike(models.Model):
    comment = models.ForeignKey(ReelComment, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('comment', 'author')

class ReelLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('reel', 'author')