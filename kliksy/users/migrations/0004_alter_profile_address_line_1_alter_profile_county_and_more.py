# Generated by Django 5.1.3 on 2024-11-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_address_line_1_profile_address_line_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address_line_1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='county',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='postalcode',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='town',
            field=models.CharField(max_length=25),
        ),
    ]
