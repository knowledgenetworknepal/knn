from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)


class Author(models.Model):
    author_name = models.CharField(max_length=50)
    author_details = models.TextField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='upload/%Y/%M', null=True, blank=True)


class Book(models.Model):
    book_name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100, unique=True)
    book_pages = models.IntegerField()
    book_description = models.TextField(max_length=500)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_category')
    price = models.FloatField()
    slug = models.SlugField(unique=True, blank=True)
    featured = models.BooleanField(default=False)    


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_image')
    image = models.ImageField(upload_to='upload/%Y/%M')
    main_image = models.BooleanField(default=False)


class BookUpload(models.Model):
    BOOK_STATUS = (
        ('new','new'),
        ('lost','lost'),
        ('none','none')
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_quantity')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    added_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=BOOK_STATUS, default='none', max_length=20)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_review')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    review = models.CharField(max_length=200)
    review_date = models.DateTimeField(auto_now=True)
    edited_date = models.DateTimeField(auto_now_add=True)
    

class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    ordered = models.BooleanField(default=False)


class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    DELIVERY_STATUS = (
        ('none','none'),
        ('delivered','delivered'),
        ('canceled','canceled'),

    )
    order_date = models.DateTimeField(auto_now_add=True)
    books = models.ManyToManyField(CartItem)
    address = models.ForeignKey(CheckoutAddress, null=True, blank=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivery_status = models.CharField(choices=DELIVERY_STATUS, max_length=20, default='none')

