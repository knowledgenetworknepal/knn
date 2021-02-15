from django.urls import path

from .views import UserListView

app_name = 'dashboard'

urlpatterns = [
    path('userlist/', UserListView.as_view(), name='user_list' ),
]