import json
from django.http.response import JsonResponse
from app.forms import  CustomerProfileForm, CustomerRegistrationForm, BillingForm
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from .models import Customer, Product,Cart,OrderPlaced
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops =Product.objects.filter(category ='L')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'totalitem':totalitem})
# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk = pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user =request.user)).exists() 
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user 
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id= product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

#@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user 
        carts = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount =70.0
        total_amount =0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user ]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price) 
                amount +=tempamount
                totalamount =amount+shipping_amount
            return render(request , 'app/addtocart.html', {'carts':carts, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html' ,{'totalitem':totalitem})
     

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount =70.0
        total_amount =0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price) 
            amount +=tempamount
            
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
             }
        return JsonResponse(data)


def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount =70.0
        total_amount =0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price) 
            amount +=tempamount
            
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount

            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        totalitem =0
        totalitem = len(Cart.objects.filter(user=request.user))
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount =70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price) 
            amount +=tempamount
           
        data ={
            'amount': amount,
            'totalamount':amount+shipping_amount,
            'totalitem':totalitem
            }

        return JsonResponse(data)
        
        
@login_required
def buy_now(request, pk):
    product = Product.objects.get(pk =pk)
    user = request.user
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user =request.user)).exists()
        if item_already_in_cart:
            cart = Cart.objects.get(Q(product=product.id) & Q(user =request.user))
            quantity = cart.quantity+1
            cart.quantity = quantity
            cart.save()
        else:
            Cart(user=user, product=product,quantity=1).save() 
    else:
        Cart(user=user, product=product,quantity=1).save() 
    return redirect('/checkout')

# def profile(request):
# return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html' , {'add':add, 'activate':'btn-primary'})


#def change_password(request):
# return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data =='Nokia' or data == 'BlackBerry' or data=='IPhone':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=800)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=800)
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Asus' or data == 'Apple' or data =='Dell' or data == 'Acer' or data=='Lenevo':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=120000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=120000)
    
    return render(request, 'app/laptop.html', {'laptops':laptops})


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Polo' or data == 'Gucci' or data =='Park' or data == 'Lee' :
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
    
    return render(request, 'app/topwear.html', {'topwears': topwears})

def bottomwear(request, data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'Rebook' or data == 'Gas' or data =='levis' or data == 'Lee'  :
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
    
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear})
    


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

def search(request):
    query = request.GET.get('query')
    allresults= Product.objects.filter(title__icontains= query)
    return render(request, 'app/search.html',{'allresults': allresults})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation!! Registered Sucessfully")
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add =Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount =70.0
    totalamount =0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price) 
            amount +=tempamount
        totalamount= amount +shipping_amount
    return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


@login_required
def payment_done(request):
    user =request.user
    custid =request.GET['custid']
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user =user)
    amount = 0.0
    shipping_amount =70.0
    totalamount =0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
    cart_len =len(cart_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price) 
            amount +=tempamount
        totalamount = amount +shipping_amount
    for c in cart:
        bill = BillingForm( initial={'name': customer.name, 'state': customer.state, 'locality':customer.state, 'totalamount':totalamount ,'totalitems':cart_len ,'date' : timezone.now()}   )
        same =  OrderPlaced.objects.filter(user=c.user, customer =customer, product=c.product, quantity=c.quantity)
        if same:
            OrderPlaced(user=user, customer =customer, product=c.product, quantity=c.quantity+1).save()
            order =OrderPlaced.objects.filter(Q(user=user) & Q(customer =customer), Q(product=c.product) & Q(quantity=c.quantity))
            order.delete()
            c.delete()
            
        else:
            OrderPlaced(user=user, customer =customer, product=c.product, quantity=c.quantity).save()
        # order =OrderPlaced.objects.filter(Q(user=user) & Q(customer =customer) & Q(quantity=c.quantity))
            # c.delete()  
        
        
        return render(request, 'app/khaltirequest.html', {'totalamount':totalamount, 'bill':bill, 'cart_product':cart_product} )




@csrf_exempt
def verify_payment(request):
   data = request.POST
   product_id = data['product_identity']
   token = data['token']
   amount = data['amount']

   url = "https://khalti.com/api/v2/payment/verify/"
   payload = {
   "token": token,
   "amount": amount
   }
   headers = {
   "Authorization": "Key test_secret_key_b353851a471942288dde2a5d0082eba1"
   }
   

   response = requests.post(url, payload, headers = headers)
   
   response_data = json.loads(response.text)
   status_code = str(response.status_code)
   print(response_data)

   if status_code == '400':
      response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
      return response

   import pprint 
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(response_data)
   
   return JsonResponse(f"Payment Done !! With IDX. { response_data['user']['idx']}",safe=False)




@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed': op})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form,'activate':'btn-primary'})

    def post(self, request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode  = form.cleaned_data['zipcode']
            reg = Customer(user= usr, name = name, locality =locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation ! Profile Updated Sucessfully')
        return render(request, 'app/profile.html', {'form': form, 'activate':'btn-primary'})