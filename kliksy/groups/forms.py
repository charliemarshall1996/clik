
from django.forms import ModelForm

from .models import Groups


class CreateGroupForm(ModelForm):
    class Meta:
        model = Groups
        fields = ['name', 'image', 'category']

    def save(self):
        return super().save(commit=False)
