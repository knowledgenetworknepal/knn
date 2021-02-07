from django.contrib import admin

from .models import Contact, BaseInfo, Ads

admin.site.register(Contact)
admin.site.register(Ads)

admin.site.register(BaseInfo)
