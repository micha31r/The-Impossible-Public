# Generated by Django 2.2.7 on 2020-07-15 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_auto_20200715_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='last_sent',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
