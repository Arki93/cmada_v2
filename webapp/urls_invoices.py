from django.urls import path, re_path
from .views import index_invoices
app_name = 'factures'

urlpatterns = [
    path('', index_invoices, name='factures'), 
    ]