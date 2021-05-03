from django.forms import ModelForm

from .models import Contact, Ads


class BaseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.field[field].widget.attrs['class'] = 'form-control'


class ContactForm(BaseForm):
    class Meta:
        model = Contact
        fields = (
            'contacted_by',
            'email',
            'phone_number',
            'message'
        )


class AdForm(BaseForm):
    class Meta:
        model = Ads
        fields = (
            'image',
            'title',
            'sub_title',
            'ad_type',
            'action_url',
            'status'
        )

        