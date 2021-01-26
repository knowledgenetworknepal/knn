from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class Loginform(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


