from django.forms import ModelForm

from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = (
            'contacted_by',
            'email',
            'phone_number',
            'message'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        