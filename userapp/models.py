from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, max_length=254)
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
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username 