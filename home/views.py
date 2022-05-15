
from functools import total_ordering
from logging import exception
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.urls import is_valid_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from account.models import Company, Customer
from home.models import Category, Product, Order, ManageOrder,Cart
from home.forms import PostProductForm, EditProductForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from account import views

# category
context={}
cats_menu=Category.objects.all()
context['cats_menu']=cats_menu

# Create your views here.
def homeView(request):
    return redirect('all_product_details')

def add_category(request):
    return render(request,'home/index.html')

def category_details(request,cats):
    category=Category.objects.get(name=cats)
    all_cats_product=Product.objects.filter(category=category)
    cats_menu=Category.objects.all()
    context={
        'all_cats_product':all_cats_product,
        'cats_menu' : cats_menu,
        'category' : category,
    }
    return render(request,'product/category_details.html',context)

def all_category_details(request):
    cats_menu=Category.objects.all()
    context={'cats_menu':cats_menu}
    # for i in context:
    #     print(i)
    print(request.path_info)
    return HttpResponseRedirect(request.path_info, context)

def update_category(request,cats):
    return render(request,'home/index.html')

def delete_category(request,cats):
    return render(request,'home/index.html')

# Product
def add_product(request):
    if request.method=='POST':
        form=PostProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "your Product has successfully added")
            return redirect('all_product_details')
        else:
            messages.success(request, "Form is Not Valid")
    else:
        form=PostProductForm()
    context['form']= form
    return render(request,'product/add_product.html', context)


def product_info(request,pk):
    product=Product.objects.get(id=pk)
    context={'product':product}
    return render(request,'product/index.html', context)

# def product_details(request,pk):
#     product_id=request.POST.get('product_id')
#     product_details=Product.objects.all
#     return render(request,'product/product_details.html',product_id)

class ProductDetailsView(DetailView):
    model=Product
    template_name='product/product_details.html'

def all_product_details(request):
    all_products=Product.objects.all().order_by('-created_at')
    # context['all_products']=all_products
    product_id=request.GET.get('product_id')
    # for i in all_products:
    #     i.order=False
    #     i.save()

    # all_bids=Bid.objects.all()
    cats_menu=Category.objects.all()
    # for i in cats_menu:
    #     print(i)
    # print(product_id)
    context={
        'all_products':all_products,
        'cats_menu': cats_menu,
        # 'all_bids':all_bids,
    }
    return render(request,'product/view_all_product.html', context)

def admin_all_product_details(request):
    all_products=Product.objects.all().order_by('-created_at')
    # context['all_products']=all_products
    product_id=request.GET.get('product_id')
    # for i in all_products:
    #     i.order=False
    #     i.save()

    # all_bids=Bid.objects.all()
    cats_menu=Category.objects.all()
    # for i in cats_menu:
    #     print(i)
    # print(product_id)
    context={
        'all_products':all_products,
        'cats_menu': cats_menu,
        # 'all_bids':all_bids,
    }
    return render(request,'product/admin_product_list.html', context)

class delete_product(DeleteView):
    model=Product
    template_name='product/delete_product.html'
    
    def get_success_url(self):
        return reverse('admin_product_list')

class update_product(UpdateView):
    model=Product
    form_class=EditProductForm
    template_name='product/update_product.html'
    
    def get_success_url(self):
        return reverse( 'admin_product_list')


def place_order(request):
    if request.method=='POST':
        product_id=request.POST.get('product_id')
        user=request.user
        items=request.POST['items']
        delivery_address=request.POST['delivery_address']

        if user.user_type=="3":
            emp_id=request.POST['emp_id']
            emp_name=request.POST['emp_name']
            purpose=request.POST['purpose']

        try:
            product=Product.objects.get(id=product_id)
            total_price=product.price*int(items)
            order=Order()
            order.product=product
            order.user=user
            order.items=items
            order.total_price=total_price
            order.delivery_address=delivery_address
            if user.user_type=="3":
               order.emp_id=emp_id
               order.emp_name=emp_name
               order.purpose=purpose    
            order.save()
            # making product order status true

            product.total_orders=product.total_orders+int(items)
            product.total_sell_price=product.total_sell_price+total_price

            if(product.total_stocks==0):
                messages.error(request,"Currently Product Not Avalabile")
                return redirect('all_product_details')

            product.total_stocks=product.total_stocks-int(items)
            product.save()
            
            messages.success(request,"Successfuly Place Order")
            return redirect('all_product_details')

        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('all_product_details')

    return render(request,'orders/add_order_details.html',context)

