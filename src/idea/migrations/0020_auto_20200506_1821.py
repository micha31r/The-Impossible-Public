# Generated by Django 2.2.7 on 2020-05-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0019_idea_body_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='publish_stats',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Public'), (3, 'Followers only')], default=1),
        ),
    ]
