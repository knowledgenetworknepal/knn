from django.views.generic.edit import UpdateView
from books.models import Order, CheckoutAddress
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import DepositForm, RegistrationForm, Loginform, UserUpdateForm, PasswordForm
from .models import Deposit, Request, Notification as Notice
from books.forms import CheckoutAddressForm
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
        context_data['address_form'] = CheckoutAddressForm
        return context_data

    def post(self, request, *args, **kwargs):
        registration = RegistrationForm(request.POST)
        address = CheckoutAddressForm(request.POST)

        if registration.is_valid and address.is_valid():
            user = registration.save(commit=False)
            user.contact = address.cleaned_data.get('phone_number')
            user.save()

            user_address = address.save(commit=False)
            user_address.user = user
            user_address.save()
            
            return reverse_lazy('registration') 
        return reverse_lazy('registration') 


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
            Notice.objects.create(deposit=deposit, sender=user, message=f'New Deposit by {user.first_name} {user.last_name}')
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))


class RequestReviewView(BaseMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        req = Request.objects.get_or_create(user=user, status=False)
        Notice.objects.create(request=req, sender=user, message=f'Requested Review for {user.first_name} {user.last_name}')
        return redirect(request.META.get('HTTP_REFERER'))   


class AccountView(BaseMixin, UpdateView):
    model = User
    template_name = 'userapp/myaccount.html'
    form_class = UserUpdateForm
    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        user = self.request.user
        context_data = super().get_context_data(**kwargs)
        context_data['orders'] = Order.objects.prefetch_related('books').filter(user=user)
        context_data['checkout_location'] = CheckoutAddress.objects.filter(user=self.request.user)
        context_data['password_form'] = PasswordForm
        return context_data

    def get_success_url(self):
        return reverse_lazy('my_account')


class ChangePassword(View):
    def post(self, request, *args, **kwargs):
        password = PasswordForm(request.POST)
        if password.is_valid():
            cpw = password.cleaned_data.get('current_password')
            pw = password.cleaned_data.get('password1')
            user = request.user
            user = authenticate(username=user, password=cpw)
            if user is not None:
                user.set_password(pw)
                user.save()
        return redirect(request.META.get('HTTP_REFERER'))   


