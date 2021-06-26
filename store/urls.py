from django.urls import path
from . import views 


urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path("contact/", views.contact, name="contact"),
	path("about/", views.about, name="about"),



	path('signup/', views.signup,name="signup"),
	path('login/', views.Login,name="login"),
	path('logout/', views.Logout,name="logout"),



	path('search/', views.search,name="search"),
	

	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),


]
