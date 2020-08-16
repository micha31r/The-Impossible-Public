# Generated by Django 2.2.7 on 2020-04-25 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0007_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tagged', to='idea.Tag'),
        ),
    ]
