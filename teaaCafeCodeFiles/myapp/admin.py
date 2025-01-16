from django.contrib import admin
from .models import Product, Order, OrderItem, CustomUser, Location,Invoice

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CustomUser)
admin.site.register(Invoice)
admin.site.register(Location)