from django.shortcuts import render, redirect
from .forms import UserRegistration, HospitalForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Hospital, Department, CustomUser


def index(request):
    return render(request, 'dashboard/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            if user.customUser.is_profile_completed:
                return redirect('add-user')
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
    return render(request, 'dashboard/hospitaldashboard.html', {'form': form})

def departement(request):
    if request.method == 'POST':
        department_Id = request.POST.get('departmentid')
        name = request.POST.get('name')
        hospital_id = request.POST.get('hospital')
        hospital = Hospital.objects.get(id=hospital_id)
        department = Department(department_Id=department_Id, name=name, hospital=hospital)
        department.save()
        return redirect('index')

    hospitals = Hospital.objects.all()
    return render(request, 'dashboard/add-departement.html', {'hospitals': hospitals})

def addUser(request):
    return render(request, 'dashboard/adduser.html')

def patient(request):
    return render(request, 'dashboard/addpatient.html')

def bed(request):
    return render(request, 'dashboard/addnewbed.html')

def metrics(request):
    return render(request, 'dashboard/addmetrics.html')

def newEntry(request):
    return render(request, 'dashboard/new-entry.html')