
import re
from django.db import models

# Create your models here.
from core.models import Category
from users.models import Profile


class Group(models.Model):
    image = models.ImageField(
        upload_to='group_pics', default='default_group_pic.png', blank=True)
    name = models.CharField(max_length=100, unique=True)
    formatted_name = models.CharField(max_length=100, unique=True, blank=True)
    creator = models.ForeignKey(
        Profile, related_name='created_groups', on_delete=models.CASCADE)
    members = models.ManyToManyField(
        Profile, related_name='groups', blank=True)
    category = models.ManyToManyField(
        Category, related_name='groups')
    description = models.TextField(max_length=1500)

    def save(self):

        formatted_name = self.name.lower().strip().replace(" ",
                                                           "_").replace("&", "and")

        self.formatted_name = re.sub(
            r'[ \x00-\x1F\x7F"#%<>[\\\]^`{|}~]', '_', formatted_name)

        super().save()


class Event(models.Model):
    image = models.ImageField(
        upload_to="event_pics", default="default_event_pic.png", blank=True)
    group = models.ForeignKey(
        Group, related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(Profile, related_name='events')
