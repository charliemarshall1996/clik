# Generated by Django 5.1.3 on 2024-11-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]