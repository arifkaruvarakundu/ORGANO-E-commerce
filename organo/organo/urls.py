from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),
    path('', include('adminpanel.urls')),
    path('', include('user.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),


    ] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path('add_product/', views.add_product, name='add_product'),
    # path('product_list', views.product_list, name='product_list'),
    # path('admin/product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('admin/product/delete/<int:product_id>/<str:active>/', views.delete_product, name='delete_product'),
    # path('admin/category/add/', views.add_category, name='add_category'),
    