from django.shortcuts import render, redirect
from .forms import UserRegistration, HospitalForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    return render(request, 'dashboard/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistration()
    return render(request, 'authentication/signup.html', {'form': form})




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('add-user')
        else:
            messages.error(request, 'Invalid credentials!!! Please enter correct username or password')
    return render(request, 'authentication/login.html')

def hospitalDashboard(request):
    form = HospitalForm()
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = HospitalForm()
            print(form.errors)
    return render(request, 'dashboard/hospitaldashboard.html', {'form': form})

def addUser(request):
    return render(request, 'dashboard/adduser.html')

def patient(request):
    return render(request, 'dashboard/addpatient.html')

def departement(request):
    return render(request, 'dashboard/add-departement.html')

def metrics(request):
    return render(request, 'dashboard/addmetrics.html')

def newEntry(request):
    return render(request, 'dashboard/new-entry.html')