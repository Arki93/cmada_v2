from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Case, When, F, IntegerField, Q, Count
from django.urls import reverse
from .models import Product, Stock, Site
from .forms import productmodelForm, stockmodelForm

def landing_page(request):
    return render(request, 'index.html')

def product_view(request):
    
    conditional_expression = Case(
        When(stock__entry_status=True, then=F('stock__product_qty')),
        When(stock__entry_status=False, then=-F('stock__product_qty')),
        default=0,
        output_field=IntegerField(),
    )
    
    products = Product.objects.all()
    
    products_with_total_qty = products.annotate(total_qty=Sum(conditional_expression))
    
     # Get unique product types
    unique_product_types = Product.objects.values_list('product_type', flat=True).distinct()

    # Annotate the count of each product type
    product_types_with_count = Product.objects.values('product_type').annotate(type_count=Count('product_type'))   
    
    context = {         
        'products': products_with_total_qty, 
        'unique_product_types': unique_product_types,
        'product_types_with_count': product_types_with_count,   
        }
    
    return render(request, 'product_view.html', context)

def product_detail(request, product_id):
    
    product = get_object_or_404(Product, product_id=product_id)    
    product_stock = Stock.objects.filter(product_name=product)
    total_qty = 0

    for stock_entry in product_stock:
        if stock_entry.entry_status:
            total_qty += stock_entry.product_qty
        else:
            total_qty -= stock_entry.product_qty
    
    context = {
        'product': product,
        'product_stock': product_stock,
        'total_qty': total_qty
    }
    
    return render(request, 'product_detail.html', context)

def type_detail(request, product_type):
    
    products = Product.objects.filter(product_type=product_type)    
    product_stock = Stock.objects.filter(product_name__in=products)
    
    # Annotate the total quantity for each product
    products = products.annotate(total_qty=Sum(
        Case(
            When(stock__entry_status=True, then=F('stock__product_qty')),
            When(stock__entry_status=False, then=-F('stock__product_qty')),
            default=0,
            output_field=IntegerField(),
        )
    ))
    
    context = {
        'products': products,
        'product_type': product_type,
        'product_stock': product_stock,        
    }
    
    return render(request, 'type_view.html', context)

def add_stock(request):
    
    form = stockmodelForm()
    if request.method == 'POST':        
        form = stockmodelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products')
    
    context = {
        'form': form
        }
    
    return render(request, 'add_stock.html', context)

def add_product(request):
    
    form = productmodelForm()
    if request.method == 'POST':        
        form = productmodelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products')
    
    context = {
        'form': form
        }
    
    return render(request, 'add_product.html', context)

def update_product(request, pk):
        
    product = Product.objects.get(id=pk)
    form = productmodelForm(instance=product)
    
    if request.method == 'POST':        
        form = productmodelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'update_product.html', context)
    
def delete_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    stock.delete()
    return redirect('/products')

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/products')

def product_search(request):
    search_query = request.GET.get('search_query','').strip()
    
    if search_query:        
        products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(product_type__icontains=search_query))
    else:
        products = Product.objects.all()
    
    products_with_total_qty = products.annotate(total_qty=Sum('stock__product_qty'))
    
    context ={
        'products': products_with_total_qty,
        'search_query': search_query,
    }
        
    return render(request, 'product_search.html', context)

def sell_product(request, pk):
    product = Stock.objects.get(id=pk)
    
    if request.method == 'POST':        
        sell_qty = int(request.POST.get('sell_qty', 0))        
        
        if sell_qty > 0 and sell_qty <= product.product_qty:           
            product.product_qty -= sell_qty
            product.save()
            return redirect('/products')
        else:            
            error_message = "Insufficient stock for the requested quantity."
    else:        
        error_message = None    
    context = {
        'product': product,
        'error_message': error_message,
    }    
    return render(request, 'sell_product.html', context)


from .forms import stockmodelForm  # Import the correct form

def transfer_product(request, pk):
    product = Stock.objects.get(id=pk)
    error_message = None  # Initialize error_message outside the if statement

    if request.method == 'POST':
        transfer_qty = int(request.POST.get('transfer_qty', 0))
        site_to = request.POST.get('site_to')

        if transfer_qty > 0 and transfer_qty <= product.product_qty:
            # Update existing stock quantity
            product.product_qty -= transfer_qty
            product.save()

            # Create a new stock entry
            new_stock_form = stockmodelForm()            
            new_stock_entry = new_stock_form.save(commit=False)
            new_stock_entry.product_name = product.product_name
            new_stock_entry.product_qty = transfer_qty
            new_stock_entry.product_site = site_to                
            new_stock_entry.stock_DDM = product.stock_DDM
            new_stock_entry.save()

            return redirect('/products')  # Redirect after both updates

        else:
            error_message = "Insufficient stock for the requested quantity."

    new_stock_form = stockmodelForm()

    context = {
        'product': product,
        'error_message': error_message,
        'new_stock_form': new_stock_form,
    }

    return render(request, 'transfer_product.html', context)

def update_stock(request, pk):
        
    stock = Stock.objects.get(id=pk)
    form = stockmodelForm(instance=stock)
    
    if request.method == 'POST':        
        form = stockmodelForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect(reverse('products:view_product', kwargs={'product_id': stock.product_name.product_id}))
    
    context = {
        'form': form,
        'stock': stock,
    }
    
    return render(request, 'update_stock.html', context)

def index_invoices(request):
    context = {}
    return render(request, 'invoices/pages/index.html', context)









