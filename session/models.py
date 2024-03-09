from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Customer


class SessionType(models.TextChoices):
    PS5 = 'PS5', _('PS5')
    PS4 = 'PS4', _('PS4')
    POOL = 'Pool', _('Pool')
    POOL_FRAME = 'PoolFrame', _('PoolFrame')
    SNOOKER = 'Snooker', _('Snooker')
    SNOOKER_FRAME = 'SnookerFrame', _('SnookerFrame')

class Session(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=50, choices=SessionType.choices)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    planned_duration = models.BigIntegerField(null=True, blank=True)
    actual_duration = models.BigIntegerField(null=True, blank=True)
    paid_in_cash = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    paid_online = models.DecimalField(null=True, max_digits=6, decimal_places=2)


class Pricing(models.Model):
    session_type = models.CharField(
        max_length=50,
        choices=SessionType.choices,
        unique=True 
    )
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_frame = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, default=0, blank=True)
    
    def __str__(self):
        return f"{self.get_session_type_display()} - {self.price_per_unit}"