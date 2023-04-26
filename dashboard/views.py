from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Hospital, Department, Profile
from .models import *
import json
from django.db.models import Count

def index(request):
    
    bed_data = Bed.objects.all().count()
    acute_bed = Bed.objects.filter(type="acute bed").count()
    swing_bed = Bed.objects.filter(type="swing bed").count()
    print("acuteBed data",acute_bed, "swingBed data",swing_bed)
    bed_labels = list(Bed.objects.values('type').annotate(count=Count('type')).values_list('type', flat=True))
    patient_data = Patient.objects.all().count()
    inpatient = Patient.objects.filter(status="inpatient").count()
    outpatient = Patient.objects.filter(status="outpatient").count()
    print("Inpatient data:",inpatient, "outpatient data",outpatient)
    patient_labels = list(Patient.objects.values('status').annotate(count=Count('status')).values_list('status', flat=True))


    context = {
        'patient_data': (patient_data),
        'patient_labels': json.dumps(patient_labels),
        'bed_data': (bed_data, swing_bed),
        'bed_labels': json.dumps(bed_labels),
        'acute_bed':(acute_bed),
        'swing_bed':(swing_bed),
        'inpatient':(inpatient),
    }
    
    return render(request, 'dashboard/index.html', context)

     
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
