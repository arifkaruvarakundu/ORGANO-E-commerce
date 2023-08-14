import decimal
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import *
from adminpanel.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.

@login_required

def add_to_cart(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id)

    # Check if a cart exists for the user, or create a new one
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    try:
        cart_item = CartItems.objects.get(cart=cart, product=variant)
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        # If it's a new item in the cart, set its price and save it
        cart_item = CartItems.objects.create(cart=cart, product=variant, price=variant.price)

    # Redirect to a relevant page, such as the cart page or product details page
    return redirect('shop')  # Replace 'cart' with the URL name of your cart page

    # Or if you want to redirect back to the product details page, use:
    # return redirect('variant_details', variant_id=variant_id)

    # Alternatively, you can return an HttpResponse with a success message
    # return HttpResponse("Added to cart successfully!")

 

# def view_cart(request):

#-------------------------------------------------------------------------------------------------------------
from django.core.exceptions import ValidationError
def view_cart(request):
    cart_obj = Cart.objects.get(is_paid=False, user=request.user)

    cart_items = cart_obj.cartitems_set.all().order_by('product__title')
    
    total_price = 0
    for item in cart_items:
        try:
            # Check if the product is out of stock
            if item.product.stock < 1:
                continue  # Skip this item if it is out of stock
            
            # Update the price of each item based on the quantity
            item.price = item.product.price * item.quantity
            item.save()

            # Add the updated item price to the total price
            total_price += item.price
        except ValidationError:
            # Handle any potential validation errors related to the product or item
            pass

    coupon = None 
    

    if request.method=='POST':
        coupon=request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
        print('===================================')
        if not coupon_obj.exists():
            messages.warning(request,'Invalid coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon:
            messages.warning(request,'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_total_price() < coupon_obj[0].minimum_amount:
            messages.warning(request,f'Amount should be greaerthan {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request,f'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_obj.coupon=coupon_obj[0]
        cart_obj.save()
        messages.success(request,'Coupon applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if cart_obj.coupon:
        coupon = cart_obj.coupon
        discount_price = coupon.discount_price
        
    else:
        discount_price = 0

    final_price=total_price-discount_price
    context = {
            'cart': cart_obj,
            'total_price': total_price,
            'coupon':coupon,
            'discount_price':discount_price,
            'final_price':final_price

            }
       
    return render(request, 'cart/view_cart.html', context)

def remove_coupon(request,cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)  # Correctly access the 'Cart' model
        # Your code to remove the coupon from the cart goes here

    except Cart.DoesNotExist:
        # Handle the case when the cart with the given ID does not exist
        pass
    cart.coupon=None
    cart.save()

    messages.success(request,'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def remove_from_cart(request,item_id):
    # if request.method == 'POST':
    #     # item_id = request.POST.get('item_id')
    #     print(item_id)
    cart_item = CartItems.objects.get(id=item_id)
    cart_item.delete()

    return redirect('view_cart')

    # return render(request, 'cart/shop_cart.html')


def update_quantity(request):
 
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        carts = Cart.objects.get(user = request.user)
        total_price = carts.get_total_price()
        product = CartItems.objects.get(id=product_id)
        product.quantity = quantity
        product.price = product.price * Decimal(product.quantity)
        product.save()
        print(product.price)
        # Prepare the response data
        response_data = {
            'success': True,
            'message': 'Quantity updated successfully!',
            'price': str(product.price),
            'quantity': str(product.quantity),
            'total_price': total_price
        }

        return JsonResponse(response_data)
    
    response_data = {
        'success': False,
        'message': 'Invalid request',
    }
    
    return JsonResponse(response_data, status=400)               



def add_to_wishlist(request, variant_id):
    product = Variant.objects.get(id=variant_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    item = wishlist.wishlistitem_set.filter(product=product)

    if item.exists():
    
        return redirect('shop')
    else:
        WishlistItem.objects.create(wishlist = wishlist, product=product)
        return redirect('shop')

def remove_wish(request, variant_id):
    product = Variant.objects.get(id=variant_id)
    wishlist = get_object_or_404(Wishlist,user=request.user)
    item = wishlist.wishlistitem_set.filter(product=product)

    if item.exists():
      item.delete()

    return redirect('view_wishlist')




def view_wishlist(request):
    wishlist= get_object_or_404(Wishlist, user=request.user)
    user_products = CartItems.objects.filter(cart__user= request.user).values_list('product__id' , flat=True)
    items= WishlistItem.objects.filter( wishlist= wishlist)
    return render(request, 'cart/view_wishlist.html', {'wishlist': wishlist, 'items': items, 'user_products':user_products})