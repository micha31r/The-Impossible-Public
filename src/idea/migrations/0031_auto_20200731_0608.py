# Generated by Django 2.2.7 on 2020-07-31 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0030_auto_20200715_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='full_description',
            field=models.TextField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='idea',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='idea',
            name='short_description',
            field=models.TextField(max_length=200),
        ),
    ]