
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.urls import is_valid_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from account.models import Company, Customer
from home.models import Category, Product, Order
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
    return render(request,'home/index.html', context)

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


def place_order(request, pk):
    if request.method=='POST':
        pass
    return render(request,'orders/add_order_details.html',context)

def add_order_details(request,pk):
    return render(request,'orders/add_order_details.html',context)

def update_order_details(request,pk):
    return render(request,'orders/update_order.html',context)

def view_order_details(request,pk):
    return render(request,'orders/view_order_details.html',context)