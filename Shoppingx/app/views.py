from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from social_django.utils import psa
from django.urls import reverse_lazy
from django.views import View
from . models import Customer, Product, Cart, OrderPlaced
from . forms import CustomRegistrationForm,LoginForm, CustomerProfileForm
from django.contrib import messages
from django.utils.translation import gettext,gettext_lazy as _ 
from  django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#  show product in home
class ProductView(View):
    def get(self,request):
        totalitem=0
        top_wears=Product.objects.filter(category='TW')
        bottom_wears=Product.objects.filter(category='BW')
        laptop=Product.objects.filter(category='L')
        mobile=Product.objects.filter(category='M')
        kurti=Product.objects.filter(category='ku')
        shoes=Product.objects.filter(category='so')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'topwear':top_wears,'bottomwear':bottom_wears,'mobile':mobile,'laptop':laptop,'kurti':kurti,'shoes':shoes,'totalitem':totalitem})

class ProductDetailView(View):
    totalitem=0
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':self.totalitem})
    
### add product in cart
@login_required
def add_to_cart(request):
    totalitem=0
    user = request.user 
    product_id= request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return redirect('/cart',{'totalitem':totalitem})

##show product in cart
@login_required
def show_to_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user 
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        totl_amount=0.0
        cart_product=[p for p in Cart.objects.all()if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.selling_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/empty.html')

##plus amount or product in cart        
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all()if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.selling_price)
            amount+=tempamount
            
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            
        }
        return JsonResponse(data)
 
##minus product in cart           
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all()if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.selling_price)
            amount+=tempamount
            
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            
        }
        return JsonResponse(data)
    
####remove cart items
@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all()if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.selling_price)
            amount+=tempamount
        
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
    
###add address of user
@login_required
def address(request):
    totalitem=0
    add=Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',{'add':add, 'active':'btn-primary','totalitem':totalitem})

#your orders
@login_required
def orders(request):
    totalitem=0
    op=OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

# see your product detail before order
@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    if not add.exists():
        messages.warning(request, "Please add an address before proceeding.")
        return render(request, 'app/checkout.html', {'totalitem': totalitem})
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem})


# payment phase for order
@login_required
def payment_done(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')

    if not custid:
        messages.error(request, 'Please select an address before continuing.')
        return redirect('checkout')  # Redirect back to the checkout page
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        messages.error(request, 'Invalid customer. Please select a valid address.')
        return redirect('checkout')  # Redirect back to the checkout page
    cart = Cart.objects.filter(user=user)
    for cart_item in cart:
        OrderPlaced(user=user, customer=customer, product=cart_item.product, quantity=cart_item.quantity).save()
        cart_item.delete()
    messages.success(request, 'Order placed successfully.')
    return redirect('orders')


# user Profile code
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary','totalitem':totalitem})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user  # Set the user field
            form.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
 
            
#   login ,Registration , Logout code
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    # def post(self,request):
    #     form=CustomRegistrationForm(request.POST)
    #     if form.is_valid():
    #         messages.success(request,'Congratulations!! Registered Succesfully')
    #         form.save()
    #     return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if user with the provided email already exists
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                messages.error(request, 'User with this email already exists. Please log in.')
                return redirect('login')  # Redirect to login page or handle it as needed
            else:
                messages.success(request, 'Congratulations!! Registered Successfully')
                form.save()
        return render(request, 'app/customerregistration.html', {'form': form})
    
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login')) 
    
# @psa('social:complete')
# def socialauth_signup(request, backend):
#     user = request.user

#     # Check if user with the provided email already exists
#     existing_user = User.objects.filter(email=user.email).first()

#     if existing_user:
#         messages.error(request, 'This email id is already registered. Please log in.')
#         return redirect('login')  # Redirect to login page or handle it as needed
#     else:
#         # If the user does not exist, proceed with saving the user data in the database
#         # Note: Ensure that the following code is not inadvertently being executed multiple times
#         try:
#             # Your user creation logic here (example: user.save())
#             messages.success(request, 'Congratulations!! Registered Successfully through Google authentication')
#             return redirect('home')  # Redirect to home page or handle it as needed
#         except Exception as e:
#             messages.error(request, 'Error during user creation. Please try again.')
#             return redirect('login')  # Redirect to login page or handle it as needed  
 
 
            
 #     All Product filtring and Showing in home page code       
def Laptop(request, data=None):
    totalitem=0
    if data == None:
        laptop=Product.objects.filter(category='L')
    elif data=='Dell' or data=='hp' or data=='Lenvo':
        laptop=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptop=Product.objects.filter(category='L').filter(selling_price__lt=50000)
    elif data=='above':
        laptop=Product.objects.filter(category='L').filter(selling_price__gt=50000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})

def Bottomwear(request, data=None):
    totalitem=0
    if data == None:
        bottom=Product.objects.filter(category='BW')
    elif data=='lux' or data=='Lyra' or data=='carban':
        bottom=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottom=Product.objects.filter(category='BW').filter(selling_price__lt=500)
    elif data=='above':
        bottom=Product.objects.filter(category='BW').filter(selling_price__gt=500)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html',{'bottom':bottom,'totalitem':totalitem})

def Topwear(request, data=None):
    totalitem=0
    if data == None:
        top=Product.objects.filter(category='TW')
    elif data=='Puma' or data=='Rayon' or data=='cotton':
        top=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        top=Product.objects.filter(category='TW').filter(selling_price__lt=500)
    elif data=='above':
        top=Product.objects.filter(category='TW').filter(selling_price__gt=500)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html',{'top':top,'totalitem':totalitem})

def Kurti(request, data=None):
    totalitem=0
    if data == None:
        kurti=Product.objects.filter(category='ku')
    elif data=='silk' or data=='Rayon' or data=='cotton':
        kurti=Product.objects.filter(category='ku').filter(brand=data)
    elif data=='below':
        kurti=Product.objects.filter(category='ku').filter(selling_price__lt=2000)
    elif data=='above':
        kurti=Product.objects.filter(category='ku').filter(selling_price__gt=2000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/kurti.html',{'kurti':kurti,'totalitem':totalitem})

def mobile(request,data=None):
    totalitem=0
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Realme8s' or data=='Samsung' or data=='Realme8' or data=='Apple':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(selling_price__lt=15000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(selling_price__gt=15000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def shoes(request,data=None):
    totalitem=0
    if data == None:
        shoes=Product.objects.filter(category='so')
    elif data=='Adda' or data=='Adidas' or data=='Nike':
        shoes=Product.objects.filter(category='so').filter(brand=data)
    elif data=='below':
        shoes=Product.objects.filter(category='so').filter(selling_price__lt=1500)
    elif data=='above':
        shoes=Product.objects.filter(category='so').filter(selling_price__gt=1500)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/shoes.html',{'shoes':shoes,'totalitem':totalitem})
