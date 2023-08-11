from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Quality)
admin.site.register(ProductImage)
