import random
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save

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

class Turnover(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    turnover_date = models.DateField(auto_now_add=False, null=True)
    turnover = models.IntegerField(max_length=255, null=True)
    


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
    status = models.CharField(max_length=255, choices=PATIENT_STATUS, null=True)
    emergency_room = models.CharField(max_length=255, choices=EMERGENCY_ROOM, null=True)
    medical_advice = models.CharField(max_length=255, choices=MEDICAL_ADVICE, null=True)
    patient_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    birthday = models.DateTimeField(null=True)
    doctor = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey(Hospital, null=True, on_delete=models.SET_NULL)
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


class Census(models.Model):
    census = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    inpatient = models.IntegerField(null=True)
    bed_type = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True)
    benchmark = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = ('Census')

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Measures(models.Model):
    mortality_rate = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True)
    readmissions = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True)
    pressure_ulcer = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, related_name="PressurEulcer")
    emergency_room_transfer = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, related_name="EmergencyRoomTransfer")
    bed_transfers = models.ForeignKey(
        Bed, on_delete=models.SET_NULL, null=True)
    medication_errors = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    benchmark = models.DateTimeField()

    class Meta:
        verbose_name_plural = ('Measures')

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
