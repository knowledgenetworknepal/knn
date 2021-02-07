from django.db import models


class BaseInfo(models.Model):
    comapny_name = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=256, null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to='company/', null=True, blank=True)


class Ads(models.Model):
    AD_TYPE = (
        ('Hero','Hero'),
        ('HE','HE'),
        ('HL','Home Left'),
        ('HR','Home Right'),
    )
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    ad_type = models.CharField(choices=AD_TYPE, max_length=256)
    title = models.CharField(max_length=256)
    sub_title = models.CharField(max_length=256, null=True, blank=True)
    action_url = models.URLField(null=True, blank=True)
    status = models.BooleanField(default=True)


class Contact(models.Model):
    contacted_by = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=256, blank=True, null=True)
    message = models.TextField(max_length=500)

    
    
