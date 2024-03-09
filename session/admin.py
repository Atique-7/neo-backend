from django.contrib import admin
from session.models import Session, Pricing

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'session_type', 'start_time', 'planned_duration', 'actual_duration']
    list_filter = ['session_type', 'start_time']
    search_fields = ['customer__name', 'customer__username']

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ['session_type', 'price_per_unit']