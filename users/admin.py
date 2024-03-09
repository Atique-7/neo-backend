from django.contrib import admin
from users.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone_number', 'debt', 'notes']
    search_fields = ['name', 'username', 'phone_number']