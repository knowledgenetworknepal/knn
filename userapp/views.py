from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views import View

from .forms import RegistrationForm


User = get_user_model()


# new user registration view
# TODO: send login form as well
class UserRegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'userapp/register.html'

    def get_success_url(self):
        pass

    def get_context_data(self, request, *args, **kwargs):
        context_data = super().get_context_data()
        return context_data


# user login view
class LoginView(View):
    model = User
    form_class = RegistrationForm
    template_name = ''

    def post(self, request, *args, **kwargs):
        pass

    def get_success_url(self):
        pass


def logout_user(request):
    pass


# view the user notificaiton
class NotificationView(View):
    pass


