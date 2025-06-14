from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

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
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_posted')
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
    tags = TaggableManager()

    class Meta:
        ordering = ['-date_posted']
        indexes = [
            models.Index(fields=['-date_posted']),
        ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
       return reverse(
          'post_detail',
          args=[self.date_posted.year,
                self.date_posted.month,
                self.date_posted.day,
                self.slug
                ]
       )
    
class Comment(models.Model):
   post = models.ForeignKey(
      Post,
      on_delete=models.CASCADE,
      related_name='comments'
   )
   name = models.CharField(max_length=80)
   email = models.EmailField()
   body = models.TextField()
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   active = models.BooleanField(default=True)
   class Meta:
      ordering = ['created']
      indexes = [
         models.Index(fields=['created']),
      ]
      def __str__(self):
         return f'Comment by {self.name} on {self.post}'

