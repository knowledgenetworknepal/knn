from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    approved = models.BooleanField(default=False)


class Notification(models.Model):
    message = models.CharField(max_length=500)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notification', null=True, blank=True)
    send_to_all = models.BooleanField(default=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notification')


class Deposit(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%M')
    amount = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='deposited_by', null=True, blank=True)
    deposit_date = models.DateTimeField(auto_now=True)

    