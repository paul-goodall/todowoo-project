from django.urls import path
from . import views

my_urls = [
    path('', views.home, name='home'),
    path('signup/',  views.signupuser, name='signupuser'),
    path('logout/',  views.logoutuser, name='logoutuser'),
    path('login/',   views.loginuser,  name='loginuser'),
]
