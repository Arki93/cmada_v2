from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum


class User(AbstractUser):
    pass 

class Product(models.Model):
    
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_unit_price = models.IntegerField(default=0)
    product_type = models.CharField(max_length=10)
    on_going_command = models.IntegerField(default=0)
     
    
    def __str__(self):
        return f'{self.product_id} {self.product_name}'
    

class Stock(models.Model):
    
    SITE_CHOISES = (
        ('LIL', 'Lille'),
        ('VIO', 'Violet'),
        ('VIA', 'Viaduc'),
        ('LOU', 'Lourmel'),
        )
    
    product_name = models.ForeignKey('Product', on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    product_site = models.CharField(choices=SITE_CHOISES, max_length=10)    
    stock_DDM = models.DateField(null=True)
    entry_status = models.BooleanField(default=True)
    mod_time = models.DateField(auto_now_add=True)
    
    
    def ddm_check(self):
        if self.stock_DDM:        
            today = timezone.now().date()
            ddm_exp = (self.stock_DDM - today).days
            return ddm_exp < 90
        else:
            return False
              
        
    def __str__(self):
        ddm_status = 'DDM Proche' if self.ddm_check() else 'OK'
        return f'{self.product_name} {self.product_site} {self.product_qty} {self.entry_status} {self.mod_time} {self.stock_DDM} {ddm_status}'    

class Site(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.name}'
    