<<<<<<< HEAD
from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
=======
from django.contrib import admin 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hospitaldashboard',views.hospitaldashboard, name='hospitaldashboard'),
>>>>>>> frontend
]