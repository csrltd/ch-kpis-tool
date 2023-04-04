
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse



def index(request):
    return render(request, 'index.html')

def hospitaldashboard(request):
    return render(request, 'hospitaldashboard.html')
