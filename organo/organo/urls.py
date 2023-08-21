from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def custom_page_not_found_view(request, exception):
    return render(request, '404/error_404.html', status=404)

def custom_server_error_view(request):
    return render(request, '500/error_500.html', status=500)

handler404 = custom_page_not_found_view
handler500 = custom_server_error_view

urlpatterns =[
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),
    path('', include('adminpanel.urls')),
    path('', include('user.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),

    ] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    