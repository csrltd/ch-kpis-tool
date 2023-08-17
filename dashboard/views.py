from django.template.defaultfilters import default
from .forms import FeedbackForm
from datetime import timezone
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Hospital, Department, Profile, Hospital, Turnover
from .models import *
from .models import Patient, Hospital
from django.http import JsonResponse
from collections import defaultdict
import calendar
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.db.models import Avg, Sum, DecimalField
from django.db.models.functions import Round
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncMonth
from django.utils.timezone import make_aware
from django.db.models.functions import ExtractMonth, ExtractYear
import datetime
from .decorators import *

# all view are secured to admin level. If you want to work on it, go
# the admin dashboard and change your user group to admin


# Definitions of the measures
measure_definitions = {
    'mortality_rate': 'Percent of acute and swing bed patient deaths for any reason during the reporting period. Total # of deaths (acute & swing bed), divided by the total # of patient days (acute & swing bed)',

    'readmissions': 'Rate of acute and swing bed patients from the CAH with an unplanned readmission to the same CAH within 30 days per 100 patient discharges. Total # of inpatients from the CAH with an unplanned readmission within 30 days of discharge to the same CAH, divided by the total # of inpatient discharges during the reporting period, multiplied by 100',

    'pressure_ulcer': 'Percent of acute and swing bed patient admissions who develop one or more pressure ulcers Stage II or greater during the reporting period. Total # of acute and swing bed patients who develop one or more Stage II pressure ulcers during the reporting period, divided by the total # of patients admitted during the reporting period.',

    'discharges_home': 'Total # of acute and swing bed patients with a Home discharge disposition on the day of discharge. Total count of acute and swing bed patients with a Home discharge disposition on the day of discharge as documented in the medical record during the reporting period.',

    'emergency_room_transfers': 'Total number of transfers from the ED to a tertiary facility. Total # of patients admitted to the ED who were then discharged, transferred, or returned to a tertiary facility. ',

    'acute_swing_bed_transfers': 'Total number of transfers from acute or swing bed to a tertiary facility. Total # of patients admitted to acute care or swing bed and is transferred to a tertiary facility.',

    'medication_errors': 'Total number of reported medication errors during the reporting period. Total number of reported/suspected medication errors',

    'falls': 'Sum of all Hospital falls. Total # of acute, swing bed, and ED patients with a reported fall during hospitalization. Data is automatically calculated based on reported fall data.',

    'against_medical_advice': 'Total number of patient encounters who left the hospital against medical advice. (ED, Obs, Acute, and SWB). Total # of acute, swing bed, observation, and ED hospital encounters with a discharge against medical advice.',

    'left_without_being_seen': "Total number of ED encounters the patient left the hospital without being seen. Total # of ED encounters with a left without being seen discharge.",

    'hospital_acquired_infection': 'Total number of hospital acquired infections. Total # of acute and swing bed hospitalizations with hospital acquired/onset infections that occur during the reporting period.',

    'covid_vaccination_total_percentage_of_compliance': 'Percentage of current staff (including Hospital & contract/agency staff) who have been partially/fully vaccinated or have an exemption. Percentage of current Hospital employees (including Hospital & contract/agency staff) who have been partially vaccinated, fully vaccinated, or have an exemption for the reporting period.',

    'complaint': 'Sum of all Hospital complaints reported. Total # of reported complaints from acute, swing bed, and ED hospital encounters. Total # of reported complaints from acute, swing bed, and ED hospital encounters. Data will be automatically calculated from previous data.',

    'grievances': 'Sum of all Hospital grievances. Total # of reported grievances from acute, swing bed, and ED hospital encounters. Data will be automatically calculated from previous data'
}


