from django.db import models
from store.models import User


class Staff(models.Model):
    """
    Staff model
    """
    role = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.fullname} ({self.role})"