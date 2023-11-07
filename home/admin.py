from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(Reviews)
admin.site.register(Payments)
admin.site.register(Cart)