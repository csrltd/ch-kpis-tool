from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hospital, Patient
from django.contrib.auth.models import Group
from django.forms import ModelForm, TextInput, Select, RadioSelect, DateTimeInput, NumberInput


class UserRegistration(UserCreationForm):
    # phone_number = forms.CharField(max_length=255)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    # hospitals = forms.ModelChoiceField(queryset=Hospital.objects.all())
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(
                'Please enter your email address', code='invalid_email')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(
                'Please enter your first name', code='invalid_first_name')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(
                'Please enter your last name', code='invalid_last_name')
        return last_name


class HospitalForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospitalId', 'name', 'address', 'phone_number', 'email', 'mortality_rate',
                  'covid_vaccination', 'pressure_ulcers', 'complaints', 'complaints', 'hires']


class patientForm(ModelForm):
    
    class Meta:
        model = Patient
        fields = ['status', 'emergency_room', 'medical_advice', 'patient_id',
                  'first_name', 'last_name', 'phone_number', 'birthday', 'admission_date', 'doctor', 'hospital']
        widgets = {
            'status': Select(),
            'emergency_room': Select(),
            'medical_advice': Select(),
            'patient_id': NumberInput(),
            'first_name': TextInput(),
            'last_name': TextInput(),
            'phone_number': TextInput(),
            'birthday': DateTimeInput(attrs={'type': 'datetime-local'}),
            'admission_date': DateTimeInput(attrs={'type': 'datetime-local'}),
            'emergency_room': RadioSelect(),
  
       
class MeasuresForm(ModelForm):
    
   
    
    class Meta:
        model = Measures
        fields = ['mortality_rate','readmissions','pressure_ulcer','discharges_home','emergency_room_transfers',
                'acute_swing_bed_transfers','medication_errors','falls','against_medical_advice','left_without_being_seen',
                'hospital_acquired_infection','covid_vaccination_total_percentage_of_compliance','complaint','grievances','hospital',
                'date_entered','date_created',
                ]
    
        widgets= {
            'mortality_rate': NumberInput(),
            'readmissions': NumberInput(),
            'pressure_ulcer': NumberInput(),
            'discharges_home': NumberInput(),
            'emergency_room_transfers': NumberInput(),
            'acute_swing_bed_transfers': NumberInput(),
            'medication_errors': NumberInput(),
            'falls': NumberInput(),
            'against_medical_advice': NumberInput(),
            'left_without_being_seen': NumberInput(),
            'hospital_acquired_infection': NumberInput(),
            'covid_vaccination_total_percentage_of_compliance': NumberInput(),
            'complaint': NumberInput(),
            'grievances': NumberInput(),
            'hospital': forms.Select(),
            'date_entered': DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_created': DateTimeInput(attrs={'type':'datetime-local'}),
        }
        

class CensusForm(ModelForm):
    
    class Meta:
        model = Census
        fields =['inpatient','swing_bed','observation',
                 'emergency_room','outpatient','rural_health_clinic',
                 'hospital','date_entered','date_created']
        
        widgets = {
            'inpatient': NumberInput(),
            'swing_bed':NumberInput(),
            'observation':NumberInput(),
            'emergency_room':NumberInput(),
            'outpatient':NumberInput(),
            'rural_health_clinic':NumberInput(),
            'hospital':Select(),
            'date_entered':DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_created':DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class TurnoverForm(ModelForm):
    
    class Meta:
        model = Turnover
        fields =['total','voluntary','hospital'
                 ,'date_entered','date_created']
        
        widgets = {
            'total': NumberInput(),
            'voluntary':NumberInput(),
            'hospital':Select(),
            'date_entered':DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_created':DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class HiringForm(ModelForm):
    
    class Meta:
        model = Hiring
        fields = ['new_hires','hospital','date_entered','date_created']
    
        widgets = {
            'new_hires': NumberInput(),
            'hospital':Select(),
            'date_entered':DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_created':DateTimeInput(attrs={'type': 'datetime-local'}),
        }