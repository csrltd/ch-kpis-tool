from datetime import timezone
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Hospital, Department, Profile, Hospital
from .models import *
from .models import Patient, Hospital
from django.http import JsonResponse
from collections import defaultdict
import calendar
from django.db.models import Avg, Sum
from django.views.decorators.http import require_http_methods


#Permissions
from .decorators import *

#all view are secured to admin level. If you want to work on it, go
#the admin dashboard and change your user group to admin
from django.shortcuts import render
from django.http import JsonResponse
from .models import Turnover
from django.db.models.functions import TruncMonth
import datetime

from django.utils.timezone import make_aware
from django.db.models.functions import ExtractMonth, ExtractYear


def turnover_data(request, hospital_id=None):
    current_year = datetime.datetime.now().year
    hospitals = Hospital.objects.all()

    data = {
        'labels': [],
        'datasets': []
    }

    for hospital in hospitals:
        turnover_data = Turnover.objects.filter(hospital=hospital) \
                                        .annotate(month=TruncMonth('date_entered')) \
                                        .values('month') \
                                        .annotate(total=Sum('total'), voluntary=Sum('voluntary')) \
                                        .values('month', 'total', 'voluntary')

        turnover_dataset = {
            'label': hospital.name,
            'data': [],
            'fill': False
        }

        for item in turnover_data:
            month = item['month'].strftime('%b %y')
            turnover_dataset['data'].append(item['total'])
            data['labels'].append(month)

        data['datasets'].append(turnover_dataset)

        # print(f'Turnover data for {hospital.name}: {turnover_data}')

    # print(f'Final data: {data}')

    return JsonResponse(data)


@require_http_methods(['GET'])
def measures_data(request):
    measures = Measures.objects.values('hospital__name').annotate(
        total_mortality_rate=Sum('mortality_rate')
    ).order_by('hospital__name')
    
    return JsonResponse(list(measures), safe=False)

def hospital_mortality_rate(request):
    data = []
    hospitals = Hospital.objects.all()
    for hospital in hospitals:
        measures = Measures.objects.filter(hospital=hospital)
        mortality_rate_avg = measures.aggregate(Avg('mortality_rate'))['mortality_rate__avg']
        data.append({
            'hospital': hospital.name,
            'mortality_rate': mortality_rate_avg,
        })
    return JsonResponse(data, safe=False)

@admin_required
def index(request):
    profileInfo = Profile.objects.get(user=request.user)
    hospitals = Hospital.objects.all()
    inpatient_count = Patient.objects.filter(status='inpatient').count()
    outpatient_count = Patient.objects.filter(status='outpatient').count()
    acute_bed_count = Bed.objects.filter(type='acute bed').count()
    swing_bed_count = Bed.objects.filter(type='swing bed').count()

    # Group Measures objects by hospital and date, and aggregate the sum of readmissions
    readmissions_by_hospital_and_date = Measures.objects.values('hospital', month=ExtractMonth('date_entered'), year=ExtractYear('date_entered')).annotate(total_readmissions=Sum('readmissions'))

    hospital_data = {} 
    for readmission in readmissions_by_hospital_and_date:
        hospital = Hospital.objects.get(id=readmission['hospital'])
        month = readmission['month']
        year = readmission['year']
        total_readmissions = readmission['total_readmissions']
        hospital_data.setdefault(hospital.name, {})[month] = total_readmissions

    # list of hospitals
    hospitals_list = Hospital.objects.order_by('name')

    # Create a list of months in the order you want them to be displayed
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    table_data = []
    for hospital in hospitals_list:
        hospital_row = {
            'hospital': hospital.name,
            'jan': hospital_data[hospital.name].get(1, 0),
            'feb': hospital_data[hospital.name].get(2, 0),
            'mar': hospital_data[hospital.name].get(3, 0),
            'apr': hospital_data[hospital.name].get(4, 0),
            'may': hospital_data[hospital.name].get(5, 0),
            'jun': hospital_data[hospital.name].get(6, 0),
            'jul': hospital_data[hospital.name].get(7, 0),
            'aug': hospital_data[hospital.name].get(8, 0),
            'sep': hospital_data[hospital.name].get(9, 0),
            'oct': hospital_data[hospital.name].get(10, 0),
            'nov': hospital_data[hospital.name].get(11, 0),
            'dec': hospital_data[hospital.name].get(12, 0),
        }
        table_data.append(hospital_row)

    context = {
        'hospitals': hospitals,
        'inpatient_count': inpatient_count,
        'outpatient_count': outpatient_count,
        'acute_bed_count': acute_bed_count,
        'swing_bed_count': swing_bed_count,
        'profileInfo': profileInfo,
        'hospitals_list': hospitals_list,
        'hospital_data': hospital_data,
        'months': months,
        'table_data': table_data,
    }
        
    return render(request, 'dashboard/index.html', context)