def turnover_data(request, hospital_id=None):
    current_year = datetime.datetime.now().year
    hospitals = Hospital.objects.all()
    data = {
        'labels': [],
        'datasets': []
    }
    unique_months = set()  # Collect unique months across all hospitals
    for hospital in hospitals:
        turnover_data = Turnover.objects.filter(hospital=hospital) \
                                        .annotate(month=TruncMonth('date_entered')) \
                                        .values('month') \
                                        .annotate(total=Sum('total'), voluntary=Sum('voluntary')) \
                                        .values('month', 'total', 'voluntary')
        turnover_data = sorted(
            turnover_data, key=lambda item: item['month'].date())
        turnover_dataset = {
            'label': hospital.name,
            'data': [],
            'fill': False
        }
        for item in turnover_data:
            month = item['month'].strftime('%b %y')
            turnover_dataset['data'].append(item['total'])
            unique_months.add(month)  # Add month to the unique_months set
        data['datasets'].append(turnover_dataset)

    # Sort the unique months in chronological order
    sorted_months = sorted(
        unique_months, key=lambda x: datetime.datetime.strptime(x, '%b %y'))

    # Populate the labels only with the unique months that have data
    data['labels'] = sorted_months

    return JsonResponse(data)


@require_http_methods(['GET'])
@admin_required
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
        mortality_rate_avg = measures.aggregate(Avg('mortality_rate'))[
            'mortality_rate__avg']
        data.append({
            'hospital': hospital.name,
            'mortality_rate': mortality_rate_avg,
        })
    return JsonResponse(data, safe=False)


@require_http_methods(['GET'])
@admin_required
def get_general_measures_data(request):
    selected_measure = request.GET.get('selected_measure')
    selected_year = request.GET.get('selected_year')

    # Convert the selected_year to an integer if needed
    selected_year = int(selected_year) if selected_year else None

    # Retrieve the measures data for all hospitals and the selected measure
    selected_measures_data = Measures.objects.filter(date_entered__year=selected_year).annotate(
        month=ExtractMonth('date_entered')).values('hospital_id', 'month', selected_measure)

    measures_data_dict = {}

    # Group the measures data by hospital
    grouped_data = {}
    for measure_data in selected_measures_data:
        hospital_id = measure_data['hospital_id']
        month = measure_data['month']
        value = measure_data[selected_measure]

        if hospital_id not in grouped_data:
            grouped_data[hospital_id] = []

        grouped_data[hospital_id].append([month, value])

    # Fetch the hospital names based on hospital IDs
    hospital_ids = grouped_data.keys()
    hospital_names = Hospital.objects.filter(
        id__in=hospital_ids).values('id', 'name')
    hospital_names_dict = {hospital['id']: hospital['name']
                           for hospital in hospital_names}

    # Populate the measures data dictionary
    measures_data_dict['data'] = [{'hospital_id': hospital_id, 'hospital_name': hospital_names_dict[hospital_id],
                                   'data': data} for hospital_id, data in grouped_data.items()]

    measures_data_dict['selected_measure'] = selected_measure
    measures_data_dict['selected_year'] = selected_year

    return JsonResponse(measures_data_dict)


@admin_required
# @ceo_required
def index(request):
    page_title = 'Overview'
    profileInfo = Profile.objects.get(user=request.user)
    hospitals = Hospital.objects.all()
    inpatient_count = Census.objects.aggregate(total=Sum('inpatient'))['total']
    outpatient_count = Census.objects.aggregate(
        total=Sum('outpatient'))['total']
    swing_bed_count = Census.objects.aggregate(total=Sum('swing_bed'))['total']
    acute_swing_bed_transfers_count = Measures.objects.aggregate(
        total=Sum('acute_swing_bed_transfers'))['total']

    # added fields on the quick numbers cards
    emergency_room_count = Census.objects.aggregate(
        total=Sum('emergency_room'))['total']
    total_rural_health_clinic = Census.objects.aggregate(
        total=Sum('rural_health_clinic'))['total']

    measures_data = []
    fields = ['mortality_rate', 'readmissions', 'pressure_ulcer', 'discharges_home', 'emergency_room_transfers', 'acute_swing_bed_transfers', 'medication_errors', 'falls',
              'against_medical_advice', 'left_without_being_seen', 'hospital_acquired_infection', 'covid_vaccination_total_percentage_of_compliance', 'complaint', 'grievances'
              ]

    for i in fields:
        data = [{'field_name': i.replace(
            '_', ' ').capitalize(), 'definition': measure_definitions[i]}]
        for j in range(1, 13):
            single_column = Measures.objects.annotate(month=ExtractMonth('date_entered'),)\
                .order_by('month')\
                .filter(month=j)\
                .aggregate(average=Round(Avg(i), 2))
            data.append(single_column)
        measures_data.append(data)
        # print(measures_data)

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
        'page_title': page_title,
        'measure_definitions': measure_definitions,
    }

    return render(request, 'dashboard/index.html', context)


