from typing import List
from django.http import request
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from .models import Book, BookUpload, CartItem, Category, Review, CheckoutAddress, Order
from .forms import ReviewForm, CheckoutAddressForm, BookForm

from userapp.forms import DepositForm
from userapp.models import Deposit
from base.models import Ads

# if something is needed all over the palce, use this mixin
class BaseMixin():

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['categories'] = Category.objects.all()
        if user.is_authenticated:
            context_data['cart_items'] = CartItem.objects.select_related('book').filter(user=user, ordered=False)
            context_data['amount'] = 100
        return context_data


# checks if the account is approved or not
class AccountAccessMixin():

    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user.approved:
            return dispatch
        return redirect(reverse_lazy('unverified'))


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
        context_data['hero_ads'] = Ads.objects.filter(ad_type='Hero', status=True)
        return context_data


class CategoryView(BaseMixin, ListView):
    model = Book
    template_name = 'books/category.html'
    paginate_by = 1
    context_object_name = 'books'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category'] = self.get_object()
        return context_data

    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(category=self.get_object())    


# single book details
# load comments as well
class BookDetailView(BaseMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    queryset = Book.objects.all()
    slug_url_kwarg = 'slug'        

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        book = self.get_object()
        book.count += 1
        book.save()
        context_data['reviews'] = Review.objects.select_related('added_by').filter(book=book).order_by('-id')
        context_data['review_count'] = context_data['reviews'].count()

        context_data['review_form'] = ReviewForm
        return context_data


# add books to cart
# one user can have only 2 books in cart
class AddToCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        book = get_object_or_404(Book, slug=self.kwargs.get('slug'))
        cart_item = CartItem.objects.filter(user=user, ordered=False)
        if cart_item.filter(book=book).exists():
            # cant order 2 same book
            return redirect(request.META.get('HTTP_REFERER'))
        if not cart_item.count() < 2:
            # count not greater than 2
            return redirect(request.META.get('HTTP_REFERER'))
       
        cart = CartItem.objects.create(book=book, user=user)
        return redirect(request.META.get('HTTP_REFERER'))


# delete car item
class DeleteCartItem(View):
    def get(self, request, *args, **kwargs):
        CartItem.objects.get(id=self.kwargs.get('pk')).delete()
        return redirect(request.META.get('HTTP_REFERER'))


# view the books in cart
class CartView(BaseMixin, AccountAccessMixin, ListView):
    model = CartItem
    queryset = CartItem.objects.all()
    template_name = 'books/cart.html'

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.prefetch_related('book').filter(user=user, ordered=False)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
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
        context_data['cart_items'] = CartItem.objects.prefetch_related('book').filter(user=self.request.user, ordered=False)
        return context_data


# order the books
# users can only order 2 books at a time
class OrderBooks(LoginRequiredMixin, AccountAccessMixin, BaseMixin, View):
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
        # books.update(available=F('available')-1)
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


# new user needs to add 3 books and deposit 200 before being approved
class NewUserView(ListView):
    model = Book
    template_name = 'userapp/new_user.html'

    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user.approved:
            return redirect(reverse_lazy('cart'))
        return dispatch

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        if self.get_queryset().count() < 3:
            context_data['book_form'] = BookForm
        context_data['deposit_form'] = DepositForm
        context_data['deposits'] = Deposit.objects.filter(user=user)

        return context_data
    
    def get_queryset(self):
        user_book = BookUpload.objects.filter(added_by=self.request.user)
        return Book.objects.filter(book_quantity__in=user_book)


class SearchView(BaseMixin, ListView):
    model = Book
    template_name = 'books/category.html'
    paginate_by = 12
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        word = self.request.GET.get('search')
        context_data = super().get_context_data(**kwargs)
        context_data['category'] = word
        return context_data

    def get_queryset(self, *args, **kwargs):
        word = self.request.GET.get('search')
        return Book.objects.filter(book_name__icontains=word)    


class OldOrderView(ListView):
    model = CartItem
    template_name = 'books/cartitems.html'
    paginate_by = 12
    context_object_name = 'cart_items'

    def get_queryset(self, *args, **kwargs):
        return CartItem.objects.select_related('books').filter(ordered=True, user=request.user)

        