from django.db import models

# Create your models here.
from core.models import Categories
from users.models import Profile


class Groups(models.Model):
    image = models.ImageField(
        upload_to='group_pics', default='default_profile_pic.jpg')
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name='groups')
    category = models.ManyToManyField(Categories, related_name='groups')


class Events(models.Model):
    group = models.ForeignKey(
        Groups, related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    attendants = models.ManyToManyField(Profile, related_name='events')
