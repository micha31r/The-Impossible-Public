# Generated by Django 2.2.7 on 2020-05-02 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userupload', '0004_auto_20200502_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usermgmt.Profile'),
        ),
    ]