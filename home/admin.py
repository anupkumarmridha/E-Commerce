from django.contrib import admin
from home.models import Category, Product, Rating, Review, Order
# Register your models here.
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(Review)