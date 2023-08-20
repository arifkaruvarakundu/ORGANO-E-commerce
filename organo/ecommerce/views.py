from django.http import JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.models import User
from organo import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
# from adminpanel.views import calculate_discounted_price
from .tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from adminpanel.models import *
from .models import *
import datetime
import pyotp
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.cache import cache_control



# # Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    # Fetch featured products from the database
    categories = Category.objects.all()
    products = Product.objects.all()
    variants = [Variant.objects.filter(product=product).first() for product in products]

    # quality_id = request.GET.get('quality_id')
    # quality = get_object_or_404(Quality, id=quality_id) if quality_id else None
    

    context = {
        'categories': categories,
        'products': products,
        'variants': variants,
        # 'quality': quality,  # Include the selected quality in the context
        # 'quality_id':quality_id,
    }

    return render(request, 'ecommerce/home.html', context) 




from django.contrib.auth import authenticate
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')

            user = authenticate(username=username, password=password)

            if user is not None:

                # Generate OTP secret
                otp_secret = pyotp.random_base32()

                # Create a PyOTP object
                totp = pyotp.TOTP(otp_secret)

                # Get the current OTP
                otp = totp.now()

                # setting timer
                expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

                # Store OTP in the session
                session = SessionStore(request.session.session_key)
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                request.session['otp_expiration_time'] = expiration_time.timestamp()

                # Compose the email content
                subject = 'OTP verification'
                message = f'Hello {user.username},\n\n' \
                        f'Please use the following OTP to verify your email: {otp}\n\n' \
                        f'Thank you!'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]

                # Send the email
                send_mail(subject, message, from_email, recipient_list)

                return redirect('otp_login')

            else:
                messages.error(request, 'wrong username or password')
                return redirect('signin')

        return render(request, 'ecommerce/signin.html')
    else:
        return render(request, 'ecommerce/home.html')

