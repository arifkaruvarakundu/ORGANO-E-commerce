from django.urls import path
from . import views

urlpatterns = [
    path('address/', views.address, name='address'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('change_password/', views.change_user_password, name= 'change_password'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
]