def add_order_details(request,pk):
    order=Order.objects.get(id=pk)
    
    cats_menu=Category.objects.all()
    # print(bid.id)
    # print(bid.product.author.address)
    if request.method=='POST':
        delivery_date=request.POST['delivery_date']
        shipping_partner=request.POST['shipping_partner']
        product_location=request.POST['product_location']
        delivery_address=request.POST.get('delivery_address')
        payment_status=request.POST['payment_status']
        try:
            order=ManageOrder(order=order,delivery_date=delivery_date,shipping_partner=shipping_partner,product_location=product_location,delivery_address=delivery_address, payment_status=payment_status)
            order.save()
            messages.success(request, "Order Details Successfully Aded")
            return redirect('view_order_details',pk=pk)
        except Exception as e:
            messages.error(request,e)
            return redirect('view_order_details',pk=pk)
  
    context={
        'order':order,
        'cats_menu':cats_menu
    }
    return render(request,'orders/add_order_details.html',context)

def update_order_details(request,pk):
    order=Order.objects.get(id=pk)
    try:
        orderDetails=ManageOrder.objects.get(order=order)
    except Exception as e:
        messages.info(request,"Please Add Order Details")
        return redirect('view_all_order') 
    cats_menu=Category.objects.all()
    # print(bid.id)
    # print(bid.product.author.address)
    if request.method=='POST':
        delivery_date=request.POST.get('delivery_date')
        shipping_partner=request.POST.get('shipping_partner')
        product_location=request.POST.get('product_location')
        delivery_address=request.POST.get('delivery_address')
        payment_status=request.POST.get('payment_status')
        try:
            
            orderDetails.delivery_date=delivery_date
            orderDetails.shipping_partner=shipping_partner
            orderDetails.product_location=product_location
            orderDetails.delivery_address=delivery_address
            orderDetails.payment_status=payment_status
            orderDetails.save()
            messages.success(request, "Order Details Successfully Updated")
            return redirect('view_order_details',pk=pk)
        except Exception as e:
            messages.error(request,e)
            return redirect('view_order_details',pk=pk)
  
    context={
        'order':order,
        'orderDetails':orderDetails,
        'cats_menu':cats_menu
    }
    return render(request,'orders/update_order.html',context)

def view_order_details(request,pk):
    order=Order.objects.get(id=pk)
    
    try:
        orderDetails=ManageOrder.objects.get(order=order)
    except Exception as e:
        messages.info(request,"Order Details Not Added")
        return redirect('view_all_order') 
    cats_menu=Category.objects.all()
    context={
        'order':order,
        'orderDetails':orderDetails,
        'cats_menu':cats_menu
    }
        
    # print(orderDetails.order.user.f_name)
    return render(request,'orders/view_order_details.html',context)

def view_all_order(request):
    cats_menu=Category.objects.all()
    user=request.user
    if user.user_type=='1':
        all_orders=Order.objects.all()
    else:
        all_orders=Order.objects.filter(user=user)
    try:
        orderDetails=ManageOrder.objects.all()
    except Exception as e:
        messages.info(request,"Please Add Order Details")
        return redirect('view_all_order') 
    # for i in all_orders:
    #     print(i.id)
    context={
        'all_orders':all_orders,
        'orderDetails':orderDetails, 
        'cats_menu':cats_menu
    }
    return render(request,'orders/view_all_orders.html',context)

def user_view_all_order(request):
    cats_menu=Category.objects.all()
    user=request.user
    all_orders=Order.objects.filter(user=user)
    for i in all_orders:
        print(i.id)
    context={
        'all_orders':all_orders,
        'cats_menu':cats_menu
    }
    return render(request,'orders/view_all_orders.html',context)


def addToCart(request,pk):
    print(pk)
    try:
        product=Product.objects.get(id=pk)
    except Exception as e:
        print(e)
    user=request.user
    cart=Cart(product,user)
    cart.save()
    messages.success(request,"Your Product Added to Cart")
    return redirect('view_all_order')

def viewCart(request):
    all_products=Cart.objects.all()
    cats_menu=Category.objects.all()
    context={
        'all_products':all_products,
        'cats_menu':cats_menu
    }
    return render('view_cart.html',context)

def removeFromCart(request):
    pass