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
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.db.models import Avg, Sum,DecimalField
from django.db.models.functions import Round
from django.views.decorators.http import require_http_methods
from django.db.models import Count


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
import uuid

def generate_password():
    password = str(uuid.uuid4())[:8]  
    return password


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
    page_title = 'Overview'
    profileInfo = Profile.objects.get(user=request.user)
    hospitals = Hospital.objects.all()
    inpatient_count = Census.objects.aggregate(total=Sum('inpatient'))['total']
    outpatient_count = Census.objects.aggregate(total=Sum('outpatient'))['total']
    swing_bed_count = Census.objects.aggregate(total=Sum('swing_bed'))['total']
    acute_swing_bed_transfers_count = Measures.objects.aggregate(total=Sum('acute_swing_bed_transfers'))['total']

    # added fields on the quick numbers cards
    emergency_room_count = Census.objects.aggregate(total=Sum('emergency_room'))['total']
    total_rural_health_clinic = Census.objects.aggregate(total=Sum('rural_health_clinic'))['total']

    measures_data = []
    fields = ['mortality_rate','readmissions','pressure_ulcer','discharges_home','emergency_room_transfers','acute_swing_bed_transfers','medication_errors','falls',
              'against_medical_advice','left_without_being_seen','hospital_acquired_infection','covid_vaccination_total_percentage_of_compliance','complaint','grievances'
              ]
    
    for i in fields:
        data = [{'field_name': i.replace('_',' ').capitalize()}]
        for j in range(1, 13):
            single_column = Measures.objects.annotate(month=ExtractMonth('date_entered'),)\
            .order_by('month')\
            .filter(month=j)\
            .aggregate(average= Round(Avg(i),2))
            data.append(single_column)
        measures_data.append(data)

    context = {
        'hospitals': hospitals,
        'inpatient_count': inpatient_count,
        'outpatient_count': outpatient_count,
        'swing_bed_count': swing_bed_count,
        'profileInfo': profileInfo,
        'measures_data': measures_data,
        'emergency_room_count': emergency_room_count,
        'total_rural_health_clinic': total_rural_health_clinic,
        'acute_swing_bed_transfers_count': acute_swing_bed_transfers_count,
        'page_title': page_title
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

@admin_required
def signup(request):
    
    form = UserRegistration()
    context = {'form': form}
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            selected_group_id = form.cleaned_data['group'].id
            selected_group = Group.objects.get(id=selected_group_id)
            # password = generate_password()
            # print(password)
            user = form.save()
            # user.set_password(password)
            # user.save()
            selected_group.user_set.add(user)

            custom_user = Profile.objects.create(user=user)
            if not custom_user.is_profile_completed:
                return redirect('complete-profile')
            custom_user.save()
            return redirect('login')
        print(form.errors)
    return render(request, 'authentication/signup.html', context)

# @hospital_admin_required
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_authenticated: 
                if user.profile.is_profile_completed:
                    if request.user.groups.filter(name='Admin').exists() :
                        return redirect('index')
                    elif request.user.groups.filter(name='CEO').exists():
                        return redirect('index')
                    elif request.user.groups.filter(name='Employee').exists():
                        hospital_id  = user.Profile.hospital_id
                        return redirect('single-hospital', hospital_id=hospital_id)
                    elif request.user.groups.filter(name='Hospital Admin').exists():
                        hospital_id  = user.profile.hospital_id
                        return redirect('single-hospital', hospital_id=hospital_id)
                    else:
                        return redirect('login')
                else:
                    from django.http import HttpResponse
                    return HttpResponse("Your profile is not complete, please contact Irene")
                
            else:
                return redirect('login')  
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

# @admin_required
def complete_profile(request):
    hospitals = Hospital.objects.all()
    departments = Department.objects.all()
    
    if request.method == 'POST':
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

def singleHospital(request, hospital_id):
    # getting all the hospitals
    hospitals = Hospital.objects.all()

    # getting a single hospital
    hospital = Hospital.objects.get(id=hospital_id)
    hospital_name = hospital.name

    # title displaying as the hospital name when a user is viewing data of that particular hospital
    page_title = hospital_name
    
    hospital_data = singleHospitalData(request, hospital_id)

    # getting specific data of a single hospital
    single_hospital_data = Census.objects.filter(hospital_id= hospital_id)
    single_hospital_acute_swing_bed_transfers = Measures.objects.filter(hospital_id= hospital_id)
    # filtering the quick numbers cards
    total_inpatient = single_hospital_data.aggregate(total_inpatient=models.Sum('inpatient'))['total_inpatient']
    total_outpatient = single_hospital_data.aggregate(total_outpatient=models.Sum('outpatient'))['total_outpatient']
    total_swing_bed = single_hospital_data.aggregate(total_swing_bed=models.Sum('swing_bed'))['total_swing_bed']
    total_emergency_room = single_hospital_data.aggregate(total_emergency_room=models.Sum('emergency_room'))['total_emergency_room']
    total_rural_health_clinic = single_hospital_data.aggregate(total_rural_health_clinic=models.Sum('rural_health_clinic'))['total_rural_health_clinic']
    total_acute_swing_bed_transfers = single_hospital_acute_swing_bed_transfers.aggregate(total_acute_swing_bed_transfers=models.Sum('acute_swing_bed_transfers'))['total_acute_swing_bed_transfers']

    measures_data = []
    fields = ['mortality_rate','readmissions','pressure_ulcer','discharges_home','emergency_room_transfers','acute_swing_bed_transfers','medication_errors','falls',
              'against_medical_advice','left_without_being_seen','hospital_acquired_infection','covid_vaccination_total_percentage_of_compliance','complaint','grievances'
              ]
    
    for i in fields:
        data = [{'field_name': i.replace('_',' ').capitalize()}]
        for j in range(1, 13):
            single_column = Measures.objects.annotate(month=ExtractMonth('date_entered'),)\
            .order_by('month')\
            .filter(month=j, hospital=hospital)\
            .aggregate(average= Round(Avg(i),2))
            data.append(single_column)
        measures_data.append(data)

    context = {
        'hospital_name': hospital_name,
        'hospitals': hospitals,
        'hospital_data': hospital_data,
        'measures_data': measures_data,
        'total_inpatient': total_inpatient,
        'total_outpatient': total_outpatient,
        'total_swing_bed': total_swing_bed,
        'total_emergency_room': total_emergency_room,
        'total_emergency_room': total_emergency_room,
        'total_rural_health_clinic': total_rural_health_clinic,
        'total_acute_swing_bed_transfers': total_acute_swing_bed_transfers,
        'page_title': page_title
    }
    return render(request, 'dashboard/hospital.html', context)

def singleHospitalData(request, hospital_id): 
    hospital = Hospital.objects.get(id = hospital_id)
    data = {
        'labels': [],
        'datasets': []
    }
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
    return JsonResponse(data)

#Adding Measures data template
def addMeasures(request):
    form = MeasuresForm()
    page_title = 'Add Measures'
    blocktitle = 'Add Measures'
    context = {'form':form, 'page_title': page_title, 'blocktitle': blocktitle}
    
    if request.method == 'POST':
        
        form = MeasuresForm(request.POST)
        if form.is_valid:
            form.save()
    
    return render(request, 'dashboard/addMeasures.html',context)

#Adding Census data template
def addCensus(request):
    page_title = 'Add Census'
    blocktitle = 'Add Census'
    form = CensusForm()
    
    context = {'form':form, 'page_title': page_title, 'blocktitle': blocktitle}
    
    if request.method == 'POST':
        
        form = CensusForm(request.POST)
        
        if form.is_valid:
            
            form.save()
    
    return render(request, 'dashboard/addCensus.html',context)

#Adding Turnover data template
def addTurnover(request):
    page_title = 'Add Turnover'
    blocktitle = 'Add Turnover'
    form = TurnoverForm()
    
    context = {'form': form, 'page_title': page_title, 'blocktitle': blocktitle}
    
    if request.method == 'POST':
        
        form = TurnoverForm(request.POST)
        
        if form.is_valid:
            
            form.save()
    
    return render(request, 'dashboard/addTurnover.html',context)

#Adding Hiring data template
def addHiring(request):
    page_title = 'Add Turnover'
    blocktitle = 'Add Turnover'
    form = HiringForm()
    
    context = {'form': form, 'page_title': page_title, 'blocktitle': blocktitle}
    
    if request.method == 'POST':
        
        form = HiringForm(request.POST)
        
        if form.is_valid:
            
            form.save()
    
    return render(request, 'dashboard/addHiring.html',context)


def comingSoon(request):
    return render(request, 'rhc/coming-soon.html')