# @admin_required
def chart_data(request):
    # filtering the data based year
    years = Measures.objects.distinct().annotate(
        year=ExtractYear('date_entered')).values('year')
    # print(years)
    selected_year = datetime.datetime.now().year
    if request.method == 'POST':
        selected_year = request.POST['selected_year']
    print(selected_year)

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
        'bed_data': bed_data,
        'swing_bed': swing_bed,
        'acute_bed': acute_bed,
        'swing_bed': swing_bed,
        'inpatient': inpatient,
        'outpatient': outpatient
    }
    return JsonResponse(context)

# New way to get data


# @admin_required
def filter_patients_by_month(request):
    hospital_names = Hospital.objects.all()
    data = {}
    for hospital_name in hospital_names:
        inpatient_hospital = Patient.objects.filter(
            hospital=hospital_name, status='inpatient')
        inpatient_data = inpatient_hospital.values_list(
            'admission_date', flat=True)
        inpatient_data_by_month = defaultdict(int)
        for date in inpatient_data:
            month = date.month
            inpatient_data_by_month[month] += 1

        outpatient_hospital = Patient.objects.filter(
            hospital=hospital_name, status='outpatient')
        outpatient_data = outpatient_hospital.values_list(
            'admission_date', flat=True)
        outpatient_data_by_month = defaultdict(int)
        for date in outpatient_data:
            month = date.month
            outpatient_data_by_month[month] += 1

        months = [calendar.month_name[month] for month in range(1, 13)]
        inpatient_totals = [inpatient_data_by_month[month]
                            for month in range(1, 13)]
        outpatient_totals = [outpatient_data_by_month[month]
                             for month in range(1, 13)]
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
            user = form.save()
            selected_group.user_set.add(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)

                return redirect('complete-profile')
        print(form.errors)
    return render(request, 'authentication/signup.html', context)


# @admin_required
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                if user.profile.is_profile_completed:
                    if request.user.groups.filter(name='Admin').exists():
                        return redirect('index')
                    elif request.user.groups.filter(name='CEO').exists():
                        return redirect('index')
                    elif request.user.groups.filter(name='Employee').exists():
                        hospital_id = user.Profile.hospital_id
                        return redirect('single-hospital', hospital_id=hospital_id)
                    elif request.user.groups.filter(name='Hospital Admin').exists():
                        hospital_id = user.profile.hospital_id
                        return redirect('single-hospital', hospital_id=hospital_id)
                    else:
                        return redirect('login')
                else:
                    # from django.http import HttpResponse
                    # return HttpResponse("Your profile is not complete, please contact Irene")
                    return redirect('complete-profile')

            else:
                return redirect('login')
        # return redirect('login')
        else:
            messages.error(
                request, 'Invalid credentials!!! Please enter correct username or password')

    return render(request, 'authentication/login.html')


