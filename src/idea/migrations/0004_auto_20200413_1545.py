# Generated by Django 2.2.7 on 2020-04-13 03:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('idea', '0003_idea_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='liked_user',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='viewed_user',
            field=models.ManyToManyField(blank=True, related_name='viewed', to=settings.AUTH_USER_MODEL),
        ),
    ]
