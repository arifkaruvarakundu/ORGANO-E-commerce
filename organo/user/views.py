from django.shortcuts import render
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from .models import *
from django.shortcuts import redirect, get_object_or_404
from .models import UserAddress

# Create your views here.
def address(request):
    user_add=request.user
    addresses = UserAddress.objects.filter(user = user_add)
    context = {
        'addresses':addresses
    }
    return render(request,'user/address.html',context) 

def add_address(request):
    if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Create a new UserAddress object and save it to the database
        user_address = UserAddress(
            user=request.user,  # Assuming the request has a logged-in user
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            email=email,
            phone_number=phone_number
        )
        user_address.save()
        return redirect('address')
    return render(request,'user/add_address.html')

def edit_address(request,address_id):
     try:
        user_address = UserAddress.objects.get(id=address_id, user=request.user)
        print(address_id)
     except UserAddress.DoesNotExist:
        return HttpResponse('Address not found.')
     if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Update the user address fields
        user_address.first_name = first_name
        user_address.last_name = last_name
        user_address.address_line_1 = address_line_1
        user_address.address_line_2 = address_line_2
        user_address.city = city
        user_address.state = state
        user_address.postal_code = postal_code
        user_address.country = country
        user_address.email = email
        user_address.phone_number = phone_number

        # Save the updated user address
      
        user_address.save()
        return redirect('address')
     context = {
         'user_address':user_address
     }
     return render(request,'user/edit_address.html',context)

def profile_view(request):
     if request.method == 'POST':
        # Get the form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Update the user object with the new information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        
        return redirect('profile_view')  # Redirect to the profile view or any other desired page after updating
   
     return render(request,'user/profile.html')


def user_address(request):
    user_add = request.user
    address = UserAddress.objects.filter(user = user_add)
    context = {
        'address':address
    }
    return render(request,'user/address.html',context)

def change_user_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            old_password = request.POST.get('password')
            new_password = request.POST.get('password1')
            confirm_new_password = request.POST.get('password2')
            user = request.user

            if user.check_password(old_password) and new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('signin')

            else:
                messages.error(request, 'Password does not match or invalid input')

        return render(request, 'user/change_password.html')

def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id)
    
    if request.method == 'POST':
        address.delete()
        # Redirect to the address list or any other desired page
        return redirect('address')
    
def error_404_view(request, exception):
    return render(request, '404/error_404.html', status=404)

def error_500_view(request):
    return render(request, '500/error_500.html', status=500)