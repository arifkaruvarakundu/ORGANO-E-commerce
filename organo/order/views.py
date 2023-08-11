from django.shortcuts import render
from cart.views import view_cart
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from user.models import *
from cart.models import *
from user.models import*
from .models import*
import razorpay
from django.conf import settings
from django.http import JsonResponse
from cart.models import Coupon
from cart.forms import CouponForm
# Create your views here.
def checkout(request, address_id):
    user_add = get_object_or_404(UserAddress, id=address_id, user=request.user)
    carts = get_object_or_404(Cart, user=request.user)

    form = CouponForm(request.POST or None)  # Create form instance with request data (if any)
    final_price = carts.get_total_price()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code=code,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now(),
                active=True
            )
            request.session['coupon_id'] = coupon.id
            return redirect('checkout')  # Redirect to your checkout view
        except Coupon.DoesNotExist:
            form.add_error('code', 'Invalid coupon code.')

     
    
    return render(request, "order/checkout.html", {"user_add": user_add, "carts": carts, 'form': form, 'final_price':final_price})


def online_payment_order(request, userId):
    if request.method == 'POST':
        payment_id = request.POST.getlist('payment_id')[0]
        orderId = request.POST.getlist('orderId')[0]
        signature = request.POST.getlist('signature')[0]
        user_adds = UserAddress.objects.get(id=userId, user=request.user)
        cartss = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cartss)
        total_price = sum(item.price * item.quantity for item in items)
        print('==========================================',total_price)
    
        order = Order.objects.create(
            user=request.user,
            address=user_adds,
            total_price=total_price,
            payment_status='PAID',
            payment_method='PAYPAL',
            razor_pay_payment_id=payment_id,
            razor_pay_payment_signature=signature,
            razor_pay_order_id = orderId,
        )

        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity
                # Set other fields as necessary
            )
        variant = cart_item.product
        variant.stock -= cart_item.quantity
        variant.save()
        orderId = order.id
        items.delete()

        return JsonResponse({'message': 'Order placed successfully','orderId':orderId})
    else:
        # Handle invalid request method (GET, etc.)
        return JsonResponse({'error': 'Invalid request method'})
    


# def place_order(request,userId):   
      
#      user_adds = UserAddress.objects.get(id=userId, user=request.user)
#      cartss = Cart.objects.get(user = request.user)
#      item = CartItems.objects.filter(cart=cartss)
#      total_price = sum(item.price * item.quantity for item in item)
#      order = Order.objects.create(
#         user=request.user,
#         address=user_adds,
#         total_price=total_price,
#         payment_status='PENDING',
#         payment_method='CASH_ON_DELIVERY',
#      )
#      orderss = order.id
#      for cart_item in item:
#         OrderItem.objects.create(
#             order=order,
#             product=cart_item.product,
#             price=cart_item.price,
#             quantity=cart_item.quantity
    
#         )
#         variant = cart_item.product
#         variant.stock-= cart_item.quantity
#         variant.save()


#      order =Order.objects.get(id=orderss)
#      items = OrderItem.objects.filter(order=order)


     
#      item.delete()
#      context = {
#            'items':items,
#            'total_price':total_price,
#            'order':order
#      }

#      return render(request,"order/order_success.html",context)


def place_order(request, userId):   
    user_adds = UserAddress.objects.get(id=userId, user=request.user)
    cartss = Cart.objects.get(user=request.user)
    items = CartItems.objects.filter(cart=cartss)
    total_price = sum(item.price * item.quantity for item in items)
    order = Order.objects.create(
        user=request.user,
        address=user_adds,
        total_price=total_price,
        payment_status='PENDING',
        payment_method='CASH_ON_DELIVERY',
    )

    for cart_item in items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.price,
            quantity=cart_item.quantity
        )
        variant = cart_item.product  # Access the product, not the variant directly
        variant.stock -= cart_item.quantity
        variant.save()

    # Fetch the updated order instance
   
    items.delete()
    context = {
        'items': OrderItem.objects.filter(order=order),
        'total_price': total_price,
        'order': order
    }
    return render(request, "order/order_success.html", context)



def ordertable(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders':orders
    }
    return render(request,'order/ordertable.html',context)

def order_view(request,order_id):
    orders = Order.objects.get(id=order_id)
    view_order = OrderItem.objects.filter(order=orders)

    context ={
        'view_order':view_order
    }

    return render(request,"order/order_view.html",context)

def cancel_orders(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.payment_status != 'PAID' and order.payment_status != 'CANCELLED':
            # Update the payment status to 'CANCELLED'
            order.payment_status = 'CANCELLED'
            order.save()
    return redirect('ordertable')



# views.py
def initiate_payment(request):
    if request.method == 'POST':
        # Retrieve the total price and other details from the backend
        cartss = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cartss)
        total_price =cartss.get_total_price()
        print(total_price,"--------------------------------------------toTal price")
        client = razorpay.Client(auth=("rzp_test_xADEzwG15zURhy","SqSffCZ1rmXL4wWih9Zq9lXk"))
        payment = client.order.create({

            'amount': int(total_price * 100),
              'currency': 'INR', 
              'payment_capture': 1
              
              })
        print(payment)
    
        response_data = {
            'order_id': payment['id'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'key': settings.RAZOR_KEY_ID
        }
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})



def order_success(request,orderId):
    orders = Order.objects.get(id=orderId)
    items = OrderItem.objects.filter(order=orders)
    total_price = sum(item.price * item.quantity for item in items)

    context = {
        'orders':orders,
        'items':items,
        'total_price':total_price
    }


    return render(request,"order/order_success.html",context)