# Generated by Django 4.1.7 on 2023-11-24 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_files_name_alter_files_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='name',
        ),
    ]
