# Generated by Django 2.2.7 on 2020-07-14 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0006_auto_20200714_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corefeed',
            name='description',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='corefeed',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