def otp_login(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Retrieve OTP from session
        session_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        expiration_time = request.session.get('otp_expiration_time')

        if session_otp == otp and datetime.datetime.now().timestamp() < expiration_time:

            try:
                my_user = User.objects.get(id=user_id)
                login(request, my_user)
                # Clear OTP-related session data
                request.session['otp'] = None
                request.session['user_id'] = None
                request.session['otp_expiration_time'] = None

                return render(request, 'ecommerce/home.html', {'user': request.user})

            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('signin')

        else:
            # Invalid OTP or expired OTP
            request.session['otp'] = None
            request.session['user_id'] = None
            request.session['otp_expiration_time'] = None
            messages.error(request, 'Invalid OTP or OTP has expired. Please request a new one.')
            return redirect('otp_login')

    elif request.user.is_authenticated:
        # User is already authenticated, show the home page
        return render(request, 'ecommerce/home.html', {'user': request.user})

    else:
        # User is not authenticated, show the OTP input form
        return render(request, 'ecommerce/otp_login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def signup(request):
    if request.method == "POST":
            username = request.POST['username']
            name     = request.POST['name']
            email    = request.POST['email']
            pass1    = request.POST['pass1']
            pass2    = request.POST['pass2']
            is_superuser = request.POST.get('is_superuser', False)

            # Check if the user with the entered username already exists
            # if User.objects.filter(username=username).exists():
            #     messages.error(request, "User already exists.")
            #     return render(request, 'signup.html')
            
            # if User.objects.filter(email=email).exists():
            #     messages.error(request,"email already registered")
            #     return render(request,'signup.html')

            # if pass1 != pass2:
            #     messages.error(request,"password didn't match!!")
            #     return render(request,'signup.html')
            
            # if not username.isalnum():
            #     messages.error(request,"Username must be alphanumeric...")
            #     return render(request,'signup.html')
            
            if is_superuser:
                myuser = User.objects.create_superuser(username, email, pass1)
                myuser.is_active = True  # Superuser accounts are activated by default
            else:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.is_active = False  # Normal user accounts require email confirmation

            
            myuser.first_name = name
            myuser.is_active  = False
            myuser.save()

            messages.success(request, "Successfully created your account. We have sent you a confirmation email,please confirm your email inorder to activate your account.")
            
            #email verification

            subject    = "welcome to organo ecommece-django project"
            message    = "Hello"+myuser.username+"!!\n"+"welcome to organo!!\n thankyou for visiting our website\n we have also sent you a cofirmation email,please confirm your email address inorder to activate your account\n\n Thanking you team ORGANO"
            from_email = settings.EMAIL_HOST_USER
            to_list    = [myuser.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            # email confirmation

            current_site  = get_current_site(request)
            email_subject = "confirm your email@organo django-login!!"
            message2      = render_to_string('ecommerce/email_confirmation.html',{
                'name'  : myuser.first_name,
                'domain': current_site.domain,
                'uid'   : urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token' : generate_token.make_token(myuser)
            })

            email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [myuser.email],
            )

            email.fail_silently = True
            email.send()




            return redirect('signin')

    return render(request, 'ecommerce/signup.html')


   
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
  
    messages.success(request,"logged Out Successfully")
    return redirect('signin')

    
    
def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser= None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'ecommerce/activation_failed.html')



from django.shortcuts import render, get_object_or_404
from adminpanel.models import Category, Product, Variant, Quality


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    # for j in products:
    #   tom = Variant.objects.filter(product=j)
    #   print("+++++++++++++++++++++++++++++++")
    #   for i in tom:
    #     print(i.title)
    variants = [Variant.objects.filter(product=product).first() for product in products]
    

    # Assuming you have a way to get the selected_quality_id (for example, from user input)
    # quality_id = request.GET.get('quality_id')
    # quality = get_object_or_404(Quality, id=quality_id) if quality_id else None

    context = {
        'categories': categories,
        'products': products,
        'variants':variants,
        
        # 'quality': quality,  # Include the selected quality in the context
        # 'quality_id':quality_id,
    }
    return render(request, 'ecommerce/shop.html', context)


from django.shortcuts import render, get_object_or_404
from adminpanel.models import Variant, Quality

def variant_details(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    product= Product.objects.get(id = variant.product.id)
    images = variant.images.all()  # Get all images related to the variant
    qualities = Quality.objects.all()
    varients =product.variants.all().order_by('id')
     
                                    
     

    # # Handling form submission
    # if request.method == 'POST':
    #     selected_quality_id = request.POST.get('quality')
    #     if selected_quality_id:
    #         try:
    #             selected_quality = Quality.objects.get(pk=selected_quality_id)
    #             other_variants = variant.product.variants.filter(quality=selected_quality)
    #         except Quality.DoesNotExist:
    #             selected_quality = None
    #             other_variants = None
    #     else:
    #         selected_quality = None
    #         other_variants = None
    # else:
    #     selected_quality = None
    #     other_variants = None

    context = {
        'variant': variant,
        'images': images,
        'qualities': qualities,
        # 'selected_quality': selected_quality,
        # 'other_variants': other_variants,
        'product':product,
        'varients':varients
    }

    return render(request, 'ecommerce/variant_details.html', context)


# def variant_details(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    # selected_variant = product.productvariant_set.first()  # Assuming you want to display the first color variant initially
    # images = selected_variant.images.all()  # Retrieve the images associated with the selected variant

    # if request.method == 'POST':
    #     selected_variant_id = request.POST.get('variant_id')
    #     selected_variant = product.productvariant_set.get(id=selected_variant_id)
    #     images = selected_variant.images.all()  # Retrieve the images associated with the newly selected variant

    # variants = product.productvariant_set.all()  # Retrieve all variants for the product

    # context = {
    #     'product': product,
    #     'selected_variant': selected_variant,
    #     'images': images,
    #     'variants': variants,
    # }
    # return render(request, 'ecommerce/variant_details.html', context)    



# def women(request):
#     # Assuming category with id=1 corresponds to women's category
#     womens_category = Category.objects.get(id=1)

#     products = Product.objects.filter(category=womens_category)
#     random_variants = {}

#     for product in products:
#         # Get all variants for the current product
#         variants = ProductVariant.objects.filter(product=product, is_active=True)

#         if variants.exists():
#             # Select a random variant from the variants queryset
#             random_variant = random.choice(variants)

#             # Add the random variant to the dictionary
#             random_variants[product] = random_variant

#     context = {
#         'random_variants': random_variants,
#     }
#     return render(request, 'authentication/women.html', context)
def autocomplete(request):
    if 'term' in request.GET:
        search_term = request.GET.get('term')
        try:
            # Use values() to fetch title and id (variant_id) values from the database
            data = Variant.objects.filter(title__icontains=search_term).values('title', 'id')[:10]
            # Convert the QuerySet to a list of dictionaries
            results = [{'label': item['title'], 'id': item['id']} for item in data]
            return JsonResponse(results, safe=False)
        except Exception as e:
            # Handle exceptions or errors (e.g., database errors)
            print(f"Error occurred while retrieving autocomplete data: {str(e)}")

    return render(request, 'ecommerce/home.html')

def error_404_view(request, exception):
    return render(request, '404/error_404.html', status=404)

def error_500_view(request):
    return render(request, '500/error_500.html', status=500)