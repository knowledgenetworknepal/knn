# Generated by Django 3.1.5 on 2021-02-25 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_category_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]