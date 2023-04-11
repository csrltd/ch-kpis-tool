from django.contrib import admin 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('add-user/', views.addUser, name='add-user'),
    path('patient/', views.patient, name='patient'),
    path('new-bed/', views.bed, name='new-bed'),
    path('add-department/', views.departement, name='add-department'),
    path('hospital-dashboard/', views.hospitalDashboard, name='hospital-dashboard'),
    path('metrics/', views.metrics, name='metrics'),
    path('new-entry/', views.newEntry, name='new-entry'),
]