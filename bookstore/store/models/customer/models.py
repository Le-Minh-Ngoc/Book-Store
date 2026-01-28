from django.db import models
from store.models import User


class Address(models.Model):
    """
    Address model for users
    """
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.num} {self.street}, {self.city}"


class Customer(models.Model):
    """
    Customer model
    """
    email = models.EmailField(unique=True, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.fullname


class MemberShip(models.Model):
    """
    Membership model for customers
    """
    id = models.CharField(max_length=50, primary_key=True)
    point = models.IntegerField(default=0)
    level = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.fullname} - {self.level}"