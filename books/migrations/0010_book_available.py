# Generated by Django 3.1.5 on 2021-02-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='available',
            field=models.IntegerField(default=0),
        ),
    ]
