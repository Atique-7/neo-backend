from django.db import models
from session.models import Session
from food.models import Sale

class Transaction(models.Model):
    FULLY_PAID = 'fully_paid'
    UNPAID = 'unpaid'
    PAYMENT_STATUS_CHOICES = [
        (FULLY_PAID, 'Fully Paid'),
        (UNPAID, 'Unpaid'),
    ]

    CASH = 'cash'
    ONLINE = 'online'
    SPLIT = 'split'
    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
        (SPLIT, 'Split'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    food = models.BooleanField(default=False)
    food_sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    unpaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid_online = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=UNPAID)
