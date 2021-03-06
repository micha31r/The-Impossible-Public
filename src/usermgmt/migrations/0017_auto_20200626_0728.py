# Generated by Django 2.2.7 on 2020-06-26 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermgmt', '0016_auto_20200626_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blocked_user',
        ),
        migrations.AddField(
            model_name='profile',
            name='blocked_user',
            field=models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
