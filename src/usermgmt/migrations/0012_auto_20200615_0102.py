# Generated by Django 2.2.7 on 2020-06-15 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0011_profile_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message_status',
            field=models.IntegerField(choices=[(1, 'Private'), (2, 'Public'), (3, 'Dissmissed')], default=1),
        ),
    ]
