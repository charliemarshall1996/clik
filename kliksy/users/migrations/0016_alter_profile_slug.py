# Generated by Django 5.1.3 on 2024-11-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(auto_created=True, blank=True, max_length=30, unique=True),
        ),
    ]
