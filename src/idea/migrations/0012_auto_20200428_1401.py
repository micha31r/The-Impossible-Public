# Generated by Django 2.2.7 on 2020-04-28 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0011_idea_header_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='header_img',
            field=models.FileField(blank=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