def logOutPage(request):
    logout(request)
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
    form = ProfileForm()

    message = ''
    blocktitle = 'Add your profile'
    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():

            profile = form.save(commit=False)
            # profile.user = request.user
            profile.is_profile_completed = True
            profile.save()
            return redirect('login')
        else:
            message = 'Please enter valid data'

    context = {
        'form': form,
        'message': message,
        'blocktitle': blocktitle,
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
            patient.hospital = Hospital.objects.get(
                id=request.POST.get('hospital'))
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
        id_prefix = "CH"
        hospital_id = f"{id_prefix}{id_suffix}"


@require_http_methods(['GET'])
def get_measures_data(request):
    """Gets a particular data for a particular hospital """
    hospital_id = request.GET.get('hospital_id')
    selected_measure = request.GET.get('selected_measure')

    # Retrieve the selected year from the request or user input
    selected_year = request.GET.get('selected_year')

    # Convert the selected_year to an integer if needed
    selected_year = int(selected_year) if selected_year else None

    # Prepare the filter conditions for the selected year
    filter_conditions = {
        'hospital_id': hospital_id,
        'date_entered__year': selected_year
    }

    # Exclude the year filter if selected_year is not provided or None
    if selected_year is None:
        del filter_conditions['date_entered__year']

    # Retrieve the measures data for the selected hospital and measure
    selected_measures_data = (
        Measures.objects.filter(**filter_conditions)
        .annotate(month=ExtractMonth('date_entered'))
        .values('month', selected_measure)
    )
    # Create a dictionary to hold the measures data
    measures_data_dict = {}
    # Loop through the selected measures data and retrieve the month and value
    data = selected_measures_data.values_list('month', selected_measure)
    measures_data_dict['data'] = list(data)

    print(measures_data_dict)

    return JsonResponse(measures_data_dict)


# @hospital_admin_required
@admin_required
def singleHospital(request, hospital_id):
    # getting all the hospitals
    hospitals = Hospital.objects.all()

    # getting a single hospital
    hospital = Hospital.objects.get(id=hospital_id)
    hospital_name = hospital.name

    hospital_data = singleHospitalData(request, hospital_id)
    profileInfo = Profile.objects.get(user=request.user)
    page_title = hospital_name

    # checking the hospital ID for the logged in user
    user_hospital_id = request.user.profile.hospital.id

    # getting specific data of a single hospital
    single_hospital_data = Census.objects.annotate(year=ExtractYear(
        'date_entered')).filter(hospital_id=hospital_id)
    single_hospital_acute_swing_bed_transfers = Measures.objects.annotate(
        year=ExtractYear('date_entered')).filter(hospital_id=hospital_id)
    # filtering the quick numbers cards
    total_inpatient = single_hospital_data.aggregate(
        total_inpatient=models.Sum('inpatient'))['total_inpatient']
    total_outpatient = single_hospital_data.aggregate(
        total_outpatient=models.Sum('outpatient'))['total_outpatient']
    total_swing_bed = single_hospital_data.aggregate(
        total_swing_bed=models.Sum('swing_bed'))['total_swing_bed']
    total_emergency_room = single_hospital_data.aggregate(
        total_emergency_room=models.Sum('emergency_room'))['total_emergency_room']
    total_rural_health_clinic = single_hospital_data.aggregate(
        total_rural_health_clinic=models.Sum('rural_health_clinic'))['total_rural_health_clinic']
    total_acute_swing_bed_transfers = single_hospital_acute_swing_bed_transfers.aggregate(
        total_acute_swing_bed_transfers=models.Sum('acute_swing_bed_transfers'))['total_acute_swing_bed_transfers']

    measures_data = []
    fields = ['mortality_rate', 'readmissions', 'pressure_ulcer', 'discharges_home', 'emergency_room_transfers', 'acute_swing_bed_transfers', 'medication_errors', 'falls',
              'against_medical_advice', 'left_without_being_seen', 'hospital_acquired_infection', 'covid_vaccination_total_percentage_of_compliance', 'complaint', 'grievances'
              ]

    for i in fields:
        data = [{'field_name': i.replace(
            '_', ' ').capitalize(), 'definition': measure_definitions[i]}]
        for j in range(1, 13):
            single_column = Measures.objects.annotate(month=ExtractMonth('date_entered'), year=ExtractYear('date_entered'))\
                .order_by('month')\
                .filter(month=j, hospital=hospital)\
                .aggregate(average=Round(Avg(i), 2))
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
        'page_title': page_title,
        'profileInfo': profileInfo,
        'user_hospital_id': user_hospital_id,
        'hospital_id': hospital_id,
    }
    return render(request, 'dashboard/hospital.html', context)


