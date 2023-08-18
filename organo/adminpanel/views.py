from datetime import datetime, timedelta, timezone
from io import BytesIO
from os import truncate
from random import random
from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *
from .forms import ProductForm, OrderForm,VariantForm
from .models import Product
from django.contrib import messages
from .models import Category
from django.db.models import Count,Sum
from order.models import Order
from django.db.models import Q
from django.utils import timezone
from django.db.models.functions import TruncDate
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from ecommerce.views import *



# Create your views here.
@never_cache

def admin_page(request):
    if request.user.is_superuser:
        
        # if request.GET.get('search') is not None :
        #     search=request.GET.get('search')
        #     users=User.objects.filter(username__icontains=search)
        # else:
        #      users=User.objects.all()
        # context={
        #     'users':users
        #      }
          
        return redirect('dashboard')
    else:
        return render(request,'ecommerce/home.html')
def products(request):
    product = Product.objects.all()
    product_count = product.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    product_quantity = Product.objects.filter()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product.name} has been added')
            return redirect('add_products')
    else:
        form = ProductForm()
    context = {
        'product': product,
        'form': form,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'adminpanel/add_products.html', context)

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(product=product)
    context = {
        'product': product,
        'variants': variants,
    }

    return render(request, 'adminpanel/product_view.html', context)



from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        category_id = request.POST.get('category')
        product_description = request.POST.get('description')
        
        # Retrieve the selected category
        category = Category.objects.get(id=category_id)

        # Create the product instance
        product = Product(
            name=product_name,
            category=category,
            description=product_description,
        )
        product.save()
        
        success_message = f"You have added {product.name} successfully."

        # Add the success message to the Django messages framework
        messages.success(request, success_message)

        # Redirect to the products list page
        return redirect('add_product')
        
    else:
    
        is_active = True

        # Retrieve the categories from the database
        categories = Category.objects.all()

        # Prepare the context for rendering the add product page
        context = {
            'categories': categories,
            'is_active': is_active,  # Pass the is_active value to the template
        }

        # Render the add product page
        return render(request, 'adminpanel/add_product.html', context)
    

from django.shortcuts import render
from django.urls import reverse
from .models import Product

def products_list(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'adminpanel/products_list.html', context)




def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        # Get the updated data from the form
        product.name = request.POST.get('name')
        category_id = request.POST.get('category')
        product.description = request.POST.get('description')

        # Retrieve the selected category
        category = Category.objects.get(id=category_id)
        product.category = category

        # Save the updated product
        product.save()

        success_message = f"You have updated {product.name} successfully."

        # Add the success message to the Django messages framework
        messages.success(request, success_message)

        # Redirect to the products list page
        return redirect('products_list')
    
    else:
        # Retrieve the categories from the database
        categories = Category.objects.all()

        # Prepare the context for rendering the edit product page
        context = {
            'product': product,
            'categories': categories,
        }

        # Render the edit product page
        return render(request, 'adminpanel/edit_product.html', context)

def delete_product(request,product_id, active):
    product = Product.objects.get(id=product_id)
    product.is_active = (active == 'true')
    product.save()
    return redirect('products_list')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Category added successfully.'
            messages.success(request, success_message)
            return redirect('category_list')  # Replace 'category_list' with the appropriate URL name for your category list view
    else:
        form = CategoryForm()
    return render(request, 'adminpanel/add_category.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()  # Retrieve all categories from the database
    productsValue = []  # Placeholder for products value (assuming it's defined elsewhere)

    context = {
        'categories': categories,
    }

    return render(request, 'adminpanel/category_list.html', context)




from django.http import HttpResponse, HttpResponseBadRequest


def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    
    if category.products.exists():
        # Category has associated products, cannot delete
        error_message = 'Cannot delete category with associated products.'
        messages.error(request, error_message)
    else:
        category.delete()
        success_message = 'Category successfully deleted.'
        messages.success(request, success_message)
    
    return redirect('category_list')



from .forms import CategoryForm


def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            success_message = 'Categor Successfully Updated.'
            messages.success(request, success_message)
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'adminpanel/edit_category.html', {'form': form, 'category': category})


