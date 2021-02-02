from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookUpload, CartItem, Category, Review, CheckoutAddress, Order
from .forms import ReviewForm, CheckoutAddressForm, BookForm

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
    queryset = Book.objects.none()
    form_class = BookForm

    # if the isbn already exists, use existing book to keep track, only increase the quantity
    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)        
        if form.is_valid():
            isbn = form.cleaned_data.get('isbn_number')
            print(isbn)
            if Book.objects.filter(isbn=isbn).exists():
                book = get_object_or_404(Book, isbn=isbn)
            else:
                book = form.save(commit=False)
                book.isbn = isbn
                book.save()
            BookUpload.objects.create(book=book, added_by=request.user, status='new')
            book.available += 1
            book.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))


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
        context_data['famous_books'] = Book.objects.all().order_by('-count')[0:12]
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
        book = self.get_object()
        book.count += 1
        book.save()
        context_data = super().get_context_data(**kwargs)
        context_data['count'] = BookUpload.objects.filter(book=self.get_object()).count()
        context_data['reviews'] = Review.objects.filter(book=self.get_object()).order_by('-id')
        context_data['review_form'] = ReviewForm
        return context_data


# add books to cart
# one user can have only 2 books in cart
class AddToCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        book = get_object_or_404(Book, slug=self.kwargs.get('slug'))
        if not CartItem.objects.filter(user=user, ordered=False).count() < 2:
            # count not greater than 2
            return redirect(request.META.get('HTTP_REFERER'))
        if CartItem.objects.filter(book=book, user=user, ordered=False).exists():
            # cant order 2 same book
            return redirect(request.META.get('HTTP_REFERER'))
        cart = CartItem.objects.create(book=book, user=user)
        return redirect(request.META.get('HTTP_REFERER'))


# view the books in cart
class CartView(BaseMixin, ListView):
    model = CartItem
    queryset = CartItem.objects.all()
    template_name = 'books/cart.html'

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user, ordered=False)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['old_order'] = CartItem.objects.filter(user=user, ordered=True)
        return context_data


# show cart and location
class ConfirmOrderView(LoginRequiredMixin, BaseMixin, ListView):
    model = CheckoutAddress
    template_name = 'books/location_page.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return CheckoutAddress.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['location_form'] = CheckoutAddressForm
        context_data['cart_items'] = CartItem.objects.filter(user=self.request.user, ordered=False)
        return context_data


# order the books
# users can only order 2 books at a time
class OrderBooks(LoginRequiredMixin, BaseMixin, View):
    def post(self, request, *args, **kwargs):
        location = get_object_or_404(CheckoutAddress, id=self.kwargs.get('location_id'))
        cart_items = CartItem.objects.filter(user=request.user, ordered=False)
        cart_books = cart_items.values_list('book_id', flat=True)
        books = Book.objects.filter(id__in=cart_books)
        order = Order.objects.create(user=request.user)
        order.books.add(*books)
        order.address = location
        order.save()
        cart_items.update(ordered=True)
        books.update(available=F('available')-1)
        return redirect(reverse_lazy("list_books"))


# add book review
class AddReview(LoginRequiredMixin, BaseMixin, View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs.get('slug'))
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.added_by = request.user
            review.save()
        return redirect(request.META.get('HTTP_REFERER'))


# add checkout location
# one user can have multiple checkout location
class AddCheckoutLoction(LoginRequiredMixin, BaseMixin, View):
    def post(self, request, *args, **kwargs):
        form = CheckoutAddressForm(data=request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.user = request.user
            loc.save()
        return redirect(request.META.get('HTTP_REFERER'))


class NewUserView(ListView):
    model = Book
    template_name = 'userapp/new_user.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.get_queryset().count() < 3:
            context_data['book_form'] = BookForm
        return context_data
    
    def get_queryset(self):
        user_book = BookUpload.objects.filter(added_by=self.request.user)
        return Book.objects.filter(book_quantity__in=user_book)

