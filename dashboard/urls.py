from django.contrib import admin 
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutPage, name='logout'),
    path('complete-profile/', views.complete_profile, name='complete-profile'),

    # hospital dashboards
    path('', views.index, name='index'),
    path('turnover_data/', views.turnover_data, name='turnover_data'),
    path('charts-data/', views.chart_data, name='charts-data'),
    path('filter_patients_by_month/', views.filter_patients_by_month, name='filter_patients_by_month'),
    path('hospital_numbers/', views.hospital_numbers, name='hospital_numbers'),
    path('single-hospital/', views.singleHospital, name="single-hospital"),
    path('single-hospital-data/<int:hospital_id>', views.singleHospitalData, name="single-hospital-data"),

    # fetching data url
    path('measures_data/', views.measures_data, name='measures_data'),
    

    # urls that were used before but might be needed later
    path('patient/', views.patient, name='patient'),
    path('new-bed/', views.bed, name='new-bed'),
    path('add-department/', views.departement, name='add-department'),
    path('hospital-dashboard/', views.hospitalDashboard, name='hospital-dashboard'),
    path('metrics/', views.metrics, name='metrics'),
    path('new-entry/', views.newEntry, name='new-entry'),
]