# Generated by Django 5.1.3 on 2024-11-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_categories_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenCageAPIRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_request', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
