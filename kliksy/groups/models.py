from django.db import models

# Create your models here.
from core.models import Category
from users.models import Profile


class Group(models.Model):
    image = models.ImageField(
        upload_to='group_pics', default='group_pics/default_group_pic.png', blank=True)
    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(
        Profile, related_name='created_groups', on_delete=models.CASCADE)
    members = models.ManyToManyField(
        Profile, related_name='groups', blank=True)
    category = models.ManyToManyField(
        Category, related_name='groups')
    description = models.TextField(max_length=1500)


class Event(models.Model):
    image = models.ImageField(
        upload_to="event_pics", default="default_event_pic.png"
    )
    group = models.ForeignKey(
        Group, related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    attendants = models.ManyToManyField(Profile, related_name='events')
