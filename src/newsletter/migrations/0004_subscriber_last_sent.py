# Generated by Django 2.2.7 on 2020-07-15 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_remove_subscriber_last_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='last_sent',
            field=models.DateTimeField(auto_now=True),
        ),
    ]