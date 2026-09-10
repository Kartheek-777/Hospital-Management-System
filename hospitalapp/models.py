from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default='fa-stethoscope')

    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    license_number = models.CharField(max_length=50, unique=True, default='')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    qualification = models.CharField(max_length=100, default='MBBS, MD')
    experience_years = models.IntegerField(default=5)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    available_days = models.CharField(max_length=100, default='Mon - Fri')
    available_time = models.CharField(max_length=50, default='09:00 AM - 05:00 PM')

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.CharField(max_length=255, default='Unknown')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    medical_record_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (MRN: {self.medical_record_number})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.patient.first_name} with Dr. {self.doctor.last_name} on {self.date} at {self.time}"

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='prescriptions')
    doctor_name = models.CharField(max_length=100, blank=True, default='')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    disease = models.CharField(max_length=100)
    prescription_text = models.TextField(help_text="Medication names, dosage and frequency instructions")
    dosage = models.CharField(max_length=100, blank=True, null=True, default='As directed')
    duration = models.CharField(max_length=50, blank=True, null=True, default='7 days')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        doc_str = self.doctor.last_name if self.doctor else self.doctor_name
        return f"Prescription for {self.patient.first_name} by Dr. {doc_str}"

class PatientQuery(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Responded', 'Responded'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='queries')
    patient_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200, default='Medical Inquiry')
    query_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Query from {self.patient_name}: {self.subject[:30]}"
