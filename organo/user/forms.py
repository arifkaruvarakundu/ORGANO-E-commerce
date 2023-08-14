from django import forms
from .models import UserAddress

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['first_name', 'last_name', 'address_line_1', 'address_line_2', 'city', 'state', 'postalcode', 'country', 'email', 'phone_number']
