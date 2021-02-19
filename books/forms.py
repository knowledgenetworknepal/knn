from django import forms
from django.forms import models
from .models import Review, CheckoutAddress, BookUpload, Book, BookImage, Category


class BaseForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ReviewForm(BaseForm):
    class Meta:
        model = Review
        fields = ('review','rating')


class CheckoutAddressForm(BaseForm):
    class Meta:
        model = CheckoutAddress
        fields = ('city','street','phone_number')


class BookForm(BaseForm):
    isbn_number = forms.CharField(max_length=200, required=True)
    class Meta:
        model = Book
        fields = ('book_name','isbn_number','book_pages','book_description','price','image')


class AdminBookForm(BaseForm):
    class Meta:
        model = Book
        fields = ('book_name','isbn','available','book_pages','book_description','price','image','featured')


class CategoryForm(BaseForm):
    class Meta:
        model = Category
        fields = ('category_name','description','featured')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured'].widget.attrs['class'] = 'form-control'