def user(request):
    users=User.objects.all()
    context = {
        'users':users
    }
    return render(request,'adminpanel/user_list.html',context)

def block_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.is_active=False
    user.save()
    return redirect('user')

def unblock_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.is_active=True
    user.save()
    return redirect('user')

def delete_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('user')

from order.models import OrderItem

def order_all(request):
    orders = Order.objects.all()
    context ={
        'orders':orders
    }
    return render(request,'adminpanel/all_orders.html',context)

def order_views(request,order_id):
    view_order = Order.objects.get(id=order_id)
    order = OrderItem.objects.filter(order=view_order)

    context ={
        'order':order,
        'view_order':view_order
    }
    return render(request,'adminpanel/order_views.html',context)


from django.shortcuts import redirect, get_object_or_404

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment_status != 'PAID' and order.payment_status != 'CANCELLED':
        # Update the payment status to 'CANCELLED'
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
        
            print(item.quantity)
            variant = item.product  
            variant.stock += item.quantity
            variant.save()
          

        order.payment_status = 'CANCELLED'
        order.save()

    return redirect('order_all')
from order.models import *
def order_shipped(request, order_id):
    if request.user.is_superuser:
        
        order = get_object_or_404(Order, id=order_id)
        
        order.order_status = 'Shipped'
        print(order.order_status)
        order.shipping_date = timezone.now()
        order.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'home.html')
    
def admin_order_cancel(request, order_id):
   
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        user = order.user
        print("hyyyyyyyyyyyyyyy")
        if order.order_status != 'Delivered' and order.order_status != 'Returned'and order.order_status !='Cancelled' and order.order_status != 'Requested for return ':
            print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                variant = item.product
                variant.stock += item.quantity
                variant.save()
            if order.payment_method in ['RAZORPAY']:
                user_wallet = Wallet.objects.get(user=user)
                # Refund the amount to the user's wallet
                refund_amount = order.total_price # Assuming you want to refund the full amount
                print('======================================>',refund_amount)

                user_wallet.balance += Decimal(refund_amount)
                user_wallet.save()
                transaction_type = 'Cancelled'
                WalletTransaction.objects.create(wallet=user_wallet, amount=refund_amount, order_id=order, transaction_type=transaction_type)

            if order.payment_status=='Pending':
                order.payment_status='No payment'
            else:
                order.payment_status='Refunded'
            order.order_status='Cancelled'
            Order.cancelled_date=timezone.now()
            order.save()

            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'home.html')
    
