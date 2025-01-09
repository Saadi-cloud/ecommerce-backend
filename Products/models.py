from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

# functionaloity of cart
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class Checkout(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online'),
    ]

    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    products = models.ManyToManyField(Product, through='CheckoutProduct')
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class CheckoutProduct(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()