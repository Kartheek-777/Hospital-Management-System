from django.db import models

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.CharField(max_length=255, default='Uknown')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    medical_record_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialty = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date} at {self.time}"
    
from django.db import models

class PatientQuery(models.Model):
    patient_name = models.CharField(max_length=100)
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name

# models.py
class Prescription(models.Model):
    doctor_name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    prescription_text = models.TextField()

    def __str__(self):
        return f"Prescription by {self.doctor_name} for {self.patient.first_name}"




