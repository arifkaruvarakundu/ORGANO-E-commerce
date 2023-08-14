from django.db import models
from django.db import models
from django.contrib.auth.models import User
#from ecommerce.models import *
from adminpanel.models import *
from django.db.models import Sum
from decimal import Decimal
from django.core.validators import MinValueValidator


# Create your models here.


from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    is_expired = models.BooleanField(default=False)

    def str(self):
        return self.coupon_code

    def check_expiry_status(self):
        # Check if 'is_expired' is True
        if self.is_expired is True:
            # Do something if 'is_expired' is True (not shown in the provided code)
            # ...
            pass
        else:
            # Update 'is_expired' to False if it's not True
            self.is_expired = False
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid =models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applied_coupon = None

    def __str__(self):
        return f"Cart #{self.pk} for {self.user.name}"

    def get_total_price(self):
        if self.coupon:
            return self.cartitems_set.aggregate(total_price=Sum('price')-self.coupon.discount_price)['total_price']

        return self.cartitems_set.aggregate(total_price=Sum('price'))['total_price']
    



class CartItems(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # def save(self, *args, **kwargs):
    #     if self.quantity <= 0:
    #         self.quantity = 1
    #     super().save(*args, **kwargs)

    # @property
    # def update_price(self):
    #     self.price = self.product.price * self.quantity
    #     self.save()

    def get_item_price(self):
        return Decimal(self.price) * Decimal(self.quantity)
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return f"Wishlist for {self.user.username}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)

    def get_item_price(self):
        return self.product.price
    


