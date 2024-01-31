from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import Product, Customer ,OrderPlaced ,Cart

@admin.register(Customer)
class Customermodel(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']
    
@admin.register(Product)
class Productmodel(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image']
    
@admin.register(Cart)
class Cartmodel(admin.ModelAdmin):  
    list_display=['id','user','product','quantity']
    
@admin.register(OrderPlaced)
class orderplacedmodel(admin.ModelAdmin): 
    list_display=['id','user','customer','product_info','product','quantity','ordered_date','status'] 
    def product_info(self,obj):
        link=reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link,obj.product.title)


# Register your models here.
