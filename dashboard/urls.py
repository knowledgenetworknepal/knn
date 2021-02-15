from django.urls import path

from .views import UserListView, UserDetail, DepositList, DepositDetail

app_name = 'dashboard'

urlpatterns = [
    # user 
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),

    # deposit
    path('deposit/', DepositList.as_view(), name='deposit_list'),
    path('deposit/<int:pk>/', DepositDetail.as_view(), name='deposit_detail'),

]