from django.db import models
from store.models.staff.models import Staff
from store.models.book.models import Book


class Supplier(models.Model):
    """
    Supplier model for managing book suppliers
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ImportSlip(models.Model):
    """
    Import slip model for tracking book imports
    """
    id = models.CharField(max_length=50, primary_key=True)
    import_date = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='import_slips_created')
    manager = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='import_slips_managed')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Import Slip {self.id}"


class ImportSlipDetail(models.Model):
    """
    Import slip detail model for tracking individual book imports
    """
    id = models.CharField(max_length=50, primary_key=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    import_slip = models.ForeignKey(ImportSlip, on_delete=models.CASCADE, related_name='details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Import Detail for {self.book.title}"