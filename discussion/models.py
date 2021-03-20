import random
from django.db import models

from django.contrib.auth import get_user_model
from books.models import Category
from django.utils.text import slugify
from ckeditor.fields import RichTextField

User = get_user_model()


class Quesiton(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='category_discussion')
    added_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    status = models.BooleanField(default=True)
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



class DiscussionVote(models.Model):
    like = models.BooleanField(default=True)
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='liked_by')
    status = models.BooleanField(default=True)


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    comment_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='disucssion_comment')
    comment_date = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Quesiton, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)

