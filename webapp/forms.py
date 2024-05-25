from django import forms
from .models import Product, Stock

class productmodelForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = (
            'product_id',
            'product_name',
            'product_unit_price',
            'product_type',
            'on_going_command',
        )

class stockmodelForm(forms.ModelForm):
    
    class Meta:
        model = Stock   
        fields = (
            'product_name',
            'product_qty', 
            'product_site',           
            'stock_DDM', 
            'entry_status',         
        )



