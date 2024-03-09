from django.db import models
from users.models import Customer

class Beverage(models.Model):
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  inventory = models.PositiveIntegerField(default=0)

  def __str__(self):
    return self.name


class Sale(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.customer.username} - {self.beverage.name} ({self.quantity})"