@admin_required
def singleHospitalData(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    data = {
        'labels': [],
        'datasets': []
    }
    turnover_data = Turnover.objects.filter(hospital=hospital) \
        .annotate(month=TruncMonth('date_entered')) \
        .values('month') \
        .annotate(total=Sum('total'), voluntary=Sum('voluntary')) \
        .values('month', 'total', 'voluntary')

    # sorts the months on the chart in chronological order(Jan - Dec)
    turnover_data = sorted(
        turnover_data, key=lambda item: item['month'].date())

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


@admin_required
def addMeasures(request):
    user_hospital_id = request.user.profile.hospital.id
    form = MeasuresForm(user_hospital_id=user_hospital_id)
    page_title = 'Add Measures'
    blocktitle = 'Add Measures'

    context = {'form': form, 'page_title': page_title,
               'blocktitle': blocktitle, 'user_hospital_id': user_hospital_id}

    if request.method == 'POST':

        form = MeasuresForm(request.POST)
        if form.is_valid:
            form.save()

    return render(request, 'dashboard/addMeasures.html', context)


@admin_required
def addCensus(request):
    user_hospital_id = request.user.profile.hospital.id
    page_title = 'Add Census'
    blocktitle = 'Add Census'
    form = CensusForm(user_hospital_id=user_hospital_id)

    context = {'form': form, 'page_title': page_title,
               'blocktitle': blocktitle}

    if request.method == 'POST':

        form = CensusForm(request.POST)

        if form.is_valid:

            form.save()

    return render(request, 'dashboard/addCensus.html', context)

# Adding Turnover data template


@admin_required
def addTurnover(request):
    user_hospital_id = request.user.profile.hospital.id
    page_title = 'Add Turnover'
    blocktitle = 'Add Turnover'
    form = TurnoverForm(user_hospital_id=user_hospital_id)

    context = {'form': form, 'page_title': page_title,
               'blocktitle': blocktitle}

    if request.method == 'POST':

        form = TurnoverForm(request.POST)

        if form.is_valid:

            form.save()

    return render(request, 'dashboard/addTurnover.html', context)

# Adding Hiring data template


@admin_required
def addHiring(request):
    page_title = 'Add hiring'
    blocktitle = 'Add hiring'
    form = HiringForm()

    context = {'form': form, 'page_title': page_title,
               'blocktitle': blocktitle}

    if request.method == 'POST':
        form = HiringForm(request.POST)

        if form.is_valid:

            form.save()

    return render(request, 'dashboard/addHiring.html', context)


@admin_required
def measuresView(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    hospitals = Hospital.objects.all()
    # hospital_data = singleHospitalData(request, hospital_id)
    profileInfo = Profile.objects.get(user=request.user)
    user_hospital_id = request.user.profile.hospital.id
    hospital_name = hospital.name
    page_title = hospital_name

    years = Measures.objects.distinct().annotate(
        year=ExtractYear('date_entered')).values('year')

    measures_data = []
    fields = ['mortality_rate', 'readmissions', 'pressure_ulcer', 'discharges_home', 'emergency_room_transfers', 'acute_swing_bed_transfers', 'medication_errors', 'falls',
              'against_medical_advice', 'left_without_being_seen', 'hospital_acquired_infection', 'covid_vaccination_total_percentage_of_compliance', 'complaint', 'grievances'
              ]

    # For now, the selected_year is static for establishing the functionality and desired results. It would be changed.
    selected_year = 2022

    # The average of the values for each measure for a particular month has been changed to sum instead.
    for i in fields:
        data = [{'field_name': i.replace(
            '_', ' ').capitalize(), 'definition': measure_definitions[i]}]
        for j in range(1, 13):
            single_column = Measures.objects.annotate(month=ExtractMonth('date_entered'), year=ExtractYear('date_entered'))\
                .order_by('month')\
                .filter(month=j, hospital=hospital, year=selected_year)\
                .aggregate(sum=Sum(i))
            data.append(single_column)
        measures_data.append(data)
        # print(measures_data)

    context = {'hospital': hospital, 'measures_data': measures_data, 'profileInfo': profileInfo,
               'user_hospital_id': user_hospital_id, 'page_title': page_title, 'hospitals': hospitals}

    return render(request, 'dashboard/measures.html', context)


def comingSoon(request):
    return render(request, 'rhc/coming-soon.html')


def feedbackForm(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('thank-you')
    else:
        user = request.user
        profile = Profile.objects.get(user=user)

        initial_values = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'hospital': profile.hospital,
        }

        form = FeedbackForm(request=request, initial=initial_values)

    context = {
        'form': form,
    }
    return render(request, 'dashboard/feedback-form.html', context)


def thankPage(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    page_title = 'Thank You'

    context = {
        'page_title': page_title,
        'hospital': profile.hospital,
    }

    return render(request, 'dashboard/thank-you.html', context)
