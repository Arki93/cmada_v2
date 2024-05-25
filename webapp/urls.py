from django.urls import path, re_path
from .views import type_detail, product_view, product_detail, add_product, update_product, delete_stock, add_stock, product_search, sell_product, transfer_product, update_stock, delete_product
app_name = 'products'


urlpatterns = [    
    path('', product_view, name='home_product'),     
    path('search/', product_search, name='search_product'),
    path('create_product/', add_product, name='create_product'),
    path('create_stock/', add_stock, name='create_stock'),
    path('product/<str:product_id>/', product_detail, name='view_product'),
    path('type/<str:product_type>/', type_detail, name='view_type'), 
               
    path('<pk>/sell/', sell_product, name='sell_product'),
    path('<pk>/transfer/', transfer_product, name='transfer_product'),  
    path('<pk>/update_product/', update_product, name='update_product'),
    path('<pk>/delete_product/', delete_product, name='delete_product'), 
    path('<pk>/update_stock/', update_stock, name='update_stock'), 
    path('<pk>/delete_stock/', delete_stock, name='delete_stock'),     
]
    
