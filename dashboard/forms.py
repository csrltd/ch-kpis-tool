from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Hospital, Patient, Measures, Census, Turnover, Hiring, Profile, FeedBack
from django.forms import ModelForm, TextInput, Select, RadioSelect, DateTimeInput, NumberInput,EmailInput,Textarea


class UserRegistration(UserCreationForm):
    phone_number = forms.CharField(max_length=255)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    # hospitals = forms.ModelChoiceField(queryset=Hospital.objects.all())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'group']

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
        fields = ['hospitalId', 'name', 'address', 'phone_number', 'email','mortality_rate',
                  'covid_vaccination', 'pressure_ulcers', 'complaints', 'complaints', 'hires']
        

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user_hospital_id = kwargs.pop('user_hospital_id', None)
        user = kwargs.pop('user', None)
    
        super(ProfileForm, self).__init__(*args, **kwargs)
    
        if user_hospital_id:
            # self.initial['user_hospital_id'] = user_hospital_id
            self.fields['hospital'].queryset = Hospital.objects.filter(id=user_hospital_id)
        
        if user:
            self.initial['user'] = user
            self.fields['user'].queryset = User.objects.filter(id=user.id)
    
    class Meta:
        model = Profile
        fields = ['user','hospital', 'role','department']
        # widgets = {
        #     'user': forms.HiddenInput(),
        # }

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
        }
  
       
class MeasuresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user_hospital_id = kwargs.pop('user_hospital_id', None)
        super(MeasuresForm, self).__init__(*args, **kwargs)
        if user_hospital_id:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=user_hospital_id)
    class Meta:
        model = Measures
        fields = ['mortality_rate','readmissions','pressure_ulcer','discharges_home','emergency_room_transfers',
                'acute_swing_bed_transfers','medication_errors','falls','against_medical_advice','left_without_being_seen',
                'hospital_acquired_infection','covid_vaccination_total_percentage_of_compliance','complaint','grievances','hospital',
                'date_entered',
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
            # 'date_created': DateTimeInput(attrs={'type':'datetime-local'}),
        }
        

class CensusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user_hospital_id = kwargs.pop('user_hospital_id', None)
        super(CensusForm, self).__init__(*args, **kwargs)
        if user_hospital_id:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=user_hospital_id)
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
    def __init__(self, *args, **kwargs):
        user_hospital_id = kwargs.pop('user_hospital_id', None)
        super(TurnoverForm, self).__init__(*args, **kwargs)
        if user_hospital_id:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=user_hospital_id)
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
        
        
class FeedbackForm(ModelForm):
    
    class Meta:
        model = FeedBack
        fields = [
            'first_name','last_name','email','is_installable','installable_description',
            'is_UI_intuitive','intuitive_description','are_features_clear','features_description','are_expectations_met',
            'expectations_descriptions','is_bug_free','bug_description','is_quick','quick_description',
            'satisfaction_rate','satisfaction_description','additional_feature','feedback_text',
        ]
        
        widgets = {
            'first_name':TextInput(attrs={'placeholder':'Alphonse'}),
            'last_name':TextInput(attrs={'placeholder':'SIBOMANA'}),
            'email':EmailInput(attrs={'placeholder':'salphonse@compstaffing.com'}),
            'is_installable': RadioSelect(),
            'installable_description': TextInput(attrs={'placeholder':'If No, what made it difficult'}),
            'is_UI_intuitive': RadioSelect(),
            'intuitive_description': TextInput(attrs={'placeholder':'If No, what made it difficult'}),
            'are_features_clear': RadioSelect(),
            'features_description': TextInput(attrs={'placeholder':'Features that we need to improve'}),
            'are_expectations_met': RadioSelect(),
            'expectations_descriptions': TextInput(attrs={'placeholder':'If not, what were your expectations, and how did the software fall short?'}),
            'is_bug_free': RadioSelect(),
            'bug_description': TextInput(attrs={'placeholder':'If so, please describe them?'}),
            'is_quick': RadioSelect(),
            'quick_description': TextInput(attrs={'placeholder':'If not, what can we improve?'}),
            'satisfaction_rate': NumberInput(attrs={'type':'range'}),
            'satisfaction_description': TextInput(attrs={'placeholder':'Was there anything that stood out as particularly positive or negative?'}),
            'additional_feature': TextInput(attrs={'placeholder':'Type what features you would like to see in the future'}),
            'feedback_text': Textarea(attrs={'placeholder':'Type your feedback'}),
        }