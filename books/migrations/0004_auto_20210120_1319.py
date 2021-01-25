# Generated by Django 3.1.5 on 2021-01-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookimage',
            name='main_image',
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='upload/%Y/%M'),
        ),
    ]