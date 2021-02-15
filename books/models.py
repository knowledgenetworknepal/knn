import random

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    featured = models.BooleanField(default=False)    
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.category_name)
        except:
            self.slug = slugify(self.category_name)+random.randint(0,99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


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
    image = models.ImageField(upload_to='upload/%Y/%M', null=True, blank=True)
    count = models.IntegerField(default=0)
    available = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.book_name)
        except:
            self.slug = slugify(self.book_name)+random.randint(0,99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.book_name


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_image')
    image = models.ImageField(upload_to='upload/%Y/%M')


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

    def __str__(self):
        return self.book.book_name


class Review(models.Model):
    STAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_review')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    review = models.CharField(max_length=200)
    review_date = models.DateTimeField(auto_now=True)
    edited_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=STAR, max_length=20, null=True, blank=True)

    def __str__(self):
        return self.book.book_name

        
# COULD: this could be used
class Favourite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favourite_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favourite')


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
    books = models.ManyToManyField(Book)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    address = models.ForeignKey(CheckoutAddress, null=True, blank=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivery_status = models.CharField(choices=DELIVERY_STATUS, max_length=20, default='none')


class Featured(models.Model):
    AD_TYPE = (
        ('none','none'),
        ('main','mani'),
        ('footer','footer')
    )
    image = models.ImageField(upload_to='upload/%Y/%M')
    title = models.CharField(max_length=100)
    url = models.URLField()
    sub_title = models.CharField(max_length=100)
    type = models.CharField(choices=AD_TYPE, max_length=50)
    status = models.BooleanField(default=True)