def order_deliverd(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        print(order)
        # Make sure the order is in the 'SHIPPED' status before marking it as 'DELIVERED'
        if order.order_status == 'Shipped':
            order.order_status = 'Delivered'
            order.delivery_date=timezone.now()
            order.return_period_expired=timezone.now()+timezone.timedelta(days=5)

        if order.payment_status=='Pending':
            order.payment_status='Paid'
        order.save()
        print(order.return_period_expired)

        return redirect(request.META.get('HTTP_REFERER'))


from django.shortcuts import render, redirect, get_object_or_404
from .models import Variant, Product, Quality
from django.utils.text import slugify

def add_variant(request, product_id):
    if request.method == 'POST':
        # Retrieve form data from the request
        variant_title = request.POST.get('title')
        quality_name = request.POST.get('quality')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        
        

        # Get the product instance

        product = get_object_or_404(Product, id=product_id)
        

        # Get the quality instance
        quality_instance, _ = Quality.objects.get_or_create(name=quality_name)

        # Create the variant
        variant = Variant.objects.create(
            title=variant_title,
            product=product,
            quality=quality_instance,
            quantity=quantity,
            price=price,
            stock=stock,
            
        )

        # Create product images
        

        return redirect('product_view', product_id=product_id)  # Redirect to the admin page after successful submission

    # Retrieve products and qualities for the form
    product = Product.objects.all()
    qualities = Quality.objects.all()

    context = {
        'product': product,
        'qualities': qualities,
        
    }

    return render(request, 'adminpanel/add_variant.html', context)









def variant_list(request):
    variants = Variant.objects.all()
    context = {'variants': variants}
    

    return render(request, 'adminpanel/variant_list.html', context)

def variant_edit(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)

    if request.method == 'POST':
        # Retrieve form data from the request
        variant_title = request.POST.get('variant_title')
        quality = request.POST.get('quality')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        quality =Quality.objects.get(id = quality)

        # Update the variant
        variant.title = variant_title
        variant.quality = quality
        variant.quantity = quantity
        variant.price = price
        variant.stock = stock
        variant.image = image

        variant.save()

        # Update or create product images
        

        return redirect('product_view', product_id=variant.product.id)  # Redirect to the product view page after successful update
    qualities = Quality.objects.all()
    

    context = {
        'variant': variant,
        'qualities': qualities,
    }

    return render(request, 'adminpanel/variant_edit.html', context)

def enable_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = True
    product.save()
    return redirect('products_list')


def disable_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = False
    product.save()
    return redirect('products_list')




#Dashboard-----------------------------------

def dashboard(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date and not end_date:
            # Calculate the current date
            current_date = timezone.now().date()

            # Calculate the date 30 days back from the current date
            default_start_date = current_date - timedelta(days=30)
            default_end_date = current_date

            # Convert to string format (YYYY-MM-DD)
            start_date = default_start_date.strftime('%Y-%m-%d')
            end_date = default_end_date.strftime('%Y-%m-%d')

        if start_date and end_date:
            order_count_date = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date, order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').count()

            total_price_date = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date, order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

            daily_totals = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date, order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').annotate(date=TruncDate('order_date')).values('date').annotate(total=Sum('total_price')).order_by('date')
            order_count = Order.objects.exclude(payment_status='CANCELLED').count()
            total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']
            today = timezone.now().date()
            today_orders = Order.objects.filter(order_date__date=today)
            order_count_today = today_orders.count()
            total_price_today = sum(order.total_price for order in today_orders)
            recent_orders = Order.objects.order_by('-order_date')[:3]
            top_selling_products = OrderItem.objects.values('product').annotate(total_quantity=Count('product')).order_by('-total_quantity')[:5]



            categories = Category.objects.all()
            data = []

            for category in categories:
                product_count = Product.objects.filter(category=category).count()
                data.append(product_count)

            context = {
                'order_count_date': order_count_date,
                'total_price_date': total_price_date,
                'start_date': start_date,
                'end_date': end_date,
                'daily_totals': daily_totals,
                'order_count': order_count,
                'total_price': total_price,
                'categories': categories,
                'data': data,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
                'recent_orders': recent_orders,
                'top_selling_products':top_selling_products,


            }

            return render(request, 'adminpanel/admin_dashboard.html', context)

        else:
            order_count = Order.objects.exclude(payment_status='CANCELLED').count()
            total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

            today = timezone.now().date()
            today_orders = Order.objects.filter(order_date__date=today)
            order_count_today = today_orders.count()
            total_price_today = sum(order.total_price for order in today_orders)

            categories = Category.objects.all()
            data = []

            for category in categories:
                product_count = products.objects.filter(category=category).count()
                data.append(product_count)


            recent_orders = Order.objects.order_by('-order_date')[:3]
            top_selling_products = OrderItem.objects.values('product_products_name').annotate(total_quantity=Count('product')).order_by('-total_quantity')[:5]
            

            


            context = {
                'order_count': order_count,
                'total_price': total_price,
                'start_date': start_date,
                'end_date': end_date,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
                'categories': categories,
                'data': data,
                'recent_orders': recent_orders,
                'top_selling_products':top_selling_products,
            }

            return render(request, 'adminpanel/admin_dashboard.html', context)
    
    return HttpResponseBadRequest("Invalid request method.")



def pdf_view(request):

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Today's totals
    today_orders = Order.objects.filter(order_date__date=today)
    order_count_today = today_orders.count()
    total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Weekly totals
    week_orders = Order.objects.filter(order_date__date__range=[week_ago, today])
    order_count_week = week_orders.count()
    total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Monthly totals
    month_orders = Order.objects.filter(order_date__date__range=[month_ago, today])
    order_count_month = month_orders.count()
    total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Top selling products
    top_selling_products_today = OrderItem.objects.values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_week = OrderItem.objects.filter(order__order_date__date__range=[week_ago, today]).values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_month = OrderItem.objects.filter(order__order_date__date__range=[month_ago, today]).values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    context = {
        'order_count_today': order_count_today,
        'total_price_today': total_price_today,
        'order_count_week': order_count_week,
        'total_price_week': total_price_week,
        'order_count_month': order_count_month,
        'total_price_month': total_price_month,
        'top_selling_products_today': top_selling_products_today,
        'top_selling_products_week': top_selling_products_week,
        'top_selling_products_month': top_selling_products_month,
    }

    return render(request, 'adminpanel/pdf_view.html',context)
     

def download_order_pdf_sales(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Today's totals
    today_orders = Order.objects.filter(order_date__date=today)
    order_count_today = today_orders.count()
    total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Weekly totals
    week_orders = Order.objects.filter(order_date__date__range=[week_ago, today])
    order_count_week = week_orders.count()
    total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Monthly totals
    month_orders = Order.objects.filter(order_date__date__range=[month_ago, today])
    order_count_month = month_orders.count()
    total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Top selling products
    top_selling_products_today = OrderItem.objects.values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_week = OrderItem.objects.filter(order__order_date__date__range=[week_ago, today]).values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_month = OrderItem.objects.filter(order__order_date__date__range=[month_ago, today]).values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    context = {
        'order_count_today': order_count_today,
        'total_price_today': total_price_today,
        'order_count_week': order_count_week,
        'total_price_week': total_price_week,
        'order_count_month': order_count_month,
        'total_price_month': total_price_month,
        'top_selling_products_today': top_selling_products_today,
        'top_selling_products_week': top_selling_products_week,
        'top_selling_products_month': top_selling_products_month,
    }

    
    html_content = render_to_string('adminpanel/pdf_download.html', context)

    # Set the response content type as 'application/pdf' to indicate that it's a PDF file
    response = HttpResponse(content_type='application/pdf')

    # Set the filename for the downloaded file
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    # Generate the PDF content from the HTML using xhtml2pdf
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), response)
    
    if pdf.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


from cart.models import *

def view_coupon(request):
   if request.user.is_superuser: 
     coupons= Coupon.objects.all()

     return render(request,'adminpanel/view_coupon.html',{'coupons':coupons})   
   else:
            return render(request,'ecommerce/home.html') 
   

def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    
    if request.method == 'POST':
        # Update the coupon instance with the form data
        coupon.code = request.POST.get('coupon_code')
        coupon.discount = request.POST.get('discount_price')
        # coupon.valid_from = request.POST.get('valid_from')
        # coupon.valid_to = request.POST.get('valid_to')
        coupon.minimum_amount = request.POST.get('minimum_amount')
        coupon.is_expired = 'is_expired' in request.POST
        # coupon.single_use_per_user = 'single_use_per_user' in request.POST
        # coupon.quantity = request.POST.get('quantity')

        # Save the updated coupon instance
        coupon.save()

        # Redirect to a success page or show a success message
        return redirect('view_coupon')  # Replace 'view_coupon' with your appropriate URL name
    
    # If the request is not POST, render the edit coupon form
    return render(request, 'adminpanel/edit_coupon.html', {'coupon': coupon}) 
     



    
    
def add_coupon(request):
    if request.method == 'POST':
       
        coupon_code = request.POST['coupon_code']
        discount_price = request.POST['discount_price']
        # valid_from = request.POST['valid_from']
        # valid_to = request.POST['valid_to']
        minimum_amount = request.POST['minimum_amount']
        is_expired = 'is_expired' in request.POST
        # single_use_per_user = 'single_use_per_user' in request.POST
        # quantity = request.POST['quantity']

        # Create a new coupon instance
        new_coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            discount_price=discount_price,
            # valid_from=valid_from,
            # valid_to=valid_to,
            minimum_amount=minimum_amount,
            is_expired=is_expired,
            #single_use_per_user=single_use_per_user,
            #quantity=quantity,
        )
       
        new_coupon.save()

       
        return redirect('view_coupon')  

    return render(request, 'adminpanel/add_coupon.html')



