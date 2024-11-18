# Generated by Django 5.1.3 on 2024-11-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_email_comms_opt_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email_comms_opt_in',
        ),
        migrations.AddField(
            model_name='profile',
            name='email_comms_opt_in',
            field=models.BooleanField(default=False),
        ),
    ]
