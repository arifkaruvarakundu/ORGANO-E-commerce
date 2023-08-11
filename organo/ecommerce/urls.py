from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('shop', views.shop, name='shop'),
    path('variant_details/<int:variant_id>/', views.variant_details, name='variant_details'),
    path('otp_login/', views.otp_login, name='otp_login'),
     path('autocomplete/', views.autocomplete, name='autocomplete'),
    
    # path('search/', views.search, name='search'),
    
    
]
