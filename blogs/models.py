from django.db import models

from django.contrib.auth import get_user_model
from books.models import Category


User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='category_blogs')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_blogs')
    added_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    comment_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='commented_by')
    comment_date = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, null=True, blank=True, on_delete=models.SET_NULL)

