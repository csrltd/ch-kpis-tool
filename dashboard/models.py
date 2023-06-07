import random
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Hospital(models.Model):
    hospitalId = models.CharField(max_length=6, unique=True, null=True)
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=False, blank=True)
    mortality_rate = models.FloatField(null=True)
    covid_vaccination = models.CharField(max_length=255, null=True)
    pressure_ulcers = models.CharField(max_length=255, null=True)
    complaints = models.CharField(max_length=255, null=True)
    hires = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Department(models.Model):
    department_Id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ROLE_CHOICE = [('doctor', 'Doctor'), ('nurse', 'Nurse'),
                   ('patient', 'Patient')]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=255, null=False,
                            blank=False, choices=ROLE_CHOICE, default='doctor')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    is_profile_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Diagnosis(models.Model):
    pass


class Observation(models.Model):
    pass


class Bed(models.Model):
    BED_TYPE = [('acute bed', 'Acute bed'), ('swing bed', 'Swing bed')]
    type = models.CharField(max_length=20, null=True,
                            choices=BED_TYPE, default='swing bed')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Patient(models.Model):
    PATIENT_STATUS = [('inpatient', 'Inpatient'), ('outpatient', 'Outpatient')]
    EMERGENCY_ROOM = [('yes', 'Yes'), ('no', 'No')]
    MEDICAL_ADVICE = [('against medical advice', 'Against medical advice'),
                      ('with medical advice', 'With medical advice')]
    status = models.CharField(
        max_length=255, choices=PATIENT_STATUS, null=True)
    emergency_room = models.CharField(
        max_length=255, choices=EMERGENCY_ROOM, null=True)
    medical_advice = models.CharField(
        max_length=255, choices=MEDICAL_ADVICE, null=True)
    patient_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    birthday = models.DateTimeField(null=True)
    doctor = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey(
        Hospital, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.first_name


class Complaint(models.Model):
    complainer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    complaint = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=False, null=True)

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


# new models from the sheet
class Census(models.Model):
    inpatient = models.IntegerField()
    swing_bed = models.IntegerField()
    observation = models.IntegerField()
    emergency_room = models.IntegerField(null=True)
    outpatient = models.IntegerField()
    rural_health_clinic = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    date_entered = models.DateTimeField()
    date_created = models.DateTimeField()

    def __str__(self):
        return self.hospital.name

    class Meta:
        verbose_name_plural = ('Census')

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Measures(models.Model):
    mortality_rate = models.IntegerField(null=True)
    readmissions = models.IntegerField()
    pressure_ulcer = models.IntegerField()
    discharges_home = models.IntegerField()
    emergency_room_transfers = models.IntegerField()
    acute_swing_bed_transfers = models.IntegerField()
    medication_errors = models.IntegerField()
    falls = models.IntegerField()
    against_medical_advice = models.IntegerField()
    left_without_being_seen = models.IntegerField()
    hospital_acquired_infection = models.IntegerField()
    covid_vaccination_total_percentage_of_compliance = models.IntegerField()
    complaint = models.IntegerField()
    grievances = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    date_entered = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hospital.name

    class Meta:
        verbose_name_plural = ('Measures')

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Turnover(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=5)
    voluntary = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    date_entered = models.DateTimeField()
    date_created = models.DateTimeField()

    def __str__(self):
        return self.hospital.name


class Hiring(models.Model):
    new_hires = models.IntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    date_entered = models.DateTimeField()
    date_created = models.DateTimeField()

    def __str__(self):
        return self.hospital.name
    
class FeedBack(models.Model):
    
    satificationChoices ={
        'strongly_dissatisfied': '0-10',
        'quite_dissatisfied': '11-30',
        'dissatisfied': '31-50',
        'satisfied': '51-60',
        'quite_satisfied': '61-80',
        'strongly_satisfied': '81-100',
    }
    
    RADIO_CHOICES =[
        (True, 'Yes'),
        (False,'No'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    is_installable = models.BooleanField(choices=RADIO_CHOICES ,default=True)
    installable_description= models.TextField()
    is_UI_intuitive = models.BooleanField(choices=RADIO_CHOICES,default=True)
    intuitive_description = models.TextField()
    are_features_clear = models.BooleanField(choices=RADIO_CHOICES,default=True)
    features_description =models.TextField()
    are_expectations_met = models.BooleanField(choices=RADIO_CHOICES,default=True)
    expectations_descriptions= models.TextField()
    is_bug_free = models.BooleanField(choices=RADIO_CHOICES,default=True)
    bug_description = models.TextField()
    is_quick = models.BooleanField(choices=RADIO_CHOICES,default=True)
    quick_description = models.TextField()
    satisfaction_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    satisfaction_description = models.TextField()
    additional_feature = models.CharField(max_length=255)
    feedback_text = models.TextField()
    
    def __str__(self) :
        return self.first_name + ' ' + self.last_name
    
    
    


