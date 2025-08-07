from django.contrib import admin
from EshopApp.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(Booking)
admin.site.register(ContactMessage)

