from django import forms
from .models import Product,Category,Variant,Quality
from order.models import Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','description','slug','is_available','is_active']

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock
    



from django import forms


class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['title', 'product', 'quality', 'quantity', 'price', 'stock', 'description', 'slug']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['user','address','total_price','payment_status','payment_method','order_date','delivery_date','razor_pay_order_id','razor_pay_payment_id','razor_pay_payment_signature']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")