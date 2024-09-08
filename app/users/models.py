from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    employee_id = models.CharField(max_length=10, unique=True)
    nic = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def __str__(self):
        if self.employee_id:
            return self.employee_id
        return self.username


