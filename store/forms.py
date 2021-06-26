from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import User

class  OrderForm(ModelForm):
	class Meta:
		model = Order
		fields ='__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)
			
		
	