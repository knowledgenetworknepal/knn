from django.views.generic import ListView, DetailView, CreateView
from django.views import View

from .models import Book, CartItem

# if something is needed all over the palce, use this mixin
class BaseMixin():

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


# add new book
# added by the user
class AddNewBookView(CreateView):
    model = Book
    template_name = ''
    queryset = Book.objects.all()

    # if the isbn already exists, use existing book to keep track, only increase the quantity
    def post(self, request, *args, **kwargs):
        pass


# book list
class ListBooksView(ListView):
    model = Book
    template_name = ''
    queryset = Book.objects.filter(featured=True)
    paginate_by = 12

    # this needs to list the featured books, newset books, popular books
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


# single book details
class BookDetailView(DetailView):
    model = Book
    template_name = ''
    queryset = Book.objects.all()
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


# add books to cart
# one user can have only 2 books in cart
class AddToCart(View):
    pass


# view the books in cart
class CartView(ListView):
    model = CartItem
    queryset = CartItem.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


# show cart and location
class ConfirmOrderView(View):
    pass


# order the books
# users can only order 2 books at a time
class OrderBooks(View):
    pass


# add book review
class AddReview(CreateView):
    pass


# add checkout location
# one user can have multiple checkout location
class AddCheckoutLoction(CreateView):
    pass


