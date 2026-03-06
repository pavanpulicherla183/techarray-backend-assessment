from django.contrib.auth.models import AbstractUser
from django.db import models


class Client(AbstractUser):
    company_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
        ]

    def __str__(self):
        return f"{self.username} - {self.company_name}"