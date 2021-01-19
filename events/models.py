from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    event_date = models.DateTimeField()
    slug = models.SlugField()


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_event')
    registraiton_date = models.DateTimeField(auto_now=True)

    