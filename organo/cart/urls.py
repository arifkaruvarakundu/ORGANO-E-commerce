from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity', views.update_quantity, name='update_quantity'),
    path('add_to_wishlist/<int:variant_id>/', views.add_to_wishlist , name='add_to_wishlist'),
    path('view_wishlist/', views.view_wishlist , name='view_wishlist'),
    path('remove_wish/<int:variant_id>/', views.remove_wish, name='remove_wish'),
    path('remove_coupon/<int:cart_id>/',views.remove_coupon, name='remove_coupon'),

]