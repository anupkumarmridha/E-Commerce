from itertools import product
from django.db import models

# Create your models here.
from django.db import models
from account.models import User, Customer,Company
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=255)
    
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    order_status=models.BooleanField(default=False)
    product_image = models.ImageField(null=True, blank=True, upload_to='images/products/')
    total_stocks=models.IntegerField()
    desc=RichTextField(blank=True, null=True)
    
    price=models.DecimalField(max_digits=8, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' | ' + str( self.author)

    @property
    def image_url(self):
        if self.product_image and hasattr(self.product_image, 'url'):
            return self.product_image.url


class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_address=models.CharField(max_length=255)
    
class Order(models.Model):
    buy=models.ForeignKey(Buy, related_name="order",on_delete=models.CASCADE)
    delivery_date=models.DateField()
    shipping_partner=models.CharField(max_length=255)
    product_location=models.CharField(max_length=255)
    delivery_address=models.CharField(max_length=255)
    payment_status=models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.product)

class Rating(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField()
    parrent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)