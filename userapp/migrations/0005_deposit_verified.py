# Generated by Django 3.1.5 on 2021-02-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_auto_20210120_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
