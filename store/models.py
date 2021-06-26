from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user= models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
	name= models.CharField(max_length=200, null=True)
	email= models.CharField(max_length=200, null=True)


	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200, null=True)

	@staticmethod
	def get_all_categories():
		return Category.objects.all()

	def __str__(self):
		return self.name


class Book(models.Model):
	Book_name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits= 7, decimal_places= 2)
	Author_name = models.CharField(max_length=200, null=True)
	category = models.ForeignKey(Category, on_delete= models.CASCADE, null= True)
	digital = models.BooleanField(default=False, null=True, blank= False)
	image = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.Book_name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except :
			url = ''
		return url

	@staticmethod
	def get_all_books():
		return Book.objects.all()

	@staticmethod
	def get_all_books_by_categoryid(category_id):
		if category_id:
			return Book.objects.filter(category= category_id)
		else:
			return Book.get_all_books()
		
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, blank= True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank= False)
	transaction_Id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
	 	shipping = False
	 	orderitems = self.orderitem_set.all()
	 	for i in orderitems:
	 		if i.book.digital == False:
	 		    shipping = True
	 	return shipping
	

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	


class OrderItem(models.Model):
	book = models.ForeignKey(Book, on_delete= models.SET_NULL,  null=True)
	order = models.ForeignKey(Order, on_delete= models.SET_NULL,  null=True)
	quantity =  models.IntegerField(default=0, null=True, blank= True) 
	date_added = models.DateTimeField(auto_now_add=True) 
	status = models.BooleanField(default=False)

	@property
	def get_total(self):
		total = self.book.price * self.quantity
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, blank= True, null=True)
	order = models.ForeignKey(Order, on_delete= models.SET_NULL, blank=True , null=True)
	address = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

	