# Generated by Django 3.1.5 on 2021-02-20 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_customuser_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='deposit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deposit_notificaiton', to='userapp.deposit'),
        ),
    ]