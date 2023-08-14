from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=140,null=True,blank=True)
    mobile = models.CharField(max_length=120,null=True,blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    @receiver(post_save, sender=User)
    def create_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True,null=True)
    def __str__(self):
         return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"slug": self.slug})
    def __str__(self):
        return str(self.name)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Product, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.name
    
class Quality(models.Model):
    name = models.CharField( max_length=50)  
    slug = models.SlugField(unique=True, blank=True, null=True)
    def __str__(self):
        return str(self.name)

class Variant(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    quality = models.ForeignKey(Quality, on_delete=models.CASCADE, default='Good')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Discount percentage for this variant (e.g., 10.50 for 10.50% off).'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Variant, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("variant_details", kwargs={"slug": self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey("Variant",on_delete=models.CASCADE , related_name='images')
    image = models.ImageField( upload_to="variants")

    def __str__(self):
        return f'{self.product.product.name}{self.product.quality}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

