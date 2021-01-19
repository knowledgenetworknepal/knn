from django.contrib import admin
from .models import *


admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(BookImage)
admin.site.register(BookUpload)
admin.site.register(Review)
admin.site.register(Author)
admin.site.register(CheckoutAddress)
admin.site.register(Order)