from django.urls import path
from home import views

urlpatterns = [

    path('', views.homeView, name='homeView'),

# ends point for category
    path('add-category', views.add_category, name='add_category'),
    path('category-details/<str:cats>', views.category_details, name='category_details'),
    path('all-category-details', views.all_category_details, name='all_category_details'),
    path('update-category/<str:cats>', views.update_category, name='update_category'),
    path('delete-category/<str:cats>', views.delete_category, name='delete_category'),

# ends point for products
    path('add-product', views.add_product, name='add_product'),
    path('product-info/<int:pk>', views.product_info, name='product_info'),
    path('product-details/<int:pk>', views.ProductDetailsView.as_view(), name='product_details'),
    path('all-product-details', views.all_product_details, name='all_product_details'),
    
    
    # path('rating-product/<int:pk>', views.rating_product, name='rating_product'),
    
    # path('company_rating/<int:pk>', views.company_rating, name='company_rating'),

    # end point for orders
    path('place_order', views.place_order, name='place_order'),
    path('add_order_details/<int:pk>', views.add_order_details, name='add_order_details'),
    path('view_order_details/<int:pk>', views.view_order_details, name='view_order_details'),
    path('update_order_details/<int:pk>', views.update_order_details, name='update_order_details'),
]