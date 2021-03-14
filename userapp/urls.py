from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegistrationView.as_view() ,name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('deposit/add/', AddDeposit.as_view(), name='add_deposit'),
    path('choice/add/', AddSelection.as_view(), name='add_choice'),
    path('notiiication/', NotificationView.as_view(), name='notiiication'),
    path('review/request/', RequestReviewView.as_view(), name='request_review'),
    path('myaccount/', AccountView.as_view(), name='my_account'),
    path('password/change/', ChangePassword.as_view(), name='change_password'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='userapp/passwordreset/form.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='userapp/passwordreset/confirm.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='userapp/passwordreset/reset.html') , name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userapp/passwordreset/complete.html'), name='password_reset_complete'),

]