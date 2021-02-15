from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import DepositForm, RegistrationForm, Loginform
from .models import Deposit

from books.views import BaseMixin

User = get_user_model()


# new user registration view
# send login form as well
class UserRegistrationView(BaseMixin, CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'userapp/register.html'
    success_url = reverse_lazy('list_books')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_form'] = Loginform
        context_data['base_rate'] = 50
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
        return redirect(reverse_lazy("registration"))


# view the user notificaiton
class NotificationView(View):
    pass


class AddDeposit(BaseMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = user
            deposit.save()
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))
