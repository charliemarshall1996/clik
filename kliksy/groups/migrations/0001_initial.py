# Generated by Django 5.1.3 on 2024-11-15 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_rename_category_categories'),
        ('users', '0018_remove_profile_interests'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_group_pic.png', upload_to='group_pics')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ManyToManyField(related_name='groups', to='core.categories')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to='users.profile')),
                ('members', models.ManyToManyField(blank=True, null=True, related_name='groups', to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_event_pic.png', upload_to='event_pics')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=100)),
                ('attendants', models.ManyToManyField(related_name='events', to='users.profile')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='groups.groups')),
            ],
        ),
    ]
