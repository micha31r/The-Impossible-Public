# Generated by Django 2.2.7 on 2020-06-12 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0006_profile_daily_limit_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=160),
        ),
    ]
