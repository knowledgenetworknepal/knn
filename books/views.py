from django.views.generic import ListView, DetailView, CreateView
from django.views import View

from .models import Book, CartItem, Category, Review

# if something is needed all over the palce, use this mixin
class BaseMixin():

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category'] = Category.objects.all()
        return context_data


# add new book
# added by the user
class AddNewBookView(BaseMixin, CreateView):
    model = Book
    template_name = ''
    queryset = Book.objects.all()

    # if the isbn already exists, use existing book to keep track, only increase the quantity
    def post(self, request, *args, **kwargs):
        pass


# book list
class ListBooksView(BaseMixin, ListView):
    model = Book
    template_name = 'books/home.html'
    queryset = Book.objects.all().order_by('-id')
    paginate_by = 12
    context_object_name = 'books'

    # this needs to list the featured books, newset books, popular books
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # TODO: needs work
        context_data['famous_books'] = Book.objects.all().order_by('-id')[0:12]

        context_data['featured_books'] = Book.objects.filter(featured=True).order_by('-id')[0:12]
        category = Category.objects.filter(featured=True)
        for cat in category:
            print(cat)
        return context_data


# single book details
# load comments as well
class BookDetailView(BaseMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    queryset = Book.objects.all()
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['reviews'] = Review.objects.filter(book=self.get_object()).order_by('-id')
        return context_data


# add books to cart
# one user can have only 2 books in cart
class AddToCart(View):
    pass


# view the books in cart
class CartView(BaseMixin, ListView):
    model = CartItem
    queryset = CartItem.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


# show cart and location
class ConfirmOrderView(BaseMixin, View):
    pass


# order the books
# users can only order 2 books at a time
class OrderBooks(BaseMixin, View):
    pass


# add book review
class AddReview(BaseMixin, CreateView):
    pass


# add checkout location
# one user can have multiple checkout location
class AddCheckoutLoction(BaseMixin, CreateView):
    pass


