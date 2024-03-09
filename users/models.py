from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)
    debt = models.IntegerField(default=0, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    ps4_tokens = models.BigIntegerField(default=0)
    ps5_tokens = models.BigIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


