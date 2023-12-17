# Generated by Django 4.1.7 on 2023-11-24 13:21

from django.db import migrations, models

import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_folders_date_remove_folders_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='folders',
            name='fdate',
            field=models.DateField(default=datetime.date.today().strftime("%Y-%m-%d"), verbose_name='Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folders',
            name='ftime',
            field=models.TimeField(default=datetime.datetime.now().strftime("%H:%M:%S"), verbose_name='Time'),
            preserve_default=False,
        ),
    ]