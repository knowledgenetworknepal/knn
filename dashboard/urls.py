from django.urls import path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    # user 
    path('', UserListView.as_view(), name='user_list'),
    path('user/<str:username>/', UserDetail.as_view(), name='user_detail'),
    path('user/<str:username>/accept/', ApproveUser.as_view(), name='approve'),
    path('user/<str:username>/reject/', RejectUser.as_view(), name='reject'),

    # books
    path('book/add/', AddBook.as_view(), name='add_book'),
    path('book/', BookList.as_view(), name='book_list'),
    path('book/<str:slug>/', BookDetail.as_view(), name='book_details'),
    path('book/<str:slug>/update/', UpdateBook.as_view(), name='book_update'),

    # deposit
    path('deposit/', DepositList.as_view(), name='deposit_list'),
    path('deposit/<int:pk>/', DepositDetail.as_view(), name='deposit_detail'),
    path('deposit/<int:pk>/verify/', VerifyDeposit.as_view(), name='verify'),
    path('deposit/<int:pk>/unverify/', RejectDeposit.as_view(), name='unverify'),

    # category
    path('category/add/', AddCategory.as_view(), name='add_category'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<slug:slug>/update/', CategoryUpdate.as_view(), name='category_update'),


    # RequestList
    path('request/', RequestList.as_view(), name='request_list'),

    # orders
    path('orders/', OrderList.as_view(), name='orders'),
    path('orders/delivered/', CompletedOrderList.as_view(), name='delivered_orders'),
    path('orders/canceled/', CanceledOrderList.as_view(), name='canceled_orders'),
    path('orders/dispatched/', DispatchedOrderList.as_view(), name='dispatched_orders'),

    path('orders/<int:pk>/dispatch/', DispatchOrder.as_view(), name='dispatched'),
    path('orders/<int:pk>/cancel/', CanceleOrder.as_view(), name='canceled'),
    path('orders/<int:pk>/delivered/', DelivereOrder.as_view(), name='delivered'),

]