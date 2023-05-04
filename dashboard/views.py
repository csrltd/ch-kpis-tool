from datetime import timezone
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Hospital, Department, Profile, Hospital
from .models import *
from .models import Patient, Hospital
from django.http import JsonResponse

def index(request):
    
    return render(request, 'dashboard/index.html')

def chart_data(request):
    
    bed_data = Bed.objects.all().count()
    acute_bed = Bed.objects.filter(type="acute bed").count()
    swing_bed = Bed.objects.filter(type="swing bed").count()
    
    
    patient_data = Patient.objects.all().count()
    inpatient = Patient.objects.filter(status="inpatient").count()
    outpatient = Patient.objects.filter(status="outpatient").count()
     
    context = {
        'patient_data': patient_data, 
        'bed_data':bed_data,
        'swing_bed':swing_bed,
        'acute_bed':acute_bed,
        'swing_bed':swing_bed,
        'inpatient':inpatient,
        'outpatient':outpatient
    }

    return JsonResponse(context)

# New way to get data

def filter_inpatients_by_month(request):
    hospital_names = Hospital.objects.all()
    print("these are the hospital names", hospital_names)
    data = {}
    for hospital_name in hospital_names:
        patient_hospital = Patient.objects.filter(hospital=hospital_name, status='inpatient')
        inpatient_data = patient_hospital.values_list('admission_date', flat=True)
        inpatient_data = [date.strftime('%B') for date in inpatient_data]
        inpatient_data_by_month = {}
        for month in inpatient_data:
            if month not in inpatient_data_by_month:
                inpatient_data_by_month[month] = 0
            inpatient_data_by_month[month] += 1
        if hospital_name not in data:
            data[hospital_name.name] = {}
        data[hospital_name.name]['months'] = list(inpatient_data_by_month.keys())
        data[hospital_name.name]['totals'] = list(inpatient_data_by_month.values())
    return JsonResponse(data)

def signup(request):
    form = UserRegistration()
    context = {'form': form}
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            custom_user = Profile.objects.create(user=user)
            if not custom_user.is_profile_completed:
                return redirect('complete-profile')
            return redirect('login')
    else:
        form = UserRegistration()

    return render(request, 'authentication/signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(
                request, 'Invalid credentials!!! Please enter correct username or password')
    return render(request, 'authentication/login.html')


def hospitalDashboard(request):
    form = HospitalForm()
    context = {'form': form}
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = HospitalForm()

    return render(request, 'dashboard/hospitaldashboard.html', context)


def departement(request):
    hospitals = Hospital.objects.all()
    if request.method == 'POST':
        department_Id = request.POST.get('departmentid')
        name = request.POST.get('name')
        hospital_id = request.POST.get('hospital')
        hospital = Hospital.objects.get(id=hospital_id)
        department = Department(
            department_Id=department_Id, name=name, hospital=hospital)
        department.save()
        return redirect('index')

    context = {'hospitals': hospitals}
    return render(request, 'dashboard/add-departement.html', context)


def complete_profile(request):
    hospitals = Hospital.objects.all()
    departments = Department.objects.all()
    form = HospitalForm()
    
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            user = request.user
            custom_user = Profile.objects.get(user=user)
            department_id = request.POST.get('department')
            hospital_id = request.POST.get('hospital')
            custom_user.department = department_id
            custom_user.hospital = hospital_id
            custom_user.role = request.POST.get('role')
            custom_user.is_profile_completed = True

            custom_user.save()

            return redirect('login')

        return redirect('login')
    else:
        form = HospitalForm()
    
    context = {
        'form': form,
        'hospitals': hospitals,
        'departments': departments,
    }

    return render(request, 'dashboard/complete-profile.html', context)


def patient(request):
    users = Profile.objects.filter(role='doctor')
    form = patientForm()
    
    if request.method == 'POST':
        form = patientForm(request.POST)
        if form.is_valid():
            print("form is valid")
            patient = form.save(commit=False)
            patient.hospital = Hospital.objects.get(id=request.POST.get('hospital'))
            patient.doctor = Profile.objects.get(id=request.POST.get('doctor'))

            patient.save()
            return redirect('index')
        else:
            print(form.errors)
    context = {'users': users, 'form': form}
    return render(request, 'dashboard/addpatient.html', context)


def bed(request):
    return render(request, 'dashboard/addnewbed.html')


def metrics(request):
    return render(request, 'dashboard/addmetrics.html')


def newEntry(request):
    return render(request, 'dashboard/new-entry.html')