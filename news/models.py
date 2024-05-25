from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from register.models import User
from common.models import BaseModel


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.published)


class Category(BaseModel):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title


class Post(BaseModel):
    class Status(models.TextChoices):
        draft = 'DF', 'Daft'
        published = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='media/')

    user = models.ForeignKey('register.User', on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('Tag')

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.draft)
    publish_time = models.DateTimeField(default=timezone.now)
    view_count = models.IntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post:post_detail_page", args=[self.slug])    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Tag(BaseModel):
    title = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body
