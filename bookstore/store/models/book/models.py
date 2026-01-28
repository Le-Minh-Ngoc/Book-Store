from django.db import models


class Category(models.Model):
    """
    Book category model
    """
    type = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type


class Publisher(models.Model):
    """
    Publisher model
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Author model
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model
    """
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    instock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title