from typing import List
from .models import Event
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class Eventform(BaseForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'event_date',
            'featured_image'
        )
        widgets = {
            'event_date': DateInput()
        }

