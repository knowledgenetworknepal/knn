# Generated by Django 3.1.5 on 2021-02-18 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0006_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='contact',
            field=models.CharField(default=123, max_length=256, verbose_name='contact'),
            preserve_default=False,
        ),
    ]