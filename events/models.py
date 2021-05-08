import random

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor.fields import RichTextField


User = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    event_date = models.DateTimeField()
    slug = models.SlugField(unique=True)
    added_date = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='event/%Y/%M', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            try:
                self.slug = slugify(self.name)
            except:
                self.slug = slugify(self.name)+random.randint(0,99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_event')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_of')
    registraiton_date = models.DateTimeField(auto_now=True)

    