@admin_required
def chart_data(request):
    
    bed_data = Bed.objects.all().count()
    acute_bed = Bed.objects.filter(type="acute bed").count()
    swing_bed = Bed.objects.filter(type="swing bed").count()
    hospitals = Hospital.objects.all().count()
    print(hospitals)
    
    
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


# displaying numbers of bed and patients in each hospital to the cards
@admin_required
def hospital_numbers(request):
    hospitals = Hospital.objects.all()
    inpatient_count = Patient.objects.filter(status='inpatient').count()
    outpatient_count = Patient.objects.filter(status='outpatient').count()
    acute_bed_count = Bed.objects.filter(type='acute bed').count()
    swing_bed_count = Bed.objects.filter(type='swing bed').count()

    context = {
        'hospitals': hospitals,
        'inpatient_count': inpatient_count,
        'outpatient_count': outpatient_count,
        'acute_bed_count': acute_bed_count,
        'swing_bed_count': swing_bed_count,
    }

    return render(request, 'dashboard/index.html', context)


# New way to get data
@admin_required
def filter_patients_by_month(request):
    hospital_names = Hospital.objects.all()
    data = {}
    for hospital_name in hospital_names:
        inpatient_hospital = Patient.objects.filter(hospital=hospital_name, status='inpatient')
        inpatient_data = inpatient_hospital.values_list('admission_date', flat=True)
        inpatient_data_by_month = defaultdict(int)
        for date in inpatient_data:
            month = date.month
            inpatient_data_by_month[month] += 1
        
        outpatient_hospital = Patient.objects.filter(hospital=hospital_name, status='outpatient')
        outpatient_data = outpatient_hospital.values_list('admission_date', flat=True)
        outpatient_data_by_month = defaultdict(int)
        for date in outpatient_data:
            month = date.month
            outpatient_data_by_month[month] += 1
        
        months = [calendar.month_name[month] for month in range(1, 13)]
        inpatient_totals = [inpatient_data_by_month[month] for month in range(1, 13)]
        outpatient_totals = [outpatient_data_by_month[month] for month in range(1, 13)]
        if hospital_name.name not in data:
            data[hospital_name.name] = {}
        data[hospital_name.name]['months'] = months
        data[hospital_name.name]['inpatient_totals'] = inpatient_totals
        data[hospital_name.name]['outpatient_totals'] = outpatient_totals
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

def logOutPage(request):
    user = request.user
    logout(request.user)

    return redirect('login')

@admin_required
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


@admin_required
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

@admin_required
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

@admin_required
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

@admin_required
def bed(request):
    return render(request, 'dashboard/addnewbed.html')

@admin_required
def metrics(request):
    return render(request, 'dashboard/addmetrics.html')

@admin_required
def newEntry(request):
    return render(request, 'dashboard/new-entry.html')

@admin_required
def HospitalCreateView(request):
    form = ""
    if form.is_valid():
        id_suffix = str(random.randint(0, 999)).zfill(4)
        id_prefix="CH"
        hospital_id=f"{id_prefix}{id_suffix}"







