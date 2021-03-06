import random
from django.db import models

from django.contrib.auth import get_user_model
from books.models import Category
from django.utils.text import slugify
from ckeditor.fields import RichTextField

User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='category_blogs')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_blogs')
    added_date = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='upload/%Y/%M', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            try:
                self.slug = slugify(self.title)
                super().save(*args, **kwargs)

            except:
                self.slug = slugify(self.title)+str(random.randint(0,99999999))
                super().save(*args, **kwargs)


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    comment_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='commented_by')
    comment_date = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, null=True, blank=True, on_delete=models.SET_NULL)

