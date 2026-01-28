from django.db import models
from store.models.customer.models import Customer
from store.models.book.models import Book


class Cart(models.Model):
    """
    Shopping cart model
    """
    id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.customer.user.fullname}"


class CartItem(models.Model):
    """
    Item in shopping cart model
    """
    id = models.CharField(max_length=50, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in cart"


class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.fullname}"


class OrderItem(models.Model):
    """
    Item in an order model
    """
    id = models.CharField(max_length=50, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in order {self.order.id}"


class Shipping(models.Model):
    """
    Shipping model
    """
    id = models.CharField(max_length=50, primary_key=True)
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_info')

    def __str__(self):
        return f"Shipping for order {self.order.id}"


class Payment(models.Model):
    """
    Payment model
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_info')

    def __str__(self):
        return f"Payment for order {self.order.id} - {self.status}"


class Rating(models.Model):
    """
    Rating model
    """
    SCORE_CHOICES = [(i, i) for i in range(1, 6)]

    id = models.CharField(max_length=50, primary_key=True)
    score = models.IntegerField(choices=SCORE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.fullname} rated {self.book.title}: {self.score}/5"


class Voucher(models.Model):
    """
    Voucher model for discounts
    """
    id = models.CharField(max_length=50, primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # percentage or fixed amount
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voucher {self.code}"


class Invoice(models.Model):
    """
    Invoice model
    """
    id = models.CharField(max_length=50, primary_key=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')

    def __str__(self):
        return f"Invoice for order {self.order.id}"


class OrderHistory(models.Model):
    """
    Order history model to track status changes
    """
    id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=50)
    update_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')

    def __str__(self):
        return f"Status {self.status} for order {self.order.id}"