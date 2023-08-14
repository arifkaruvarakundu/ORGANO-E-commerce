# forms.py
from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount_price', 'minimum_amount', 'is_expired']
