# Generated by Django 4.1.7 on 2023-11-19 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_files_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='specialname',
        ),
        migrations.AddField(
            model_name='folders',
            name='specialname',
            field=models.CharField(default=' ', max_length=256, unique=True, verbose_name='Special Name'),
            preserve_default=False,
        ),
    ]
