from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

