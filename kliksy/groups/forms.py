
from django.forms import ModelForm, DateInput, TimeInput

from .models import Group, Event


class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'image', 'description', 'category']

    def save(self):
        return super().save(commit=False)


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['image', 'name', 'description', 'date', 'time', 'location']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }

    def save(self):
        return super().save(commit=False)
