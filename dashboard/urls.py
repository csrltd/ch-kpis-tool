from django.contrib import admin 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charts-data/', views.chart_data, name='charts-data'),
    path('linechart/', views.linechart_data, name='linechart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('complete-profile/', views.complete_profile, name='complete-profile'),
    path('patient/', views.patient, name='patient'),
    path('new-bed/', views.bed, name='new-bed'),
    path('add-department/', views.departement, name='add-department'),
    path('hospital-dashboard/', views.hospitalDashboard, name='hospital-dashboard'),
    path('metrics/', views.metrics, name='metrics'),
    path('new-entry/', views.newEntry, name='new-entry'),
]