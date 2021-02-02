from django import forms
from django.forms import models
from .models import Review, CheckoutAddress, BookUpload, Book, BookImage


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)


class CheckoutAddressForm(forms.ModelForm):
    class Meta:
        model = CheckoutAddress
        fields = ('city','street','phone_number')


class BookForm(forms.ModelForm):
    isbn_number = forms.CharField(max_length=200, required=True)
    class Meta:
        model = Book
        fields = ('book_name','isbn_number','book_pages','book_description','price','image')


