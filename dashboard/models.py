from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Hospital(models.Model):
    hospitalId = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=False, blank=True)
    mortality_rate = models.CharField(max_length=4, null=True)
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
    patientId = models.IntegerField(null=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=255, null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, default='')
    doctor = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT, default='')
    status = models.CharField(
        max_length=255, choices=PATIENT_STATUS, null=False, default='Inpatient')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.lastName

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})


class Complaint(models.Model):
    complainer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    complaint = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

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
