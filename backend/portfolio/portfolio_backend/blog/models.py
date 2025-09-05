from django.db import models
import uuid
from django.utils.text import slugify
from django.conf import settings
from useraccount.models import User

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.slug
            slug = base_slug
            while Tag.objects.filter(slug=slug).exclude(id=self.pk).exists():
                count = 1
                slug = f'{base_slug}-{count}'
                count+=1
            self.slug = slug

        super().save(*args, **kwargs)

class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    cover = models.ImageField(upload_to='uploads/covers', blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)

    viewable = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False) # We need extra logic that if a blog is deleted, set the viewable to false
                                                #automatically

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count=1
            while Blog.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f'{base_slug}-{count}'
                count+=1
            self.slug = slug

        super().save(*args, **kwargs)

    def cover_url(self):
        if self.cover:
            return f'{settings.WEBSITE_URL}{self.cover.url}'
        else:
            return None
