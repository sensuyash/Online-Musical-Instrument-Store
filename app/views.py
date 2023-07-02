from django.shortcuts import render,redirect
from .models import Customer,Product,OrderPlaced,Cart
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView


class ProductView(View):
    def get(self, request):
        non_electrical=Product.objects.filter(category='NEI')
        electrical=Product.objects.filter(category='EI')
        nonpercussion=Product.objects.filter(category='NP')
        percussion=Product.objects.filter(category='P')
        return render(request,'app/home.html',{'electrical':electrical,'non_electrical':non_electrical,'nonpercussion':nonpercussion,'percussion':percussion})


class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

def percussion(request,data=None):
    if data==None:
        percussion =Product.objects.filter(category='P')
    elif data == 'below':
        percussion = Product.objects.filter(category='P').filter(discounted_price__lt=5000)
    elif data == 'above': 
        percussion = Product.objects.filter(category='P').filter(discounted_price__gt=10000)       
    return render(request, 'app/percussion.html',{'percussion':percussion})   


def nonpercussion(request,data=None):
    if data==None:
        non_percussion=Product.objects.filter(category='NP')
    elif data=='Yamaha' or data=='Givson':
        non_percussion = Product.objects.filter(category='NP').filter(brand='data')
    elif data == 'below':
        non_percussion = Product.objects.filter(category='NP').filter(discounted_price__lt=5000)
    elif data == 'above': 
        non_percussion = Product.objects.filter(category='NP').filter(discounted_price__gt=10000)       
    return render(request, 'app/nonpercussion.html',{'non_percussion':non_percussion})    

def guitar(request,data=None):
    if data==None:
        guitar=Product.objects.filter(category='G')
    elif data == 'below':
        guitar= Product.objects.filter(category='G').filter(discounted_price__lt=5000)
    elif data == 'above': 
        guitar= Product.objects.filter(category='G').filter(discounted_price__gt=10000) 	      
    return render(request, 'app/guitar.html',{'guitar':guitar})        

def harmonium(request,data=None):
    if data==None:
        harmonium=Product.objects.filter(category='H')
    elif data == 'below':
        harmonium= Product.objects.filter(category='H').filter(discounted_price__lt=5000)
    elif data == 'above': 
        harmonium= Product.objects.filter(category='H').filter(discounted_price__gt=10000)       
    return render(request, 'app/harmonium.html',{'harmonium':harmonium})        
  

def tabla(request,data=None):
    if data==None:
        tabla=Product.objects.filter(category='T')
    elif data == 'below':
        tabla= Product.objects.filter(category='T').filter(discounted_price__lt=5000)
    elif data == 'above': 
        tabla= Product.objects.filter(category='T').filter(discounted_price__gt=10000)       
    return render(request, 'app/tabla.html',{'tabla':tabla})        

def keyboard(request,data=None):
    if data==None:
        keyboard=Product.objects.filter(category='K')
    elif data == 'below':
        keyboard= Product.objects.filter(category='K').filter(discounted_price__lt=5000)
    elif data == 'above': 
        keyboard= Product.objects.filter(category='K').filter(discounted_price__gt=10000)       
    return render(request, 'app/keyboard.html',{'keyboard':keyboard})    

def sitar(request,data=None):
    if data==None:
        sitar=Product.objects.filter(category='SI')
    elif data == 'below':
        sitar= Product.objects.filter(category='SI').filter(discounted_price__lt=5000)
    elif data == 'above': 
        sitar= Product.objects.filter(category='SI').filter(discounted_price__gt=10000)       
    return render(request, 'app/sitar.html',{'sitar':sitar})        

       

def cajonbox(request,data=None):
    if data==None:
        cajonbox=Product.objects.filter(category='CB')
    elif data == 'below':
        cajonbox= Product.objects.filter(category='CB').filter(discounted_price__lt=5000)
    elif data == 'above': 
        cajonbox= Product.objects.filter(category='CB').filter(discounted_price__gt=10000)       
    return render(request, 'app/cajonbox.html',{'cajonbox':cajonbox})        


def voilin(request,data=None):
    if data==None:
        voilins=Product.objects.filter(category='V')
    elif data == 'below':
        voilins= Product.objects.filter(category='V').filter(discounted_price__lt=5000)
    elif data == 'above': 
        voilins= Product.objects.filter(category='V').filter(discounted_price__gt=10000)       
    return render(request, 'app/voilin.html',{'voilins':voilins})        

def melodica(request,data=None):
    if data==None:
        melodica=Product.objects.filter(category='HM')
    elif data == 'below':
        melodica= Product.objects.filter(category='HM').filter(discounted_price__lt=5000)
    elif data == 'above': 
        melodica= Product.objects.filter(category='HM').filter(discounted_price__gt=10000)       
    return render(request, 'app/melodica.html',{'melodica':melodica})        


@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    c=Cart(user=user,product=product)
    c.save()
    return redirect('/cart/')
@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 99.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'app/emptycart.html', {'totalitem':totalitem})


def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 99.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount

		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


        
def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 99.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount
			
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")




def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= .0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount
			
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

 

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add,'active':'btn-danger'})


@login_required   
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'app/orders.html', {'order_placed':op})





class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})    
class PasswordChangeView(auth_views.PasswordChangeView):
    template_name="app/password_change.html"
    form_class="MyPasswordChangeForm"   
    success_url='/passwordchangedone/'

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-info', 'totalitem':totalitem,'active':'btn-danger'})


@login_required   
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 99.00
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
			totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})      
	

	
	
class SearchView(TemplateView):
	template_name='app/searchp.html'  
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		kw=self.request.GET.get("keyword")
		results=Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
		context['results']=results
		print(context)
	
		return context
	
	
@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")
	

