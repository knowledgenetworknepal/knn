# Generated by Django 3.1.5 on 2021-02-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]