from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4, UUID


class User(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    mail_dir = models.CharField(max_length=2000, null=True, blank=True)
    reset_password = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    hash = models.CharField(max_length=200, null=True, blank=True)
    hash_key = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.email
