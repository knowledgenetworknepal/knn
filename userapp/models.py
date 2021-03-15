from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, max_length=254)
    contact = models.CharField(_('contact'), max_length=256)
    approved = models.BooleanField(default=False)
    books_received = models.BooleanField(default=False)


class SignupChoice(models.Model):
    CHOICE = [
        ('I would like to upload 3 books and pay Rs. 200', 'I would like to upload 3 books and pay Rs. 200'),
        ('I would like to deposit Rs. 1000 and pay Rs. 200','I would like to deposit Rs. 1000 and pay Rs. 200')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='signup_choice')
    selection = models.CharField(choices=CHOICE, max_length=256)


class Deposit(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%M')
    amount = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='deposited_by', null=True, blank=True)
    deposit_date = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username 


class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requested_by', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    message = models.CharField(max_length=500)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notification', null=True, blank=True)
    send_to_all = models.BooleanField(default=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notification')
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='deposit_notificaiton', blank=True, null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='request_notificaiton', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
