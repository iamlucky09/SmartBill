from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cashier')
    phone = models.CharField(max_length=15, blank=True, unique=True)
    employee_id = models.CharField(max_length=20, blank=True, unique=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"