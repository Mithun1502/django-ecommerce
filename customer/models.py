from django.db import models
from django.contrib.auth.models import User
from custom_admin.models import Product


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile = models.CharField(max_length=10, unique=True)

    address = models.TextField(max_length=266, blank=True, null=True)
    def __str__(self):
        return self.user.username

# class Order(models.Model):
#     customer_name = models.CharField(max_length=100)
#     customer_email = models.EmailField()
#     mobile = models.CharField(max_length=10)

#     product_name = models.CharField(max_length=200)
#     quantity = models.PositiveIntegerField()
#     total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.customer_name
