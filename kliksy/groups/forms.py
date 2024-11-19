
from django.forms import ModelForm, DateInput, TimeInput, CheckboxSelectMultiple
from mptt.forms import TreeNodeMultipleChoiceField

from core.models import Category

from .models import Group, Event


class CreateGroupForm(ModelForm):

    category = TreeNodeMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=CheckboxSelectMultiple
    )

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
