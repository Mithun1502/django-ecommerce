from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)

    def __str__(self):
        return self.shop_name


class Product(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="products/")
    description = models.CharField(max_length=250)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MaxValueValidator(9999999999)]
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
