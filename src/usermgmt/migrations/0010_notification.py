# Generated by Django 2.2.7 on 2020-06-14 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0009_auto_20200613_0517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message_status', models.IntegerField(choices=[(1, 'Private'), (2, 'Public')], default=1)),
            ],
        ),
    ]
