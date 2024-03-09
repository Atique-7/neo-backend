from django.contrib import admin
from transactions.models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['session', 'total_cost', 'payment_method', 'unpaid_amount', 'payment_status']
    list_filter = ['payment_status', 'payment_method']
    search_fields = ['session__customer__name', 'session__customer__username']