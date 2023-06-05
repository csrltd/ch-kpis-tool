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
    path('turnover-data/', views.turnover_data, name='turnover-data'),
    path('charts-data/', views.chart_data, name='charts-data'),
    path('filter-patients-by-month/', views.filter_patients_by_month, name='filter-patients-by-month'),
    path('single-hospital/<int:hospital_id>', views.singleHospital, name="single-hospital"),
    path('add-measures/',views.addMeasures,name='add-measures'),
    path('add-census/',views.addCensus,name='add-census'),
    path('add-turnover/',views.addTurnover,name='add-turnover'),
    path('add-hiring/',views.addHiring,name='add-hiring'),
    path('single-hospital/<int:hospital_id>/measures',views.measuresView,name='single-hospital-measures'),
    

    # fetching data url
    path('measures_data/', views.measures_data, name='measures_data'),
    path('single-hospital-data/<int:hospital_id>', views.singleHospitalData, name="single-hospital-data"),
    

    # urls that were used before but might be needed later
    path('patient/', views.patient, name='patient'),
    path('new-bed/', views.bed, name='new-bed'),
    path('add-department/', views.departement, name='add-department'),
    path('hospital-dashboard/', views.hospitalDashboard, name='hospital-dashboard'),
    path('metrics/', views.metrics, name='metrics'),
    path('new-entry/', views.newEntry, name='new-entry'),
    path('coming-soon/', views.comingSoon, name='coming-soon'),
]