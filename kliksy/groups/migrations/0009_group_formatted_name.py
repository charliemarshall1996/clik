# Generated by Django 5.1.3 on 2024-11-18 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_rename_attendants_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='formatted_name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]