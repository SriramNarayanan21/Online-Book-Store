from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
import json
import datetime
from .models import *
from  .forms import CreateUserForm
from .forms import ContactForm
from .utils import cookieCart, cartData, guestOrder




# Create your views here.


def store(request):

	data = cartData(request)


	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	
	books = None
	categories = Category.get_all_categories()
	categoryID = request.GET.get('category')
	if categoryID:
		books = Book.get_all_books_by_categoryid(categoryID)
	else: 
		books = Book.get_all_books()

	paginator = Paginator(books, per_page=12)
	page_no = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_no)

	context = {'books' :page_obj.object_list,'categories':categories, 'cartItems': cartItems, 'paginator': paginator, 'page_no':int(page_no)}
	return render(request,'store/store.html', context)

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ('store')
      
	form = ContactForm()
	return render(request, "contact.html", {'form':form})


def about(request):
	return render(request, "about.html")

def signup(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get(' username ')
			messages.success(request, 'Account has been created for ' +  user)

			return redirect('login')
			
	context = {'form' : form}
	return render(request, 'signup.html',context)

def Login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username= username, password= password)

		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Username Or password is incorrect')

	context={}
	return render(request, 'login.html',context) 

def Logout(request):
	logout(request)
	return redirect('login')
	


def search(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	q= request.GET['q']
	data = Book.objects.filter(Book_name__icontains= q ).order_by('id')
	context = {'data' : data,'items': items, 'order': order , 'cartItems' : cartItems}
	return render(request, 'store/store.html', context)



def cart(request):
	data = cartData(request)


	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items': items, 'order': order , 'cartItems' : cartItems }
	return render(request,'store/cart.html', context)
			

def checkout(request):
	data = cartData(request)


	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items': items, 'order': order, 'cartItems' : cartItems }
	return render(request,'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	bookId = data['bookId']
	action = data['action']

	print('Action:',action)
	print('bookId:',bookId)


	customer = request.user.customer
	book = Book. objects.get(id=bookId)
	order, created = Order.objects.get_or_create(customer= customer, complete= False)

	orderItem, created = OrderItem.objects.get_or_create(order = order, book = book)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
  		orderItem.delete()

	return JsonResponse('Item was added',safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)


	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		
				
	else:
		customer, order = guestOrder(request, data)
		
			

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
			ShippingAddress.objects.create(customer=customer,order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)

	return JsonResponse('Payment submitted..',safe=False)
			

