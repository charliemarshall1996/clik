# Generated by Django 5.1.3 on 2024-11-16 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_category_categories'),
        ('groups', '0004_alter_groups_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]
