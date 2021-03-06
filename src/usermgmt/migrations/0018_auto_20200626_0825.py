# Generated by Django 2.2.7 on 2020-06-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0017_auto_20200626_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comment_setting',
            field=models.IntegerField(choices=[(1, 'No Comments'), (2, 'From Followers'), (3, 'From Everyone')], default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='discover_setting',
            field=models.IntegerField(choices=[(1, 'Hide'), (2, 'Discoverable')], default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='like_setting',
            field=models.IntegerField(choices=[(1, 'Off'), (2, 'From Followers'), (3, 'From Everyone')], default=1),
        ),
    ]
