from django.db import models
from django.contrib.auth.models import AbstractUser #inbuilt class, provides functionality for user auth
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=15) 
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    house = models.CharField(max_length=100)

class Location (models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='orders')
    date_ordered = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_item = models.BooleanField(default=False)  # Add the last_item field


class Invoice(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(default=timezone.now)
    prod_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    
    