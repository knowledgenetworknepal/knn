from django.urls import path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    # user 
    path('', UserListView.as_view(), name='user_list'),
    path('user/approved/', ApprovedUserList.as_view(), name='approved_users'),
    path('user/unapproved/', UnapprovedUserList.as_view(), name='unapproved_users'),
    path('user/<str:username>/', UserDetail.as_view(), name='user_detail'),

    path('user/<str:username>/accept/', ApproveUser.as_view(), name='approve'),
    path('user/<str:username>/reject/', RejectUser.as_view(), name='reject'),
    path('user/<str:username>/book/receive/', ReceiveBook.as_view(), name='receive_book'),

    # books
    path('book/add/', AddBook.as_view(), name='add_book'),
    path('book/', BookList.as_view(), name='book_list'),
    path('book/available/', AvailabelBookList.as_view(), name='available_books'),
    path('book/unavailable/', UnavailabelBookList.as_view(), name='unavailable_books'),

    path('book/<str:slug>/', BookDetail.as_view(), name='book_details'),
    path('book/<str:slug>/update/', UpdateBook.as_view(), name='book_update'),
    path('book/delete', DeleteBook.as_view(), name='book_delete'),

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
    path('category/delete', CategoryDelete.as_view(), name='category_delete'),

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

    # search
    path('user/search/', UserSearch.as_view(), name='user_search'),
    path('book/search/', BookSearch.as_view(), name='book_search'),
    path('order/search/', OrderSearch.as_view(), name='order_search'),

    # ads
    path('ads/', AdsView.as_view(), name='ads'),
    path('ads/<int:pk>/', AdsDetailView.as_view(), name='ad_details'),
    path('ads/add/', CreateAd.as_view(), name='ad_create'),
    path('ads/<int:pk>/update/', UpdateAd.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete', DeleteAd.as_view(), name='ad_delete'),

    # contact
    path('messages', ContactView.as_view(), name='contact'),

    # blog
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
    path('blog/add/', CreateBlog.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', UpdateBlog.as_view(), name='blog_update'),
    path('blog/delete', DeleteBlog.as_view(), name='blog_delete'),

    # event
    path('event/', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/add/', CreateEvent.as_view(), name='event_create'),
    path('event/<int:pk>/update/', UpdateEvent.as_view(), name='event_update'),
    path('event/delete', DeleteEvent.as_view(), name='event_delete'),

]