# Generated by Django 5.1.3 on 2024-11-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_interests_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='users/default_profile.jpg', upload_to='profile_pics'),
        ),
    ]