def disable_coupon(request, coupon_id):
    if request.user.is_superuser: 

      coupon = get_object_or_404(Coupon, id=coupon_id)
      coupon.is_expired = True
      coupon.save()

      return redirect('view_coupon')
    else:
            return render(request,'ecommerce/home.html') 
    

def enable_coupon(request, coupon_id):
   if request.user.is_superuser: 
      coupon = get_object_or_404(Coupon, id=coupon_id)
      coupon.is_expired= False
      coupon.save()

      return redirect('view_coupon')
   else:
            return render(request,'ecommerce/home.html')
   



# views.py
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
def generate_otp():
    # Generate a 6-digit random OTP
    return str(random.randint(100000, 999999))

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle case when the email is not found in the database
            return render(request, 'password_reset_request.html', {'error_message': 'Email not found'})

        # Create a UserProfile object and associate it with the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Generate OTP and store it along with its expiration time in the UserProfile model
        otp = generate_otp()
        user_profile.otp = otp
        user_profile.otp_expiry = datetime.now() + timedelta(minutes=10)
        user_profile.save()

        # Send the OTP to the user's email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            'nedungadanharif@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('verify_otp')
    return render(request, 'adminpanel/password_reset_request.html')



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        try:
            print( otp)
            userprofile = UserProfile.objects.get(otp=otp, otp_expiry__gte=timezone.now())
        except UserProfile.DoesNotExist:
            return render(request, 'adminpanel/verify_otp.html', {'error_message': 'Invalid OTP'})

        # Store the userprofile in the session to use it in the reset_password view
        request.session['userprofile_id'] = userprofile.id

        return redirect('reset_password')
    return render(request, 'adminpanel/verify_otp.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']

        # Retrieve the userprofile from the session
        userprofile_id = request.session.get('userprofile_id')
        if userprofile_id is None:
            # Redirect to the verify_otp view if the userprofile is not found in the session
            return redirect('verify_otp')

        try:
            userprofile = UserProfile.objects.get(pk=userprofile_id)
        except UserProfile.DoesNotExist:
            # Redirect to the verify_otp view if the userprofile is not found in the database
            return redirect('verify_otp')

        # Get the associated user from the userprofile
        user = userprofile.user

        # Update the user's password with the new one
        user.set_password(password)
        user.save()

        # Clear the userprofile from the session after successful password reset
        del request.session['userprofile_id']

        return redirect('signin')  # Redirect to the login page or any other page

    return render(request, 'adminpanel/resetpassword.html')

def order_deliverd(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        
        # Make sure the order is in the 'SHIPPED' status before marking it as 'DELIVERED'
        if order.order_status == 'Shipped':
            order.order_status = 'Delivered'
            order.delivery_date=timezone.now()
            order.return_period_expired=timezone.now()+timezone.timedelta(days=5)

        if order.payment_status=='Pending':
            order.payment_status='Paid'
        order.save()
        

        return redirect(request.META.get('HTTP_REFERER'))


