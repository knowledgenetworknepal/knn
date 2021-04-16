from django.urls import path
from .views import AllBooksView, DeleteCartItem, NewUserView, CategoryView, AddCheckoutLoction, AddNewBookView, AddReview, AddToCart, BookDetailView, CartView, ConfirmOrderView, ListBooksView, OldOrderView, OrderBooks, SearchView

urlpatterns = [
    path('', ListBooksView.as_view(), name='list_books'),
    path('books/', AllBooksView.as_view(), name='all_books'),

    path('book/add/', AddNewBookView.as_view(), name='add_new_book'),
    path('book/<str:slug>/', BookDetailView.as_view(), name='book_details'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category_view'),
    path('search', SearchView.as_view(), name='search'),

    path('book/<str:slug>/review/add/', AddReview.as_view(), name='add_review'), 

    path('book/<str:slug>/cart/add/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/item/<int:pk>/remove/', DeleteCartItem.as_view(), name='delete_cart_item'),

    path('cart/', CartView.as_view(), name='cart'),
    
    path('old/orders/', OldOrderView.as_view(), name='old_orders'),

    path('order/confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('order/checkout/location/', AddCheckoutLoction.as_view(), name='add_checkout_location'),

    path('order/<int:location_id>/', OrderBooks.as_view(), name='order'),
    path('user/unverified/', NewUserView.as_view(), name='unverified'),

]