from django.contrib import admin 
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('turnover_data/', views.turnover_data, name='turnover_data'),
    path('charts-data/', views.chart_data, name='charts-data'),
    path('filter_patients_by_month/', views.filter_patients_by_month, name='filter_patients_by_month'),
    path('hospital_numbers/', views.hospital_numbers, name='hospital_numbers'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('complete-profile/', views.complete_profile, name='complete-profile'),
    path('patient/', views.patient, name='patient'),
    path('new-bed/', views.bed, name='new-bed'),
    path('add-department/', views.departement, name='add-department'),
    path('hospital-dashboard/', views.hospitalDashboard, name='hospital-dashboard'),
    path('metrics/', views.metrics, name='metrics'),
    path('new-entry/', views.newEntry, name='new-entry'),
    path('measures_data/', views.measures_data, name='measures_data'),
]