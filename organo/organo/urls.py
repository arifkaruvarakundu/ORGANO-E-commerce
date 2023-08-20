from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.views import error_404_view, error_500_view
from adminpanel.views import error_404_view, error_500_view
from user.views import error_404_view, error_500_view
from cart.views import error_404_view, error_500_view
from order.views import error_404_view, error_500_view

handler404 = 'ecommerce.views.error_404_view'
handler500 = 'ecommerce.views.error_500_view'
handler404 = 'adminpanel.views.error_404_view'
handler500 = 'adminpanel.views.error_500_view'
handler404 = 'user.views.error_404_view'
handler500 = 'user.views.error_500_view'
handler404 = 'cart.views.error_404_view'
handler500 = 'cart.views.error_500_view'
handler404 = 'order.views.error_404_view'
handler500 = 'order.views.error_500_view'

urlpatterns =[
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),
    path('', include('adminpanel.urls')),
    path('', include('user.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),

    ] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    