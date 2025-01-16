from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'), #empty is homepage
    #render file, send a html repsonse or json response in views
    path('about.html', views.about, name='about'),
    path('order.html', views.order, name='order'),
    path('location.html', views.location, name='location'),
    path('home.html', views.home, name='home'),
    path('user_page.html', views.userpage, name='userpage'),
    path('signup_page.html', views.signuppage, name='signuppage'),
    path('invoice.html', views.invoice, name='invoice'),
      
]