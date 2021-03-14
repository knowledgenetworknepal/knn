from django.contrib import admin
from .models import CustomUser, Notification, Deposit, Request, SignupChoice

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Notification)
admin.site.register(Deposit)
admin.site.register(Request)
admin.site.register(SignupChoice)

