from knn.userapp.models import Notification
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view() ,name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('notiiication/', NotificationView.as_view(), name='notiiication')
    
]