from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import RegistrationForm, Loginform


User = get_user_model()


# new user registration view
# send login form as well
class UserRegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'userapp/register.html'
    success_url = reverse_lazy('list_books')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_form'] = Loginform
        return context_data


# user login view
class LoginView(View):
    model = User
    success_url = reverse_lazy('list_books')

    def post(self, request, *args, **kwargs):
        form = Loginform(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(reverse_lazy('list_books'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("register"))


# view the user notificaiton
class NotificationView(View):
    pass


