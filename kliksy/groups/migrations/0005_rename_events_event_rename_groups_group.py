# Generated by Django 5.1.3 on 2024-11-16 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_categories_category'),
        ('groups', '0004_alter_groups_image'),
        ('users', '0018_remove_profile_interests'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
        migrations.RenameModel(
            old_name='Groups',
            new_name='Group',
        ),
    ]
