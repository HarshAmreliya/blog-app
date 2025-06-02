from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
 def get_queryset(self):
    return (
    super().get_queryset().filter(status=Post.Status.PUBLISHED)
            )

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    slug = models.SlugField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ['-date_posted']
        indexes = [
            models.Index(fields=['-date_posted']),
        ]
    def __str__(self):
        return self.title

