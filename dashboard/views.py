from django.shortcuts import render


def register(request):
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def hopsital(request):
    return render(request, 'dashboard/hopsital.html')

