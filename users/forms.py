from django import forms
from .models import Customer

class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'username', 'id_proof', 'debt', 'phone_number', 'ps4_tokens', 'ps5_tokens', 'notes')

    def clean_username(self):
        username = self.cleaned_data['username']
        if Customer.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username