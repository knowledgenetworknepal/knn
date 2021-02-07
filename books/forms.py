from django import forms
from django.forms import models
from .models import Review, CheckoutAddress, BookUpload, Book, BookImage


class BaseForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ReviewForm(BaseForm):
    class Meta:
        model = Review
        fields = ('review',)


class CheckoutAddressForm(BaseForm):
    class Meta:
        model = CheckoutAddress
        fields = ('city','street','phone_number')


class BookForm(BaseForm):
    isbn_number = forms.CharField(max_length=200, required=True)
    class Meta:
        model = Book
        fields = ('book_name','isbn_number','book_pages','book_description','price','image')


