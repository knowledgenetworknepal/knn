from django.urls import path
from .views import NewUserView, AddCheckoutLoction, AddNewBookView, AddReview, AddToCart, BookDetailView, CartView, ConfirmOrderView, ListBooksView, OrderBooks

urlpatterns = [
    path('', ListBooksView.as_view(), name='list_books'),
    path('book/add/', AddNewBookView.as_view(), name='add_new_book'),
    path('book/<str:slug>/', BookDetailView.as_view(), name='book_details'),

    path('book/<str:slug>/review/add/', AddReview.as_view(), name='add_review'), 

    path('book/<str:slug>/cart/add/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),

    path('order/confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('order/checkout/location/', AddCheckoutLoction.as_view(), name='add_checkout_location'),

    path('order/<int:location_id>/', OrderBooks.as_view(), name='order'),
    path('user/unverified/', NewUserView.as_view(), name='unverified'),

]